# capability-board

A single self-contained HTML page that probes the browser platform features a
modern Rust→WASM creative app depends on, and prints a pass / fail / warn matrix
with a one-line visual and the exact probe code for each.

No build, no dependencies, no network — open the file and it runs. We wrote it to
track, release by release, **when an engine becomes able to run our apps**, and it
turns out to be a handy cross-engine capability snapshot for anyone doing graphics,
storage or worker-heavy work on the web. It runs in a normal browser tab and
headless in [Servo](https://servo.org/)'s `servoshell`.

## What it probes (~32 checks)

- **GPU / canvas** — WebGPU (requestAdapter → device → render offscreen → pixel
  readback), WebGL2, WebGL1, Canvas2D, OffscreenCanvas
- **Storage** — OPFS (`navigator.storage.getDirectory`), a worker-side
  `FileSystemSyncAccessHandle` probe, IndexedDB, localStorage
- **Concurrency** — Web Workers, SharedArrayBuffer + Atomics, `crossOriginIsolated`,
  Web Locks, zero-copy `postMessage` transfer
- **Crypto / misc** — `crypto.subtle` (SHA-256), BroadcastChannel, structuredClone,
  pointer events + capture, ResizeObserver / IntersectionObserver / requestIdleCallback,
  `performance.now`

Each row shows status, a short result string, and the code it ran, so a failure is
self-documenting.

## Run it

**In a browser** — just open `capability-board.html`.

**With cross-origin isolation** (so the SharedArrayBuffer / threads probes are honest —
`file://` and a plain static server can't set the required headers):

```sh
python3 serve.py        # http://localhost:8000/capability-board.html
```

**Headless, e.g. in Servo:**

```sh
servoshell --headless \
  --pref dom_webgpu_enabled=true \
  --pref dom_webgl2_enabled=true \
  http://localhost:8000/capability-board.html
```

It prints `[CAPBOARD] <feature> = pass|fail|warn` lines and a final `DONE {…}` JSON
summary you can paste into a bug report.

## Recording runs over time (optional)

The page can POST each run's summary to a server and draw a score-over-time chart.
It's **off by default** and needs no server to be useful. To enable it, point the
page at an endpoint that accepts `POST` (store a run) and `GET` (list runs) at the
same path:

```
capability-board.html?server=https://your-host/endpoint&record=1
```

Without `?server=`, nothing is sent anywhere.

## Add a probe

Each check is one object in the `ATOMS` array near the top of the `<script>`:

```js
{ id:'webgpu', cat:'GPU / Canvas', label:'WebGPU',
  code:`navigator.gpu.requestAdapter()`,
  run: async () => (await navigator.gpu?.requestAdapter()) ? PASS('adapter') : FAIL('none') }
```

`run` returns `PASS(msg)`, `FAIL(msg)`, `WARN(msg)` or `SKIP(msg)`. Add an object,
reload — the matrix, the visual and the JSON summary pick it up automatically.
Contributions of new probes are welcome.

## License

Dual-licensed under either of [Apache-2.0](LICENSE-APACHE) or [MIT](LICENSE-MIT),
at your option.
