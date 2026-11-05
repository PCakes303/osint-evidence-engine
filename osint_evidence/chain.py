"""Deterministic hash-linked custody event metadata; not signatures or trusted timestamps."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker

from .records import EvidenceError, _canonical_json, _parse_time

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "evidence-chain.schema.json"
_SCHEMA = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
_VALIDATOR = Draft202012Validator(_SCHEMA, format_checker=FormatChecker())

def _event_hash(event: Mapping[str, Any]) -> str:
    value = {key: item for key, item in event.items() if key != "event_hash"}
    return hashlib.sha256(_canonical_json(value)).hexdigest()

def create_event(
    *, event_id: str, timestamp: str, event_type: str, actor_id: str,
    details: Mapping[str, Any], previous_hash: str | None = None
) -> dict[str, Any]:
    if not isinstance(details, Mapping):
        raise EvidenceError("event details must be an object")
    _parse_time(timestamp)
    details_hash = hashlib.sha256(_canonical_json(dict(details))).hexdigest()
    event = {
        "event_id":event_id,"timestamp":timestamp,"event_type":event_type,"actor_id":actor_id,
        "details_sha256":details_hash,"previous_hash":previous_hash,"event_hash":"",
    }
    event["event_hash"] = _event_hash(event)
    errors = list(_VALIDATOR.iter_errors({"chain_version":"1.0","events":[event]}))
    if errors:
        raise EvidenceError(f"chain event schema error: {errors[0].message}")
    return event

def verify_chain(events: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...]) -> bool:
    chain = {"chain_version":"1.0","events":list(events)}
    errors = list(_VALIDATOR.iter_errors(chain))
    if errors:
        raise EvidenceError(f"chain schema error: {errors[0].message}")
    seen: set[str] = set()
    previous_hash = None
    previous_time = None
    for event in chain["events"]:
        if event["event_id"] in seen:
            raise EvidenceError("duplicate event_id")
        seen.add(event["event_id"])
        timestamp = _parse_time(event["timestamp"])
        if previous_time is not None and timestamp < previous_time:
            raise EvidenceError("event timestamps are not monotonic")
        if event["previous_hash"] != previous_hash:
            raise EvidenceError("previous_hash does not match preceding event")
        if event["event_hash"] != _event_hash(event):
            raise EvidenceError("event hash mismatch")
        previous_hash = event["event_hash"]
        previous_time = timestamp
    return True

def append_event(
    events: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...], *,
    event_id: str, timestamp: str, event_type: str, actor_id: str, details: Mapping[str, Any]
) -> tuple[dict[str, Any], ...]:
    existing = tuple(dict(item) for item in events)
    verify_chain(existing)
    previous_hash = existing[-1]["event_hash"] if existing else None
    event = create_event(event_id=event_id,timestamp=timestamp,event_type=event_type,actor_id=actor_id,details=details,previous_hash=previous_hash)
    result = existing + (event,)
    verify_chain(result)
    return result
