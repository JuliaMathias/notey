# Workflow sketch review

Status: user likes the overall wireframes; two specific editor/audio revisions are requested. The file is not a fully accepted design or implemented behavior.

[Figma file: Notey — workflow sketches](https://www.figma.com/design/kdO3b46Ezqj4bz64arLRAG), in the user-selected personal Starter team. One file, three pages; no paid plan or Make generation requested.

## Inventory

Each screen has a 1200 px laptop frame and a 390 px phone frame:

| Page | Screens |
| --- | --- |
| 01 Library & sessions | Library; Session setup |
| 02 Processing & review | Processing; Review sources; Reference library |
| 03 Reading & export | Edit notes; Read notes; Event export |

All example names, titles, filenames and prose are synthetic. Bible passage boxes are explicit placeholders, not fabricated quotations. The screens use editable text, auto-layout containers and reusable Simple Design System control instances. Gray styling and type treatment are provisional. There are no real uploads, processing actions or downloads; buttons are visual controls, not a wired prototype.

## Evidence and limitations

- Passed: structural inspection of all 16 frames, nonzero text/control counts, populated frame placeholders cleared, and no horizontal overflow detected by bounds checks.
- Inspected visually: session setup on laptop, review on phone, reading on laptop, and event export on phone.
- Adjusted: body-text contrast in many shaded panels and narrower text width in the laptop reading view. Structural bounds checks passed after those edits.
- Blocked: final screenshots after those edits, and a remaining contrast adjustment in the session attachment panels, because Figma returned its Starter MCP tool-call limit. Do not claim full visual or accessibility acceptance. The file remains available for manual inspection.
- Not run: real browser/device accessibility and interaction checks; implementation/database/model tests, because this is design exploration.
- Pending: the event sketch describes inclusion/exclusion but needs explicit per-session selection controls in the next revision. The preference for output language vs source/edition language needs clearer wording; no translation policy is established by the example.

## Manual review procedure

Prerequisites: access to the linked file in the selected personal team. No real user source files are needed.

1. Open page 01. Inspect Library, then Session setup in both widths. Confirm category/event selection, multiple speakers, place/date/time and the three distinct attachment roles are understandable.
2. Open page 02. Inspect normal processing and the unavailable-service alternate state. Check the correction flow, optional original-page access, recording boundaries, source playback and Bible confirmation. Handwriting previews must not enter the finished notes.
3. Open page 03. Compare editing and reading. Check that personal notes are integrated, outside enrichment is labeled, and long passages have a readable place in the document.
4. Inspect Event export. Confirm chapter ordering, unfinished-session behavior and the proposed combined PDF structure. Record the missing explicit selection control as a design gap, not working behavior.
5. At 100% zoom, inspect the 390 px phone frames and the laptop layouts for readability, cropped text, visual order and controls that would be awkward on a phone. The tall frames represent scrolling content.
6. Add comments or report screen names and desired changes. Record accepted/revise decisions per flow, not only visual preferences.

Pass criteria: the user can explain the route from session creation to review and export on both sizes, with unresolved decisions recorded. This is design acceptance only; functional acceptance requires later implementation tests. Cleanup: none; the file contains synthetic material and should remain for revision.

## Delivery plan

Review these sketches before creating feature issues. Complete the known contrast/selection gaps and final visual QA when tool access is available, or inspect manually in Figma. Do not upgrade plans or incur costs without separate authorization. Deployment remains future work in the local Notey repository; no changes were made to Lara or shared services.

## User feedback requiring a design revision

- Edit notes: show selected-paragraph evidence immediately on the right on laptop and below the editor on phone. Retain an explicit full-source opener, but do not hide the useful excerpts behind “Inspect paragraph sources”.
- Review sources: replace “Play source audio” with an inline player showing play/pause, timeline and timestamps. Proposed playback is the relevant interval with adjustable context; full-recording playback is an explicit alternative.
- The user requested retaining these changes for later Figma revision. No Figma calls or edits were attempted for this feedback. Proposed data provenance and playback behavior are recorded in product.md and are not implemented.

The user requested a final whole-application visual review and polish pass after feature work and the NLT import profile. It is tracked as draft N25 in issue-drafts.md. It includes review of the actual responsive application and export presentation, without deferring ordinary feature-level usability/accessibility until that final pass.
