# Testing and evidence

## Local automated checks

Prerequisites and local setup are in the README. Ordinary tests use the local PostgreSQL test database, synthetic data and ExUnit SQL sandbox rollback. They never contact Lara, Drive, personal accounts or AI services.

```sh
docker compose -f compose.dev.yaml up -d --wait
mix setup
mix format --check-formatted
mix compile --warnings-as-errors
mix test
mix assets.build
MIX_ENV=prod mix compile --warnings-as-errors
MIX_ENV=prod mix assets.deploy
MIX_ENV=prod mix release
```

The foundation suite checks PostgreSQL's actual UUID column type and record reload, LiveView mount/click/new-mount persistence, readiness success plus deterministic unavailable/unexpected query results, and HTML/JSON errors. A LiveView test drives the server-side LiveView process; it does not test a real browser WebSocket, responsive layout or touch interaction.

CI repeats these checks on Ubuntu with PostgreSQL. Report the exact latest PR revision and CI result independently of local results. `docker build -t notey:foundation-review .` additionally builds a production image for the local architecture; a Mac ARM image is not evidence that an amd64 release runs on Lara.

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
