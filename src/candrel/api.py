from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import requests


BASE_URL = "https://api.cellmodelpassports.sanger.ac.uk"


class ApiError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class CachedApi:
    def __init__(
        self,
        cache_dir: Path,
        timeout: float = 30.0,
        retries: int = 3,
        expected_hashes: dict[str, str] | None = None,
    ):
        self.cache_dir = cache_dir
        self.timeout = timeout
        self.retries = retries
        self.expected_hashes = expected_hashes or {}
        cache_dir.mkdir(parents=True, exist_ok=True)

    def _validate(self, path: Path, expected_name: str | None = None) -> None:
        expected = self.expected_hashes.get(expected_name or path.name)
        if expected is None:
            return
        observed = sha256_file(path)
        if observed != expected:
            raise ApiError(
                f"Input drift for {path.name}: expected {expected}, observed {observed}"
            )

    def get(self, path: str, params: dict[str, str], cache_key: str) -> tuple[dict[str, Any], Path]:
        target = self.cache_dir / f"{cache_key}.json"
        if target.exists():
            self._validate(target)
            return json.loads(target.read_text()), target

        error: Exception | None = None
        for attempt in range(self.retries):
            try:
                response = requests.get(
                    f"{BASE_URL}{path}", params=params, timeout=self.timeout
                )
                response.raise_for_status()
                payload = response.json()
                if payload.get("errors"):
                    raise ApiError(json.dumps(payload["errors"], sort_keys=True))
                temporary = target.with_suffix(".tmp")
                temporary.write_text(json.dumps(payload, sort_keys=True))
                self._validate(temporary, target.name)
                temporary.replace(target)
                return payload, target
            except (requests.RequestException, ValueError, ApiError) as exc:
                error = exc
                if attempt + 1 < self.retries:
                    time.sleep(2**attempt)
        raise ApiError(f"GET {path} failed after {self.retries} attempts: {error}")
