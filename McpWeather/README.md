# MCP Weather Server

A local Model Context Protocol (MCP) server exposing simple weather tools backed by the National Weather Service (api.weather.gov).

## Tools

- `get-forecast(latitude:number, longitude:number)`: returns a concise forecast summary for the next period.
- `get-alerts(state:string)`: returns a summary of active alerts for a US state.

## Setup (macOS, zsh)

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## VS Code (GitHub Copilot) Wiring

Create `.vscode/mcp.json` (already included):

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

Reload VS Code window, open Copilot Chat, and verify `weather-server` tools.

## Claude Desktop Wiring (Optional)

Create `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

Restart Claude Desktop after changes.

### CLI (macOS)

```sh
mkdir -p ~/Library/"Application Support"/Claude
cat > ~/Library/"Application Support"/Claude/claude_desktop_config.json <<'JSON'
{
  "mcpServers": {
    "weather-server": {
      "command": "/ABSOLUTE/PATH/TO/McpWeather/venv/bin/python",
      "args": ["/ABSOLUTE/PATH/TO/McpWeather/server.py"]
    }
  }
}
JSON

# Optional: open in VS Code
code ~/Library/"Application Support"/Claude/claude_desktop_config.json
```

### CLI (Windows, PowerShell)

```powershell
$path = Join-Path $env:APPDATA "Claude"
New-Item -ItemType Directory -Force $path | Out-Null
$config = @'
{
  "mcpServers": {
    "weather-server": {
      "command": "C:\\ABSOLUTE\\PATH\\TO\\McpWeather\\venv\\Scripts\\python.exe",
      "args": ["C:\\ABSOLUTE\\PATH\\TO\\McpWeather\\server.py"]
    }
  }
}
'@
Set-Content -Path (Join-Path $path "claude_desktop_config.json") -Value $config -Encoding UTF8
```

## Test

- Forecast: "What is the weather at lat 40.7, long -74.0?"
- Alerts: "Any active weather alerts for NY?"

## Notes

- NWS requires `User-Agent` and recommends `Accept: application/geo+json`.
- Caching reduces load: 10m for points/forecast, 2m for alerts.
- Backoff for 429/5xx: 1s, 2s, 4s (cap ~15s), respect `Retry-After`.
