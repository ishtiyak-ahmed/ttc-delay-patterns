"""Acquire an explicitly selected approved TTC tracer using the installed certifi trust store."""
import argparse
import hashlib
import json
import ssl
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import certifi

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = {
    'subway': '0b6e5c52-e993-46d6-8d74-8602ee224457',
    'bus': 'b5725365-9252-4bfe-b6f4-cda7ddf74341',
    'streetcar': 'cf2fdd12-6f0e-4644-aae7-0bbfc31df031',
    'lrt': '9a800c92-0362-4cee-8232-7374596b6a43',
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=RESOURCES, default='subway')
    args = parser.parse_args()
    resource_id = RESOURCES[args.mode]
    manifest = json.loads((ROOT / 'source_manifest.json').read_text())
    matches = [(p, r) for p in manifest['packages'] for r in p['resources'] if r['resource_id'] == resource_id]
    assert len(matches) == 1
    package, resource = matches[0]
    assert package['package_name'] == 'ttc-' + args.mode + '-delay-data'
    assert resource['format'] == 'CSV'
    assert resource['name'] == ('TTC LRT Delays.csv' if args.mode == 'lrt' else 'TTC ' + args.mode.capitalize() + ' Delay Data since 2025.csv')
    context = ssl.create_default_context(cafile=certifi.where())
    assert context.check_hostname and context.verify_mode == ssl.CERT_REQUIRED
    started = datetime.now(timezone.utc)
    stamp = started.strftime('%Y%m%dT%H%M%S%fZ')
    request = urllib.request.Request(resource['url'], headers={'User-Agent': 'ttc-reliability-analytics/0.1', 'Accept-Encoding': 'identity'})
    # Complete the verified request before creating a raw file. Never overwrite a snapshot.
    with urllib.request.urlopen(request, context=context, timeout=60) as response:
        assert response.status == 200, response.status
        body = response.read()
        assert body, 'Empty response'
        length = response.headers.get('Content-Length')
        if length is not None:
            assert len(body) == int(length), 'Incomplete response'
        record = dict(package_name=package['package_name'], package_id=package['package_id'], resource_id=resource_id,
                      resource_name=resource['name'], source_url=resource['url'], final_url=response.geturl(),
                      attempt_started_at_utc=started.isoformat(), retrieved_at_utc=datetime.now(timezone.utc).isoformat(),
                      http_status=response.status, response_headers=dict(response.headers.items()),
                      python_executable=sys.executable, python_version=sys.version, ca_bundle=certifi.where(),
                      ca_bundle_sha256=hashlib.sha256(Path(certifi.where()).read_bytes()).hexdigest(),
                      certificate_verification='CERT_REQUIRED', hostname_verification=True,
                      file_size_bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), status='downloaded')
    raw = ROOT / 'data/raw' / args.mode / (stamp + '__' + resource_id + '.csv')
    raw.parent.mkdir(parents=True, exist_ok=True)
    with raw.open('xb') as output:
        output.write(body)
    record['raw_path'] = str(raw.relative_to(ROOT))
    provenance = ROOT / 'data/provenance' / (stamp + '__' + args.mode + '.json')
    provenance.parent.mkdir(parents=True, exist_ok=True)
    with provenance.open('x') as output:
        json.dump(record, output, indent=2)
        output.write('\n')
    print(json.dumps(record, indent=2))
    print('Provenance:', provenance)

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        failed = ROOT / 'data/provenance' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '__failed_attempt.json')
        failed.parent.mkdir(parents=True, exist_ok=True)
        with failed.open('x') as output:
            json.dump({'status': 'failed', 'command': sys.argv, 'error_type': type(exc).__name__, 'error': str(exc), 'failed_at_utc': datetime.now(timezone.utc).isoformat()}, output, indent=2)
        raise
