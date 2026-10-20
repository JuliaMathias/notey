# Notey working instructions

## Read first and report honestly

Read README.md, docs/product.md, docs/delivery.md, docs/architecture.md and the current GitHub issue before editing. Read directory instructions when present. Product decisions and the latest direct user instructions override older proposals. Check the actual clock and append America/Sao_Paulo date/time to every user-facing message. Use plain language and explain one useful concept with meaningful deliveries. Delegate only when the user explicitly authorizes it.

Inspect branch, working tree and implementation before changes. Preserve unrelated edits/private data. Make reasonable reversible choices within authorized scope. Ask only for material unresolved product/cost/privacy/data-loss decisions; explain why. Verify changing upstream APIs/versions from official sources. Distinguish approved requirements, assumptions and proposals. Existing plans and screenshots are not evidence that code works.

## Ownership and environments

Develop application code in this Mac repository. Lara is the deployment/integration host, not an application development workspace. Shared services own domain-neutral inference/extraction and resource coordination; Notey owns sessions, domain records, prompts, review, references and exports. Keep connections/credentials configurable, handle unavailable services and long jobs, and make ordinary development usable without Lara using fake adapters.

Inspect current infrastructure/service contracts before integration. Notey preparation does not authorize unrelated changes to Lara, shared services or networking. Identify necessary app-specific ingress/provisioning changes and their owning infrastructure repository before proceeding. Keep companion PRs separate. Keep deployment recipes in Git; credentials, original sources, Bible text/databases, model weights, runtime files and backups stay outside Git/logs. Do not install tools, create services or incur costs beyond the user's authorization.

## Code and tests

Prefer small concrete functions and explicit dependencies. Keep business rules separate from UI/storage/service adapters. Avoid speculative frameworks, unrelated refactors and unneeded dependencies. Document module purpose/boundaries; every Elixir module needs @moduledoc and every function @doc and @spec. Private functions use @doc false plus an adjacent explanatory comment; shared multi-clause functions use one documented/spec'ed head. Apply the same requirement to generated source and test support; macro-generated framework functions are not hand-authored functions. Kotlin classes/functions require KDoc if introduced.

Add meaningful deterministic behavioral tests with controlled clocks and fake remote services. Test failure cases and observable behavior. Ordinary tests run locally; record real remote/model/browser/device integration separately. Run relevant checks before committing; build success or zero tests is not behavioral acceptance. CI must pass on the latest PR head. Record manual prerequisites, exact fixture data/actions/expected results, evidence, pass/fail and cleanup in the issue or linked test guide. Preserve uncertainty: source IDs establish traceability, not truth.

## Git and completion

Use GitHub issues before changes, appropriate existing labels, and codex/issue-<number>-<description> branches. Stage explicit paths, inspect staged diffs and whitespace, and retain signed descriptive commits with a complete body explaining changes, purpose, validation and limitations. Do not disable signing. Keep PR descriptions aligned with final scope and verify the Development association. Never merge, auto-merge, queue or schedule merges for the user. Prefer squash as the documented merge strategy, leaving the merge to the user.

After a user merge, verify the actual merged revision before branch cleanup; preserve unpublished/uncommitted work and do not delete remote branches without authorization. Keep README/setup/run/test/status accurate. Record consequential architecture decisions and preserve superseded ones. GitHub issues are the implementation backlog; docs/issue-drafts.md is an approved historical planning snapshot after publication. Update delivery sequencing, dependencies/risks and remaining acceptance gates with each change, or record why no adjustment is needed. Distinguish ready for review, accepted, merged and deployed. End delivery reports with changes, actual checks, commit/PR links, limitations and required user action.

## Approved product constraints

Sessions are central; support multiple speakers, reusable places/categories, events and original recording/note/slide sources. Keep personal contributions in their original language: consistently other-language notes set the generation language; mixed notes follow the recording for new prose while preserving English contributions in English. Source evidence is visible beside editing on laptop and below it on phone. Source-link warnings after edits are nonblocking, with no acknowledgment workflow.

Trash expires 30 days after deliberate deletion, without deleting Drive/Supernote originals. Scripture comes only from an explicitly selected validated edition (NAA/NIV, later NLT). Extra enrichment is opt-in and labeled. Draft exports are supported. Start with Tailscale-only access; extra login is deferred. Deploy passing merged changes automatically unless a PR states an exception and supplies a manual rollout plan. No automatic PR merging. Backups target Google Drive; verify encryption/recovery and settle unapproved retention before automated expiry. No speculative model tuning or claims of accuracy without real evidence.
