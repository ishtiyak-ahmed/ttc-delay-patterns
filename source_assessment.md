# Source assessment — 2025-onward TTC delay resources

Assessment date: 2026-10-21  
Catalog snapshot: `source_manifest.json`, `retrieved_at_utc` `2026-10-21T15:29:29+00:00`, `inventory_complete` true.

This note uses the local manifest first. No dataset files were downloaded. Values below are copied from that snapshot unless labelled otherwise.

## How to read this note

- **Confirmed (manifest):** present in `source_manifest.json`.
- **Inference:** a reasonable reading of names, formats, or CKAN resource types. Not verified against file contents.
- **Unresolved:** cannot be answered without inspecting files, watching updates over time, or additional official documentation.

A 2025-onward analysis scope does not mean these resources are complete, consistent, or continuously appended. Package `refresh_rate` of `Monthly` does not establish publication mechanics.

The complete inventory, including yearly 2014–2024 files, remains in `source_manifest.json`. Those historical resources are out of the initial ingestion scope and are mentioned only as catalog context.

## Catalog context retained from earlier research

Subway, Bus, and Streetcar packages contain historical XLSX delay files whose names indicate periods within 2014–2024, plus newer resources whose names include `since 2025`. Bus and Streetcar have yearly labels; Subway includes a combined January 2014–April 2017 workbook and a separate May–December 2017 workbook, followed by yearly 2018–2024 labels. The LRT package has no yearly 2014–2024 delay files. That catalog split is why the initial version can target 2025-onward resources without ingesting the older yearly workbooks. It does not prove that the newer resources begin on 2025-01-01, that they exclude earlier dates, or that they share a schema with the yearly files.

---

## Subway — package `ttc-subway-delay-data`

Portal: https://open.toronto.ca/dataset/ttc-subway-delay-data/  
Package UUID: `996cfe8d-fb35-40ce-b569-698d51fc683b`

| Field | Manifest value |
|---|---|
| title | TTC Subway Delay Data |
| state / is_retired | `active` / `false` |
| date_published | `2019-07-23 18:12:29.554797` |
| last_refreshed | `2026-09-21 12:50:39.597734` |
| metadata_modified | `2026-09-21T12:50:42.489293` |
| refresh_rate | Monthly |
| num_resources | 19 |
| license_title | missing |
| notes | `TTC Subway & SRT Train Service Delay Data` |

### Resources that appear relevant to 2025-onward delay records

| Role | resource_id | name | format | url_type | size | last_modified | created | record_count | URL |
|---|---|---|---|---|---|---|---|---|---|
| Delay datastore table | `6088e14f-e46e-4f5c-9daa-dea1359ad396` | TTC Subway Delay Data since 2025 | XLSX | datastore | null | null | `2025-03-11T17:35:14.714319` | 45475 | https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/6088e14f-e46e-4f5c-9daa-dea1359ad396 |
| Delay CSV cache | `0b6e5c52-e993-46d6-8d74-8602ee224457` | TTC Subway Delay Data since 2025.csv | CSV | upload | 3069485 | `2026-09-21T12:50:36.746003` | `2025-03-11T17:39:39.023085` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/0b6e5c52-e993-46d6-8d74-8602ee224457/download/ttc-subway-delay-data-since-2025.csv |
| Delay XML cache | `021e6a9d-d31e-436a-bea5-72461f3faa3b` | TTC Subway Delay Data since 2025.xml | XML | upload | 11217078 | `2026-09-21T12:50:38.421804` | `2025-03-11T17:39:40.410565` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/021e6a9d-d31e-436a-bea5-72461f3faa3b/download/ttc-subway-delay-data-since-2025.xml |
| Delay JSON cache | `fed58a09-14bc-403f-9166-00397c7822a7` | TTC Subway Delay Data since 2025.json | JSON | upload | 9104182 | `2026-09-21T12:50:39.597734` | `2025-03-11T17:39:41.661188` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/fed58a09-14bc-403f-9166-00397c7822a7/download/ttc-subway-delay-data-since-2025.json |

Related lookup resources created in 2025 (not delay incident files):

| Role | resource_id | name | format | url_type | size | last_modified | record_count | URL |
|---|---|---|---|---|---|---|---|---|
| Code datastore table | `9e9efbb6-3a2f-4934-ac94-9150ecaeb548` | Code Descriptions | XLSX | datastore | null | null | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/9e9efbb6-3a2f-4934-ac94-9150ecaeb548 |
| Code CSV cache | `b2d8f5e0-0997-46b5-8abd-caa685a0290b` | Code Descriptions.csv | CSV | upload | 5610 | `2025-04-07T19:22:45.345293` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/b2d8f5e0-0997-46b5-8abd-caa685a0290b/download/code-descriptions.csv |
| Code XML cache | 17c3d86c-0691-4227-b546-eda280ef6fec | Code Descriptions.xml | XML | upload | 15374 | 2025-04-07T19:22:46.878337 | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/17c3d86c-0691-4227-b546-eda280ef6fec/download/code-descriptions.xml |
| Code JSON cache | 5bfef644-1bd8-4b8a-849b-95697c845cdc | Code Descriptions.json | JSON | upload | 11222 | 2025-04-07T19:22:48.430241 | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/5bfef644-1bd8-4b8a-849b-95697c845cdc/download/code-descriptions.json |

Names and cache flags suggest alternate lookup encodings; content equivalence has not been checked.

The package also still contains `ttc-subway-delay-codes` (`3900e649-f31e-4b79-9f20-4731bbfd94f7`, XLSX, `last_modified` `2022-04-06T18:51:05`). That file is older than the 2025 Code Descriptions resources. Whether it still applies to 2025-onward delay codes is unresolved. Its catalog URL is https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/3900e649-f31e-4b79-9f20-4731bbfd94f7/download/ttc-subway-delay-codes.xlsx.

### What the metadata establishes

- Confirmed: a resource named `TTC Subway Delay Data since 2025` exists as a CKAN datastore table (`url_type` `datastore`, `datastore_active` true, format labelled `XLSX` but URL is a datastore dump).
- Confirmed: CSV, XML, and JSON resources with the same "since 2025" name prefix exist as uploads with `is_datastore_cache_file` true, non-null sizes, and `last_modified` on 2026-09-21.
- Confirmed: the datastore delay resource reports `record_count` 45475. That is catalog metadata, not a verified file row count.
- Confirmed: package-level `refresh_rate` is Monthly and `last_refreshed` is 2026-09-21.
- Inference: the CSV/XML/JSON files are generated exports of the datastore table. The close created timestamps (datastore 17:35, caches 17:39 on 2025-03-11) support that reading. Identity of rows across encodings has not been checked.

### Still needs to be checked in the actual file

Schema, date field, actual min/max dates, missing months, zero-minute records, duplicate rows, code fields, and whether CSV row count matches `record_count` 45475. Also whether "SRT" in the package notes still appears in 2025-onward records.

---

## Bus — package `ttc-bus-delay-data`

Portal: https://open.toronto.ca/dataset/ttc-bus-delay-data/  
Package UUID: `e271cdae-8788-4980-96ce-6a5c95bc6618`

| Field | Manifest value |
|---|---|
| title | TTC Bus Delay Data |
| state / is_retired | `active` / `false` |
| date_published | `2019-07-23 18:10:36.791844` |
| last_refreshed | `2026-09-21 12:32:40.647204` |
| metadata_modified | `2026-09-21T12:32:42.839445` |
| refresh_rate | Monthly |
| num_resources | 20 |
| license_title | missing |

### Resources that appear relevant to 2025-onward delay records

| Role | resource_id | name | format | url_type | size | last_modified | created | record_count | URL |
|---|---|---|---|---|---|---|---|---|---|
| Delay datastore table | `c3451ac9-c04a-4645-bd80-0e2a3b7d7199` | TTC Bus Delay Data since 2025 | XLSX | datastore | null | null | `2025-03-11T17:35:13.755913` | 102257 | https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/c3451ac9-c04a-4645-bd80-0e2a3b7d7199 |
| Delay CSV cache | `b5725365-9252-4bfe-b6f4-cda7ddf74341` | TTC Bus Delay Data since 2025.csv | CSV | upload | 9492730 | `2026-09-21T12:32:37.710724` | `2025-03-11T17:39:02.523907` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/e271cdae-8788-4980-96ce-6a5c95bc6618/resource/b5725365-9252-4bfe-b6f4-cda7ddf74341/download/ttc-bus-delay-data-since-2025.csv |
| Delay XML cache | `7124b998-bcaa-49a1-91d9-ee4e7137704f` | TTC Bus Delay Data since 2025.xml | XML | upload | 27775911 | `2026-09-21T12:32:39.283318` | `2025-03-11T17:39:03.957146` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/e271cdae-8788-4980-96ce-6a5c95bc6618/resource/7124b998-bcaa-49a1-91d9-ee4e7137704f/download/ttc-bus-delay-data-since-2025.xml |
| Delay JSON cache | `69a35f47-9f24-4080-8d52-708b040e6300` | TTC Bus Delay Data since 2025.json | JSON | upload | 23035665 | `2026-09-21T12:32:40.647204` | `2025-03-11T17:39:05.388079` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/e271cdae-8788-4980-96ce-6a5c95bc6618/resource/69a35f47-9f24-4080-8d52-708b040e6300/download/ttc-bus-delay-data-since-2025.json |

Related lookup:

| Role | resource_id | name | format | url_type | size | last_modified | URL |
|---|---|---|---|---|---|---|---|
| Code datastore table | `816f2214-97e2-4c4b-820e-24b425ed08e0` | Code Descriptions | XLSX | datastore | null | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/816f2214-97e2-4c4b-820e-24b425ed08e0 |
| Code CSV cache | `874ae66c-9f6f-443f-91e0-1d37d416e0d8` | Code Descriptions.csv | CSV | upload | 1340 | `2025-04-07T19:21:37.400182` | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/e271cdae-8788-4980-96ce-6a5c95bc6618/resource/874ae66c-9f6f-443f-91e0-1d37d416e0d8/download/code-descriptions.csv |
| Code XML cache | efecb2d3-018f-49c9-887c-2d83d7c8f3c3 | Code Descriptions.xml | XML | upload | 4538 | 2025-04-07T19:21:38.980018 | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/e271cdae-8788-4980-96ce-6a5c95bc6618/resource/efecb2d3-018f-49c9-887c-2d83d7c8f3c3/download/code-descriptions.xml |
| Code JSON cache | 1fd9edd5-fc3a-4c1d-b524-95efcdc8eb8a | Code Descriptions.json | JSON | upload | 3142 | 2025-04-07T19:21:40.629062 | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/e271cdae-8788-4980-96ce-6a5c95bc6618/resource/1fd9edd5-fc3a-4c1d-b524-95efcdc8eb8a/download/code-descriptions.json |

Names and cache flags suggest alternate lookup encodings; content equivalence has not been checked.

### What the metadata establishes

- Confirmed: the same datastore-plus-three-cache pattern as subway, with names `TTC Bus Delay Data since 2025`.
- Confirmed: datastore `record_count` 102257; CSV size 9,492,730 bytes; `last_modified` 2026-09-21.
- Confirmed: bus datastore `record_count` is larger than subway (45475) and streetcar (23703). That is not a reliability comparison. Exposure, reporting practice, and coverage are unknown.
- Confirmed: Code Descriptions.csv is much smaller than subway's equivalent (1340 vs 5610 bytes). Byte size alone does not establish the number of codes, schema, or categories in either file.

### Still needs to be checked in the actual file

Schema versus subway/streetcar/LRT, date coverage, missing periods, route identifier fields, duration field, and whether 102257 catalog records match the CSV.

---

## Streetcar — package `ttc-streetcar-delay-data`

Portal: https://open.toronto.ca/dataset/ttc-streetcar-delay-data/  
Package UUID: `b68cb71b-44a7-4394-97e2-5d2f41462a5d`

| Field | Manifest value |
|---|---|
| title | TTC Streetcar Delay Data |
| state / is_retired | `active` / `false` |
| date_published | `2019-07-23 18:12:13.621158` |
| last_refreshed | `2026-09-21 12:39:58.077997` |
| metadata_modified | `2026-09-21T12:39:59.732861` |
| refresh_rate | Monthly |
| num_resources | 21 |
| license_title | missing |

### Resources that appear relevant to 2025-onward delay records

| Role | resource_id | name | format | url_type | size | last_modified | created | record_count | URL |
|---|---|---|---|---|---|---|---|---|---|
| Delay datastore table | `7d545629-745c-4fbf-a348-76692bb2772d` | TTC Streetcar Delay Data since 2025 | XLSX | datastore | null | null | `2025-03-11T17:35:13.756825` | 23703 | https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/7d545629-745c-4fbf-a348-76692bb2772d |
| Delay CSV cache | `cf2fdd12-6f0e-4644-aae7-0bbfc31df031` | TTC Streetcar Delay Data since 2025.csv | CSV | upload | 1882886 | `2026-09-21T12:39:55.662429` | `2025-03-11T17:38:20.255805` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b68cb71b-44a7-4394-97e2-5d2f41462a5d/resource/cf2fdd12-6f0e-4644-aae7-0bbfc31df031/download/ttc-streetcar-delay-data-since-2025.csv |
| Delay XML cache | `e0e35789-0ac4-4042-9c5b-d1cd9f7e180e` | TTC Streetcar Delay Data since 2025.xml | XML | upload | 6113645 | `2026-09-21T12:39:57.080640` | `2025-03-11T17:38:21.564072` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b68cb71b-44a7-4394-97e2-5d2f41462a5d/resource/e0e35789-0ac4-4042-9c5b-d1cd9f7e180e/download/ttc-streetcar-delay-data-since-2025.xml |
| Delay JSON cache | `6f3c2a92-a348-41e4-b31c-15dcb14d50bf` | TTC Streetcar Delay Data since 2025.json | JSON | upload | 5022967 | `2026-09-21T12:39:58.077997` | `2025-03-11T17:38:23.164165` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b68cb71b-44a7-4394-97e2-5d2f41462a5d/resource/6f3c2a92-a348-41e4-b31c-15dcb14d50bf/download/ttc-streetcar-delay-data-since-2025.json |

Related lookup:

| Role | resource_id | name | format | url_type | size | last_modified | URL |
|---|---|---|---|---|---|---|---|
| Code datastore table | `b1fc714c-c533-424c-8ce4-4994e9c6fb1d` | Code Descriptions | XLSX | datastore | null | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/b1fc714c-c533-424c-8ce4-4994e9c6fb1d |
| Code CSV cache | `06d13be4-a8b7-4365-ac68-2169de8e0630` | Code Descriptions.csv | CSV | upload | 2791 | `2025-04-07T19:22:11.131875` | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b68cb71b-44a7-4394-97e2-5d2f41462a5d/resource/06d13be4-a8b7-4365-ac68-2169de8e0630/download/code-descriptions.csv |
| Code XML cache | b52ce141-2d85-40b0-9eb8-d197619aa5ff | Code Descriptions.xml | XML | upload | 8676 | 2025-04-07T19:22:12.736884 | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b68cb71b-44a7-4394-97e2-5d2f41462a5d/resource/b52ce141-2d85-40b0-9eb8-d197619aa5ff/download/code-descriptions.xml |
| Code JSON cache | 4f2f6528-3c3b-4dd8-91c4-b71fba78f457 | Code Descriptions.json | JSON | upload | 6096 | 2025-04-07T19:22:14.298587 | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b68cb71b-44a7-4394-97e2-5d2f41462a5d/resource/4f2f6528-3c3b-4dd8-91c4-b71fba78f457/download/code-descriptions.json |

Names and cache flags suggest alternate lookup encodings; content equivalence has not been checked.

### Catalog complication outside initial ingestion

Two historical streetcar resources are both named as 2020 files:

- `71b8b735-8a89-45a9-afb0-3edc38b2fad9`, name `ttc-streetcar-delay-data-2020` plus a trailing tab character, URL ending `ttc-streetcar-delay-data-202009.xlsx`
- `082d481b-f94f-4dee-9a5f-08eb9784053e`, name `ttc-streetcar-delay-data-2020`, URL ending `ttc-streetcar-delay-data-2020.xlsx`

Both have size 500709. They are not 2025-onward inputs. They remain in the inventory because the discovery manifest is meant to stay complete.

### What the metadata establishes

- Confirmed: same 2025 datastore-plus-cache pattern as subway and bus.
- Confirmed: datastore `record_count` 23703; CSV size 1,882,886 bytes; `last_modified` 2026-09-21.
- Confirmed: the 2025-onward streetcar delay resources do not have the duplicate-name problem seen in the 2020 historical files.

### Still needs to be checked in the actual file

Schema, date coverage, location/route fields, and comparability with bus and subway. Do not assume streetcar "since 2025" matches the other modes field-for-field because the resource names are parallel.

---

## LRT — package `ttc-lrt-delay-data`

Portal: https://open.toronto.ca/dataset/ttc-lrt-delay-data/  
Package UUID: `d4d64b0e-2945-4c92-960e-f0103ad48b02`

| Field | Manifest value |
|---|---|
| title | TTC LRT Delay Data |
| state / is_retired | `active` / `false` |
| date_published | `2026-01-20 21:46:35.950138` |
| last_refreshed | `2026-09-21 12:20:18.624795` |
| metadata_modified | `2026-09-21T12:20:20.830755` |
| refresh_rate | Monthly |
| num_resources | 8 |
| license_title | License not specified |
| notes | Timing, location, and cause of TTC LRT delays |

### Resources that appear relevant to the initial LRT scope

LRT has no resource named `since 2025`. The delay series in this package is:

| Role | resource_id | name | format | url_type | size | last_modified | created | record_count | URL |
|---|---|---|---|---|---|---|---|---|---|
| Delay datastore table | `8de5f6e3-9e5b-49c5-9f06-9f3b556966ec` | TTC LRT Delays | XLSX | datastore | null | null | `2026-01-21T17:51:56.410514` | 4569 | https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/8de5f6e3-9e5b-49c5-9f06-9f3b556966ec |
| Delay CSV cache | `9a800c92-0362-4cee-8232-7374596b6a43` | TTC LRT Delays.csv | CSV | upload | 313915 | `2026-09-21T12:20:15.577596` | `2026-01-21T17:53:19.592499` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/d4d64b0e-2945-4c92-960e-f0103ad48b02/resource/9a800c92-0362-4cee-8232-7374596b6a43/download/ttc-lrt-delays.csv |
| Delay XML cache | `3f28065f-835c-4f11-a5bc-81fd0a23cbf0` | TTC LRT Delays.xml | XML | upload | 1124621 | `2026-09-21T12:20:17.321061` | `2026-01-21T17:53:20.806607` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/d4d64b0e-2945-4c92-960e-f0103ad48b02/resource/3f28065f-835c-4f11-a5bc-81fd0a23cbf0/download/ttc-lrt-delays.xml |
| Delay JSON cache | `3888954e-21e9-4563-8d08-6d2bbd666184` | TTC LRT Delays.json | JSON | upload | 918516 | `2026-09-21T12:20:18.624795` | `2026-01-21T17:53:22.275779` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/d4d64b0e-2945-4c92-960e-f0103ad48b02/resource/3888954e-21e9-4563-8d08-6d2bbd666184/download/ttc-lrt-delays.json |

Related lookup:

| Role | resource_id | name | format | url_type | size | last_modified | record_count | URL |
|---|---|---|---|---|---|---|---|---|
| Code datastore table | `1df53164-1023-40c1-900e-def362d105e4` | Code Descriptions | XLSX | datastore | null | null | 130 | https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/1df53164-1023-40c1-900e-def362d105e4 |
| Code CSV cache | `662bc8f7-887f-4112-8b8d-dbc6bc4ebfb1` | Code Descriptions.csv | CSV | upload | 4928 | `2026-02-20T18:31:37.182708` | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/d4d64b0e-2945-4c92-960e-f0103ad48b02/resource/662bc8f7-887f-4112-8b8d-dbc6bc4ebfb1/download/code-descriptions.csv |
| Code XML cache | 201d0a1f-27e1-4bba-b657-ccc6f0bcaffb | Code Descriptions.xml | XML | upload | 13954 | 2026-02-20T18:31:38.127430 | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/d4d64b0e-2945-4c92-960e-f0103ad48b02/resource/201d0a1f-27e1-4bba-b657-ccc6f0bcaffb/download/code-descriptions.xml |
| Code JSON cache | feca337a-7df4-42e3-8345-7c8c00bd837d | Code Descriptions.json | JSON | upload | 9830 | 2026-02-20T18:31:39.175306 | null | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/d4d64b0e-2945-4c92-960e-f0103ad48b02/resource/feca337a-7df4-42e3-8345-7c8c00bd837d/download/code-descriptions.json |

Names and cache flags suggest alternate lookup encodings; content equivalence has not been checked.

### What the metadata establishes

- Confirmed: LRT is a separate package with 8 resources, all delay or code-description encodings. There are no yearly 2014–2024 LRT delay workbooks in this catalog snapshot.
- Confirmed: package `date_published` is 2026-01-20; delay resources were created 2026-01-21. That is the catalog publication date, not the first incident date.
- Confirmed: delay datastore `record_count` 4569; CSV size 313,915 bytes; delay CSV `last_modified` 2026-09-21, same calendar day as the other modes' 2025 delay caches.
- Confirmed: LRT Code Descriptions datastore reports `record_count` 130. Subway/bus/streetcar code datastore tables have `record_count` null in this snapshot.
- Confirmed: LRT code CSV `last_modified` is 2026-02-20, not 2026-09-21. The delay CSV was modified more recently than the code CSV.
- Inference: LRT is a candidate for the initial scope because it is the only delay series listed. That does not prove the file starts in 2025, contains all LRT lines, or matches subway/bus/streetcar fields.

### Still needs to be checked in the actual file

Whether dates begin in 2025, 2026, or another period; which LRT lines are present; schema versus the other three modes; and whether "cause" in the package notes is a reported category rather than a verified root cause.

---

## Supporting documentation and shared metadata caveats

All four packages list `owner_division` as `Toronto Transit Commission` and `owner_email` as `opendata@ttc.ca`. The delay and code datastore resources are `active`, have `datastore_active` true, null size and `last_modified`, and an XLSX format/MIME label. Their dump URLs do not establish the response format. The corresponding cache resources are `active` uploads, have `datastore_active` false and `is_datastore_cache_file` true, and use MIME type `application/octet-stream`. Format labels still require parsing verification. All 68 resource `hash` values are null; no source checksum is available in this snapshot. Resource `metadata_modified` is catalog metadata, not evidence of changed rows; exact values and lookup creation timestamps remain in the manifest.

The three older modes also list README workbooks. Their applicability to the current resources is unverified. Consult them later if needed to interpret fields; they are supporting documentation, not historical incident inputs or a mandatory addition to the tracer set.

| Role | resource_id | name | format | url_type | size | last_modified | URL |
|---|---|---|---|---|---|---|---|
| Documentation | ca43ac3d-3940-4315-889b-a9375e7b8aa4 | ttc-subway-delay-data-readme | XLSX | upload | 12704 | 2022-04-06T18:51:09 | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/ca43ac3d-3940-4315-889b-a9375e7b8aa4/download/ttc-subway-delay-readme.xlsx |
| Documentation | 71bb1283-7388-4d23-aa4e-0f393a80abce | ttc-bus-delay-data-readme | XLSX | upload | 12839 | 2022-04-05T19:21:58 | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/e271cdae-8788-4980-96ce-6a5c95bc6618/resource/71bb1283-7388-4d23-aa4e-0f393a80abce/download/ttc-bus-delay-data-readme.xlsx |
| Documentation | 0fe61851-c67b-49bc-8c27-3a89b33b43af | ttc-streetcar-delay-data-readme | XLSX | upload | 12886 | 2022-04-05T19:14:38 | https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b68cb71b-44a7-4394-97e2-5d2f41462a5d/resource/0fe61851-c67b-49bc-8c27-3a89b33b43af/download/ttc-streetcar-delay-data-readme.xlsx |

## Smallest set of resources to inspect next

The four delay CSV caches below are the minimum representative candidate set for eventual coverage of all four modes: one encoding per mode. For Task 2.1, use this metadata to propose one tracer and justify any necessary second resource. This is a candidate list, not a direction to acquire all four files. Acquisition belongs to Task 2.2 after selection and approval; actual schema and coverage profiling belongs to Task 2.3. Extend inspection to the remaining modes when needed.

| Mode | resource_id | name | Why this file |
|---|---|---|---|
| Subway | `0b6e5c52-e993-46d6-8d74-8602ee224457` | TTC Subway Delay Data since 2025.csv | Named 2025-onward subway delay file; downloadable upload with size and `last_modified`; CSV is simpler to profile than XML/JSON; datastore dump is labelled XLSX but is not a static file with size metadata. |
| Bus | `b5725365-9252-4bfe-b6f4-cda7ddf74341` | TTC Bus Delay Data since 2025.csv | Same role for bus. Parallel names do not prove a shared schema, so bus must be inspected separately. |
| Streetcar | `cf2fdd12-6f0e-4644-aae7-0bbfc31df031` | TTC Streetcar Delay Data since 2025.csv | Same role for streetcar. Needed to test whether streetcar fields align with bus. |
| LRT | `9a800c92-0362-4cee-8232-7374596b6a43` | TTC LRT Delays.csv | Only LRT delay series in the package. The name does not include `since 2025`, so coverage has to be read from the file. |

For subsequent approved acquisition, consider XML, JSON, or datastore dumps only if a selected CSV is missing, unreadable, or appears incomplete; justify the additional resource.

Code-description CSVs are the next files to inspect if the delay CSVs contain code fields that need a lookup. They are not required to answer "what columns and dates are in the delay files." If needed, start with:

- Subway `b2d8f5e0-0997-46b5-8abd-caa685a0290b`
- Bus `874ae66c-9f6f-443f-91e0-1d37d416e0d8`
- Streetcar `06d13be4-a8b7-4365-ac68-2169de8e0630`
- LRT `662bc8f7-887f-4112-8b8d-dbc6bc4ebfb1`

No final tracer is selected here. Task 2.1 should propose one resource from this candidate set, explain its suitability and remaining coverage uncertainty, and document any justified additional inspection.

## Questions that could change pipeline design

1. **Do the four delay CSVs share compatible fields?** If not, the project can still keep four modes, but only some columns can be standardized.
2. **What dates are actually present?** Resource names are not coverage. LRT in particular may start later than 2025-01-01.
3. **Are the CSV caches full exports of the datastore tables?** If not, the pipeline may need the datastore dump or a different encoding.
4. **When a monthly refresh occurs, is the CSV replaced in place under the same resource ID?** `last_modified` on 2026-09-21 for all four delay CSVs is consistent with a shared refresh day. It does not prove in-place replacement, append, or rewrite of older rows.
5. **Can previously published 2025-onward rows change?** If they can, hashes and snapshots matter more than append-only logic.
6. **Are code tables mode-specific, and do they change independently of delay files?** LRT codes were last modified 2026-02-20 while LRT delays were last modified 2026-09-21.
7. **Which encoding should the pipeline ingest going forward?** CSV is the practical first choice. That choice should be confirmed after parsing and row-count checks.
8. **Does "since 2025" include all of 2025, or only records after the March 2025 resource creation date?** Resource `created` timestamps are 2025-03-11 for subway/bus/streetcar delay tables. That is not the incident date range.

## What we need to learn about monthly updates

Confirmed from the manifest:

- All four packages report `refresh_rate` `Monthly`.
- All four packages have `last_refreshed` on 2026-09-21.
- The four delay CSV caches also have `last_modified` on 2026-09-21.
- The snapshot lists named current delay series and no separate yearly 2025 delay workbook. A single snapshot cannot establish whether future updates retain IDs or introduce replacement resources.

Still unknown, and required before implementing update logic:

- Whether the City replaces the CSV bytes under the same resource ID.
- Whether datastore `record_count` only grows, or can shrink if rows are corrected or removed.
- Whether older months in a "since 2025" table are revised after first publication.
- How to detect a change: resource `last_modified`, file checksum, `record_count`, or a combination.
- How to rerun safely without duplicating incidents if the file is a full replacement each month.
- Whether a replacement receives a new resource ID or URL, and whether removed or superseded resources remain discoverable.
- Publication lag, missed refreshes, and whether metadata timestamps reliably signal changes to file contents.

Investigate these questions using official publication documentation and successive dated metadata and raw snapshots after acquisition is approved. Compare IDs, URLs, timestamps, byte hashes, schema, date coverage, and record-level differences for overlapping periods. A single snapshot or increasing total count cannot rule out historical revisions. Check lookup versions independently. This is an evidence plan, not an implemented update strategy.

Do not implement an append-only monthly job from this metadata.

## Confirmed facts versus inferences versus unresolved questions

### Confirmed (manifest)

- The four delay packages exist, are `active`, and are not marked retired in CKAN.
- Subway, bus, and streetcar each have a resource named `... since 2025` plus CSV/XML/JSON caches.
- LRT has `TTC LRT Delays` plus CSV/XML/JSON caches, and no yearly historical delay workbooks in this snapshot.
- Package names, package UUIDs, and resource IDs are distinct.
- Size and `last_modified` are present on the CSV caches and absent on the datastore tables.
- Datastore delay `record_count` values are subway 45475, bus 102257, streetcar 23703, LRT 4569.
- Historical yearly XLSX files remain in the subway, bus, and streetcar packages.

### Inferences

- CSV/XML/JSON files with `is_datastore_cache_file` true are exports of the matching datastore table.
- For subway, bus, and streetcar, the 2025-onward named resources are the intended current delay series, distinct from yearly 2014–2024 workbooks.
- LRT's single listed delay series is the candidate initial LRT input, subject to verifying its dates and relevance.
- CSV is the most practical first format to inspect.

### Unresolved

- Actual schemas, column meanings, and date coverage for every mode.
- Whether the four modes are comparable.
- Completeness of 2025 and 2026, including missing days or months.
- Publication behaviour: replace versus append versus revise.
- Whether Code Descriptions join cleanly to delay code fields.
- Whether the older subway `ttc-subway-delay-codes.xlsx` is still relevant.
- Licensing: subway, bus, and streetcar `license_title` is missing in the snapshot; LRT is `License not specified`. Attribution requirements are not established here.
- Routes and schedules remain a candidate source only, and are not part of this 2025-onward delay inventory.

## Task 1.2 audit and verification — 2026-10-21

Task 1.2 is complete against the local catalog snapshot. No actual dataset records have been inspected, and no final tracer has been selected.

- The working directory contains five project files and no Git repository. `git status --short` returned “not a git repository”; historical diffs and the previous agent's change counts cannot be verified. Pre-edit copies were retained outside the project for this session's comparison.
- `instructions.md` and `ROADMAP.md` already agree on the 2025-onward four-mode scope, optional historical expansion, periodic updates based on investigated publication behaviour, the central research question, analytical integrity, reproducibility, and the Power BI deliverable. Neither required changes.
- Python standard-library JSON and assertion checks validate all four expected package names, successful recorded request flags, no errors or failed package requests, declared/list resource counts of 19/20/21/8, required resource fields, parent package IDs, and 68 unique resource IDs. The 19 warnings concern missing optional metadata, not failed requests. `inventory_complete` describes this recorded package inventory; it does not prove complete incident coverage or current live availability.
- Resource-table fields, cited UUIDs, full URLs, package tables, and the recommended candidate names/IDs were checked against the local manifest. Historical URL suffixes and the Streetcar trailing tab were also checked. The assessment preserves missing values rather than treating them as zeros.
- A metadata-only live check using Python `urllib.request.urlopen` attempted all four recorded `package_show` URLs. Every request failed DNS resolution with `[Errno 8] nodename nor servname provided, or not known`. There was no successful live API verification; all source facts here remain local-snapshot claims.
- Only this assessment was edited. The governing documents, discovery script, and manifest were checked byte-for-byte against pre-edit copies. No data files were downloaded, dependencies added, or later tasks started.
