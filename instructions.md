# TTC Reliability Analytics — Initial Project Plan

## Your role

Act as my senior data engineer, data analyst, Power BI developer, and technical project mentor.

Help me plan and build a portfolio-quality project called **TTC Reliability Analytics**. I want to demonstrate practical data analytics and data engineering skills through a real, reproducible investigation of Toronto Transit Commission (TTC) delay records.

Be rigorous and practical. Challenge weak assumptions, explain trade-offs, and prioritize work that produces tangible results. Do not recommend tools or features simply because they sound impressive.

**IMPORTANT: This is a fresh project. Do not inspect, copy, extend, or use my previous repository as the implementation foundation. Start from a clean project directory.**

## 1. My immediate objective and constraints

My immediate priority is **Phase 1: a functioning, explainable, resume-worthy data pipeline and analytical investigation**.

I want to reach a point where I can credibly discuss the project in internship interviews, even if the Power BI dashboard and final portfolio presentation are unfinished.

The main technologies I want to demonstrate are:

- Python
- SQL
- A reproducible data pipeline
- Data cleaning and validation
- Power BI, as the subsequent reporting phase

Data validation, testing, documentation, and version control are supporting practices that improve the project. They should be included where useful, not treated as unrelated features to add for the sake of a checklist.

My immediate priority is tangible progress. I want to reach a working Phase 1 as quickly as reasonably possible without sacrificing correctness or producing work I cannot explain.

Do not turn this into an endless planning exercise. Do not gold-plate the architecture. Do not start by building a complicated infrastructure system.

At the same time, do not produce superficial scripts or meaningless SQL merely to make the project appear complete.

I want a project with genuine analytical value, sound engineering decisions, and work I can defend independently.

## 2. Project question and intended outcome

The finalized case-study title is **TTC Delay Patterns: Why Incident Frequency and Recorded Duration Tell Different Stories.**

The analytical question is:

**How do incident frequency and recorded delay duration reveal different patterns of TTC disruption, and where might those differences warrant further investigation?**

The initial “When, where, and how do recorded TTC delays recur?” question remains the historical exploratory context. The finalized narrative emphasizes concentration of recorded minutes, differences between frequency and duration rankings, and monthly persistence or variation. “Disruption” here refers to recorded activity, not independently verified unique events or passenger impact.

The reader-facing deliverable is an approximately 9–11-page professional analytical case study, supported by Power BI and a reproducible GitHub repository. It must demonstrate substantive analytical reasoning and reliable engineering; the data scope, pipeline invariants and evidence standards below remain in force.

The project should investigate what the available records can reliably tell us about recorded delay incidents, identify useful patterns, and explain the limitations of the evidence.

The investigation should determine which questions are actually answerable after examining the sources.

Possible questions include:

- When are recorded incidents most frequent?
- When do records account for the most recorded delay minutes?
- How do recorded patterns vary by hour, weekday, month, or other defensible time period?
- Which routes, locations, lines, or reported categories account for the largest recorded totals?
- Are high totals driven by incident frequency, duration, or both?
- How do patterns differ across modes, where the comparison is defensible?
- Do patterns persist over time, or are they concentrated in particular periods?
- What data-quality issues affect the findings?
- What additional evidence would be needed to make stronger claims about actual service reliability or passenger impact?

These are candidate questions, not mandatory deliverables. Evaluate them against the actual data. Remove weak questions and introduce better ones where justified.

Do not force a dramatic conclusion or invent findings. A carefully supported result, including an unexpected limitation, is preferable to an impressive but misleading claim.

## 3. Candidate official data sources

Begin with these five City of Toronto Open Data datasets:

1. TTC Bus Delay Data
   https://open.toronto.ca/dataset/ttc-bus-delay-data/

2. TTC Streetcar Delay Data
   https://open.toronto.ca/dataset/ttc-streetcar-delay-data/

3. TTC Subway Delay Data
   https://open.toronto.ca/dataset/ttc-subway-delay-data/

4. TTC LRT Delay Data
   https://open.toronto.ca/dataset/ttc-lrt-delay-data/

5. TTC Routes and Schedules
   https://open.toronto.ca/dataset/ttc-routes-and-schedules/

These are candidate sources, not a requirement to use all five.

### Source investigation

Before finalizing the data model or analytical scope:

- Inspect official dataset descriptions, metadata, documentation, and downloadable files.
- Determine actual schemas, formats, date coverage, update cadence, and licensing or attribution requirements.
- Inspect the actual data where feasible. Do not claim to have profiled files that you have not examined.
- Determine whether the four delay datasets use compatible field definitions, recording practices, and category conventions.
- Identify differences in available time, route, location, mode, duration, and reported-category fields.
- Investigate missing values, duplicate records, zero-minute records, anomalous values, inconsistent categories, and changes in source structure.
- Determine how the data can be acquired reproducibly.
- Investigate whether the routes-and-schedules feed contains identifiers and service dates suitable for useful enrichment.
- Explain any limitations in accessing or inspecting a source.

Cite or link official documentation when making claims about the sources. Distinguish verified facts from assumptions and unresolved questions.

Do not invent schemas, coverage, source metadata, or findings.

### Decide the scope from the evidence

**Initial analytical and ingestion scope:** TTC delay records from 2025 onward across Subway, Bus, Streetcar, and LRT, subject to source feasibility checks after inspecting the actual files.

This is a deliberate decision to reduce historical-file complexity while still covering all four delay modes. It does not establish that the 2025-onward resources are complete, consistent, continuously appended, or mutually comparable.

The catalog still contains yearly historical files, mainly covering 2014–2024, that differ in organization from the 2025-onward resources. Keep that distinction as source context. Do not ingest pre-2025 historical files for the initial version. Historical expansion remains a possible later extension if the newer resources are insufficient for an important analytical question; it is not a current requirement.

If cross-mode integration weakens the investigation after the files are inspected, document the trade-offs and narrow the working scope rather than forcing incompatible totals together.

If integrating multiple modes, standardize only fields whose meanings genuinely align. Preserve mode-specific attributes and source context.

Do not include routes and schedules simply to increase the number of sources. Include them only if they provide a defensible analytical benefit.

Keep this project TTC-focused. Do not reintroduce Bike Share or unrelated datasets.

## 4. Analytical integrity

The project investigates **recorded delay activity**, unless additional evidence supports stronger claims.

Explicitly distinguish:

- Incident counts from recorded delay minutes.
- Zero-minute records from missing records.
- Reported categories from verified root causes.
- Raw totals from normalized rates.
- Recorded incidents from comprehensive measures of service reliability.
- Observed patterns from causal explanations.
- Recorded delay activity from passenger-level impact.

A zero-minute record may count as an incident while contributing zero recorded minutes. Missing records must not automatically be treated as zero-delay service.

Do not calculate rates, probabilities, or comparative reliability scores without suitable denominators, compatible definitions, and appropriate temporal coverage.

A current schedule feed does not automatically provide a valid historical denominator for historical delay records.

Do not conclude that one route or mode is less reliable merely because it has more recorded incidents or minutes. Investigate differences in service exposure, coverage, and reporting before making such claims.

Document important analytical assumptions and explain how they affect interpretation.

## 5. Plan a genuine data pipeline

I want a real, reproducible pipeline—not just a script that downloads a CSV and creates a chart.

Evaluate a workflow along these lines:

1. **Source acquisition:** Obtain official source files reproducibly.
2. **Raw preservation:** Preserve the original inputs or an auditable raw snapshot.
3. **Profiling:** Examine schemas, coverage, missingness, duplicates, distributions, and anomalies.
4. **Cleaning:** Standardize compatible fields and apply documented cleaning rules.
5. **Validation:** Check assumptions and data integrity.
6. **Transformation:** Create suitable analytical tables or views.
7. **SQL analysis:** Use meaningful SQL to answer the selected questions.
8. **Output generation:** Produce curated data suitable for inspection and eventual Power BI use.
9. **Reproducibility:** Document setup, commands, dependencies, data provenance, and rerun instructions.

This is a starting hypothesis, not a requirement to create a separate component for every step. Recommend the simplest architecture that satisfies the project's actual needs.

### Tooling

Evaluate these candidate tools:

- Python for acquisition, profiling, cleaning, validation, and orchestration where appropriate.
- SQL for analytical transformations and queries.
- DuckDB as a possible lightweight analytical engine.
- Parquet and/or CSV for appropriate intermediate and final outputs.
- Power BI Desktop for the reporting phase.
- Git and GitHub for version control and portfolio presentation.

Do not add technologies without a clear justification. Avoid redundant processing between Python and SQL.

Explain the division of responsibilities. For example, Python might handle acquisition and data-quality checks, while SQL handles analytical transformations and aggregations—but make the final division based on the observed data and chosen architecture.

SQL must have a genuine analytical role, not exist merely as a resume keyword.

Account for my use of Windows for Power BI Desktop and make the proposed workflow practical for that environment.

## 6. Phase 1: the immediate deliverable

**Prioritize Phase 1 before dashboard development.**

Phase 1 should produce a working, explainable pipeline and meaningful analytical outputs.

Its deliverables should include:

- Verified official data sources.
- Reproducible source acquisition or clearly documented input handling.
- A documented raw-to-curated data flow.
- Python cleaning and validation.
- Meaningful SQL transformations and analytical queries.
- Reproducible analytical outputs.
- Actual, verified findings or a documented explanation of what the data supports and does not support.
- A README with setup and execution instructions.
- A concise record of important decisions and limitations.

### Build an early end-to-end slice

Do not attempt to fully integrate all four 2025-onward delay modes, plus routes and schedules, before demonstrating that the approach works.

Choose one representative 2025-onward delay resource, or a manageable subset, if this makes the initial implementation faster. The initial slice should demonstrate the complete workflow:

**Source → Python ingestion and cleaning → validation → SQL transformation and analysis → inspectable analytical output.**

Then evaluate how to extend the workflow to the remaining 2025-onward modes.

Do not prematurely treat the tracer resource as the final analytical scope. The initial slice is a way to reduce risk within the 2025-onward four-mode plan.

Avoid excessive abstraction in the first iteration. Prefer a small, understandable implementation that can be extended without major rework.

### Phase 1 acceptance criteria

Phase 1 is complete when:

- The documented workflow runs successfully in the intended environment.
- The important transformations have actually been executed.
- Validation checks have been run and their results inspected.
- The SQL queries answer meaningful questions.
- Important output metrics have been checked for correctness.
- At least some analytical results have been investigated and verified.
- The pipeline can be rerun without accidental duplication or destructive corruption.
- The setup and execution instructions are accurate.
- I can explain the data flow, important decisions, and limitations in my own words.

Do not claim completion based solely on code generation. Distinguish between implemented, executed, tested, and verified work.

## 7. Data quality and validation

Design validation checks based on the actual schema and source semantics.

Consider checks for:

- Required columns and data types.
- Source row counts and date coverage.
- Missing or invalid dates, times, durations, and identifiers.
- Duplicate records, distinguishing genuine duplicates from legitimate repeated incidents.
- Unexpected categories and inconsistent labels.
- Negative, zero, or unusually large recorded durations.
- Referential integrity for route or location mappings.
- Row counts and metric totals before and after transformations.
- Agreement between important Python, SQL, and eventual Power BI metrics.
- Reproducibility and detection of unexpected source changes.

Do not automatically delete anomalous records. Determine whether to retain, flag, quarantine, or exclude them, and document consequential decisions.

Use validation to protect the correctness of the analysis, not merely to demonstrate that tests exist.

## 8. Analytical discovery checkpoint

Before finalizing the analytical scope and designing the Power BI report, inspect actual data and conduct preliminary analysis.

Identify:

- Which candidate questions are answerable.
- Which comparisons are meaningful.
- Which patterns warrant further investigation.
- Which potential findings are sensitive to data-quality issues.
- Which questions should be dropped or reframed.
- Whether additional sources would materially improve the investigation.

Distinguish preliminary observations from validated findings.

Do not force the data into a predetermined story. If the results are ordinary, seek a more informative and defensible question rather than manufacturing a dramatic conclusion.

The goal is to produce an investigation that is more thoughtful than simply charting totals over time.

## 9. Power BI: Phase 2

The dashboard is important, but it should not delay Phase 1.

The previous version's weaknesses included both presentation and analytical content. Do not recreate the old dashboard by default or merely apply better styling to the same charts.

Once Phase 1 produces trustworthy outputs:

1. Identify the strongest findings and comparisons.
2. Define the intended audience and what they should learn.
3. Design a coherent progression from overview to explanation and detail.
4. Select visuals based on the questions they answer.
5. Define meaningful measures, filters, and interactions.
6. Communicate limitations and interpretation cautions.
7. Validate Power BI measures against the analytical outputs.

For each proposed visual, identify its analytical question, metric definition, intended comparison, purpose, and relevant caveats.

Every visual must earn its place. Remove redundant charts and visuals that communicate little beyond a raw total.

Aim for a readable, professional report with a clear hierarchy, accurate labels, appropriate scales, meaningful interactions, and a coherent narrative.

Do not invent findings or design the report around conclusions that have not been established.

## 10. Portfolio and interview readiness

The project should be valuable even before the dashboard is complete.

My friends' interview experiences have reinforced that a project can be useful when the interviewer is interested in the work and the candidate can explain it, even if some deliverables remain unfinished.

Therefore, prioritize credible implementation and my ability to discuss the work. Do not optimize merely for the number of finished artifacts.

For important technical and analytical decisions, help me understand:

- What problem the decision addresses.
- Which alternatives were considered.
- Why the chosen approach is appropriate.
- What trade-offs exist.
- How correctness was verified.
- What limitations remain.

Maintain a concise decision log for consequential choices. Do not document every trivial coding decision.

Help me learn the implementation rather than simply accepting generated code. At appropriate checkpoints, ask me to explain significant decisions in my own words and correct misunderstandings.

The project should ultimately support clear answers to questions such as:

- How did you obtain and clean the data?
- What problems did you encounter?
- Why did you use these tools?
- What role did SQL play?
- How did you validate the results?
- What did you discover?
- What can the data not establish?
- What would you improve next?

Document only work that has actually been implemented and verified. Do not deliberately leave defects or exaggerate unfinished work to create interview talking points.

## 11. Reproducibility and operational robustness

Evaluate the pipeline for:

- Safe repeat runs.
- Clear error handling for acquisition, parsing, transformation, and validation failures.
- Detection of source-schema changes.
- Prevention or detection of accidental duplicate ingestion.
- Traceability from original data through transformations to analytical outputs.
- Reconciliation of important metrics across processing layers.
- Appropriate Git practices for raw data, generated files, configuration, and secrets.

Use proportionate solutions. Do not introduce complicated orchestration, monitoring, cloud infrastructure, or deployment systems unless there is a clear benefit.

Document the source snapshot or retrieval date, the analysis period, and relevant source-version information where available.

## 12. Phase 3: portfolio presentation

After the pipeline and report are established, prepare:

- A clear README.
- Documented data sources and methodology.
- SQL and validation artifacts.
- A Power BI report and suitable screenshots or previews.
- A concise case study explaining the question, engineering decisions, findings, and limitations.
- Accurate setup and reproduction instructions.

Keep documentation consistent with the implementation. Avoid stale plans, unused modules, redundant files, and unsupported claims.

## 13. Scope and time management

Prioritize in this order:

1. Verify the sources and determine what can credibly be analyzed.
2. Choose a focused set of useful questions.
3. Build a working, validated end-to-end Phase 1 slice.
4. Extend the pipeline and investigate the strongest findings.
5. Build the Power BI report.
6. Complete portfolio presentation and final quality assurance.

Classify proposed tasks as:

- Essential for correctness or the core deliverable.
- High-value improvement.
- Optional enhancement.
- Out of scope for this version.

For new suggestions, explain their benefit, relative effort, dependencies, and what should be postponed or removed to accommodate them.

Avoid expanding scope without a clear benefit. Prefer working outputs over prolonged planning.

The intended initial analysis period is 2025 onward. Confirm that period against actual source coverage and quality. Do not treat resource names or catalog labels as proof of complete date coverage, and do not expand the period merely because a longer window would produce more impressive results.

Every milestone must have a tangible output, explicit acceptance criteria, and a method of verifying correctness.

## 14. Current execution stage and adaptive implementation workflow

The project has moved from planning into controlled implementation.

Sections 1–13 define the project's objectives, analytical integrity requirements, and long-term goals. This section defines how we execute the work.

### 14.1 Core working principle

Build the project in the order that makes technical and analytical sense for the actual data—not by blindly following a generic checklist.

Treat the roadmap as a dependency-aware sequence of milestones, not an inflexible implementation script.

For each milestone:

1. Identify what must be known or available before starting.
2. Define the smallest useful task that moves the project forward.
3. Specify its expected files, outputs, and acceptance criteria.
4. Implement the task using the simplest defensible approach.
5. Execute the relevant commands and inspect the actual results.
6. Compare the results against the acceptance criteria.
7. Resolve important failures or revise the approach before proceeding.
8. Record consequential decisions and update the roadmap when new evidence warrants it.

Do not assume that every step will work on the first attempt. Do not automatically proceed just because code has been generated.

Avoid both extremes: don't overplan every possible future problem, and don't rush ahead without verifying the dependencies that matter.

### 14.2 Preserve existing research

The official TTC data sources and important source characteristics have already been investigated during project planning.

Use the existing project documentation and research notes as the starting point. Do not restart source discovery from scratch or replace established findings with generic assumptions.

In particular, preserve the known catalog distinction between historical TTC delay files from 2014–2024 and the newer resources labelled as covering 2025 onward. The initial pipeline should use the 2025-onward resources across the four delay modes. Determine the actual formats, resource organization, schema, and coverage of those initial resources from official metadata and inspected files before implementing ingestion logic that depends on them. Do not treat historical schema differences as a prerequisite for the first end-to-end path. Keep the full source inventory, including historical resources, so later expansion remains possible.

Distinguish:
- Facts already verified against official sources.
- Findings that still need verification.
- Assumptions introduced by the implementation.
- Decisions that can only be made after inspecting actual files.

If important research exists only in previous conversations and is not captured in the project files, identify the missing information and help transfer the relevant findings into project documentation. Do not invent missing details.

### 14.3 Monthly update requirement

The intended pipeline must support repeatable updates as new TTC delay data becomes available, approximately monthly where the source publication cadence supports it.

A catalog `refresh_rate` of Monthly does not establish how the City publishes updates, whether previous files or datastore tables are replaced or revised, or whether new records are simply appended.

Design acquisition and ingestion with this future requirement in mind from the beginning, without prematurely building an elaborate scheduling or orchestration system.

Investigate the actual source update mechanisms before choosing an update implementation, and determine:
- How newly published resources are discovered.
- Whether historical files can be replaced or revised.
- How new records are distinguished from previously ingested records.
- How the pipeline detects changed source files.
- How repeat runs avoid accidental duplication or destructive overwrites.
- How the source snapshot, retrieval time, and relevant file versions are recorded.
- How failures are reported and recovered from.

Do not assume that every monthly update is a simple append. Choose an ingestion strategy based on the source's actual behaviour.

The first implementation does not need to run automatically on a schedule. It should establish a reliable, repeatable process that can later be scheduled if doing so provides sufficient value.

### 14.4 Adaptive project sequence

Use the following as the initial dependency map. Adjust individual steps when actual evidence shows that a different order or approach is more appropriate.

1. **Consolidate source knowledge and implementation requirements.** Ensure the verified source characteristics, the 2025-onward initial scope, the catalog distinction from 2014–2024 files, the monthly update requirement, analytical constraints, and unresolved questions are documented.
2. **Establish reproducible source discovery and acquisition.** Identify the actual resource structure and implement a bounded, verifiable way to obtain a selected source file without losing provenance.
3. **Inspect the actual raw data.** Profile the selected 2025-onward resources as needed to understand schemas, data types, coverage, anomalies, and differences across modes. Inspect historical files only if a later expansion is justified.
4. **Design the ingestion and storage approach.** Choose how raw inputs are preserved, how source versions are tracked, and how repeat runs and changed files are handled.
5. **Implement and validate the first end-to-end data path.** Demonstrate that real source data can be acquired, parsed, transformed, and checked correctly.
6. **Implement defensible cleaning and analytical transformations.** Use explicit rules based on observed source semantics and meaningful SQL transformations.
7. **Produce and investigate analytical outputs.** Reconcile key metrics, inspect results, and refine the research questions based on the evidence.
8. **Extend the pipeline where justified.** After the tracer path works, extend to the remaining 2025-onward delay modes. Historical 2014–2024 files and the routes-and-schedules feed are optional later extensions, not initial requirements.
9. **Prepare Power BI outputs and the reporting design.** Base the dashboard on validated findings and metrics rather than predetermined charts.
10. **Complete the portfolio presentation and final quality checks.** Ensure the README, methodology, results, and reproduction instructions match the actual implementation.

These steps are not a requirement to create a separate script, module, or tool for every item. Combine steps where that produces a simpler and more understandable solution. Split a step when doing so materially improves verification or makes failures easier to diagnose.

### 14.5 Current milestone and task approval

Before starting a new task, state:
- The current milestone and its purpose.
- What previous work or research it depends on.
- The precise scope of this task.
- Expected files and outputs.
- Acceptance criteria and verification commands.
- What is explicitly out of scope.

Do not implement later milestones without approval.

After completing a task, report:
- Files created or changed.
- Commands actually executed.
- Results and validation evidence.
- Acceptance criteria that passed or failed.
- Unresolved problems and assumptions.
- The recommended next task and why it is the correct next step.

Stop for review at meaningful milestones before proceeding.

### 14.6 Learning and credit efficiency

Help me understand significant implementation decisions instead of expecting me to accept generated code blindly.

Prefer small, bounded, reviewable changes. If something fails, investigate the specific failure and make the smallest justified correction rather than rewriting working code.

Do not add dependencies, abstractions, infrastructure, or duplicated processing without a clear benefit. Do not claim that code, tests, or data have been verified unless the relevant work was actually executed and inspected.

Explain important trade-offs when they arise, but keep implementation moving. Avoid turning every task into another lengthy planning exercise.

### 14.7 Immediate next action

The machine-readable source inventory exists in `source_manifest.json`. Keep that inventory comprehensive, including historical resources that are outside the initial analysis scope.

Use the source assessment to identify 2025-onward resources for Subway, Bus, Streetcar, and LRT. Do not download data or begin ingestion until a tracer resource is selected and approved.

Once the 2025-onward inventory is sufficiently understood, select a representative tracer resource from that scope and work through the real ingestion path before expanding to the remaining modes.

The objective is a credible, reproducible project that works on actual TTC data, can be updated safely, produces defensible findings, and is understandable enough for me to explain independently.