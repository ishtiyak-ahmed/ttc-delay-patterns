"""Fail-closed, mode-specific enrichment from pinned official TTC code references."""
import collections
import csv
import hashlib
import io
import json
import re
from pathlib import Path

REFERENCE = Path(__file__).resolve().parents[1] / 'references/ttc_delay_codes/2026-10-26/manifest.json'
MODES = {'bus', 'lrt', 'streetcar', 'subway'}
ORIGINAL_COLUMNS = ['code_key', 'source_mode', 'category_eligible', 'raw_code']
ADDED_COLUMNS = ['code_description', 'code_display_label']


def encoding_defect(text):
    """Conservative corruption detection, not encoding repair or punctuation normalization."""
    return bool(re.search(r'[\ufffd\u0080-\u009f]|â[\u0080-\u00bf\u20ac\u2018-\u201f]|[ÃÂ][\u0080-\u00bf]', text))


def prepare_lookup(mode_rows):
    lookup = {}
    for mode, rows in mode_rows.items():
        if mode not in MODES:
            raise ValueError('Unknown dictionary mode')
        grouped = collections.defaultdict(list)
        for row in rows:
            if not isinstance(row.get('CODE'), str) or not row['CODE'].strip():
                raise ValueError('Dictionary CODE must be nonblank text')
            description = row.get('DESCRIPTION')
            if description is not None and not isinstance(description, str):
                raise ValueError('Dictionary DESCRIPTION must be text or null')
            grouped[row['CODE']].append(description)
        for code, descriptions in grouped.items():
            usable = {d for d in descriptions if d is not None and d.strip()}
            if len(usable) > 1:
                status = 'ambiguous'
            elif len(usable) == 0 or any(d is None or not d.strip() for d in descriptions):
                status = 'missing_description'
            elif encoding_defect(next(iter(usable))):
                status = 'encoding_defect'
            else:
                status = 'accepted'
            lookup[(mode, code)] = dict(
                status=status, description=next(iter(usable)) if status == 'accepted' else None,
                source_rows=len(descriptions), distinct_descriptions=len(usable),
                source_descriptions=sorted(set(descriptions), key=lambda d: (d is not None, d or '')))
    return lookup


def load_reference(path=REFERENCE):
    path = Path(path)
    manifest = json.loads(path.read_text())
    resources = manifest['resources']
    if len(resources) != 4 or {r['mode'] for r in resources} != MODES:
        raise ValueError('A complete, unique four-mode reference set is required')
    mode_rows = {}
    for resource in resources:
        source = (path.parent / resource['file']).resolve()
        if source.parent != path.parent.resolve():
            raise ValueError('Reference file must remain inside its version directory')
        body = source.read_bytes()
        if (hashlib.sha256(body).hexdigest() != resource['sha256']
                or len(body) != resource['file_size_bytes'] or resource['http_status'] != 200):
            raise ValueError('Reference integrity/provenance mismatch')
        if resource['format'] == 'csv':
            rows = list(csv.DictReader(io.StringIO(body.decode('utf-8-sig'))))
        else:
            payload = json.loads(body)
            if resource['format'] == 'json':
                rows = payload
            elif resource['format'] == 'ckan_json':
                if not payload['success']:
                    raise ValueError('CKAN reference retrieval failed')
                rows = payload['result']['records']
                if len(rows) != payload['result']['total']:
                    raise ValueError('Incomplete CKAN reference page')
            else:
                raise ValueError('Unsupported reference format')
        if not isinstance(rows, list) or not rows:
            raise ValueError('Empty or invalid reference')
        mode_rows[resource['mode']] = rows
    return prepare_lookup(mode_rows), manifest


def enrich_dimension(rows, facts, lookup):
    result = []
    statuses = {}
    keys = set()
    for row in rows:
        if list(row) != ORIGINAL_COLUMNS or row['code_key'] in keys:
            raise ValueError('Unexpected original dimension columns or duplicate key')
        keys.add(row['code_key'])
        reference = lookup.get((row['source_mode'], row['raw_code']))
        status = ('missing_code' if not row['category_eligible'] else
                  reference['status'] if reference is not None else 'unmapped')
        description = reference['description'] if status == 'accepted' else None
        # The raw code remains visible even for unresolved references; labels add no invented meaning.
        label = ('[Missing code]' if not row['category_eligible'] else
                 row['raw_code'] + ' — ' + description if description is not None else row['raw_code'])
        enriched = dict(row, code_description=description, code_display_label=label)
        if {k: enriched[k] for k in ORIGINAL_COLUMNS} != row:
            raise ValueError('Original dimension value changed')
        result.append(enriched)
        statuses[row['code_key']] = status
    weights = collections.Counter()
    for row in facts:
        if row['code_key'] not in keys:
            raise ValueError('Fact references an absent original code key')
        weights[row['code_key']] += row['recorded_incidents']
    coverage = {}
    unresolved = []
    for row in rows:
        mode = row['source_mode']
        mode_counts = coverage.setdefault(mode, {})
        status = statuses[row['code_key']]
        counts = mode_counts.setdefault(status, dict(dimension_rows=0, incident_records=0))
        counts['dimension_rows'] += 1
        counts['incident_records'] += weights[row['code_key']]
        if status != 'accepted':
            unresolved.append(dict(source_mode=mode, raw_code=row['raw_code'], status=status,
                                   incident_records=weights[row['code_key']]))
    return result, dict(coverage=coverage, unresolved_codes=unresolved)
