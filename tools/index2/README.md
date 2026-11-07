# Index2 verification tools

Run these from `D:\hacomv2-2026`. The finished page does not need Python or a build step.

```powershell
python tools/index2/final-index2-audit.py
python tools/index2/inspect-index2-results.py
python tools/index2/write-index2-report.py
```

Static checks use `html5lib`; screenshot processing uses Pillow. Install them only when rerunning verification:

```powershell
python -m pip install html5lib Pillow
```

For browser checks, serve the workspace on `127.0.0.1:8765`, then run the saved MCP command batches:

```powershell
python tools/index2/chrome-mcp-check.py reference/index2-matrix-commands.json reference/index2-matrix-results.json
python tools/index2/chrome-mcp-check.py reference/index2-interaction-commands.json reference/index2-interaction-results.json
python tools/index2/chrome-mcp-check.py reference/index2-keyboard-commands.json reference/index2-keyboard-results.json
python tools/index2/chrome-mcp-check.py reference/index2-lighthouse-commands.json reference/index2-lighthouse-results.json
```

The recovery client starts Chrome DevTools MCP exclusively through `C:\Users\ADMIN\.codex\scripts\start-chrome-devtools-mcp.ps1`. It resolves the exact task-owned URL before every operation; MCP page IDs are never reused across connections. It does not connect to personal Chrome or use another browser automation backend.

The original page lazy-loads SVG scripts. The comparison harness disconnects its observer and prevents duplicate registration while loading all reference sections; this avoids testing stale, detached SVG instances. It changes only the test tab, never original files.

`build-index2.py` at the workspace root rebuilds native HTML and typography tokens from the measured JSON fixtures. Existing WebP assets are reused; small vector artwork is rebuilt from the graphics-only fixtures. Core CSS before the generated typography marker is preserved. New snapshots should only be captured after the original design is deliberately changed.

Full-page capture of the reference can stall Chrome's compositor. Capture mobile sections in 1080px tiles using the saved command fixtures or the capture helpers. Use a fresh task-owned tab for visual capture after Lighthouse. Keep before/after viewports, device scale factor and font readiness identical.

## Native header correction

The current acceptance report is `HEADER-HTML-AUDIT.md`; the earlier `INDEX2-AUDIT.md` is a historical baseline. Run `python tools/index2/audit-header.py` after the saved header checks to rebuild its current visual diff and scoped report.

`build-index2.py` calls `normalize-header.py` (authoring dependency: beautifulsoup4). Native component CSS lives in `index2.css` before the generated typography marker. `prepare-header-art.py` uses opencv-python-headless/numpy only to prepare the clean local hero artwork; it is not needed to view the page or rebuild HTML with existing assets.

`header-decoration.webp` is a lossless Chrome-rendered cache of the graphics-only header SVG. A SHA-256 file validates this cache; if the SVG changes, the generator uses the SVG until the cache is rebuilt through the managed Chrome MCP canvas command in `reference/header-raster-commands.json`. No original assets are changed. The cleaned hero source intentionally contains no advertising copy; native HTML supplies every inventoried hero string.

The MCP recovery client can save tool image blocks in memory (`_saveImage`) when the MCP process workspace does not allow direct screenshot output paths. `_clickLabel` resolves a current snapshot UID within the same client before an actual MCP click. Neither path uses a separate automation backend.
