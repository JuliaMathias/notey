# Delivery status

GitHub [Project 8](https://github.com/users/JuliaMathias/projects/8) and its issues are the implementation backlog. All 25 approved tasks are published with labels, eight milestones and 64 native blocking relationships, verified after publication on 2026-10-20. `issue-drafts.md` is the historical planning snapshot; update actual work in GitHub and this concise status, not a second backlog.

## N01 — Foundation in progress

Branch: `codex/issue-1-project-foundation`. Issue: [notey#1](https://github.com/JuliaMathias/notey/issues/1). Companion ingress: [home-server-infra#11](https://github.com/JuliaMathias/home-server-infra/issues/11).

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
| Real browser interaction | Pending: in-app browser tooling timed out; LiveView automated test is separate evidence |
| Latest PR CI | Pending publication |
| Signed commits / PR review | Planning commit `89418db` signed and verified; foundation PR pending |
| Lara app deployment / exact revision and image | Pending |
| Caddy route and preserved existing route | Pending separate infrastructure PR and user merge |
| Laptop HTTPS/WebSocket through Tailscale | Pending |
| Phone over cellular/Tailscale | Pending user device check |
| Deployed restart/persistence | Pending |

N01 is not accepted or complete while these deployment/device gates remain. Leave its issue open even if a code PR is ready. Never use a closing keyword to prematurely erase these gates. The exact manual procedure is in [testing.md](testing.md); release operations are in [deployment.md](deployment.md).

At the end of task 1, **remind Julia to start a new chat** with this document, product/architecture docs and the current issue/PR links as the handoff. A quiet completion reminder is also attached to this chat.

Infrastructure companion prepared in a separate worktree: commit `5283d97`, Compose/Caddy validation passed, no live routing switch.

## Published sequence

| Milestone | Issues |
| --- | --- |
| 01 Foundation and library | [1](https://github.com/JuliaMathias/notey/issues/1) foundation; [2](https://github.com/JuliaMathias/notey/issues/2) sessions; [3](https://github.com/JuliaMathias/notey/issues/3) events; [4](https://github.com/JuliaMathias/notey/issues/4) private assets |
| 02 Recording and source review | [5](https://github.com/JuliaMathias/notey/issues/5) transcription; [6](https://github.com/JuliaMathias/notey/issues/6) audio review; [7](https://github.com/JuliaMathias/notey/issues/7) shared contracts; [8](https://github.com/JuliaMathias/notey/issues/8) typed PDFs; [9](https://github.com/JuliaMathias/notey/issues/9) handwriting/photos |
| 03 Verified Bible library | [10](https://github.com/JuliaMathias/notey/issues/10) normalized import; [11](https://github.com/JuliaMathias/notey/issues/11) NAA; [12](https://github.com/JuliaMathias/notey/issues/12) NIV; [13](https://github.com/JuliaMathias/notey/issues/13) citations |
| 04 Integrated notes | [14](https://github.com/JuliaMathias/notey/issues/14) boundaries/speakers; [15](https://github.com/JuliaMathias/notey/issues/15) generation; [16](https://github.com/JuliaMathias/notey/issues/16) editor; [17](https://github.com/JuliaMathias/notey/issues/17) finalization/draft exports |
| 05 Session and event documents | [18](https://github.com/JuliaMathias/notey/issues/18) session PDF; [19](https://github.com/JuliaMathias/notey/issues/19) event PDF |
| 06 Private hosting and updates | [20](https://github.com/JuliaMathias/notey/issues/20) access boundary; [21](https://github.com/JuliaMathias/notey/issues/21) persistent app release; [22](https://github.com/JuliaMathias/notey/issues/22) automatic updates/backups |
| 07 Optional enrichment | [23](https://github.com/JuliaMathias/notey/issues/23) opt-in external context |
| 08 Final editions and visual polish | [24](https://github.com/JuliaMathias/notey/issues/24) NLT; [25](https://github.com/JuliaMathias/notey/issues/25) visual review |

## Plan adjustments and outstanding boundaries

- N01 includes the first real manual deployment and Tailscale verification. N21 extends deployment for private assets/remote jobs; N22 adds automatic rollout and backup/recovery. This sequencing avoids calling a Dockerfile a deployed app.
- Keep application and shared ingress PRs separate. Existing Lara port 443 and private AI access must remain intact; Notey uses its own port 8443 ingress. Deployment waits for the user to merge the required PRs.
- Preserve the unrelated active infrastructure branch/worktree; prepare ingress in a separate worktree.
- N07 discovers current shared contracts before promising unsupported extraction/generation. Synthetic tests cannot establish model fidelity.
- NIV follows NAA; NLT is near the end, followed by visual polish. Source PDF availability and full validation remain edition-specific acceptance gates.
- Upload caps need technical verification. Backup destination is Google Drive; automatic backup expiry must wait for a separate approved retention policy.
- The current user-approved product choices supersede old proposals in the historical issue draft. The flow is reviewed; remaining Figma amendments are tracked in design-review.md and do not block foundation work.
