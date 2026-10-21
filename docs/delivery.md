# Delivery status

GitHub [Project 8](https://github.com/users/JuliaMathias/projects/8) and its issues are the implementation backlog. All 25 approved tasks are published with labels, eight milestones and 64 native blocking relationships, verified after publication on 2026-10-20. `issue-drafts.md` is the historical planning snapshot; update actual work in GitHub and this concise status, not a second backlog.

## N01 — Foundation in progress

Branch: `codex/issue-1-project-foundation`. Application [PR #26](https://github.com/JuliaMathias/notey/pull/26). Issue: [notey#1](https://github.com/JuliaMathias/notey/issues/1). Companion ingress: [home-server-infra#11](https://github.com/JuliaMathias/home-server-infra/issues/11).

Implemented locally: pinned Phoenix/LiveView/PostgreSQL scaffold; UUID schema/migration defaults; real persistence page; readiness endpoint; development database; production release/Docker/Compose recipes; CI; working/setup/testing guidance. No session or AI feature is claimed.

Evidence on 2026-10-20:

| Check | Result |
| --- | --- |
| Development PostgreSQL provision/create/migrate | Passed |
| Formatting and warning-free compilation | Passed |
| Behavioral tests with PostgreSQL | Passed: 9 tests, 0 failures |
| Development and production assets | Passed |
| Production release | Passed |
| Native Mac Docker image build | Passed, `notey:foundation-review`; not an amd64 Lara deployment |
| Local HTTP `/health` | Passed |
| Production Compose activation / release migration / container readiness | Passed locally with synthetic private test env |
| Real local browser interaction | Passed after resetting browser tools: in-app Chromium save/reload preserved UUID; server confirmed WebSocket transport |
| Local responsive/keyboard inspection | Passed at 1280x720 and 390x844; narrow page width equals viewport (390px), button reachable by Tab; physical phone remains pending |
| PR CI | Passed on foundation `ae80102` (1m33s); latest head must also pass before handoff, with results recorded in PR/issue |
| Signed commits / PR review | Signed planning `89418db` and foundation `ae80102` pushed; PR #26 open for user review |
| Lara app deployment / exact revision and image | Pending |
| Caddy route and preserved existing route | Pending separate infrastructure PR and user merge |
| Laptop HTTPS/WebSocket through Tailscale | Pending |
| Phone over cellular/Tailscale | Pending user device check |
| Production-container restart/persistence on Mac | Passed: saved UUID survived dedicated app/database restart; not Lara acceptance |
| Deployed restart/persistence on Lara | Pending |

N01 is not accepted or complete while these deployment/device gates remain. Leave its issue open even if a code PR is ready. Never use a closing keyword to prematurely erase these gates. The exact manual procedure is in [testing.md](testing.md); release operations are in [deployment.md](deployment.md).

The PR explicitly references #1. A Development closing association is intentionally pending: GitHub closes linked issues on merge, but #1 must stay open through deployment/device acceptance. See [GitHub linking behavior](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue). Both PRs are on Project 8 and attached to this chat. This is a documented remaining workflow limitation, not a claimed Development association.

At the end of task 1, **remind Julia to start a new chat** with this document, product/architecture docs and the current issue/PR links as the handoff. A quiet completion reminder is also attached to this chat.

Infrastructure companion [PR #12](https://github.com/JuliaMathias/home-server-infra/pull/12) prepared in a separate worktree: commit `5283d97`, Compose/Caddy validation passed, no live routing switch.

## Published sequence

| Milestone | Issues |
| --- | --- |
| 01 Foundation and library | [1](https://github.com/JuliaMathias/notey/issues/1) foundation; [22](https://github.com/JuliaMathias/notey/issues/22) automatic releases/backup recovery (second task); [2](https://github.com/JuliaMathias/notey/issues/2) sessions; [3](https://github.com/JuliaMathias/notey/issues/3) events; [4](https://github.com/JuliaMathias/notey/issues/4) private assets |
| 02 Recording and source review | [5](https://github.com/JuliaMathias/notey/issues/5) transcription; [6](https://github.com/JuliaMathias/notey/issues/6) audio review; [7](https://github.com/JuliaMathias/notey/issues/7) shared contracts; [8](https://github.com/JuliaMathias/notey/issues/8) typed PDFs; [9](https://github.com/JuliaMathias/notey/issues/9) handwriting/photos |
| 03 Verified Bible library | [10](https://github.com/JuliaMathias/notey/issues/10) normalized import; [11](https://github.com/JuliaMathias/notey/issues/11) NAA; [12](https://github.com/JuliaMathias/notey/issues/12) NIV; [13](https://github.com/JuliaMathias/notey/issues/13) citations |
| 04 Integrated notes | [14](https://github.com/JuliaMathias/notey/issues/14) boundaries/speakers; [15](https://github.com/JuliaMathias/notey/issues/15) generation; [16](https://github.com/JuliaMathias/notey/issues/16) editor; [17](https://github.com/JuliaMathias/notey/issues/17) finalization/draft exports |
| 05 Session and event documents | [18](https://github.com/JuliaMathias/notey/issues/18) session PDF; [19](https://github.com/JuliaMathias/notey/issues/19) event PDF |
| 06 Private hosting and updates | [20](https://github.com/JuliaMathias/notey/issues/20) access boundary; [21](https://github.com/JuliaMathias/notey/issues/21) private-file/job release and backup extensions |
| 07 Optional enrichment | [23](https://github.com/JuliaMathias/notey/issues/23) opt-in external context |
| 08 Final editions and visual polish | [24](https://github.com/JuliaMathias/notey/issues/24) NLT; [25](https://github.com/JuliaMathias/notey/issues/25) visual review |

## Plan adjustments and outstanding boundaries

- N01 includes the first real manual deployment and Tailscale verification. N02 / issue #22 is now the second task and adds automatic rollout with foundation backup/recovery. N22 / issue #21 later extends that same pipeline for private assets/remote jobs. This sequencing avoids calling a Dockerfile a deployed app.
- Keep application and shared ingress PRs separate. Existing Lara port 443 and private AI access must remain intact; Notey uses its own port 8443 ingress. Deployment waits for the user to merge the required PRs.
- Preserve the unrelated active infrastructure branch/worktree; prepare ingress in a separate worktree.
- N08 discovers current shared contracts before promising unsupported extraction/generation. Synthetic tests cannot establish model fidelity.
- NIV follows NAA; NLT is near the end, followed by visual polish. Source PDF availability and full validation remain edition-specific acceptance gates.
- Upload caps need technical verification. Backup destination is Google Drive; automatic backup expiry must wait for a separate approved retention policy.
- The current user-approved product choices supersede old proposals in the historical issue draft. The flow is reviewed; remaining Figma amendments are tracked in design-review.md and do not block foundation work.

## PR template adoption — 2026-10-21

The user approved the structured PR template and requested it globally, in Notey and in the AI/infrastructure project. `.github/PULL_REQUEST_TEMPLATE.md` is the repository version, with an explicit manual-testing decision and runnable procedure when needed. Both open PR descriptions use the structure. No implementation sequencing or runtime acceptance gates change: user merges and actual Lara/device verification remain pending.

## Coverage addition — 2026-10-21

The user requested ExCoveralls in N01 / PR #26. Add test-only tooling, a line-coverage report and a CI minimum of 35% against an initial 36.2% baseline (9 passing tests). Keep generated application components visible; exclude only test support. CI retains a private downloadable report for seven days without an external coverage account. Local validation passed at 35%; a deliberate temporary 100% minimum correctly exited with failure despite all 9 tests passing, and the tracked 35% setting was restored. Latest-head CI remains a separate check. No sequencing changes are needed because this extends the foundation's existing test/CI scope; actual Lara and physical-phone acceptance remain pending.

## Coveralls.io and factory follow-up — 2026-10-21

The user requested the hosted Coveralls.io integration and ExMachina after the initial local-only coverage increment. This supersedes the earlier no-external-upload direction. Use ExCoveralls' multiple-report task to test once, enforce the local minimum and post through GitHub authentication. Julia confirmed Notey is enabled in her Coveralls account; publication was verified in [Coveralls build 82509820](https://coveralls.io/builds/82509820) for `16cc022` / PR #26 (66/182 relevant lines, 36.26%); no paid subscription/trial was started. ExMachina provides sandboxed synthetic setup for latest-record ordering and pre-existing-record page tests: 11 tests pass locally at 36.2%. Existing deployment/device gates and issue sequencing need no changes because this remains test/CI work within N01.

The user also approved ExCoveralls/Coveralls.io and ExMachina as defaults for new Elixir projects in the global working instructions. Factories replace reusable test-data fixture helpers, while assertions exercise real application code. Hand-authored callbacks now identify their specific behaviour instead of `@impl true`; this changes compiler/readability guidance, not application behavior.

CI passed for `16cc022` in [run 39640022771](https://github.com/JuliaMathias/notey/actions/runs/39640022771): 11 tests, local minimum/report, successful hosted upload, assets and production release. The signed documentation follow-up must also pass CI on its latest head. Lara deployment/phone acceptance remains pending.

## Dialyzer addition — 2026-10-21

The user requested Dialyzer in N01 / PR #26, inspired by Moolah's CI, and as a default for new Elixir projects in global guidance. Add dev/test-only Dialyxir, a local command selecting the test environment, and a failing-on-findings CI step with separately cached type-analysis tables. Keep generated PLTs outside Git/Docker inputs and production releases. Local analysis passed with 0 errors and 0 skipped findings. A temporary intentional invalid contract produced exit status 2 and a GitHub warning annotation; the probe was removed, then clean analysis passed again. Formatting, 11 PostgreSQL tests (36.2% coverage) and production compilation passed. Latest-head CI remains a separate gate. No sequencing adjustments are needed: this extends foundation validation; Lara deployment and physical-phone acceptance remain separate and pending.

## Approved resequencing — 2026-10-21

Julia requested automatic deployment immediately after task 1, before session features. Task N02 is now [issue #22](https://github.com/JuliaMathias/notey/issues/22), in the first milestone and directly after issue #1 in Project 8. It builds immutable amd64 images in CI and deploys tested user-merged revisions on Lara, with serialized rollout, readiness, migration/recovery checks and foundation database backups. It is planning only; implementation has not started.

GitHub issue numbers/URLs stay stable. Task labels N02–N21 become N03–N22; former N22 becomes N02; N01 and N23–N25 are unchanged. Current issue titles/bodies and active documentation use the new labels. `issue-drafts.md` remains the approved historical snapshot with its original numbering; use GitHub/current delivery docs for implementation order.

Issue #22 now depends on accepted issue #1, not future issues #20/#21. Issue #21 later extends the early pipeline for actual private files and remote jobs and now depends on #22; issue #20 still gates hosted private-data access. Do not block synthetic-foundation automation on features that do not exist yet. Google Drive credentials, encryption/recovery evidence and unapproved backup-expiry retention remain implementation decisions/gates; no paid services or automated deletion are authorized by resequencing. Other feature dependencies are unchanged. N01 still requires its first manual deployment and real device acceptance.
