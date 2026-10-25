# TTC Transit Service Reliability Analytics — Execution Roadmap

## Project objective

Build a reproducible Python + SQL pipeline supporting **TTC Delay Patterns: Why Incident Frequency and Recorded Duration Tell Different Stories.**

**How do incident frequency and recorded delay duration reveal different patterns of TTC disruption, and where might those differences warrant further investigation?**

The initial “when, where, and how” question remains historical context. The professional case study (approximately 9–11 pages), Power BI report and reproducible repository will emphasize recorded-minute concentration, frequency-versus-duration rankings, and monthly persistence/variation. All existing engineering, eligibility and interpretive constraints remain unchanged.

The finished project should include a trustworthy data pipeline, defensible analytical findings, a Power BI report, and documentation suitable for internship applications and technical interviews.

This roadmap specifies the intended sequence of work. Each task must be completed and verified before dependent tasks begin. Implementation details may change when actual source evidence requires it, but changes must be justified and documented.

## Current state

- `instructions.md` contains the project objectives, constraints, and coding-agent rules.
- The official TTC Bus, Streetcar, Subway, LRT, and Routes and Schedules dataset pages have been identified.
- `discover_metadata.py` and `source_manifest.json` record the complete CKAN package and resource inventory for the four delay datasets, including historical files.
- Catalog research and the inventory show a resource-organization split: yearly historical delay files, mainly covering 2014–2024, exist alongside newer resources labelled as covering 2025 onward. That distinction remains useful context. Exact schemas, date coverage, and update behaviour are not established until the relevant files are inspected.
- **Initial scope:** ingest and analyze 2025-onward delay records across Subway, Bus, Streetcar, and LRT, subject to source feasibility checks. Pre-2025 historical ingestion is not a current requirement. Historical expansion is a possible later extension if the newer resources are insufficient for an important analytical question.
- Keep the source-discovery script and manifest comprehensive. Do not remove historical resources from the inventory because they are outside the initial analysis scope.
- Monthly or periodic update capability remains a requirement. Implementation depends on investigating actual source-publication behaviour. A catalog refresh rate of Monthly does not establish how updates are published or whether previously published data changes.
- No implementation should be assumed complete until files have been created, commands executed, and results inspected.

## Milestone 1 — Establish the source inventory

### Task 1.1: Discover dataset packages and resources

Query the official Toronto Open Data API for the four TTC delay datasets.

Record package identifiers, resource identifiers, resource names, formats, direct URLs, and available size and modification metadata. Distinguish missing metadata from failed requests.

**Deliverables:** `discover_metadata.py`, `source_manifest.json`.

**Verification:** Confirm successful API responses, validate the manifest structure, inspect the resource inventory, and compare representative metadata with the official portal.

**Do not:** Download data files, create a database, or begin transformations.

### Task 1.2: Reconcile the inventory with the 2025-onward scope

Use the inventory and existing research to identify the resources that appear relevant to the 2025-onward Subway, Bus, Streetcar, and LRT scope.

Record what catalog metadata actually establishes, what still requires file inspection, and which resources should be inspected next. Keep historical 2014–2024 resources in the inventory as context. Do not assume that one resource represents an entire dataset's history, that the four modes share a schema, or that a "since 2025" label proves complete coverage.

**Deliverable:** `source_assessment.md`, including confirmed facts, inferences, and unresolved questions.

**Verification:** Every proposed next input has an identifiable source and a defensible reason for inclusion. Resource identifiers in the assessment match the manifest.

### Gate 1

Do not select the final tracer resource until the inventory is sufficient to make that choice. Do not download all resources pre-emptively.

## Milestone 2 — Acquire and understand representative raw data

### Task 2.1: Select the tracer resource

Choose one 2025-onward resource using its actual format, coverage, relevance, and ability to demonstrate the pipeline. Prefer a representative, manageable resource rather than an arbitrary year.

If a second resource is necessary to understand cross-mode schema differences or the relationship between a datastore table and its downloadable cache file, justify that additional inspection explicitly. Do not require a historical 2014–2024 file for the initial tracer.

**Deliverable:** A documented tracer selection.

### Task 2.2: Download and preserve the selected resource

Download only the selected resource. Check the HTTP response, file existence, non-zero size, and ability to parse the file.

Preserve the source file unchanged. Record the source URL, retrieval timestamp, file size, checksum, resource identifier, and other useful provenance metadata. Never overwrite an existing raw file silently.

**Deliverables:** Raw source file and provenance record.

**Verification:** The file can be traced to its source and its format is confirmed by inspection.

### Task 2.3: Profile the raw data

Inspect actual columns, types, date coverage, missingness, parsing failures, duplicate candidates, category distributions, zero-minute records, negative values, and unusual durations.

Inspect additional 2025-onward resources as needed to verify schema and coverage differences across modes. Do not profile files that have not been acquired and inspected. Historical files are out of scope for this profiling step unless a later expansion is approved.

**Deliverables:** Profiling report and data dictionary.

**Verification:** Row counts, date ranges, and important quality findings are supported by actual output.

## Milestone 3 — Design and implement reliable ingestion

### Task 3.1: Choose the minimal storage architecture

Based on observed formats, data volume, analytical needs, and the Power BI workflow, choose one SQL engine, such as SQLite or DuckDB.

Define the roles of Python, SQL, raw files, staging data, curated outputs, and provenance records.

Do not add both database engines by default, introduce unnecessary frameworks, or build a star schema before the analytical grain and relationships are understood.

**Deliverable:** A short architecture and data-flow decision record.

### Task 3.2: Implement raw staging

Load the tracer resource into a staging table while preserving source values and traceability. Avoid premature type conversions or column removal.

Record or otherwise account for source rows that fail parsing or insertion.

**Deliverables:** Staging implementation and database.

**Verification:** Reconcile parser row counts, inserted rows, and any recorded failures.

### Task 3.3: Make ingestion repeatable

Define how the pipeline handles reruns, previously ingested resources, changed source files, and interrupted operations.

Use resource identifiers, file hashes, record keys, or other mechanisms only where appropriate to the actual source. A file hash detects file changes; it does not establish record-level uniqueness.

**Deliverable:** A safe, repeatable ingestion procedure.

**Verification:** Run it again and demonstrate that the second run does not silently duplicate data or corrupt existing outputs.

## Milestone 4 — Clean and validate the data

### Task 4.1: Define transformation rules

Use the profiling evidence to define explicit rules for dates, durations, missing values, categories, and other relevant fields.

Preserve source context. Flag, quarantine, retain, or exclude anomalies according to documented reasons. Do not silently discard unusual records.

Treat zero-minute incidents separately from missing or invalid durations. Do not interpret missing records as evidence of zero-delay service.

### Task 4.2: Implement SQL transformations

Create the smallest useful set of documented SQL views or tables that produces analytically usable fields.

Avoid duplicating the same transformation unnecessarily in Python and SQL.

**Deliverables:** Transformation SQL and curated dataset or views.

**Verification:** Check required fields, types, date coverage, row counts, exclusion counts, and important metric totals before and after transformations.

## Milestone 5 — Build and investigate the analytical SQL

### Task 5.1: Establish metric definitions

Specify the grain, filters, time basis, and definitions for incident counts and recorded delay minutes.

Keep the count of incidents distinct from recorded duration. Do not claim passenger impact, causal explanations, or normalized reliability without suitable evidence and denominators.

### Task 5.2: Implement analytical queries

Start with meaningful questions supported by the available fields, such as:
- When are recorded incidents most frequent?
- When do records account for the most recorded delay minutes?
- How do patterns vary by hour, weekday, month, or other defensible period?
- Which recorded locations, routes, or categories contribute the largest totals?
- Are high totals driven by incident frequency, duration, or both?

These are candidates, not mandatory charts or conclusions. Refine the questions after inspecting results.

**Deliverables:** Readable SQL queries, result tables, and metric definitions.

**Verification:** Execute the queries, inspect the outputs, validate important totals independently, and document actual findings and limitations.

### Analytical handoff status (Milestone 5)

The original task descriptions above are retained as planning history. Executed task briefs expanded 5.1 to core analytical SQL, 5.2 to analytical viability/strategy, and 5.3 to temporal persistence. Verified evidence is in `reports/core_analytical_findings.md` and `reports/temporal_persistence_evidence.md`. The final Power BI export/model contract is `docs/power_bi_data_contract.md`. This handoff prepares validated data only; Power BI visuals and source-update automation remain unimplemented and require their own task approval.

## Milestone 6 — Extend to the monthly update workflow

### Task 6.1: Confirm actual publication behaviour

Determine how the source publishes new resources and whether previous files are replaced or revised. Do not assume that every update is append-only.

### Task 6.2: Implement safe updates

Extend the proven ingestion process to discover new or changed resources, record provenance, avoid accidental duplication, and rebuild or update curated outputs safely.

Keep the update process runnable manually first. Automatic scheduling is optional and comes only after the process is reliable.

**Deliverables:** An update command or workflow, change detection, and documented recovery behaviour.

**Verification:** Test a normal rerun and, where practical, a changed or newly published resource. Confirm that the outputs remain correct.

## Milestone 7 — Optional later extensions

This milestone is not required for the initial 2025-onward four-mode version. Use it only if verified evidence shows that historical files or another official TTC source would materially improve the investigation.

### Task 7.1: Consider historical files or additional official sources

Evaluate 2014–2024 delay files, or the routes-and-schedules feed, only after the 2025-onward pipeline is working and a specific analytical gap has been identified.

Preserve mode-specific fields and standardize only genuinely comparable concepts. Do not ingest historical files by default.

### Task 7.2: Reassess the research questions

Investigate whether a broader period or an additional source adds value. Document incompatible definitions, missing coverage, and the limitations of comparisons.

**Deliverables:** If pursued, an expanded pipeline, validation results, and a revised analytical specification.

**Verification:** Existing 2025-onward results remain reproducible and new sources do not silently alter metric meanings.

## Milestone 8 — Prepare the Power BI reporting layer

### Task 8.1: Define the report before building visuals

Choose the audience, key findings, report structure, metrics, filters, and comparisons using the validated analysis.

For each proposed visual, document the question it answers and why it deserves space in the report.

### Task 8.2: Export validated reporting tables

Create a repeatable export to CSV unless another integration offers a clear practical advantage.

**Deliverables:** Reporting tables, export script, and report blueprint.

**Verification:** Reconcile exported metrics against SQL results.

### Task 8.3: Build Power BI manually

Create the report in Power BI Desktop. Use DAX where needed, and validate measures against SQL outputs.

Communicate the findings and the limitations of the recorded data. Remove redundant or misleading visuals.

**Deliverable:** A coherent Power BI report.

## Milestone 9 — Finish the portfolio project

### Task 9.1: Complete the repository documentation

Document setup, dependencies, source URLs, acquisition, data flow, transformations, validation, metric definitions, analytical findings, limitations, and update instructions.

Ensure the README reflects what actually exists and runs.

### Task 9.2: Complete the presentation and quality review

Capture appropriate report screenshots, remove stale plans and unused code, review Git history, and ensure no secrets or inappropriate raw data are committed.

Prepare an accurate project explanation covering technical decisions, validation, findings, limitations, and possible improvements.

**Deliverables:** Portfolio-ready repository, report preview, and case-study narrative.

**Verification:** Follow the documented reproduction steps and confirm that the instructions match the implementation.

## Coding-agent execution protocol

For each implementation task:

1. Inspect relevant files and source evidence.
2. State the task objective, permitted changes, dependencies, expected outputs, acceptance criteria, and verification commands.
3. Implement only that task.
4. Execute appropriate checks and report actual results.
5. Diagnose failures narrowly; do not rewrite unrelated code.
6. Report files changed, commands run, acceptance-criteria status, and unresolved issues.
7. Stop for review before starting the next task.

Do not ask the coding agent to implement multiple future milestones in one prompt.

## Definition of project completion

The project is complete when the ingestion and update workflow is reproducible, the transformations and SQL have been executed and validated, the analytical findings are defensible, the Power BI report agrees with the validated outputs, and the repository documents how to reproduce and interpret the work.

Each milestone may be revised in response to verified evidence, but consequential changes must be explained and recorded. Code generation alone is not proof of completion.