# Technical documentation and evidence index

Start with the root [technical README](../README.md). The directories and historical records below retain their established paths.

## Current reading path

1. [Storage contracts](storage_foundation.md) and [snapshot versioning](snapshot_versioning.md): lossless staging, immutable content identity and explicit selection. Read task-era status statements as historical.
2. [Cleaning/eligibility specification](cleaning_validation_rules.md) and [curated verification](../reports/curated_layer_verification.md). The specification is hash-recorded in curated metadata and was not edited for presentation.
3. [Core findings](../reports/core_analytical_findings.md), [viability review](../reports/analytical_viability_review.md) and [temporal evidence](../reports/temporal_persistence_evidence.md), in that order. Later temporal evidence supersedes pending proposals in the viability/strategy documents.
4. [Power BI contract](power_bi_data_contract.md), [Desktop build](power_bi_desktop_build.md) and [approved bundle](../results/power_bi/). The bundle manifest is the current export-integrity authority; older verification JSON files are checkpoint evidence.
5. Description history: [initial enrichment](../reports/code_description_enrichment.md) → [reviewed encoding recovery](../reports/code_description_encoding_recovery.md) → [display fallback](../reports/code_display_fallback.md). No inferred operational families are implemented.
6. [Website v2 instructions](../website/README.md), [v2 content coverage](../website/docs/v2-content-coverage.md) and [v2 validation](../website/docs/v2-validation.md). The [v0.1 content map](../website/docs/content-coverage.md) and [v0.1 validation](../website/docs/validation.md) remain preserved as baseline evidence.

## Evidence retained

- [Source assessment](../source_assessment.md), [catalog manifest](../source_manifest.json), [readiness assessment](../reports/data_model_readiness.md) and [cross-mode assessment](../reports/cross_mode_assessment.md).
- [Tracked provenance](../data/provenance/) and [immutable dictionaries](../references/ttc_delay_codes/2026-10-26/). One failed Subway acquisition is retained as failure evidence; it is not a successful snapshot.
- [Staging report](../reports/staging_ingestion.md), repeat-verification JSON and curated verification JSON document the progression. `curated_verification.json` and `curated_repeat_verification.json` are byte-identical by design of the observed repeat; both are retained.
- [SQL measure definitions](../sql/analysis/README.md) and [monthly-profile contracts](../sql/analysis/persistence/README.md).

## Historical references and status

Some task-era prose mentions pre-privacy-rewrite commit identifiers: `dc22280` in storage notes, `aa0f010` in cleaning notes and `c305b1e` in core findings. They are not part of the current branch's reachable history and should not be used as cloneable checkpoints. Consult `git log -- <path>` for retained file history; the current analytical/Power BI baseline is `c151470f5c76426062552f00cdcd7aa0924685a6`. No historical evidence was rewritten or deleted in the website task.

The roadmap retains historical task numbering and planned updates. Source-update scheduling, exposure normalization and GTFS integration are not implemented. Power BI Desktop validation was previously reported by the author; no PBIX/screenshots or verified public report are in this checkout. Do not equate an old “pending Desktop” note with proof that the author's current model is unbuilt, or with proof of publication.

## Privacy and reproducibility boundaries

Raw datasets, local SQLite files and intermediate analysis exports are ignored. A fresh clone can test the code and build the website, but exact frozen-source reproduction requires restoring the original raw bytes at the provenance-relative paths. Acquiring today's resource does not establish the same content checksum. The optional acquisition/profiling producer-side path cleanup remains a separate task; do not commit new provenance blindly.
