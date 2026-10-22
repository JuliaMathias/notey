# Testing and evidence

## N02 release and recovery checks

Run `python3 -m unittest discover -s deploy -p 'test_*.py' -v` for deterministic
archive and adapter tests. Opt-in Docker/DB integration tests are skipped unless
their explicit environment variables are supplied; skipped checks are not passes.
Use [release-operations.md](release-operations.md) for setup, live Drive recovery,
first automatic rollout, laptop behavior and preservation gates. The maintained
[backup test](backup-format.md#runnable-local-verification) restores a real local
PostgreSQL dump after a destructive column change.

The optional actual image exercise requires a downloaded CI `release-package`,
the existing local `notey:foundation-review` image, and reviewed installed shared
runtime tools (not an infrastructure development checkout). Set
`NOTEY_RELEASE_TEST_PACKAGE=/PRIVATE/package` and
`NOTEY_MECHANISM_TEST_DIR=/PRIVATE/tools`, then run
`python3 -m unittest discover -s deploy -p test_release_integration.py -v`.
It creates random `notey-n02-test-*` projects/networks/volumes, uses synthetic
credentials/data, and removes only those resources. It tests real image loading,
migrations, activation, persistence, failed readiness, a dropped-column query
failure and dump restoration into a new isolated database. The Mac emulation fixture adds OTP’s documented `+JMsingle true` JIT option
through a temporary Compose override; the published recipe/Lara are unchanged.
Storage and the failure injection are faked. Local container HTTP does not establish Lara HTTPS
or WebSocket behavior. No ordinary test contacts Google/GitHub/Lara.

Execution on 2026-10-22: the two actual Docker exercises passed using the CI
39735572645 package; successful update preserved the exact UUID and failed
readiness held recovery, with the pre-migration dump restoring the dropped
column/UUID into a new database. The separate PostgreSQL archive test passed.
Current ordinary suite: 14 deterministic passes, three explicit integration
skips. Live credentials, Drive recovery and Lara browser/timers remain unrun.

N02's separate [backup-format checks](backup-format.md#runnable-local-verification)
cover archive integrity and an opt-in real local PostgreSQL restore, including a
destructive schema change that image rollback alone cannot recover. They do not
establish live encryption, Google Drive access or Lara release acceptance.

## Local automated checks

Prerequisites and local setup are in the README. Ordinary tests use the local PostgreSQL test database, synthetic data and ExUnit SQL sandbox rollback. They never contact Lara, Drive, personal accounts or AI services.

```sh
docker compose -f compose.dev.yaml up -d --wait
mix setup
mix format --check-formatted
mix compile --warnings-as-errors
mix coveralls.html
mix dialyzer
mix assets.build
MIX_ENV=prod mix compile --warnings-as-errors
MIX_ENV=prod mix assets.deploy
MIX_ENV=prod mix release
```

The foundation suite checks PostgreSQL's actual UUID column type and record reload, LiveView mount/click/new-mount persistence, readiness success plus deterministic unavailable/unexpected query results, and HTML/JSON errors. A LiveView test drives the server-side LiveView process; it does not test a real browser WebSocket, responsive layout or touch interaction.

CI repeats these checks on Ubuntu with PostgreSQL. Report the exact latest PR revision and CI result independently of local results. `docker build -t notey:foundation-review .` additionally builds a production image for the local architecture; a Mac ARM image is not evidence that an amd64 release runs on Lara.

## Dialyzer type analysis

Run `mix dialyzer` after `mix deps.get`. The command automatically uses the test environment, so it analyzes application modules and compiled test-support modules, including the factory, against the same dependencies as tests. ExUnit is explicitly added to the lookup tables because test-support modules call it. ExUnit `.exs` test cases are executed by the test suite rather than compiled into this analysis. Dialyxir 1.4.8 is the Mix integration for Erlang's Dialyzer; it is a dev/test-only dependency with `runtime: false` and is excluded from production releases.

Dialyzer compares inferred types with function contracts and reports inconsistencies, such as passing a value a function cannot accept. It does not run application workflows or prove every spec correct, so keep behavioral tests, coverage and browser/integration checks separate.

The first run builds persistent lookup tables (PLTs): reusable type information for Erlang, Elixir and dependencies. These are generated under `.dialyzer/`, ignored by Git and excluded from Docker build context. CI caches them separately by OS, pinned Erlang/Elixir versions and dependency/project configuration. A compatible fallback cache is checked and updated automatically; `mix dialyzer --format github` always runs the analysis, even on a cache hit, and findings fail the check. No warning ignore file or exit-status bypass is configured. The initial run exposed missing ExUnit lookup information and JS helper contracts that claimed LiveView's opaque internal type while constructing public `%JS{}` structs. Including ExUnit and using the public struct contracts resolves these without changing runtime behavior or suppressing findings.

To reproduce CI locally, run `mix dialyzer --format github`. Success requires exit status 0 and no warnings. When a warning appears, inspect its source location and compare the spec with actual possible values before changing code or types. A rebuild can be forced by moving only the generated `.dialyzer/` directory aside, then rerunning; never delete application data to reset analysis. No database, Lara connection or phone test is needed for static analysis itself.

Validation on 2026-10-21: the clean project passed with 0 errors/0 skips; a temporary `integer()` return contract with an atom result failed with exit status 2 and an `invalid_contract` GitHub annotation. The probe was removed, and clean analysis and all 11 tests passed again. The probe is not tracked or part of the application.

The cache and GitHub annotation format follow the pattern in [Moolah's CI](https://github.com/JuliaMathias/moolah/blob/main/.github/workflows/ci.yml), adapted to Notey's pinned actions/toolchain and existing coverage/release checks. Source: [Dialyxir documentation](https://dialyxir.hexdocs.pm/readme.html).

## Coverage checks

ExCoveralls 0.18.5 runs the existing ExUnit suite with line coverage. It is a test-only dependency; CAStore is also test-only to satisfy ExCoveralls' optional certificate-module reference without a compiler warning. The user requested Coveralls.io integration after the initial local-report setup. CI uses GitHub's short-lived job token; no personal access token is stored in the repository.

```sh
mix coveralls
mix coveralls.html
mix coveralls.detail --filter lib/notey/health.ex
```

All three commands select the test environment automatically. `mix coveralls.html` writes `cover/excoveralls.html`; the HTML highlights lines the tests did/did not execute. Reports remain outside Git. CI runs `mix coveralls.multiple --type html --type github`: one test run produces the HTML report, checks the 35% minimum, then posts source-code line coverage and commit/PR metadata to Coveralls.io. The local HTML artifact remains available for seven days. Git history is fetched so ExCoveralls can identify the tested PR commit. The `html` type runs first, so a failed local minimum stops the upload.

The initial measured baseline on 2026-10-21 is **36.2%**, with the original 9 tests passing; the ExMachina addition brings the suite to 11 tests with the same line coverage. `coveralls.json` sets an initial **35% minimum**. This is a conservative starting guard against dropping below the current baseline, not a desired final coverage level or a guarantee against every smaller regression. Only `test/` helpers are excluded; unused generated components and release operations remain visible. Do not hide application files or add tests that merely call code to raise a percentage. Raise the minimum with meaningful tests as application behavior grows.

Coverage records which executable lines ran. It does not establish that assertions are good, every branch was checked, a browser/phone works or a model produced faithful notes. Zero-line modules may show 0% without lowering the line-weighted total.

Verification of this tooling must include both a passing run at the configured minimum and a controlled failure above the measured coverage, restoring the tracked configuration afterward. A missing report must not be described as a successful coverage check. Manual phone/Lara acceptance remains a separate N01 gate; adding coverage does not repeat or complete it.

Source: [ExCoveralls configuration and minimum coverage](https://excoveralls.hexdocs.pm/readme.html#coverage-options).

## Test data with ExMachina

`Notey.Factory` in `test/support/factory.ex` uses test-only ExMachina 2.8.2 with the existing PostgreSQL sandbox. Import it only in tests that need setup data. `build(:foundation_check)` creates an unsaved struct; `insert(:foundation_check, inserted_at: timestamp)` saves a synthetic record inside the test transaction. Let Ecto create UUIDs/timestamps unless the behavior under test requires explicit values.

Use factories to establish starting data, then call the application operation under test. Do not replace `Foundation.save_check/0` with a factory insertion when testing whether the app saves correctly. Current examples cover selecting the latest entry with deterministic date/UUID tie-breaking, and opening the page when an entry already exists. They add behavior assertions rather than tests of ExMachina itself. Test fixtures never use personal source data.

## Coveralls.io setup and verification

Julia confirmed Notey is enabled in her Coveralls account on 2026-10-21. Real publication was verified for `16cc022`: [Coveralls build 82509820](https://coveralls.io/builds/82509820) identifies PR #26 and the correct branch/commit, with 66 of 182 relevant lines covered (36.26%). ExCoveralls truncates its local display to 36.2%; the underlying covered/total counts agree. Keep this check separate from local tests.

1. If setting up again, sign in to the existing [Coveralls account](https://coveralls.io/) and add/enable `JuliaMathias/notey`. The repository is private; confirm the account supports private-repository coverage. [Current pricing](https://coveralls.io/pricing) lists paid private-repository plans. Do not start a subscription/trial, enter payment information or change repository visibility as an incidental setup step.
2. Complete any GitHub authorization/selected-repository setup requested by Coveralls. This account step belongs to Julia. Do not paste credentials or tokens into chat or Git. The configured ExCoveralls GitHub mode uses `${{ secrets.GITHUB_TOKEN }}` from the Actions run, not a new repository token in source.
3. Re-run the PR's CI workflow or push the next reviewed commit. Expect 11 passing tests, a coverage percentage above the tracked minimum, an HTML artifact, and ExCoveralls' explicit successful-upload message.
4. In Coveralls, verify the new build belongs to `JuliaMathias/notey`, matches the CI commit/PR and shows the expected source files/line coverage. Record the build URL and result in PR #26. Enabling the repository alone is not evidence of a successful report.
5. If registration/authorization fails, fix the account setup and rerun; keep that failure visible. ExCoveralls 0.18.5 treats some timeouts/maintenance errors as nonfatal, so a green CI job alone is not proof that Coveralls accepted a report. Preserve the local minimum/report check and record remote publication as blocked/unverified until an actual report is confirmed.

Local `mix test` and `mix coveralls.html` never upload to Coveralls. CI's external integration is intentional and authorized; its report includes tracked application source text and coverage, not private recordings/notes/Bible data. No production behavior changes and no additional phone test are needed for these test tools. Existing N01 deployment/device checks still apply.

Sources: [ExMachina](https://ex-machina.hexdocs.pm/readme.html), [ExCoveralls GitHub integration](https://excoveralls.hexdocs.pm/readme.html#mix-coveralls-github-post-coverage-from-github-actions), and the installed ExCoveralls 0.18.5 `Mix.Tasks.Coveralls.Multiple` implementation (one run, multiple report types).

## N01 browser and deployed acceptance procedure

Prerequisites: a recorded source revision, tested release image, deployed dedicated database and app, approved/applied ingress, and the phone/laptop connected to the intended tailnet. Use only synthetic `foundation_checks` records. No personal material is required. The target URL is `https://lara.taila21247.ts.net:8443`; verify the host's actual configuration before use. For local browser checks use `http://localhost:4000` after `mix phx.server`.

1. Record date/time, source SHA, image ID/digest, URL, device/browser and connection type. Open `/health`: expect HTTP 200 with `{"status":"ok"}` and no connection secrets. Open `/`: expect Notey and the connection-check control.
2. In browser developer tools on the laptop, observe `/live/websocket` upgrade (101). Click **Save connection check**: expect a UUID to appear without a full-page reload, no console/network error and a working enabled button afterward. Record that UUID; reload and expect the same UUID. HTTP 200 alone does not establish LiveView connectivity.
3. Inspect laptop and narrow phone layouts: text/UUID wraps, control is touchable, keyboard focus is visible and the result is announced through the status region. No horizontal page scrolling should be needed.
4. From the phone, disable home Wi-Fi, keep Tailscale connected and use cellular. Repeat load, save and reload. Record the new UUID and connection evidence. A Mac check cannot stand in for this physical-device result.
5. On Lara, restart only the Notey stack using the procedure in deployment.md. Open the page again and expect the last recorded UUID to remain. Record HTTP readiness and WebSocket interaction after restart. Never restart shared AI, Caddy or other applications as part of the application persistence check.
6. Verify existing `https://lara.taila21247.ts.net/` still serves its previous response, and existing AI container health/network publication are unchanged. Inspect Notey database/app published ports: neither should have a host mapping. Ingress must publish 8443 only on the verified Tailscale address, with a valid hostname certificate.
7. Cleanup only the UUIDs created by these checks, using parameterized application deletion from a release eval or a reviewed SQL statement restricted to the recorded UUIDs. Do not truncate the table or remove database volumes. Keep the requested app running.

Pass requires all applicable steps. Record failed, blocked or not-run steps explicitly, including phone access awaiting Julia. Never label the foundation complete from a Docker build or mocked browser test.

## Evidence record

Add dated results to issue #1 / delivery status with source/image identity, commands, check outcome and browser/device details. Screenshots can support layout review but not prove persistence or model accuracy. Do not capture cookies, env files, connection URLs containing passwords or private user sources. N01 provides no AI quality or Bible-import evidence.

## Foundation evidence — 2026-10-20

Local in-app Chromium at 1280x720: save/reload retained synthetic UUID
`f3d19b63-7114-4777-8233-94f9a0e0e7b7`; Phoenix logs confirmed `Transport: :websocket`.
At 390x844, page scroll width and viewport width were both 390px, the UUID wrapped
within the page, and Tab reached the save button. This is responsive desktop-browser
evidence, not a physical-phone/cellular result. Screenshots are temporary local
artifacts `/tmp/notey-foundation-browser.png` and `/tmp/notey-foundation-phone-width.png`.

Separately, the production image activated through `deploy/apply.sh` with fresh
local synthetic credentials, ran its migration, returned healthy readiness, and
retained UUID `809b51db-e24d-4322-b63e-1682e0fa8b98` after both database and web
containers restarted. Image: `notey:foundation-review`, local ARM architecture,
ID `sha256:d1ca43e4a57fa9a970437adb0496560916afe1e4c92d43de79b07c60cd27302d`.
It was built before committing the foundation; Lara must build/test its own actual
merged revision for amd64. The temporary production-test stack can be stopped
without deleting its volume; ordinary development PostgreSQL remains separate.

No Lara app rollout, Caddy switch or real remote AI call was performed. The runtime
acceptance gates remain in issue #1.

## Lara deployment evidence — 2026-10-21

Release `23e61d8642ed9ab37c3fa1b60441933e7be6a6db` and image identity are recorded in [deployment.md](deployment.md#deployed-release--2026-10-21). Merged-main CI [39675826365](https://github.com/JuliaMathias/notey/actions/runs/39675826365) passed separately from these live checks.

| Live check | Result and evidence |
| --- | --- |
| Migration and readiness | Passed: dedicated PostgreSQL migration `20261020195000`; app/database healthy; Mac and Lara HTTPS `/health` returned 200 with the expected JSON. |
| Real laptop browser | Passed: in-app Chromium at the deployed URL saved UUID `80d0ca6b-28b2-4007-96d3-6d7f241b1c00` at 21:07:58 UTC; reload retained it. Server logs confirmed `CONNECTED TO Phoenix.LiveView.Socket` with `Transport: :websocket`. A developer-tools HTTP 101 capture was not collected; transport evidence is from the server and successful browser events. |
| Restart persistence | Passed: the exact UUID was queried before and after restarting only `notey` db/web; both containers became healthy and browser reload retained the UUID. A new save afterward produced `21ec3532-a3af-45eb-8852-8312d2c00f8d` at 21:12:16 UTC; reload retained it too. |
| Existing routes and publication | Passed: port-443 body unchanged before/after; Caddy ports bound to Tailscale IPv4; no Notey/database host mappings and no direct mapping on the running generation service. Transcription was already stopped; no AI quality or health-restoration claim. |
| Physical phone, cellular/Tailscale and touch/layout | Passed, reported by Julia on 2026-10-21 at approximately 18:32 BRT in response to the full procedure. Browser/device and UUID were not supplied; not directly observed by the agent. |
| Test-data cleanup | Passed for the two agent-created UUIDs above: exact-ID SQL deletion returned only those two rows. The unidentified phone record was deliberately preserved. |

No host reboot, backup restore, AI integration, session upload or Bible-import acceptance is implied by these checks. The screenshot `/tmp/notey-deployed-lara.png` is temporary local visual evidence, not a tracked private-data artifact.
