# Delivery status

GitHub [Project 8](https://github.com/users/JuliaMathias/projects/8) and its issues are the implementation backlog. All 25 approved tasks are published with labels, eight milestones and 64 native blocking relationships, verified after publication on 2026-10-20. `issue-drafts.md` is the historical planning snapshot; update actual work in GitHub and this concise status, not a second backlog.

## N01 — Deployed, accepted and documentation merged

Application [PR #26](https://github.com/JuliaMathias/notey/pull/26) and build follow-up [PR #28](https://github.com/JuliaMathias/notey/pull/28) are user-merged. Issue: [notey#1](https://github.com/JuliaMathias/notey/issues/1). Companion ingress [PR #12](https://github.com/JuliaMathias/home-server-infra/pull/12) is user-merged and active.

Current rollout status (2026-10-21, 18:32 BRT): **deployed and runtime accepted**. Julia reported that the requested physical-phone cellular/Tailscale, touch/layout and save/reload procedure passed. Device/browser and phone UUID were not supplied; this is user-reported evidence, not a directly observed agent test. Lara runs merged revision `23e61d8642ed9ab37c3fa1b60441933e7be6a6db`, amd64 image `sha256:df8a07872039be08fa5dd306cdb13809b852cfdee7b734717c4b67e01fb973e3`. [Merged-main CI passed](https://github.com/JuliaMathias/notey/actions/runs/39675826365). The dedicated database migration and container readiness passed. [Notey](https://lara.taila21247.ts.net:8443) returns valid HTTPS; a real in-app Chromium save/reload worked, Phoenix confirmed WebSocket transport, and the saved UUID survived a controlled restart of only Notey and its database. A second save/reload after restart also worked.

Port 443 retains its previous response byte-for-byte. Only Caddy publishes the Tailscale-bound 8443 route; Notey, PostgreSQL and the running generation service have no direct host port mapping. Shared AI services were not operated by this rollout: transcription was already stopped before deployment, while generation was running under separate work. No claim is made that this deployment restored transcription or validated AI behavior. Exact deployment paths, image identities and recovery limits are in [deployment.md](deployment.md#deployed-release--2026-10-21).

Cleanup: the two exact agent-created UUIDs recorded in testing.md were deleted, with SQL returning precisely those two rows. The phone record was preserved because its UUID was not supplied. Final evidence documentation was user-merged in PR #29 as `c27241df535c20edf9b7eb74d7a89d12ba6b1a66`; no runtime redeployment is needed for it. No private user material has been imported. Automatic updates and off-host backup/recovery remain N02 / issue #22, the next implementation task.

Implemented locally: pinned Phoenix/LiveView/PostgreSQL scaffold; UUID schema/migration defaults; real persistence page; readiness endpoint; development database; production release/Docker/Compose recipes; CI; working/setup/testing guidance. No session or AI feature is claimed.

Historical local evidence on 2026-10-20 (the current rollout status above supersedes the pending deployment entries below):

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

The historical pending gates above were completed by the current deployment and user-reported phone results. Runtime acceptance is complete; PR #29 is merged and issue #1 is closed. The exact manual procedure is in [testing.md](testing.md); release operations are in [deployment.md](deployment.md).

Historical association note: the implementation PRs referenced #1 without closing it before runtime acceptance. Final documentation PR #29 used `Closes #1`; its verified merge closed the issue. See [GitHub linking behavior](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue). Both PRs are on Project 8 and attached to this chat. The final documentation merge resolves that acceptance gate.

At the end of task 1, **remind Julia to start a new chat** with this document, product/architecture docs and the current issue/PR links as the handoff. A quiet completion reminder is also attached to this chat.

Infrastructure companion PR #12 was prepared separately and later user-merged as `72c37eeb195d2851ec157d7f7c3c601b3eb663f7`. Its ingress is now active; see the current rollout record above.

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

## Initial deployment handoff — 2026-10-21

N01 is deployed and runtime accepted. No further sequencing adjustment is needed: N02 / issue #22 is next. This documentation records the deployed application without implementing automatic deployment. PR #29 was user-merged at `c27241d`; it did not need another runtime rollout. Julia should start a new chat using this document and the next issue as the handoff. Agent-created synthetic records were removed; the unidentified phone record was preserved.

## N02 — Backup contract implemented; reusable delivery in progress

Verified on 2026-10-21: PR #29 is user-merged at `c27241d`; N01 is accepted.
Issue [#22](https://github.com/JuliaMathias/notey/issues/22) is the current task,
on `codex/issue-22-tested-releases`. The unrelated untracked `CLAUDE.md` is preserved.

The first focused increment implements a versioned archive/manifest with source,
image and payload checksums, rejects unsafe/corrupt contents and refuses restore
overwrite. Six deterministic tests and an isolated real PostgreSQL 17 dump/restore
passed locally, including recovery of a dropped column and synthetic source file.
See [backup format and test procedure](backup-format.md). This establishes the
foundation recovery contract, not live backups or automatic deployment.

Approved on 2026-10-21: backups before each deployment plus daily. Keep every
backup from the last five days and at least the newest 30 backups regardless of
age. A backup is eligible for expiry only when it is both older than five days
and outside the newest 30. Failed/incomplete backups must not displace successful
recovery points. No expiry mechanism has been implemented or enabled.

Approved on 2026-10-21: Lara-side pull deployment; public-key encryption with
Julia’s recovery key stored in her password manager and a protected offline copy.
Julia also requested a reusable workflow for future Lara apps, with per-app policy
parameters and onboarding documentation. Shared mechanisms belong to companion
[home-server-infra#17](https://github.com/JuliaMathias/home-server-infra/issues/17),
developed on Lara in tmux session `notey-n02`; Notey integration stays on this Mac.
Live repository/Drive credentials and recovery-key setup remain pending. The
five-minute checking interval is a proposed reversible operating setting.

Remaining acceptance gates: CI/image publication and identity verification;
merged-only/passing-CI selection and serialization; pre-migration encrypted backup;
successful and failed-health update exercises; safe migration recovery; real Drive
upload/download and external-key restore; live laptop HTTPS/WebSocket/data checks;
preserved existing ingress and shared AI state. Infrastructure guidance and
policy code are being prepared in the separate issue #17 worktree; no live
infrastructure configuration or runtime deployment has changed. Provisioning belongs
in a separately reviewed owning-repository PR.

Plan review: no feature-sequence adjustment is needed. N02 remains before session
features; #21 later extends file/job consistency and #20 gates private asset access.
Do not mark issue #22 accepted or close it from this contract-only increment.

Companion verification so far: 13 deterministic infrastructure policy tests passed
on Lara without contacting Docker, Drive, GitHub or AI services. The shared
runner/adapters and runtime acceptance gates remain incomplete. Notey local
formatting, 11 application tests (36.2% coverage) and Dialyzer passed separately.
Latest-head CI remains required after the branch is pushed.
