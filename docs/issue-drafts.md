> Historical approved planning snapshot, published on 2026-10-20. GitHub issues are the implementation backlog; see [delivery.md](delivery.md). Current approved decisions below supersede earlier proposals. This file is not a second task tracker.

# Notey implementation issue drafts

**Approved for publication on 2026-10-20.** The user authorized publishing these issues and beginning N01 after recording the decisions below. Publication status and live issue links are recorded in docs/delivery.md. `N01`–`N25` are planning identifiers, not GitHub issue numbers. The existing [foundation issue #1](https://github.com/JuliaMathias/notey/issues/1) would be narrowed to N01 after review; it should not become an umbrella PR implementing this entire plan.

[Product direction](product.md) defines requirements. [Wireframe review](design-review.md) records design feedback and evidence. This document defines proposed delivery boundaries, not a second product specification. Once approved and published, GitHub issues become the implementation backlog and this document becomes a linked historical planning snapshot.

## How the work is divided

Each implementation issue should normally produce **one independently reviewable PR** containing its migration/context, UI or CLI, tests and documentation. Do not create separate PRs merely for a table, context, controller and screen belonging to one behavior. Conversely, do not combine importing originals, model processing, generation and export into one PR.

A dependency means the prerequisite behavior must exist, not that all earlier numbers must be complete. Discovery issues deliver a decision and reproducible evidence, not a promised production feature. Split further only when investigation reveals a distinct deployable behavior or a material unresolved decision; update the issue before expanding scope.

Existing state: generated, unvalidated Phoenix files; UUID generator configuration; draft product/design documentation. No domain features, CI, deployable release or production AI integration have been established by this scaffold. Shared AI planning docs describe a transcription baseline and generation trials; they are not proof of current live contracts or production extraction/generation readiness.

## Delivery map

| Milestone | Drafts | Usable result |
| --- | --- | --- |
| Foundation and library | N01–N04 | Run the initial app on Lara through Tailscale, then create sessions/events and retain originals |
| Recording and document review | N05–N09 | Transcribe, extract and review sources with timestamps/pages |
| Verified reference material | N10–N13 | Import an edition, retrieve exact passages and resolve citations |
| Integrated notes | N14–N17 | Generate, edit, inspect evidence, finalize and read session notes |
| Documents to take away | N18–N19 | Linked session PDF and ordered event PDF |
| Hosted application hardening | N20–N22 | Tailscale-only access protection, persistent-feature deployment and tested update/recovery |
| Optional enrichment | N23 | Explicit, externally cited additions distinct from session content |
| Final additions and visual review | N24–N25 | NLT import profile, then a cohesive visual polish pass across the completed app |

This table groups outcomes, not a mandatory serial schedule. Access protection and release preparation can happen early after their prerequisites. N01 includes the first real deployment of the empty foundation on Lara and verified Tailscale access. N20–N22 extend that baseline for private user data, feature integration and automatic updates; they are not prerequisites for showing the initial app on Lara. Enrichment is agreed product scope but need not block the first usable notes workflow.

## Foundation and library

### N01 — Build, test and deploy the Phoenix foundation to Lara through Tailscale

**Outcome:** a fresh checkout runs locally with LiveView, PostgreSQL and UUID conventions, independently of Lara; the initial app is also deployed on Lara and reachable from the user's laptop and phone through Tailscale.

**Include:** finish the existing scaffold; pin compatible tools/dependencies; development PostgreSQL setup; configurable runtime settings; meaningful database and LiveView smoke tests; CI for formatting, warnings, tests and assets; AGENTS.md and accurate setup/testing guidance. Add the minimal reproducible release/image and application deployment recipe, persistent PostgreSQL configuration, migration/start/restart commands and a health check. Transfer the reviewed application code or built release to Lara, deploy it as a managed service, and connect it to the existing private HTTPS/Tailscale ingress. Record the product direction and design links without building feature screens. Development remains in this Mac repository; Lara runs the deployed release, not a development server.

**Acceptance:** setup works from documented prerequisites; UUID persistence is exercised against PostgreSQL; a real LiveView mount/update test runs; CI passes on the PR head; private materials and secrets are excluded from Git. Document the distinction between application migrations and external database provisioning. Deploy the exact tested revision to Lara and record its commit/image identity and actual HTTPS URL. Verify page loading and a LiveView WebSocket interaction through Tailscale from both laptop and phone, including access outside home Wi-Fi; confirm the deployed service and database remain available after a controlled restart. The database and AI endpoints must not become publicly accessible as a side effect. Keep the first deployment limited to the empty foundation/synthetic data until the Tailscale-only access boundary is verified for those routes in N20.

**Deployment evidence:** inspect current infrastructure docs/configuration before choosing service paths, resource limits, database provisioning or URL. Put Notey release/runtime recipes in this repository. Identify any necessary Caddy route, private-network or database provisioning change and its owning `JuliaMathias/home-server-infra` repository before changing it; keep any companion infrastructure PR separate and limited to the requested Notey access. Do not change unrelated services or bypass the user's PR merge policy. A prepared recipe without an actual successful deployment does not meet N01 acceptance. When deployment depends on the user merging a PR, retain the live verification gate as pending until that merge and deployment are verified.

**Manual verification:** prerequisites are a running deployed revision, recorded URL, valid private HTTPS configuration and laptop/phone connected to Tailscale. Open that URL on the laptop, exercise the scaffold's LiveView update and reload; repeat on the phone over cellular with home Wi-Fi disabled. Restart only Notey and its dedicated database using the documented procedure and repeat the checks, preserving the synthetic UUID test record. Record revision, URL, device/browser, connectivity, interaction and persistence results. Pass requires all checks; failure/pending connectivity is reported explicitly. Remove only the synthetic verification record afterward; leave the requested app available.

**Depends on:** none; inspect existing Lara deployment prerequisites during implementation. **PR boundary:** scaffold plus the first manual deployment of that scaffold, not sessions, application login, inference adapters, automated rollout, backup platform or recovery drills. A minimal infrastructure companion PR is separate if needed. Automatic updates and full recovery remain N21–N22. Resolve signing without disabling it. Reuse existing GitHub issue #1 rather than creating a duplicate.

### N02 — Create, edit and browse sessions with reusable metadata

**Outcome:** save a session and find it again with its category, multiple speakers, date/time and optional place intact.

**Include:** UUID-backed session/category/speaker/place records and speaker associations; create/edit/detail/library views; create or select reusable metadata; useful metadata filters; date-only sessions and explicit timezone handling. Implement phone and laptop layouts together.

**Acceptance:** create, reload and edit a session with two speakers; reuse those speakers/place on another session; validation preserves entered values; metadata filters return expected sessions; date-only information is not silently converted into an invented time. Referenced metadata cannot be deleted in a way that silently destroys session history.

**Depends on:** N01. **PR boundary:** no recordings, AI, complex metadata merge tools, nested categories or standalone notebooks. Event selection arrives in N03.

### N03 — Group and order sessions in events

**Outcome:** organize a conference or retreat into a reusable event with an explicit session order.

**Include:** event create/edit/detail views, optional session membership, assign/reassign/remove membership, ordering controls usable by touch and keyboard, and event selection on the session form.

**Acceptance:** add several sessions, reorder them, reload and retain that order; removing a session from an event preserves the session and sources; a session without an event remains usable.

**Depends on:** N02. **PR boundary:** organization only; combined PDF arrives in N19. Initial default is one optional event per session, without nested events.

### N04 — Attach and retrieve private original source files

**Outcome:** upload recordings, personal notes, slide PDFs and slide photos, then reopen the preserved originals from their session.

**Include:** explicit attachment roles; a configurable private storage adapter/root; streaming uploads and validation; asset UUIDs, checksums and immutable original identity; upload/retrieval UI; safely handled interrupted uploads and duplicate submissions; recoverable Trash with restore and automatic permanent expiry 30 days after deliberate deletion. Notey deletion never removes the original Drive/Supernote file. Multiple recordings are allowed; identify which one to process without pretending their timestamps align.

**Acceptance:** round-trip synthetic audio/PDF/image bytes; reject oversized or unsupported files safely; original filenames cannot escape storage paths; originals are never served from public static assets; failed uploads do not appear ready; retrieval respects session access boundaries. Document proposed upload limits before implementing them; test Trash restoration, 30-day expiry with a controllable clock, affected citations and safe retry without deleting unrelated/shared source records.

**Depends on:** N02. **PR boundary:** no extraction, Drive connection or automatic destructive cleanup. Before hosted personal-data use, verify N20's private-network boundary for attachments. No extra application login is required now.

## Recording and document review

### N05 — Submit recordings for asynchronous transcription

**Outcome:** a user starts transcription, leaves the page, and later sees a durable completed transcript or an actionable failure.

**Include:** Notey-owned processing records and bounded lifecycle handling; fake transcription adapter for local development/tests; configurable remote adapter matching the verified Lara contract; submission/status/result handling; durable recording-specific segments and technical provenance; progress/error UI and safe retry behavior. Use the smallest suitable job mechanism rather than building a general workflow engine.

**Acceptance:** fake-service tests cover success, rejected uploads, unavailability, timeout, application restart and repeated completion responses. Preserve timestamps and raw result revisions. An ambiguous submission timeout must not trigger a blind duplicate model job. Separately verify a real synthetic recording against the actual service, recording that result separately from unit tests.

**Depends on:** N01, N04; current transcription contract inspection. **PR boundary:** no model changes, shared scheduler or transcript editor. If the service lacks a required recovery/idempotency capability, record that gap in its owning repository and keep the limitation visible.

### N06 — Review transcripts with an inline interval audio player

**Outcome:** inspect uncertain words, hear the relevant recording passage and save corrections without losing the raw transcript.

**Include:** timestamped transcript review; play/pause, seek position, replay, small seek jumps and speed; proposed bounded interval playback with adjustable context; opening the full recording at the same timestamp; correction revisions and explicit uncertainty. The player is reusable in the later note-source panel.

**Acceptance:** synthetic media tests cover interval boundaries at recording start/end, pause at the chosen end, user seeking, unavailable media and no autoplay. Corrections preserve original source identity and raw transcript history. Phone/laptop browser testing covers keyboard/touch use and the actual media format; timestamps belong to the selected recording.

**Depends on:** N05. **PR boundary:** no multi-recording alignment, waveform editor, automatic recognition tuning or claim that every low-confidence word is an error. The roughly three-second context margin is a proposed default to review here.

### N07 — Establish document extraction and generation integration contracts

**Type:** bounded discovery/integration design, normally a documentation-and-contract-test PR.

**Outcome:** know what Notey can call remotely for typed PDFs, slide photos, handwriting and language-model generation before implementing adapters against imaginary services.

**Include:** read current owning-repository contracts and service availability; agree request/result schemas, supported inputs, locator/revision conventions, job/resource limits and error behavior; define synthetic adapter fixtures; identify gaps with their owning repository and a runnable integration-check procedure. Use existing private evaluation evidence where available; do not launch expensive model experiments by default.

**Acceptance:** each capability is marked available, trial-only or missing with evidence; Notey/shared-service ownership is explicit; model/provider selection and any significant resource/cost/privacy decision remain visible. Record decisions about source/output languages, uncertain diagrams and source fidelity.

**Depends on:** N01, N04. **PR boundary:** no shared-service deployment or infrastructure changes. Extraction and generation implementation is gated by the corresponding contract being ready; fakes alone do not satisfy real integration acceptance. If unresolved, convert concrete shared-service gaps into separately approved work in the owning repository.

### N08 — Extract typed notes and slide PDFs with page provenance

**Outcome:** add a text-based PDF and review its extracted material page by page before using it in generated notes.

**Include:** document adapter integration, extraction jobs using N05's lifecycle where suitable, immutable source units with page locators, personal-note versus slide roles, and an extraction preview. Keep useful headings/order and label unsupported diagrams or unreadable pages.

**Acceptance:** deterministic fixtures cover multi-page text, blank pages, damaged PDFs and ordering; every extracted unit opens the correct original page. Scanned pages are explicitly routed to N09 or marked unsupported, never silently treated as empty. Record a separate real integration result when the capability is available.

**Depends on:** N04, N05's job lifecycle, typed-PDF part of N07. **PR boundary:** no handwriting OCR, universal slide-diagram interpretation or Bible-specific parsing.

### N09 — Extract and correct handwritten notes and slide photos

**Outcome:** review text recovered from images/scanned pages and correct uncertain extraction before note generation.

**Include:** OCR/extraction adapter for the supported inputs; page/image and optional region locators; uncertainty handling and original-image access on demand; correction revisions; explicit handling of writing grids and non-text visual material.

**Acceptance:** synthetic fixtures verify corrections, source links, failures and preserved originals. A separate authorized private sample review establishes which handwriting/photo inputs are usable; do not claim OCR quality from adapter tests. Finished reading notes receive corrected text rather than handwriting or grid imagery.

**Depends on:** N08, image/handwriting part of N07. **PR boundary:** no native .note parsing or guaranteed diagram understanding. If handwriting needs a different unavailable shared capability, keep that acceptance gate blocked rather than hiding it behind a generic OCR success status.

## Verified reference material

### N10 — Import structured Bible editions and retrieve exact passages

**Outcome:** repeatably import a structured edition into Notey PostgreSQL and retrieve validated passage ranges.

**Include:** edition/import/verse identity and source provenance; staging versus available status; a repeatable CLI command accepting a documented normalized format; validation and transactional promotion; exact range retrieval and focused edition/import status UI. Use synthetic verse content in Git and tests.

**Acceptance:** cover missing/duplicate records, invalid ranges, repeat imports, source hashes and edition separation; failed import cannot replace an available edition; unavailable verses return an explicit error rather than model-filled text. Support translation-specific canon/numbering without a guessed global verse count.

**Depends on:** N01. **PR boundary:** normalized import and lookup only; PDF parsing belongs in N11. This is a complete operator workflow, not an isolated schema PR. Bible text lives in private PostgreSQL/storage, not Git or shared inference state.

### N11 — Add a repeatable NAA PDF import profile and validation review

**Outcome:** the user's supplied NAA PDF can feed N10 through a documented, repeatable extraction and review process.

**Include:** a PDF layout profile, extraction report and source-page mapping; validation/approval UI; explicit handling of headings, footnotes, small caps and layout boundaries. Inspect the experimental SQLite contents and offer a non-destructive staging import path if useful, preserving its source provenance. NIV receives its own profile next in N12; NLT follows at the end in N24. Additional editions receive their own profiles when requested.

**Acceptance:** synthetic layout tests plus a private manual comparison of actual source passages across book/chapter/page boundaries; repeated runs have explainable results; gaps and partial coverage are visible. Do not mark an entire Bible available on the strength of a few sampled verses. Define coverage checks and the human acceptance procedure before full promotion.

**Depends on:** N10 and PDF extraction availability. **PR boundary:** NAA profile and its validation workflow, not a universal Bible PDF parser. Original PDFs, extracted verses and the experimental SQLite file remain outside Git. NIV and NLT reuse the importer, not the NAA layout assumptions. Their identities and languages must be confirmed from their actual source editions.

### N12 — Add and validate the supplied NIV Bible PDF import profile

**Outcome:** repeatably import the user's NIV Bible PDF into the same reference library, keeping it distinct from NAA and other imported editions.

**Include:** inspect the actual PDF from the user's private bibles folder once it is available; confirm its title, language, publisher/edition and source hash; implement a layout-specific extraction profile using N10's normalized format and N11's validation workflow. Preserve page locators and provide an extraction/coverage report and edition-selection entry. The user clarified that the intended translation is the English NIV; the earlier use of NVI referred to the Portuguese name, not a separate requested edition.

**Acceptance:** synthetic layout regression tests plus private source comparisons across book/chapter/page boundaries, headings, footnotes and edition-specific typography; exact passage lookup returns the selected edition's text without mixing editions; repeated import behavior and incomplete coverage are explicit. Follow the same whole-edition promotion criteria as N11, not sampled success alone. Missing source PDF remains a visible input dependency.

**Depends on:** N10, N11 and availability of the supplied NIV PDF. **PR boundary:** one NIV extraction profile, validation evidence and its use in the existing library; no importer rewrite, NLT profile or new translation default. Schedule immediately after N11. If the file is still downloading, continue independent work and leave real-source validation pending.

### N13 — Resolve and review Bible references in session material

**Outcome:** confirm explicit or suggested indirect references and attach complete exact passages from the chosen edition.

**Include:** reference candidates tied to recording/note/slide source locations, edition selection, confirmation/correction UI, exact retrieval and unresolved-reference states. Candidate identification may use an adapter, but final wording always comes from ReferenceLibrary.

**Acceptance:** cover ambiguous names, book aliases, cross-chapter ranges, missing editions/verses and rejected guesses; confirmed passages preserve edition/range/source identity; unresolved references cannot masquerade as verified quotations.

**Depends on:** N08 or N05 for source material; N10; N11 before real NAA use; N12 before real NIV use; generation part of N07 if model-assisted detection is used. **PR boundary:** reference resolution only; do not silently paraphrase scripture or define an unapproved language-translation policy.

## Integrated notes

### N14 — Review session boundaries, included material and speakers

**Outcome:** decide which recording material belongs in the notes, including useful material after the main talk, and confirm speaker attribution.

**Include:** proposed semantic sections/classifications and speaker suggestions using approved inference; manual overrides; include/exclude controls; evidence for suggestions and explicit unknown speakers. Keep worthwhile prayers/discussion selectable without deleting media.

**Acceptance:** deterministic adapter fixtures cover introductions, announcements, talk, closing prayer, relevant discussion and incidental recording; overrides survive reprocessing; speaker suggestions cannot silently overwrite reusable person records. Real quality review is separate from request-success tests.

**Depends on:** N06 and the generation contract in N07. **PR boundary:** application interpretation/review only, not training voice identification or implementing diarization inside Notey. This can proceed alongside the reference work once prerequisites exist.

### N15 — Generate a source-linked integrated draft

**Outcome:** generate one organized document from the included transcript, optional corrected personal notes, slide material and confirmed passages.

**Include:** durable generation jobs and configurable adapter; bounded/staged processing for long sources; explicit input revision snapshots; stable note-block UUIDs; many-to-many evidence links to source-unit IDs; draft persistence and visible generation failures. Handle the no-personal-notes path too. New drafts must not overwrite edited notes silently.

**Acceptance:** synthetic fixtures verify multiple sources per block, valid session/reference scope, locator bounds, missing/foreign IDs, invalid model output, job retries and long-input coverage. Include a separately recorded real session evaluation for fidelity/completeness, with manual acceptance; valid IDs alone do not prove supported claims.

**Depends on:** N08/N09 for supplied documents, N13 for sermons, N14, and a ready generation contract from N07. **PR boundary:** draft generation and traceability, not a rich-text editor, outside enrichment, model training or automatic quality acceptance.

### N16 — Edit notes with sources visible beside the active block

**Outcome:** edit a draft while its relevant source excerpts remain visible on the right on laptop and below the active editing area on phone.

**Include:** a simple block editor; stable IDs across ordinary edits; visible recording/text/page/verse evidence; reusable inline audio player; full-source opening; add/remove source links and personal additions; safe save/conflict behavior. Preserve edit/scroll position and distinguish historical provenance from currently reviewed support.

**Acceptance:** cover selecting a block, multi-source links, personal text without recording evidence, nonblocking stale-support warnings after material edits, split/merge/reorder behavior, and avoiding silent loss when another revision is saved. Phone/keyboard checks verify evidence remains reachable without scrolling past the whole document. Changing selection does not auto-play audio.

**Depends on:** N15, N06. **PR boundary:** editing/evidence as one coherent workflow; no full collaborative editor or generic notebook product. Decide the simplest adequate editor representation here rather than committing to a large editor framework in N01.

### N17 — Check, finalize and read a revision of the notes

**Outcome:** review meaningful quality concerns, finalize a specific revision and open a clean reading view or Markdown export.

**Include:** checks for unresolved source decisions/references, missing passages, nonblocking changed-support warnings and possible omissions; a finalization policy; saved finalized revisions; responsive reader and Markdown serialization. Clearly distinguish deterministic checks, model-assisted warnings and human decisions.

**Acceptance:** failures/warnings are actionable; apply the approved hard-error versus overridable-warning policy below; paragraph source warnings never require per-paragraph acknowledgment; edits do not silently mutate an already exported finalized revision. Reading mode has no handwriting/grid imagery or editing panels. Markdown retains headings, complete confirmed passages and clearly labeled additions.

**Depends on:** N16. **PR boundary:** finalization and canonical reading output, not PDF layout. Do not equate a green checklist with proven recognition accuracy or faithful synthesis.

## Documents to take away

### N18 — Export a linked, Supernote-friendly session PDF

**Outcome:** export a finalized session as a readable PDF with useful document navigation.

**Include:** PDF renderer from the same finalized document model as N17; headings, full passages, edition labels, page breaks and supported internal links/bookmarks; private download handling. Keep the export reproducible for a fixed revision.

**Acceptance:** fixture exports are rendered and visually inspected for clipping, Unicode/Portuguese accents, long passages and links; failures do not produce an apparently successful download. Run and record a manual Manta test for readability and navigation. No claim of tested Supernote compatibility until that device check passes.

**Depends on:** N17. **PR boundary:** single-session PDF only; no editable native .note or event synthesis.

### N19 — Export selected event sessions as ordered PDF chapters

**Outcome:** produce one event PDF with selected finalized sessions, preserving chapter order and session identity.

**Include:** explicit include/exclude controls, keyboard/touch ordering, chapter readiness, cover/table of contents and combined export using N18's renderer. Preserve speakers, dates, citations and enrichment labels per chapter.

**Acceptance:** ordering and selection survive reload; unfinished sessions require finalization or explicit exclusion; export links point to correct chapters; cover/contents/page numbering are visually checked across mixed session lengths and on Manta where relevant.

**Depends on:** N03, N18. **PR boundary:** document compilation, not cross-session AI synthesis or deduplication that rewrites source notes.

## Private hosted application

### N20 — Verify Tailscale-only access to the private workspace and its assets

**Outcome:** the hosted application, files, processing results and exports are reachable only through the intended private Tailscale route. The user chose no extra application login for now.

**Include:** verify the deployed private-network/ingress boundary, direct asset/result/download routes, HTTP and LiveView behavior, origin/session controls and redacted errors/logs. Document that an allowed Tailscale client with network access can use Notey; do not imply per-person application authorization or add signup/login screens.

**Acceptance:** verify access from approved tailnet devices, no unintended LAN/public listener or direct published database/AI endpoint, and private delivery of asset/result/export URLs. Verify HTTP and WebSocket behavior in a browser. Read current tailnet/ingress configuration without broadening it silently; record any needed change in the infrastructure repository. Recheck the same boundary as new resources are implemented.

**Depends on:** N01, N02, N04; extend checks to later resources as they arrive. **PR boundary:** verify and enforce the existing private access choice, not a multi-tenant permission system or a new login mechanism. Separate private-account authentication is recorded as future work rather than a blocker for this initial choice.

### N21 — Extend the initial Lara release for private assets and remote processing

**Outcome:** the N01 deployment can run the growing Notey application with protected original files, durable processing state and configurable remote AI connections.

**Include:** extend N01's existing release/deployment recipe rather than creating another one; configure private asset volumes and job state; service connection configuration and feature-aware health/readiness; operational checks for release replacement and temporary AI unavailability. Identify any newly required resource/ingress changes in the owning infrastructure repository.

**Acceptance:** verify original-file/database/job persistence across release replacement with synthetic data; clear application behavior when remote AI is unavailable; secrets stay outside Git/images/logs; previously verified Tailscale access continues working. Local development remains independent of Lara. Document update transport prerequisites and rollback limitations for N22.

**Depends on:** N01, N04, N05; N20 before hosted personal-data use. **PR boundary:** application deployment integration and persistence for the new features, not the initial deployment already delivered in N01 and not automated rollout. Shared infrastructure changes remain separately scoped in their owning repository; recheck current docs before changing anything.

### N22 — Prepare and validate updates, backups and recovery for Lara

**Outcome:** automatically deploy passing merged revisions to Lara and retain a recoverable private database/file set in Google Drive. A PR requiring a different rollout must explicitly explain the exception and provide a runnable manual update plan before merge.

**Include:** the approved update transport; CI artifact publication and revision selection; a gated rollout/health-check procedure; migration strategy; encrypted Google Drive backup/restore pairing of PostgreSQL with original assets, with credentials/recovery keys outside Git; failure/recovery reporting. Keep implementation small; no Kubernetes or general deployment platform.

**Acceptance:** exercise an isolated successful update, failed-health update, database/file restore and a migration that cannot be undone by reverting only the image. Preserve user data and pin deployed revisions. Automated rollout never merges PRs and must not deploy a failed/unverified revision.

**Depends on:** N20, N21 and an approved infrastructure companion change if needed. **PR boundary:** Notey configuration/workflow plus separate changes in the owning infrastructure repository; neither is hidden inside the other PR. The first manual foundation deployment is already required by N01. The user authorized automatic updates after merges, subject to the reviewed implementation. PR-specific exceptions must carry a manual rollout plan; never assume a database migration can be undone by reverting only the image. The application is not complete for hosted use until that integration evidence exists.

## Optional enrichment

### N23 — Add explicitly requested and externally cited enrichment

**Outcome:** request outside context without confusing it with the recording, slides or personal reflections.

**Include:** an explicit request/review flow; approved retrieval sources and configurable provider; source snapshots/citations; labeled enrichment blocks that remain distinct in reading, Markdown and PDF exports. Record provider/network/cost/privacy decisions before connecting external retrieval.

**Acceptance:** ordinary generation makes no enrichment request; unsupported external claims and missing citations are flagged; accepting or rejecting enrichment preserves session content; labels/citations survive session and event export. Tests use fake retrieval/generation adapters; live external retrieval is a separate authorized integration check.

**Depends on:** N16–N18 and an approved retrieval contract/provider choice. **PR boundary:** bounded enrichment, not unrestricted web browsing, agents acting on documents or library-wide chat.

## Final additions and visual review

### N24 — Add and validate an NLT Bible PDF import profile

**Outcome:** import the user's supplied NLT edition repeatably after the main application features are in place.

**Include:** inspect the supplied private PDF and confirm edition/language/source identity; implement its own extraction profile on N10's importer; retain page provenance, extraction reports and validation/approval controls. Add it to the existing edition-selection workflow without changing the user's defaults automatically.

**Acceptance:** synthetic profile tests, private source comparisons at layout boundaries and coverage checks follow N11's criteria; exact range retrieval is edition-specific; missing or uncertain passages stay visible and do not fall back to another edition. Keep actual Bible content and validation exports private. Source availability and human acceptance remain explicit gates.

**Depends on:** N10–N12 and availability of the supplied NLT PDF. **PR boundary:** one NLT profile and its validation, separate from visual polish. Schedule at the end of the implementation sequence, after N23 and before N25; this scheduling choice does not make unrelated features technical prerequisites or block their delivery.

### N25 — Visually review and polish the completed application

**Outcome:** make the finished workflows feel consistent, readable and polished on phone and laptop, using the implemented app as the review target.

**Include:** review all in-scope screens and their loading, empty, error, processing and completed states; agree a restrained visual direction, then refine typography, spacing, colors/contrast, hierarchy, form controls, navigation, source panels and inline audio players. Apply reusable tokens/components and review reading views plus session/event PDF presentation. Include the previously requested always-visible evidence panel, explicit event selection controls and outstanding wireframe feedback. Use the existing Figma file only if current free-plan access permits; a paid upgrade is not a prerequisite.

**Acceptance:** record before/after screenshots using deterministic synthetic sessions, multiple speakers, notes/slides, long titles/passages and an event with both ready and unfinished chapters. Inspect representative phone, tablet and laptop widths in a real browser; check keyboard focus, touch targets, contrast, wrapping, scrolling and media controls. Re-run affected behavioral tests, verify source/editing/export flows remain intact, render PDFs for visual review, and record any pending physical phone/Manta checks explicitly. Obtain user review of the visual direction/result; screenshot evidence alone is not functional or accessibility acceptance.

**Depends on:** N01–N24 for the final whole-app review, subject to their recorded acceptance status. **PR boundary:** one bounded visual review/polish pass, not a redesign of approved product behavior, new features, a framework migration or an open-ended design-system project. Functional usability/accessibility defects remain responsibilities of their original feature PRs; this task does not authorize deferring them until the end. If a necessary cross-cutting redesign is materially larger, propose that scope separately rather than expanding this PR silently.

## Follow-on work, outside the first usable release

These are outlines, not implementation commitments or extra PRs to create now:

- **Drive ingestion:** read-only, authorized folder selection; revision-aware downloads, idempotency and provenance. Uploading exports back to Drive is a separate explicit write workflow. Start after manual ingestion works.
- **Supernote .note/Digest feasibility:** verify native parsing, metadata/links and how Digests are actually accessible. Preserve originals; do not assume Drive contains the Digest database. Native editable export requires its own device evidence.
- **Multiple-recording alignment/comparison:** align source-specific timestamps and offer comparison evidence; the better microphone is not a reference transcript. Storing several recordings in N04 does not establish this capability.
- **Library search and conversational questions:** search finalized notes and sources with access controls and evidence links, once reliable source-linked notes exist.
- **Optional application login:** deferred by explicit user choice. Add a private account/session flow later if needed, without treating it as a current prerequisite.
- **Further Bible import profiles:** NAA, NIV and NLT are explicitly covered by N11, N12 and N24. Any additional editions reuse N10 but require their own source/format validation.

Standalone notebooks, voice-profile identification, cross-event AI synthesis and a generic workflow platform remain outside the initial plan.

## Cross-cutting acceptance for every relevant PR

- UUID primary/foreign keys, clear ownership, documented function contracts and migrations belong in the feature that uses them.
- Responsive phone/laptop behavior, loading/empty/error states, keyboard/touch access and source privacy are part of each screen PR, not a last-minute polish issue.
- Use local PostgreSQL, synthetic fixtures and fake external adapters for ordinary tests. Test failures and boundaries, not just happy-path rendering. Never call a zero-test run a pass.
- Real model/service, media/browser, private-content quality and Manta checks have separate evidence and acceptance gates. They are not replaced by passing mocks.
- A published issue must include the manual procedure applicable to its actual implementation: prerequisites, exact synthetic fixture names, numbered actions/expected results, pass/fail conditions, evidence to record and cleanup. Draft acceptance examples above inform those procedures; they are not claims that runnable feature tests exist today.
- Source citations are locators and review aids, not proof that generated wording is supported. Keep original, extracted, corrected and generated revisions distinguishable.
- No credentials, weights, private recordings/notes, Bible text/databases or personal generated output in commits/logs. Keep runtime data out of releases.
- Implement on issue branches; validate local checks and latest required CI; stage explicit paths and use descriptive signed commits with bodies. Leave PRs for the user's review/merge.
- Record scope/dependency changes and remaining gates in the same PR. Shared-service work belongs in its owning repository and needs separate authorization.

## Approved choices and remaining technical checks

These are questions for product review. Decisions explicitly recorded below are approved; other recommendations remain proposals. The user may approve a whole recommendation or change individual parts. Technical verification is the implementer's responsibility; do not ask the user to invent API limits, service contracts or free-disk measurements.

### 1. What can be uploaded, and what happens when something is deleted? — N04

**Decision A: starting upload limits.** Proposed application limits: 2 GB per recording, 500 MB per PDF and 50 MB per photo, configurable rather than baked into the data model. These are upload caps, not promises that every file can be processed by a model. Start by supporting the user's existing formats and verify codec/PDF/image support during implementation. A large supplied Bible may need a separate operator import limit rather than the session attachment limit. Do not silently resize originals or reduce recording quality to make them fit.

**Tradeoff:** generous limits accommodate long talks and high-resolution material but need storage, upload recovery and processing preflight. Small limits conserve resources but can make ordinary recordings unusable. Before finalizing caps, inspect current free storage, actual sample sizes and remote service limits; the app must explain any mismatch before submitting a processing job. No user decision about RAM or API payload mechanics is required.

**Decision B: original retention.** User approved this behavior on 2026-10-20: preserve originals until the user deletes the session/file, with no automatic cleanup of originals after processing. Delete reproducible temporary processing files separately, without confusing them with user originals, corrected transcripts or finalized notes.

**Decision C: deletion behavior.** The user approved recoverable Trash with automatic expiry on 2026-10-20. This supersedes the proposed manual-only purge default. The user confirmed 30 days after deliberate deletion as the automatic expiry period. Preserve restore before expiry and use a controllable clock for purge tests. Make expiry visible and restore possible before the deadline; closing or processing a session never starts deletion on its own. Warn about citations and exports affected by permanently deleting a source. Backups have a separate retention policy and may still contain deleted data until they expire.

**Decision D: scope of deletion.** User approved this behavior on 2026-10-20: deleting Notey's copy does not delete anything from Drive or the Supernote. Future cloud deletion would need its own explicit write workflow. When storage is low, warn and pause new work safely rather than silently removing sources. The implementer proposes a storage budget after measuring Lara, without changing other applications' allocations.

**Decision status:** retention/deletion behavior accepted, with automatic Trash expiry selected. Expiry confirmed: 30 days. File-size caps remain subject to technical verification. The subsequent decisions below supersede the earlier pending-answer state.

### 2. How should audio excerpts and edited source links behave? — N06/N16

**Decision A: playback interval.** Approved on 2026-10-20: start playback three seconds before the cited/unclear interval and stop three seconds after it, clamped to the recording boundaries. Example: a 12:10–12:28 reference plays 12:07–12:31. Offer more context, replay, speed and opening the full recording at that timestamp. No autoplay or automatic looping. Timestamps stay specific to each recording.

**Decision B: player movement.** Approved on 2026-10-20: within excerpt mode, the seek bar/jump controls stay within the displayed playback interval. A user can expand the interval or select full-recording mode to listen beyond it. Pause when changing to another paragraph/source, so an unrelated passage does not keep playing. The displayed interval must always match what is actually playing.

**Decision C: edits to a note paragraph.** Approved on 2026-10-20: keep source links and stable block IDs, and show a nonblocking support warning after material changes or split/merge. No per-paragraph acknowledgment or confirmation flow is required; keep editing simple. Allow adjusting sources or marking personal content when useful. Avoid nagging on obvious whitespace/punctuation-only edits; do not claim a perfect algorithm can distinguish every harmless edit from a meaning change. Never erase edit history or silently detach evidence.

**Decision D: correcting a source later.** Approved behavior: flag affected draft blocks and show the changed source excerpt; do not silently rewrite the user's notes. Preserve the source revision used by an already finalized/exported document; use a new document revision for accepted corrections.

**Answer format:** approve/change the context margin and pause behavior; approve retained links with review flags, or prefer a less interruptive warning-only approach. N17 separately decides which unresolved warnings block finalization.

### 3. What language should the notes and quotations use? — N07/N13/N15

**Technical checks, not product questions:** inspect what Lara's currently available services accept and return, and record missing capabilities in the owning project. The user should not be asked to choose request schemas or guess model readiness. Trial success is not production capability or verified content quality.

**Approved language rules (2026-10-20):**

- With no personal notes, generated prose follows the recording's main language, with an explicit session override available.
- If personal notes consistently use another language, that notes language takes precedence for generated prose. Example: Portuguese recording plus English notes produces English enhanced notes.
- If personal notes mix languages, generated connecting/enhancing prose follows the recording's main language. Preserve the language of the user's individual contributions. Example: Portuguese recording with Portuguese and English notes produces mainly Portuguese enhanced notes while retaining the user's English contributions in English.
- Do not silently translate the user's English contributions merely to make the document monolingual. Language detection uncertainty is visible and can be overridden. Preserve original sources and record source-to-output mappings.
- Direct quotations retain original wording unless explicitly translated and labeled as such. Bible defaults remain Portuguese NAA / English NIV according to the primary output language, with explicit edition overrides and later NLT availability. Exact Bible text always comes from the selected imported edition; never silently substitute another edition or rewrite what the speaker actually quoted.

These rules must be in N07 contract expectations, N13 citation handling, N15 generation fixtures and N17 exports. Add tests for the three explicit examples above; a successful API response is not evidence of language preservation or fidelity.

### 4. What does 'finalized' mean when questions remain? — N17

**Decision:** user approved the proposed distinction and draft exports on 2026-10-20. Apply distinguish invalid output, unresolved decisions and advisory warnings instead of one opaque quality score.

| Finding | Proposed behavior |
| --- | --- |
| Missing/foreign source IDs, broken document structure, or failed generation | Cannot mark that invalid revision finalized; repair the output, regenerate or remove the affected content |
| A Bible passage is marked verified but the edition/range/text is unavailable or mismatched | Cannot export it as a verified quotation; correct it or explicitly keep an unresolved reference without fabricated verse text |
| Uncertain handwriting/speech or a possible omitted example | Allow finalization after an explicit reviewed choice; retain uncertainty wording where needed |
| A materially edited paragraph has unreviewed support links | Show a nonblocking warning; no acknowledgment or confirmation is required for that paragraph |
| Optional outside enrichment is unsupported or uncited | Resolve/remove it, or retain it visibly labeled unverified; never silently treat it as established session content |

**Tradeoff:** blocking every uncertainty can make a mostly useful document impossible to finish. Allowing silent bypass makes 'finalized' misleading. Recommended meaning: the user accepted a particular revision and its disclosed limitations, not that the AI proved every statement correct.

**Exports:** the editor checklist need not clutter a clean reading copy. However, unresolved wording/references and unverified additions should remain visibly identified at the relevant content; do not hide them only in internal logs. Provide a clearly labeled draft export before finalization, without counting it as a finalized chapter in an event.

**Answer format:** approve/change the strict-versus-overridable categories; decide whether draft export is useful; confirm how uncertainty should remain visible in exports.

### 5. Who can open Notey, when do updates happen, and where are backups? — N20–N22

**Already established:** deploy on Lara, develop on the Mac, use private Tailscale access, and deliver the initial manual foundation deployment in N01. No public signup, public exposure, new paid provider or automatic PR merging is assumed. The initial empty/synthetic deployment does not establish protected personal-data hosting.

**Decision A: application login.** Approved: Tailscale-only access now; no extra application login. Record private-account login as future work. N20 verifies the intended private route for pages, source files, processing results, exports and LiveView. Do not claim per-user identity/permissions from a network boundary alone.

**Decision B: update timing.** Approved: automatic updates after the user merges a passing PR. If a PR needs a different update procedure, it must explicitly say so and include a concrete manual update plan before merge. Drain/recover active uploads and jobs rather than terminating work blindly. Do not assume an incompatible migration can be rolled back by swapping only the image. Automatic deployment never means automatic PR merging.

**Decision C: update transport.** This is primarily an implementation choice. The implementer should inspect existing infrastructure and propose the smallest mechanism consistent with approved security/cost boundaries (for example Lara fetching a verified release versus an approved private deployment connection). Ask the user only when the choice changes permissions, services or costs. N22 implements the agreed mechanism; CI success alone is not deployment evidence.

**Decision D: backup location.** Approved: Google Drive for now. Store encrypted backup sets outside Lara covering database, private originals and other nonreproducible application state. Inspect existing approved Drive access and select a dedicated backup folder during N22; no public sharing, Git-stored credentials or unapproved paid storage. Recovery keys must be available outside the failed host. A mirrored source folder alone is not a backup of the application database/corrections. Real upload/restore integration remains to be verified.

**Decision E: backup frequency and expiry.** Proposed initial policy: daily backups, a pre-migration recovery point, and retention of seven daily plus four weekly recovery points. This means a failure might lose up to a day's recent changes unless the policy is tightened. We must estimate storage and record how a consistent database/file set is obtained; separate expiry of database versus original assets must not break restores. Confirm retention before automatic expiry deletes backups, and test a restore in an isolated environment before claiming recovery works.

**Remaining checks:** confirm the dedicated Drive folder, access mechanism, available capacity and recovery-key handling during N22. Backup frequency/retention remains the proposed daily/pre-migration, seven-daily/four-weekly policy until explicitly settled; the user chose the destination, not an expiry schedule.

### Decision status

The choices explicitly marked approved above govern implementation. Remaining technical caps, backup expiry and deployment mechanics must be verified at their owning issue; do not reopen decisions already made or treat unanswered retention numbers as approval.

## Plan adjustment and review gate

The user approved publication and starting N01 on 2026-10-20. Narrow the existing foundation issue, publish the agreed tasks with labels/dependencies/milestones in Project 8, and use the issue tracker as the delivery source of truth. Record issue links and current validation/deployment gates in docs/delivery.md. Update pending Figma feedback when available; it does not block this planning review. Re-evaluate scope after N07 rather than promising unavailable shared capabilities. Plan adjustment: move the minimal actual Lara deployment and Tailscale verification into N01; N21 extends that deployment for persistent feature data and remote processing, while N22 owns automatic updates and recovery. This planning change does not claim a deployment has run.

Revision requested on 2026-10-20: NIV profile immediately after NAA (N12); NLT profile near the end (N24); whole-app visual review/polish last (N25). Renumbered the original N12–N22 to N13–N23 and updated their references. These were subsequently approved and published as GitHub issues; see delivery.md.
