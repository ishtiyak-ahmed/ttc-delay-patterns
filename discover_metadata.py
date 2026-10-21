#!/usr/bin/env python3
"""Discover Toronto Open Data metadata for TTC delay dataset packages.

Queries the City of Toronto CKAN Action API (package_show) for the four
TTC delay packages and writes resource metadata to source_manifest.json.

This script records catalog metadata only. It does not download dataset files.
"""

from __future__ import annotations

import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CKAN_PACKAGE_SHOW_URL = (
    "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
)
CKAN_API_HELP_URL = (
    "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/help_show"
    "?name=package_show"
)
PORTAL_DATASET_URL_TEMPLATE = "https://open.toronto.ca/dataset/{package_name}/"

# Candidate CKAN package names from official portal dataset URLs.
# These are catalog names, not resource identifiers.
CANDIDATE_PACKAGE_NAMES = [
    "ttc-subway-delay-data",
    "ttc-bus-delay-data",
    "ttc-streetcar-delay-data",
    "ttc-lrt-delay-data",
]

REQUEST_TIMEOUT_SECONDS = 30
USER_AGENT = "ttc-reliability-analytics/0.1 (source-metadata-discovery)"

SCRIPT_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = SCRIPT_DIR / "source_manifest.json"

REQUIRED_PACKAGE_FIELDS = ("id", "name", "resources")
OPTIONAL_PACKAGE_FIELDS = (
    "title",
    "state",
    "is_retired",
    "metadata_modified",
    "last_refreshed",
    "date_published",
    "refresh_rate",
    "num_resources",
    "license_title",
    "owner_division",
    "owner_email",
    "notes",
)
REQUIRED_RESOURCE_FIELDS = ("id", "name", "format", "url")
OPTIONAL_RESOURCE_FIELDS = (
    "size",
    "last_modified",
    "created",
    "metadata_modified",
    "mimetype",
    "url_type",
    "state",
    "package_id",
    "datastore_active",
    "is_datastore_cache_file",
    "record_count",
    "hash",
)
# Warn only for the optional fields this task is meant to capture.
# CKAN commonly returns empty hashes and omits record_count for file uploads.
OPTIONAL_RESOURCE_FIELDS_TO_WARN = (
    "size",
    "last_modified",
    "created",
    "metadata_modified",
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_ssl_context() -> ssl.SSLContext:
    """Use the default CA store; fall back to certifi if it is already installed.

    urllib on some Python.org macOS builds fails certificate verification.
    certifi is used only when already present. This script does not install it.
    """
    try:
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        return context
    except ssl.SSLError:
        pass

    try:
        import certifi
    except ImportError as exc:
        raise RuntimeError(
            "Could not create a verifying SSL context, and certifi is not "
            "installed. Install OS certificates or certifi before rerunning."
        ) from exc

    context = ssl.create_default_context(cafile=certifi.where())
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    return context


def http_get_json(url: str, ssl_context: ssl.SSLContext) -> tuple[int | None, Any, str | None]:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        method="GET",
    )
    try:
        with urllib.request.urlopen(
            request, timeout=REQUEST_TIMEOUT_SECONDS, context=ssl_context
        ) as response:
            status = response.status
            raw = response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body) if body else None
        except json.JSONDecodeError:
            parsed = None
        return exc.code, parsed, f"HTTP {exc.code}: {exc.reason}"
    except urllib.error.URLError as exc:
        return None, None, f"Request failed: {exc.reason}"
    except TimeoutError:
        return None, None, "Request timed out"

    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return status, None, f"Response was not valid JSON: {exc}"

    return status, parsed, None


def missing_or_null(record: dict[str, Any], field: str) -> bool:
    if field not in record:
        return True
    value = record[field]
    return value is None or value == ""


def copy_optional_fields(
    source: dict[str, Any], fields: tuple[str, ...]
) -> tuple[dict[str, Any], list[str]]:
    copied: dict[str, Any] = {}
    missing: list[str] = []
    for field in fields:
        if missing_or_null(source, field):
            copied[field] = None
            missing.append(field)
        else:
            copied[field] = source[field]
    return copied, missing


def summarize_resource(resource: Any, expected_package_uuid: str | None) -> dict[str, Any]:
    if not isinstance(resource, dict):
        return {
            "ok": False,
            "errors": ["Resource entry is not an object."],
            "warnings": [],
            "missing_optional_metadata": [],
            "resource": None,
        }

    errors: list[str] = []
    warnings: list[str] = []

    for field in REQUIRED_RESOURCE_FIELDS:
        if missing_or_null(resource, field):
            errors.append(f"Missing required resource field '{field}'.")

    optional, missing_optional = copy_optional_fields(resource, OPTIONAL_RESOURCE_FIELDS)

    resource_id = resource.get("id")
    package_id_on_resource = resource.get("package_id")
    if (
        expected_package_uuid
        and package_id_on_resource
        and package_id_on_resource != expected_package_uuid
    ):
        warnings.append(
            "Resource package_id does not match the parent package UUID "
            f"({package_id_on_resource!r} vs {expected_package_uuid!r})."
        )

    if resource_id and resource_id == expected_package_uuid:
        warnings.append("Resource id is identical to the parent package UUID.")

    summary = {
        "resource_id": resource_id if resource_id else None,
        "name": resource.get("name") if resource.get("name") else None,
        "format": resource.get("format") if resource.get("format") else None,
        "url": resource.get("url") if resource.get("url") else None,
        **optional,
    }
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "missing_optional_metadata": missing_optional,
        "resource": summary,
    }


def summarize_package(
    requested_name: str,
    http_status: int | None,
    payload: Any,
    request_error: str | None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    result: dict[str, Any] = {
        "requested_package_name": requested_name,
        "request_url": f"{CKAN_PACKAGE_SHOW_URL}?id={urllib.parse.quote(requested_name)}",
        "portal_url": PORTAL_DATASET_URL_TEMPLATE.format(package_name=requested_name),
        "http_status": http_status,
        "api_success": None,
        "package_name": None,
        "package_id": None,
        "title": None,
        "request_ok": False,
        "structure_ok": False,
        "errors": errors,
        "warnings": warnings,
        "missing_optional_metadata": [],
        "resources": [],
    }

    if request_error:
        errors.append(request_error)
        return result

    if http_status != 200:
        errors.append(f"Unexpected HTTP status {http_status}.")
        return result

    if not isinstance(payload, dict):
        errors.append("API response is not a JSON object.")
        return result

    if "success" not in payload or "result" not in payload:
        errors.append("API response is missing required keys 'success' and/or 'result'.")
        return result

    result["api_success"] = payload.get("success")
    if payload.get("success") is not True:
        errors.append(f"API reported success={payload.get('success')!r}.")
        error_detail = payload.get("error")
        if error_detail is not None:
            errors.append(f"API error detail: {error_detail!r}")
        return result

    package = payload.get("result")
    if not isinstance(package, dict):
        errors.append("API result is not a package object.")
        return result

    result["request_ok"] = True

    for field in REQUIRED_PACKAGE_FIELDS:
        if field not in package or package[field] in (None, ""):
            errors.append(f"Missing required package field '{field}'.")

    optional, missing_optional = copy_optional_fields(package, OPTIONAL_PACKAGE_FIELDS)
    result["missing_optional_metadata"] = missing_optional
    result.update(optional)

    package_name = package.get("name")
    package_id = package.get("id")
    result["package_name"] = package_name if package_name else None
    result["package_id"] = package_id if package_id else None
    result["title"] = optional.get("title")

    if package_name and package_name != requested_name:
        warnings.append(
            f"Returned package name {package_name!r} differs from requested name "
            f"{requested_name!r}."
        )
    if package_id and package_id == requested_name:
        warnings.append("Package UUID unexpectedly matches the requested package name.")

    resources = package.get("resources")
    if not isinstance(resources, list):
        errors.append("Package 'resources' is missing or is not a list.")
        return result

    declared_count = package.get("num_resources")
    if isinstance(declared_count, int) and declared_count != len(resources):
        warnings.append(
            f"num_resources={declared_count} does not match resources list length "
            f"{len(resources)}."
        )

    resource_ids: list[str] = []
    for index, resource in enumerate(resources):
        summarized = summarize_resource(resource, package_id if isinstance(package_id, str) else None)
        resource_record = summarized["resource"] or {
            "resource_id": None,
            "name": None,
            "format": None,
            "url": None,
            "position": index,
        }
        resource_record["position"] = index
        resource_record["errors"] = summarized["errors"]
        resource_record["warnings"] = summarized["warnings"]
        resource_record["missing_optional_metadata"] = [
            field
            for field in summarized["missing_optional_metadata"]
            if field in OPTIONAL_RESOURCE_FIELDS_TO_WARN
        ]
        result["resources"].append(resource_record)

        if not summarized["ok"]:
            errors.extend(
                f"Resource index {index}: {message}" for message in summarized["errors"]
            )
        warnings.extend(
            f"Resource index {index}: {message}" for message in summarized["warnings"]
        )
        resource_id = resource_record.get("resource_id")
        if isinstance(resource_id, str):
            if resource_id in resource_ids:
                warnings.append(f"Duplicate resource_id {resource_id!r}.")
            resource_ids.append(resource_id)

    result["structure_ok"] = not errors
    result["resource_count"] = len(result["resources"])
    return result


def build_manifest(package_records: list[dict[str, Any]]) -> dict[str, Any]:
    failed_packages = [
        record["requested_package_name"]
        for record in package_records
        if not record.get("request_ok") or not record.get("structure_ok")
    ]
    inventory_complete = not failed_packages

    warnings: list[str] = []
    errors: list[str] = []
    for record in package_records:
        name = record["requested_package_name"]
        for message in record["warnings"]:
            warnings.append(f"{name}: {message}")
        for message in record["errors"]:
            errors.append(f"{name}: {message}")
        for field in record.get("missing_optional_metadata", []):
            warnings.append(f"{name}: optional package field '{field}' is missing or empty.")
        for resource in record.get("resources", []):
            resource_label = resource.get("resource_id") or resource.get("name") or f"position {resource.get('position')}"
            for field in resource.get("missing_optional_metadata", []):
                warnings.append(
                    f"{name} / {resource_label}: optional resource field '{field}' "
                    "is missing or empty."
                )

    return {
        "retrieved_at_utc": utc_now_iso(),
        "inventory_complete": inventory_complete,
        "failed_package_requests": failed_packages,
        "api": {
            "package_show_url": CKAN_PACKAGE_SHOW_URL,
            "help_url": CKAN_API_HELP_URL,
            "note": (
                "City of Toronto Open Data is served by CKAN. package_show "
                "returns catalog metadata for a package name or UUID. Package "
                "names/UUIDs are distinct from resource IDs."
            ),
        },
        "requested_package_names": CANDIDATE_PACKAGE_NAMES,
        "errors": errors,
        "warnings": warnings,
        "packages": package_records,
    }


def print_summary(manifest: dict[str, Any]) -> None:
    print(f"Wrote {MANIFEST_PATH}")
    print(f"Retrieved at (UTC): {manifest['retrieved_at_utc']}")
    print(f"Inventory complete: {manifest['inventory_complete']}")
    if manifest["failed_package_requests"]:
        print("Failed package requests:")
        for name in manifest["failed_package_requests"]:
            print(f"  - {name}")

    for package in manifest["packages"]:
        status = "OK" if package.get("request_ok") and package.get("structure_ok") else "FAILED"
        print(
            f"[{status}] {package['requested_package_name']} "
            f"http={package['http_status']} "
            f"package_id={package.get('package_id')} "
            f"resources={len(package.get('resources', []))}"
        )

    if manifest["errors"]:
        print("Errors:")
        for message in manifest["errors"]:
            print(f"  - {message}")
    if manifest["warnings"]:
        print("Warnings:")
        for message in manifest["warnings"]:
            print(f"  - {message}")


def main() -> int:
    try:
        ssl_context = build_ssl_context()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    # urllib on some macOS Python builds rejects the default CA bundle even
    # though create_default_context() succeeds. Probe once and switch to
    # certifi if it is already installed.
    probe_url = f"{CKAN_PACKAGE_SHOW_URL}?id={urllib.parse.quote(CANDIDATE_PACKAGE_NAMES[0])}"
    status, _, error = http_get_json(probe_url, ssl_context)
    if error and "CERTIFICATE_VERIFY_FAILED" in error:
        try:
            import certifi
        except ImportError:
            print(
                "ERROR: TLS certificate verification failed and certifi is not "
                "installed. Refusing to disable verification.",
                file=sys.stderr,
            )
            return 1
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        print("WARNING: Default CA store failed verification; using existing certifi bundle.")

    package_records: list[dict[str, Any]] = []
    for package_name in CANDIDATE_PACKAGE_NAMES:
        url = f"{CKAN_PACKAGE_SHOW_URL}?id={urllib.parse.quote(package_name)}"
        http_status, payload, request_error = http_get_json(url, ssl_context)
        package_records.append(
            summarize_package(package_name, http_status, payload, request_error)
        )

    manifest = build_manifest(package_records)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print_summary(manifest)

    if not manifest["inventory_complete"]:
        print(
            "Manifest was written, but inventory_complete is false because at "
            "least one package request failed or had an unexpected structure.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
