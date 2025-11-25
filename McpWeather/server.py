import asyncio
import time
from typing import Any, Dict, Optional, Tuple

import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

# --- Config ---
USER_AGENT = "weather-mcp (contact: you@example.com)"
ACCEPT_HEADER = "application/geo+json"
POINTS_TTL_SECONDS = 600  # 10 minutes
FORECAST_TTL_SECONDS = 600  # 10 minutes
ALERTS_TTL_SECONDS = 120  # 2 minutes
MAX_BACKOFF_SECONDS = 15

# --- HTTP Client ---
client: Optional[httpx.AsyncClient] = None

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": ACCEPT_HEADER,
}

# --- Caches ---
_points_cache: Dict[Tuple[float, float], Tuple[float, Dict[str, Any]]] = {}
_forecast_cache: Dict[Tuple[float, float], Tuple[float, Dict[str, Any]]] = {}
_alerts_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}


def _cache_get(cache: Dict, key: Any, ttl_seconds: int) -> Optional[Dict[str, Any]]:
    now = time.monotonic()
    entry = cache.get(key)
    if not entry:
        return None
    ts, data = entry
    if now - ts <= ttl_seconds:
        return data
    # expired
    cache.pop(key, None)
    return None


def _cache_set(cache: Dict, key: Any, data: Dict[str, Any]) -> None:
    cache[key] = (time.monotonic(), data)


async def _fetch_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    assert client is not None
    backoff = 1.0
    while True:
        try:
            resp = await client.get(url, params=params, headers=HEADERS)
            if resp.status_code in (429, 500, 502, 503, 504):
                retry_after = resp.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait = float(retry_after)
                    except ValueError:
                        wait = backoff
                else:
                    wait = backoff
                if wait > MAX_BACKOFF_SECONDS:
                    wait = MAX_BACKOFF_SECONDS
                await asyncio.sleep(wait)
                backoff = min(backoff * 2, MAX_BACKOFF_SECONDS)
                continue
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            # Propagate 404/400 specifically for points mapping
            raise
        except httpx.HTTPError:
            # transient network errors: backoff
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, MAX_BACKOFF_SECONDS)


# --- NWS Logic ---
async def nws_points(latitude: float, longitude: float) -> Dict[str, Any]:
    key = (latitude, longitude)
    cached = _cache_get(_points_cache, key, POINTS_TTL_SECONDS)
    if cached:
        return cached
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    data = await _fetch_json(url)
    _cache_set(_points_cache, key, data)
    return data


async def nws_forecast(latitude: float, longitude: float) -> Dict[str, Any]:
    key = (latitude, longitude)
    cached = _cache_get(_forecast_cache, key, FORECAST_TTL_SECONDS)
    if cached:
        return cached
    points = await nws_points(latitude, longitude)
    forecast_url = points.get("properties", {}).get("forecast")
    if not forecast_url:
        raise httpx.HTTPStatusError("Forecast URL not found", request=None, response=None)
    forecast = await _fetch_json(forecast_url)
    _cache_set(_forecast_cache, key, forecast)
    return forecast


async def nws_alerts(state: str) -> Dict[str, Any]:
    cached = _cache_get(_alerts_cache, state, ALERTS_TTL_SECONDS)
    if cached:
        return cached
    url = "https://api.weather.gov/alerts"
    params = {
        "area": state,
        "status": "actual",
        "message_type": "alert",
    }
    alerts = await _fetch_json(url, params=params)
    _cache_set(_alerts_cache, state, alerts)
    return alerts


async def get_forecast(latitude: float, longitude: float) -> str:
    try:
        forecast = await nws_forecast(latitude, longitude)
        periods = forecast.get("properties", {}).get("periods", [])
        if not periods:
            return "No forecast data available for the location."
        p = periods[0]
        name = p.get("name")
        temp = p.get("temperature")
        unit = p.get("temperatureUnit") or ""
        wind = p.get("windSpeed") or ""
        short = p.get("shortForecast") or ""
        # timezone hint from points
        points = await nws_points(latitude, longitude)
        tz = points.get("properties", {}).get("timeZone")
        tz_hint = f" ({tz})" if tz else ""
        return f"{name}: {short}. Temp {temp}°{unit}, Wind {wind}{tz_hint}."
    except httpx.HTTPStatusError as e:
        # If points returned 404/400, map to friendly message
        return "Location not covered. Check coordinates."
    except Exception:
        return "Unable to retrieve forecast at this time. Please try again later."


async def get_alerts(state: str) -> str:
    try:
        alerts = await nws_alerts(state)
        features = alerts.get("features", [])
        if not features:
            return f"No active weather alerts for {state}."
        # Summarize top 1-2 alerts
        summaries = []
        for feat in features[:2]:
            props = feat.get("properties", {})
            event = props.get("event")
            headline = props.get("headline")
            severity = props.get("severity")
            instruction = props.get("instruction")
            part = ", ".join(
                x for x in [event, f"Severity: {severity}" if severity else None] if x
            )
            if headline:
                part = f"{headline} — {part}" if part else headline
            if instruction:
                part = f"{part}. {instruction}" if part else instruction
            summaries.append(part)
        return " \n".join(summaries)
    except Exception:
        return f"Unable to retrieve alerts for {state} at this time."


# --- MCP Server ---
server = Server("weather-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get-forecast",
            description="Get weather forecast for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
            },
        ),
        types.Tool(
            name="get-alerts",
            description="Get weather alerts for a U.S. state",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "Two-letter state code (e.g. CA, NY)",
                    },
                },
                "required": ["state"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]):
    if name == "get-forecast":
        lat = float(arguments["latitude"])  # type: ignore[index]
        lon = float(arguments["longitude"])  # type: ignore[index]
        text = await get_forecast(lat, lon)
        return [types.TextContent(type="text", text=text)]
    elif name == "get-alerts":
        state = str(arguments["state"])  # type: ignore[index]
        text = await get_alerts(state)
        return [types.TextContent(type="text", text=text)]
    raise ValueError(f"Unknown tool: {name}")


async def _init_http_client() -> None:
    global client
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0, connect=10.0),
        limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        headers=HEADERS,
    )


async def _close_http_client() -> None:
    global client
    if client is not None:
        await client.aclose()
        client = None


async def main():
    await _init_http_client()
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="weather",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    finally:
        await _close_http_client()


if __name__ == "__main__":
    asyncio.run(main())
