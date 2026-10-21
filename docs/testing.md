# Testing and evidence

## Local automated checks

Prerequisites and local setup are in the README. Ordinary tests use the local PostgreSQL test database, synthetic data and ExUnit SQL sandbox rollback. They never contact Lara, Drive, personal accounts or AI services.

```sh
docker compose -f compose.dev.yaml up -d --wait
mix setup
mix format --check-formatted
mix compile --warnings-as-errors
mix coveralls.html
mix assets.build
MIX_ENV=prod mix compile --warnings-as-errors
MIX_ENV=prod mix assets.deploy
MIX_ENV=prod mix release
```

The foundation suite checks PostgreSQL's actual UUID column type and record reload, LiveView mount/click/new-mount persistence, readiness success plus deterministic unavailable/unexpected query results, and HTML/JSON errors. A LiveView test drives the server-side LiveView process; it does not test a real browser WebSocket, responsive layout or touch interaction.

CI repeats these checks on Ubuntu with PostgreSQL. Report the exact latest PR revision and CI result independently of local results. `docker build -t notey:foundation-review .` additionally builds a production image for the local architecture; a Mac ARM image is not evidence that an amd64 release runs on Lara.

## Coverage checks

ExCoveralls 0.18.5 runs the existing ExUnit suite with line coverage. It is a test-only dependency; CAStore is also test-only to satisfy ExCoveralls' optional certificate-module reference without a compiler warning. No hosted coverage service or upload token is configured.

```sh
mix coveralls
mix coveralls.html
mix coveralls.detail --filter lib/notey/health.ex
```

All three commands select the test environment automatically. `mix coveralls.html` writes `cover/excoveralls.html`; the HTML highlights lines the tests did/did not execute. Reports remain outside Git. CI runs the HTML command instead of running the same test suite twice, enforces the configured minimum, then uploads `cover/` to the private run's **coverage-report** artifact for seven days. An artifact is not sent to Coveralls.io.

The initial measured baseline on 2026-10-21 is **36.2%**, with 9 tests passing. `coveralls.json` sets an initial **35% minimum**. This is a conservative starting guard against dropping below the current baseline, not a desired final coverage level or a guarantee against every smaller regression. Only `test/` helpers are excluded; unused generated components and release operations remain visible. Do not hide application files or add tests that merely call code to raise a percentage. Raise the minimum with meaningful tests as application behavior grows.

Coverage records which executable lines ran. It does not establish that assertions are good, every branch was checked, a browser/phone works or a model produced faithful notes. Zero-line modules may show 0% without lowering the line-weighted total.

Verification of this tooling must include both a passing run at the configured minimum and a controlled failure above the measured coverage, restoring the tracked configuration afterward. A missing report must not be described as a successful coverage check. Manual phone/Lara acceptance remains a separate N01 gate; adding coverage does not repeat or complete it.

Source: [ExCoveralls configuration and minimum coverage](https://excoveralls.hexdocs.pm/readme.html#coverage-options).

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
