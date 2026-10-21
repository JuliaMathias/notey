# Notey product direction

Status: product direction and workflow sketches were reviewed on 2026-10-19/20. The user approved publication of 25 implementation issues and starting N01. GitHub is the implementation backlog; see delivery.md for actual acceptance evidence. Approval is not proof of working features.

## Purpose

Turn recordings, personal notes and supporting presentation material into complete, organized, reviewable study notes. Sessions are the core unit. Sermons are the first use case; classes, technical talks and other study gatherings also fit. Standalone notebooks are a possible later extension, not an equal first-version focus.

## Confirmed requirements

- A session accepts one or more recordings, handwritten or typed notes, slide photos and additional PDFs including lecturer-provided slides. Slide content must inform the resulting notes.
- Sessions have categories, for example sermon, class, technical conference talk, retreat sermon, spiritual conference talk and small group Bible study.
- Sessions can belong to an event. Users can generate a single PDF for an entire event.
- Session metadata includes multiple speakers, date, time and place. Reusable speaker and place records are desired; exact fields and relationships remain to be designed.
- Preserve original private sources. Corrections and generated outputs do not overwrite originals.
- Detect proposed recording boundaries, meaningful material afterward and speakers; permit manual overrides.
- Check uncertain handwriting extraction before finalization. Finished notes contain extracted text, not side-by-side handwriting images. An original-page preview is a proposed review aid, not the final reading layout.
- Integrate personal notes seamlessly with the recording and supplied slide material. Generate notes when personal notes are absent. Prefer completeness and quality over speed.
- Include cited Bible passages in full from the user's verified edition. NAA is the Portuguese preference; NIV was accepted for English in the earlier conversation. The selected edition must remain explicit.
- Outside-source enrichment is explicitly requested and clearly distinguished in the output. Its exact visual treatment requires design review.
- The app must be usable on both phone and laptop.
- Develop on the Mac; host on Lara with remote access outside the home and automatic updates.
- Initial usable exports include a clean linked PDF. Native Supernote .note output remains a feasibility question.
- Search across the library and conversational questions about notes are later extensions.
- Designs must account for the user's free Figma plan.

## Agreed interaction flow

Library → create/edit session and attach sources → process recordings, handwriting and slides → review uncertain extraction, boundaries and references → generate integrated draft → edit and finalize → read/export. An event view groups and orders sessions for a combined export.

Review should focus on meaningful uncertainties. Full transcript proofreading is not proposed as a mandatory gate. Keep original-source inspection available without cluttering finished notes.

Phone layouts should offer the same core tasks through sequential views, with large controls and readable text. The editor shows relevant sources by default on the right on a laptop and below the editing area on a phone. Selecting a note paragraph/block changes the visible evidence; inspecting evidence should not require an extra reveal button. Source imagery belongs to source inspection and extraction review, not the final document.

## Domain ownership and record design

Phoenix LiveView with PostgreSQL and UUID identifiers is confirmed. Agreed context boundaries are Library (sessions/events/speakers/places/source assets), Processing (application jobs and review), ReferenceLibrary (Bible editions/imports/verses) and Notes (drafts/revisions/citations/exports). These boundaries are agreed, but modules are not implemented and exact schema fields remain to be designed.

Use a session-speaker join relationship so multiple sessions can share multiple speakers. Agreed initial defaults: one reusable category and optional event per session, optional reusable place, timezone-aware session time with date-only support when the exact time is unknown. Multiple categories, event nesting and cross-event membership are outside the initial defaults; revisit only if a concrete need arises.

Slide photos and slide PDFs are distinct source roles from personal notes even when all are attachments. Agreed behavior: extract text and meaningful diagrams, preserve page/image citations, and flag uncertain or conflicting content without assuming that an unmentioned slide was spoken aloud. Precise handling of visual diagrams and duplicate slides remains to be evaluated.

## Bible library boundary

Notey owns repeatable Bible imports, validation, edition selection, exact passage retrieval and citations. Canonical application storage should use Notey PostgreSQL; original PDFs stay in private file storage. Retain source hashes, extraction locations and import validation evidence. PDF layout profiles may vary by edition; universal PDF parsing is not promised.

The experimental SQLite database on Lara is private staging evidence, not a second permanent application database. Preserve it during ongoing evaluations. A later migration/import must validate it before promoting data to Notey PostgreSQL. No full-Bible import is currently established by the app scaffold.

Shared AI services on Lara own reusable inference and extraction capabilities. They do not own Notey's speakers, sessions, Bible library, prompts, review decisions or exports.

## Agreed hosting and update direction

Deploy Notey independently under Lara's application area, using its existing private networking and HTTPS ingress. Use existing Tailscale access for the user's phone/laptop outside the home; publicly accessible hosting has not been selected.

Agreed pipeline: develop on a task branch → reviewed PR and passing CI → user merges → build an immutable release image → Lara deploys the successful revision → migrate with a documented recovery procedure and health-check. Automatic deployment must never mean automatic PR merging. Do not store user data inside release images or overwrite it on updates.

The initial foundation milestone includes an actual managed deployment to Lara and verified private HTTPS/Tailscale access from laptop and phone outside home Wi-Fi, not only deployment configuration. Initial verification uses an empty app/synthetic data until application access protection is ready. Automatic rollout and recovery remain later increments.

The exact automatic-update transport (private-network runner versus Lara pulling published releases), authentication, backup/restore, migration recovery and service resource limits still need verification/design. No deployment or automatic-update mechanism has been configured by this scaffold.

## Agreed screen exploration

Use one Figma Design file and three pages: Library & sessions; Processing & review; Reading & export. Place both laptop and phone frames on each page. Prioritize low-detail flow sketches before visual polish. Free-plan availability and any AI credits must be checked for the chosen tools; no paid service is approved.

## Delivery sequencing and acceptance

The approved 25 tasks are published in GitHub Project 8; N01 is in progress. See [delivery status](delivery.md) for issue links, dependencies and actual verification gates. The first milestone includes a real manual Lara deployment, not only a Dockerfile; N02 / issue #22 is the second implementation task for automatic releases and foundation backups; later N22 / issue #21 extends that pipeline for private files and remote jobs.

Validate complete workflows against recordings, personal notes, slide material and exact Bible sources. Automated checks do not establish note fidelity. Phone, laptop and Supernote Manta checks remain necessary for their respective workflows. Private sources and generated outputs stay outside Git.

Lara's shared services are established integration targets. Check their actual contracts before implementation; use configurable connections, asynchronous jobs, unavailable-service handling and fake local adapters. Keep shared infrastructure changes in separate owning-repository PRs. The initial requested ingress is specifically covered by home-server-infra#11.

## Workflow sketches

The selected team is **personal**. See [wireframe review and evidence](design-review.md) for the Figma link, screen inventory, verification limits and review procedure. These are editable flow sketches, not an implemented or accepted UI.

## Editor evidence and audio review refinement

Confirmed feedback from wireframe review on 2026-10-19:

- Replace the editor's primary “Inspect paragraph sources” reveal action with sources already visible beside the editor on laptop, below it on phone. Full-source inspection remains an additional action.
- Replace “Play source audio” with an inline audio player including play/pause, a seek timeline and elapsed/total time. Keep this revision in project documentation while Figma integration access is limited.

Approved interaction behavior and planned implementation (not yet implemented):

- Show the selected paragraph/block's relevant source excerpts, not every complete file. Include transcript/audio ranges, extracted handwritten text, slide/PDF page excerpts and exact Bible references as applicable. Offer opening the complete source at the referenced location.
- Use stable UUIDs for note blocks, immutable source/extraction revisions and source units. Link note blocks to source units through an evidence relationship. Source units retain original asset identity plus audio start/end times, PDF page and optional region, image region, or exact edition/book/chapter/verse. One block can use many source units and a source unit can support several blocks.
- Require generation to return supplied source-unit IDs with each draft block. Validate that IDs exist, belong to the session or approved reference source, and that locators are valid. These mechanical checks establish traceability, not whether the source actually supports every claim. Do not present model citation selection as proof of fidelity.
- Do not identify paragraphs by their text or list position. Preserve block IDs through ordinary edits; allow adding/removing source links and marking text as personal content. Substantial rewrites or split/merge operations retain provenance and show a nonblocking source-support warning; do not silently call changed text verified. New user text need not have a recording source. Preserve source-version history when transcripts are corrected or generation is repeated.
- Playback starts only after an explicit play action and focuses on the cited/uncertain interval. Proposed default: include roughly three seconds of context on each side, clipped to recording bounds, visibly label the core interval and playback interval, and pause at the playback interval end. Provide replay, seek, small backward/forward jumps, playback speed, expanding context and opening the full recording at that timestamp. Exact controls and context margin remain design defaults until reviewed.
- Keep timestamps specific to each recording. A second recording needs an explicit alignment mapping; do not reuse timestamps across differently started recordings. Playback can seek within the original recording; saving a separate physical audio clip for every citation is not required.
- Phone evidence should be reachable near the active editing area, rather than placing it after a very long whole-session document. Selecting another block must not auto-play audio. Preserve the user's edit/scroll position when inspecting full sources.

Validation to add with implementation: multi-source block links; evidence isolation across sessions; edits and stale-support flags; corrected source revisions; recording-specific offsets; seeking and bounded stop/pause; clip bounds at recording start/end; no autoplay; unavailable media handling; phone/laptop keyboard and touch workflows. Ordinary tests use synthetic sources and fake AI adapters; real media/browser integration is separate.

Plan adjustment: revise these two wireframe areas when available, then review the interaction defaults. General positive feedback on the wireframes does not establish completion of these revisions or app behavior.

## Issue planning review

The Markdown drafts were reviewed and approved for publication on 2026-10-20. All 25 issues are now published with labels, milestones and native blocker relationships. [Issue drafts](issue-drafts.md) retain the historical planning snapshot; [delivery status](delivery.md) points to the current GitHub backlog.

## Additional edition profiles and final visual pass

Confirmed on 2026-10-20: add a dedicated English NIV PDF import profile immediately after NAA. The user is downloading that PDF and will place it in the private bibles folder. The user clarified that NIV is intended; the earlier NVI wording came from remembering the Portuguese name. There is no separate NVI import requirement. Confirm the exact publisher/edition from the supplied PDF.

Add an NLT profile at the end of the feature sequence, followed by a final visual review/polish task for the application on phone and laptop. Verify NLT source/edition details when supplied. The visual pass should refine the working workflows and exported reading material; feature-level usability and accessibility remain acceptance criteria throughout development.

Plan adjustment: [issue drafts](issue-drafts.md) now contain 25 drafts, with NIV originally labeled N12 (now N13 after resequencing), NLT as N24 and visual review/polish as N25. Independent work can proceed while private source PDFs or validation are pending. No Bible import, Figma mutation or application implementation was performed for this planning revision.

## Superseded proposals

The original draft had pending questions about manual-only Trash cleanup, application login, paragraph acknowledgment and output language. The following approved set supersedes those proposals. The initial retention reply was completed by the user's explicit 30-day expiry choice; it is no longer an open question. Keep backup expiry distinct: its numbers remain unapproved.

## Approved decision set — 2026-10-20

- Keep originals until deliberate deletion; recoverable Trash automatically expires 30 days later. Deletion affects Notey copies, not Drive/Supernote originals.
- Audio uses the proposed interval/context controls. Retain evidence links with nonblocking warnings after edits; no per-paragraph acknowledgment is required.
- Without personal notes, generated prose follows the recording. Consistently different-language notes take precedence (Portuguese recording + English notes → English enhanced notes). Mixed Portuguese/English notes over a Portuguese recording produce mainly Portuguese enhancements while preserving the user's English contributions in English. Preserve source-language contributions and allow explicit overrides; do not silently force a monolingual document.
- Finalization distinguishes hard integrity errors from overridable warnings, and draft exports are included. Changed-paragraph warnings remain nonblocking without acknowledgment. A finalized revision is user-accepted, not a claim of AI-proven truth.
- Access is Tailscale-only initially; extra application login is deferred. Automatic updates follow user merges of passing PRs. Any exceptional rollout must be explicit in that PR with a manual update plan. No automatic merging.
- Backups go to Google Drive. Verify a private folder, encryption/key recovery, access and restore. The proposed backup frequency/expiry numbers have not been explicitly approved and must be settled before scheduled deletion.
- The user authorized publishing the issues, adding them to GitHub Project 8 with relationships/milestones, and beginning the foundation issue. Development remains local; no delegation was authorized.

These choices supersede conflicting earlier recommendations (including manual-only Trash, an extra login now, automatic translation of all personal notes and paragraph acknowledgment gates). Implementation/status evidence is recorded in docs/delivery.md rather than inferred from approval.
