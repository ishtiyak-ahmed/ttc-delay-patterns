"""Fail-closed, mode-specific enrichment from pinned official TTC code references."""
import collections
import csv
import hashlib
import io
import json
import re
from pathlib import Path

REFERENCE = Path(__file__).resolve().parents[1] / 'references/ttc_delay_codes/2026-10-26/manifest.json'
RECOVERY = REFERENCE.parents[3] / 'config/code_description_recovery.json'
RECOVERY_METHOD = 'latin1_encode_utf8_decode_strict_en_dash_v1'
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


def recover_dash(description):
    """Strict reversal of the reviewed signature; never a general text cleaner."""
    bad_dash = '\u00e2\u0080\u0093'
    if bad_dash not in description or any(ord(c) >= 128 for c in description.replace(bad_dash, '')):
        raise ValueError('Unsupported dash recovery input')
    try:
        recovered = description.encode('latin1', errors='strict').decode('utf-8', errors='strict')
    except UnicodeError as error:
        raise ValueError('Non-reversible dash recovery') from error
    if (recovered.encode('utf-8').decode('latin1') != description
            or recovered != description.replace(bad_dash, '\u2013')
            or encoding_defect(recovered)):
        raise ValueError('Dash recovery changed unrelated text')
    return recovered


def apply_reviewed_recoveries(mode_rows, manifest, manifest_sha256, evidence):
    """Only the 56 explicit, checksum-bound mode/code originals may be recovered."""
    if (evidence['method'] != RECOVERY_METHOD or evidence['reference_version'] != manifest['reference_version']
            or evidence['reference_manifest_sha256'] != manifest_sha256 or len(evidence['entries']) != 56):
        raise ValueError('Recovery evidence does not match pinned reference')
    raw_lookup = prepare_lookup(mode_rows)
    resources = {r['mode']: r for r in manifest['resources']}
    approved = {}
    for entry in evidence['entries']:
        key = (entry['source_mode'], entry['raw_code'])
        original = raw_lookup.get(key)
        if (key in approved or original is None or original['status'] != 'encoding_defect'
                or original['source_descriptions'] != [entry['original_text']]
                or resources[key[0]]['sha256'] != entry['reference_sha256']):
            raise ValueError('Recovery entry is duplicate, changed, ambiguous or not eligible')
        recovered = recover_dash(entry['original_text'])
        if recovered != entry['recovered_text']:
            raise ValueError('Recovery result differs from reviewed evidence')
        approved[key] = recovered
    return {mode: [dict(row, DESCRIPTION=approved[(mode, row['CODE'])])
                  if (mode, row['CODE']) in approved else dict(row) for row in rows]
            for mode, rows in mode_rows.items()}


def load_reference(path=REFERENCE, *, recover=True):
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
    if recover:
        evidence = json.loads(RECOVERY.read_text(encoding='utf-8'))
        mode_rows = apply_reviewed_recoveries(mode_rows, manifest,
            hashlib.sha256(path.read_bytes()).hexdigest(), evidence)
    # Recheck ambiguity, blanks and encoding after the narrowly scoped recovery.
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
