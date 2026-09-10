"""HTTP client for Dynatrace API."""
from __future__ import annotations
import httpx
from typing import Any, Optional

DEFAULT_BASE = "https://api.dynatrace.com"

class DynatraceClient:
    def __init__(self, api_key: str, base_url: str = ""):
        self.api_key = api_key.strip()
        self.base_url = (base_url.strip() if base_url else DEFAULT_BASE).rstrip("/")
        
        # Determine Authorization format:
        # For api.dynatrace.com (Account Management / Environments), OAuth Bearer token is used.
        # For dedicated tenant environments (*.live.dynatrace.com), Api-Token header is standard.
        if "live.dynatrace.com" in self.base_url or "/api/v2" in self.base_url:
            auth_val = f"Api-Token {self.api_key}" if not self.api_key.startswith(("Api-Token ", "Bearer ")) else self.api_key
        else:
            auth_val = f"Bearer {self.api_key}" if not self.api_key.startswith(("Bearer ", "Api-Token ")) else self.api_key

        self.headers = {
            "Authorization": auth_val,
            "Content-Type": "application/json",
            "User-Agent": "Imperal-Dynatrace-Connector/1.0.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def verify_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                if "api.dynatrace.com" in self.base_url:
                    resp = await client.get(f"{self.base_url}/env/v1/environments", headers=self.headers)
                else:
                    resp = await client.get(f"{self.base_url}/metrics", headers=self.headers)
                if resp.status_code in (200, 201, 204):
                    return {"status": "ok", "data": resp.json() if resp.content else {}}
                return {"status": "error", "error": f"HTTP {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"status": "error", "error": str(e)}

    async def list_metrics(self, limit: int = 20) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}/metrics" if "/api/v2" in self.base_url else f"{self.base_url}/v2/metrics"
            resp = await client.get(url, headers=self.headers, params={"limit": limit})
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list): return data
                for k in ["data", "metrics", "items", "results"]:
                    if k in data and isinstance(data[k], list): return data[k]
                return []
            return []

    async def get_metric(self, metric_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}/metrics/{metric_id}" if "/api/v2" in self.base_url else f"{self.base_url}/v2/metrics/{metric_id}"
            resp = await client.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            raise ValueError(f"HTTP {resp.status_code}: {resp.text}")
