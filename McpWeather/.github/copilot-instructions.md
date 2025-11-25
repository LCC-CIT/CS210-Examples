# Copilot Instructions: MCP Weather Server

This repo hosts a local Model Context Protocol (MCP) weather server and integration notes for desktop LLMs. If the repo is empty, use the quick start to scaffold and then re-scan.

## Prerequisites
- Python 3.10 or higher
- Client (choose one):
  - Claude Desktop app installed
  - Visual Studio Code with GitHub Copilot extension installed and an active Copilot subscription

## Quick Start (macOS, zsh)
- Create project env:
  ```sh
  python -m venv venv
  source venv/bin/activate
  pip install mcp
  ```
- Expected entry: `server.py` using `mcp.server.stdio.stdio_server` and tools `get-forecast`, `get-alerts`.
- Keep tool inputs simple JSON schemas (type: object, properties, required).

## Server Structure (Python)
- `server.py`: initialize `Server("weather-server")`; register tools via `@server.list_tools()` and `@server.call_tool()`; run with `asyncio.run(main())`.
- Tools:
  - `get-forecast(latitude:number, longitude:number)` → returns text forecast.
  - `get-alerts(state:string)` → returns text alerts summary.
- Capabilities: use `server.get_capabilities(NotificationOptions())` for stdio MCP.

## Claude Desktop Wiring
- Config file (create if missing):
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Minimal config:
  ```json
  {
    "mcpServers": {
      "weather-server": {
        "command": "/ABSOLUTE/PATH/TO/McpWeather/venv/bin/python",
        "args": ["/ABSOLUTE/PATH/TO/McpWeather/server.py"]
      }
    }
  }
  ```
- Use absolute path to `venv/bin/python` (not system python). Restart Claude Desktop after changes.

## VS Code (GitHub Copilot) Wiring
- Create project config:
  - In your project folder, create `.vscode/mcp.json`.
- Minimal config:
  ```json
  {
    "servers": {
      "weather-server": {
        "command": "/ABSOLUTE/PATH/TO/McpWeather/venv/bin/python",
        "args": ["/ABSOLUTE/PATH/TO/McpWeather/server.py"]
      }
    }
  }
  ```
- Use absolute paths; on Windows use double backslashes `\\` in JSON.

## Test & Troubleshoot
- In Claude, look for the plug icon and tools `get-forecast`, `get-alerts`.
- Sample prompt: "What is the weather at lat 40.7, long -74.0?"
- Logs: macOS `~/Library/Logs/Claude/mcp.log`.
- If tools missing: verify JSON paths and `venv` activation; ensure `mcp` is installed.
 - VS Code: no global MCP log; check Copilot Chat output and your server's terminal logs (stdout/stderr).

## Testing in VS Code Copilot
- Reload VS Code: `Cmd+Shift+P` → "Reload Window".
- Open Copilot Chat: click the Chat icon in the sidebar.
- Check for tools: look for a paperclip icon or Agent/Tools dropdown; `weather-server` should be listed.
- Ask: "What is the weather like at lat 40.7, long -74.0?". Copilot will detect tool use, run `server.py`, and show the result.

## Patterns & Conventions
- Separation: plain Python functions for logic; thin MCP handlers mapping input → output.
- Config: prefer `.env` for any optional keys; do not hardcode secrets.
- Networking: add timeouts/backoff; respect `Retry-After` on 429. Keep concurrency low.
- Units: standardize output (°F/°C), and surface location/timezone consistently.
 - Timezone: NWS `periods[]` include `startTime`/`endTime`; if including timestamps, format with the correct timezone.

## Repo Pointers
- Place `server.py` at repo root or `src/`; keep `venv/` excluded from commits.
- Add `README.md` with run commands and tool descriptions once code exists.

## API: National Weather Service (api.weather.gov)
- Base: `https://api.weather.gov` (no API key required). Set headers:
  - `User-Agent`: identify app and contact (e.g., `weather-mcp (contact: you@example.com)`).
  - `Accept`: `application/geo+json`.
- Forecast flow (`get-forecast`):
  1. `GET /points/{lat},{lon}` → read `properties.forecast` URL.
  2. `GET {forecastUrl}` → use `properties.periods[]` for name, temperature, temperatureUnit, windSpeed, shortForecast.
  3. Return a concise text summary for the next period (or today), include units and timezone.
- Alerts flow (`get-alerts`):
  - `GET /alerts?area={STATE}&status=actual&message_type=alert`.
  - Summarize `features[].properties.event`, `headline`, `severity`, and `instruction`.
- Error handling:
  - Map 404/400 from `/points` to: "Location not covered. Check coordinates.".
  - On 429/5xx: retry with exponential backoff (e.g., 1s, 2s, 4s; cap ~15s); respect `Retry-After`.
- Caching:
  - Cache `/points` and forecast responses for ~10 minutes to reduce load.
  - Cache alerts for ~2 minutes; alerts are time-sensitive.

## Tool I/O Contracts (NWS)
- `get-forecast` input:
  ```json
  { "latitude": 40.7, "longitude": -74.0 }
  ```
  Output: single text string summarizing the next forecast period.
- `get-alerts` input:
  ```json
  { "state": "NY" }
  ```
  Output: single text string summarizing active alerts; if none, "No active weather alerts for NY.".

---
When code is added, I will re-scan and expand commands and file references (build, tests, adapters, domain models). Share your intended API (NWS/OpenWeather) and directory layout to refine this doc.