# Environment Variables

Complete reference for every environment variable the Aspose.Cells Cloud MCP
Server reads, where it is read, and what happens when it is missing, empty or
malformed.

## Configuration rules

Three rules apply to **every** variable below, and they explain most
"but I set it and nothing changed" reports:

1. **Empty string means unset.** Every reader uses `os.getenv(NAME) or fallback`
   (or `if value:`), so `MCP_FILE_TTL_HOURS=""` is equivalent to not setting it
   at all. No error is reported.
2. **Malformed values usually fall back silently, but not always.** Most
   variables degrade to their default on unparseable input; `MCP_PORT` is the
   one exception and crashes the process at startup. The per-variable notes
   below call this out.
3. **Function arguments beat the environment.** `run_server(transport=...)` and
   `run_server(client_id=..., client_secret=...)` take precedence over the
   corresponding variables — see [mcp_server.py:536](../mcp_server.py#L536).

### When each variable is read

| Read at | Variables |
| --- | --- |
| Process start (`run_server`) | `MCP_TRANSPORT`, `TRANSPORT`, `MCP_HOST`, `HOST`, `MCP_PORT`, `PORT`, `MCP_PATH`, `MCP_SSE_PATH`, `LOG_LEVEL` |
| Every tool call | `ASPOSE_CLOUD_CLIENT_ID`, `ASPOSE_CLOUD_CLIENT_SECRET`, `ASPOSE_CLOUD_API_URL`, `MCP_CLOUD_TIMEOUT_SECONDS` |
| First use of the registry (once, then cached) | `MCP_STATE_DIR` |
| Every file registration (upload or conversion) | `MCP_FILE_TTL_HOURS` |

The first row means a transport/port change requires a restart. The second row
is why **missing credentials do not fail at startup** — see the warning under
Required.

## Required

| Variable | Default | Read by |
| --- | --- | --- |
| `ASPOSE_CLOUD_CLIENT_ID` | *(none)* | [core/utils/spreadsheet_util.py:37](../core/utils/spreadsheet_util.py#L37) |
| `ASPOSE_CLOUD_CLIENT_SECRET` | *(none)* | [core/utils/spreadsheet_util.py:38](../core/utils/spreadsheet_util.py#L38) |

Aspose Cloud credentials, created on the
[Aspose Cloud dashboard](https://dashboard.aspose.cloud/). All spreadsheet
processing happens in Aspose Cloud Storage and the Aspose.Cells Cloud REST API,
so the server is unusable without them.

> **These are read lazily, once per tool call — the server does not validate
> them at startup.** A missing or wrong credential produces a clean start, one
> masked log line (`client_id=ab****xy`), and then a failure on *every* tool
> call. A pod configured this way stays `Ready` and looks healthy.

Credentials are never written to logs; only the masked form is ever printed
([mcp_server.py:18](../mcp_server.py#L18)).

## Cloud connection

| Variable | Default | Read by | Notes |
| --- | --- | --- | --- |
| `ASPOSE_CLOUD_API_URL` | SDK default (`https://api.aspose.cloud/v4.0`) | [core/utils/spreadsheet_util.py:39](../core/utils/spreadsheet_util.py#L39) | Unset or empty both select the SDK default. Set it to point at a regional or mock endpoint. |
| `MCP_CLOUD_TIMEOUT_SECONDS` | `300` | [core/utils/spreadsheet_util.py:23](../core/utils/spreadsheet_util.py#L23) | Upper bound, in seconds, on each Aspose Cloud HTTP call. Applied as a process-wide `socket.setdefaulttimeout`, which also caps the OAuth token fetch the SDK performs in its constructor. **`0` or a negative value disables the bound entirely** — a stalled backend then hangs the tool call forever. Unparseable values silently fall back to `300`. |

## Transport and binding

| Variable | Default | Fallback variable | Read by |
| --- | --- | --- | --- |
| `MCP_TRANSPORT` | `stdio` | `TRANSPORT` | [mcp_server.py:540](../mcp_server.py#L540) |
| `MCP_HOST` | `0.0.0.0` | `HOST` | [mcp_server.py:549](../mcp_server.py#L549) |
| `MCP_PORT` | `8080` | `PORT` | [mcp_server.py:550](../mcp_server.py#L550) |
| `MCP_PATH` | `/mcp` | — | [mcp_server.py:551](../mcp_server.py#L551) |
| `MCP_SSE_PATH` | `/sse` | — | [mcp_server.py:552](../mcp_server.py#L552) |

- `MCP_TRANSPORT` accepts `stdio`, `streamable-http` or `sse` (matched
  case-insensitively, surrounding whitespace stripped). Anything else falls
  through to the `stdio` branch.
- `MCP_PATH` is used **only** by `streamable-http`; `MCP_SSE_PATH` **only** by
  `sse`. Setting the one that does not match the active transport has no effect.
- The `TRANSPORT` / `HOST` / `PORT` fallbacks exist for older deployments; prefer
  the `MCP_`-prefixed names.
- `MCP_HOST` and `MCP_PORT` are ignored for `stdio`, which does not listen on a
  socket.
- ⚠️ **`MCP_PORT` is the one variable that fails loudly.** It is parsed with
  `int()` with no guard, so `MCP_PORT=8080tcp` (or any non-integer) raises
  `ValueError` and the process exits at startup.

The server also answers two plain HTTP routes alongside the MCP endpoint,
independent of the transport: `GET /health` → `{"status": "ok"}` and
`GET /version` → `{"version": "..."}` ([mcp_server.py:566](../mcp_server.py#L566)).
Their paths are not configurable.

## State and storage

| Variable | Default | Read by |
| --- | --- | --- |
| `MCP_STATE_DIR` | Platform user-data directory (`platformdirs.user_data_dir("aspose-cells-cloud-mcp")`); the Linux image sets `/state` | [core/storage.py:61](../core/storage.py#L61) |
| `MCP_FILE_TTL_HOURS` | unset → **files never expire** | [core/storage.py:185](../core/storage.py#L185) |

`MCP_STATE_DIR` holds `registry.db`, the SQLite database that maps each
`file_uuid` to the cloud object name and its metadata (provenance, timestamps,
TTL). The file *bytes* always live in Aspose Cloud Storage; only this small
metadata table is local.

- **In containers, always set this to a writable volume.** Left unset, the
  database is written inside the image's own filesystem and is lost on every
  container restart, which silently invalidates all previously issued
  `file_uuid` handles. The Linux image sets it to `/state` for exactly this
  reason ([Dockerfile.Linux:54](../Dockerfile.Linux#L54)) — point a volume at
  that path.
- The directory is created if missing; the database is created on first use.
  To pre-create or migrate it explicitly (for example, on a freshly mounted
  volume before the server starts), run
  `python scripts/init_registry_db.py` — see
  [scripts/init_registry_db.py](../scripts/init_registry_db.py).

`MCP_FILE_TTL_HOURS` expires a stored file that many hours after it was
**registered** — that is, from upload or conversion time, *not* from its last
use. Fractional values are accepted (the value is scaled by 3600). An
unparseable value silently means "never expire". A `ttl_seconds` argument to the
underlying registry API, where a caller supplies one, takes precedence over this
variable.

> **This variable does not free cloud storage.** Expiry deletes only the local
> `registry.db` row; the file's bytes stay in Aspose Cloud Storage and keep being
> billed. Nothing in this codebase calls a cloud delete API: `purge_expired()`
> returns the expired rows "for best-effort cloud cleanup"
> ([core/storage.py:385](../core/storage.py#L385)) but its only caller discards
> that return value ([core/storage.py:243](../core/storage.py#L243)), and
> `storage.remove()` is called solely for a failed upload
> ([core/io.py:29](../core/io.py#L29)). So the only effect of setting a TTL is
> that handles stop resolving — it bounds the growth of `registry.db`, whose rows
> are tiny, and nothing else. Size it against **how long a workflow may hold a
> `file_uuid`**, not against storage cost, and treat cloud-side cleanup as an
> unimplemented follow-up.

> **Known discrepancy:** the [README](../README.md) and the `MCP_FILE_TTL_HOURS`
> row in its variable table describe this as "hours after *last use*". That is
> not what the code does: `expires_at` is computed once as `created_at + ttl`
> ([core/storage.py:196](../core/storage.py#L196)), and `_touch` — called on
> every resolve — updates `last_used_at` but never extends `expires_at`
> ([core/storage.py:310](../core/storage.py#L310)). Treat the TTL as
> **time-since-creation** and size it accordingly: a handle that is used
> constantly still expires. Either document that as intended, or make `_touch`
> push `expires_at` forward if sliding expiry was the goal.

> Unset (the default) means nothing ever expires, so a `file_uuid` keeps working
> indefinitely. That is the safer default for a service whose callers may hold a
> handle for a long time; leaving it unset costs only a tiny amount of
> `registry.db` growth, since the cloud bytes are retained regardless (see the
> box above).

## Logging

| Variable | Default | Read by |
| --- | --- | --- |
| `LOG_LEVEL` | `INFO` | [mcp_server.py:28](../mcp_server.py#L28) |

Standard Python logging level names, resolved with
`getattr(logging, level, logging.INFO)`. ⚠️ **The name must be uppercase**:
`DEBUG` works, `debug` silently falls back to `INFO`, which can look like the
variable was ignored.

## Build-time only

These affect the image build, not the running server.

| Variable | Default | Location |
| --- | --- | --- |
| `PYTHON_IMAGE` | `python:3.10-slim` | [Dockerfile.Linux:19](../Dockerfile.Linux#L19) (declared as an `ARG`) |
| `PIP_INDEX_URL` | `https://pypi.tuna.tsinghua.edu.cn/simple` | [Dockerfile.Linux:30](../Dockerfile.Linux#L30) (declared as an `ARG`) |
| `PIP_NO_CACHE_DIR`, `PYTHONDONTWRITEBYTECODE`, `PYTHONUNBUFFERED` | Set in the image | [Dockerfile.Linux](../Dockerfile.Linux) |

Both are build arguments, so they only affect the builder — not the running
container. Pass them when neither Docker Hub nor PyPI is reachable from the
build host:

```bash
docker build -f Dockerfile.Linux \
  --build-arg PYTHON_IMAGE=internal.registry/mirror/python:3.10-slim \
  --build-arg PIP_INDEX_URL=https://pypi.org/simple \
  -t aspose-cells-cloud-mcp .
```

## Framework (FastMCP) variables

Not read by this codebase, but they change how the server starts. Both images
pre-set `FASTMCP_CHECK_FOR_UPDATES=off`.

| Variable | Default | Effect |
| --- | --- | --- |
| `FASTMCP_CHECK_FOR_UPDATES` | `stable` (FastMCP's own default) | `stable` \| `prerelease` \| `off`. **At `stable` the server calls `https://pypi.org/pypi/fastmcp/json` on startup** to print a "new version available" banner. On a cluster without egress to PyPI this delays or fails startup for no benefit, so the images set it to `off`. Note the value is the literal `off` — not `0` or `false`. |
| `FASTMCP_SHOW_SERVER_BANNER` | `true` | Set to `false` to suppress the ASCII startup banner in logs. Cosmetic only. |

## Removed — do not set

| Variable | Status |
| --- | --- |
| `MCP_AUTH_TOKEN`, `MCP_AUTH_ENFORCE` | Removed. HTTP endpoints are served anonymously now, so no bearer token is required. A leftover `auth-token` key in a Secret is ignored, and [tests/test_manifests.py:46](../tests/test_manifests.py#L46) asserts the manifests never wire these again. |

## Test and CI only

Not read by the server. Listed because the naming differs from the runtime
variables and mixing them up is easy — setting `CellsCloudClientId` inside a Pod
has no effect.

| Variable | Used by |
| --- | --- |
| `CellsCloudApiBaseUrl`, `CellsCloudClientId`, `CellsCloudClientSecret` | GitLab CI job variables ([.gitlab-ci.yml](../.gitlab-ci.yml)), mapped to the `ASPOSE_CLOUD_*` names by the integration tests |
| `ASPOSE_TEST_DATA_DIR` | Overrides the sample-workbook directory for integration tests |
| `SPREADSHEET_DATA_DIR` | Set by [tests/conftest.py](../tests/conftest.py) |
| `NO_PROXY` / `no_proxy` | Extended by the HTTP/Docker tests so loopback bypasses a local proxy |

## Examples

### Kubernetes

The manifests in [configuration/prod](../configuration/prod) and
[configuration/qa](../configuration/qa) wire the following:

```yaml
env:
  - name: MCP_TRANSPORT
    value: streamable-http
  - name: MCP_PATH
    value: /cells/mcp
  # registry.db lives here; must be a writable, mounted volume.
  - name: MCP_STATE_DIR
    value: C:\state            # Windows nodes; use /var/lib/cells-mcp on Linux
  # Credentials from a Secret — never inline values.
  - name: ASPOSE_CLOUD_CLIENT_ID
    valueFrom:
      secretKeyRef:
        name: cells-cloud-mcp-credentials
        key: client-id
  - name: ASPOSE_CLOUD_CLIENT_SECRET
    valueFrom:
      secretKeyRef:
        name: cells-cloud-mcp-credentials
        key: client-secret
```

Create the Secret first (see [configuration/README.md](../configuration/README.md)):

```bash
kubectl -n cells create secret generic cells-cloud-mcp-credentials \
  --from-literal=client-id=<CLIENT_ID> \
  --from-literal=client-secret=<CLIENT_SECRET>
```

`MCP_HOST` and `MCP_PORT` are intentionally omitted: the defaults (`0.0.0.0`,
`8080`) already match the container's port and the Service's `targetPort`.

`MCP_FILE_TTL_HOURS` is set to `"24"` in **qa only**, to exercise the expiry
path; it is deliberately commented out in **prod**, where expiring a handle buys
no storage back and only breaks long-lived workflows. If you enable it anywhere,
note the value must be quoted — Kubernetes rejects a bare integer for an env
value.

### Docker

```bash
docker run -d --name cells-mcp -p 8080:8080 \
  -e MCP_TRANSPORT=streamable-http \
  -e MCP_PATH=/mcp \
  -e MCP_STATE_DIR=/state \
  -v cells-mcp-state:/state \
  -e ASPOSE_CLOUD_CLIENT_ID=xxxxxx \
  -e ASPOSE_CLOUD_CLIENT_SECRET=yyyyyy \
  aspose-cells-cloud-mcp
# MCP endpoint http://localhost:8080/mcp, health check at /health
```

### stdio

Only the credentials are needed; every other variable keeps its default:

```bash
export ASPOSE_CLOUD_CLIENT_ID=xxxxxx
export ASPOSE_CLOUD_CLIENT_SECRET=yyyyyy
aspose-cells-cloud-mcp
```

## Quick summary

- **Required:** `ASPOSE_CLOUD_CLIENT_ID`, `ASPOSE_CLOUD_CLIENT_SECRET`.
- **Required in containers:** `MCP_STATE_DIR` (on a writable volume — an
  `emptyDir` invalidates every issued `file_uuid` when the pod is recreated).
- **Considered but not recommended by default:** `MCP_FILE_TTL_HOURS`. It only
  expires handles; it frees no cloud storage, so leave it unset unless you
  specifically want to bound `registry.db` growth.
- **Set when needed:** `ASPOSE_CLOUD_API_URL` (non-default endpoint),
  `MCP_CLOUD_TIMEOUT_SECONDS` (non-default bound).
- **Everything else has a working default.**
