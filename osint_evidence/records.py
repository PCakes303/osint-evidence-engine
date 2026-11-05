"""Public, non-personal evidence manifest and digest validation; no storage is provided."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "evidence-manifest.schema.json"
_SCHEMA = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
_VALIDATOR = Draft202012Validator(_SCHEMA, format_checker=FormatChecker())
MAX_EVIDENCE_BYTES = 10_485_760
MAX_FUTURE_SKEW = timedelta(seconds=30)

class EvidenceError(ValueError):
    """Raised for invalid evidence metadata or artifact mismatch."""

def _canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as exc:
        raise EvidenceError("metadata is not canonical JSON") from exc

def _parse_time(value: Any) -> datetime:
    if not isinstance(value, str):
        raise EvidenceError("acquired_at must be a timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise EvidenceError("acquired_at is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise EvidenceError("acquired_at must include a timezone")
    return parsed.astimezone(timezone.utc)

def _https_url(value: Any) -> bool:
    if not isinstance(value, str) or len(value) > 2048 or any(ch.isspace() for ch in value):
        return False
    try:
        parts = urlsplit(value)
        parts.port
        return parts.scheme == "https" and bool(parts.hostname) and parts.username is None and parts.password is None
    except ValueError:
        return False

def validate_manifest(manifest: Mapping[str, Any]) -> None:
    errors = sorted(_VALIDATOR.iter_errors(manifest), key=lambda e: (list(e.absolute_path), e.message))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "<root>"
        raise EvidenceError(f"manifest schema error at {location}: {first.message}")
    if not _https_url(manifest["source_url"]):
        raise EvidenceError("source_url must be HTTPS without embedded credentials")
    if manifest["data_classification"] != "public" or manifest["legal_hold"] is not False:
        raise EvidenceError("initial evidence profile permits public data only and no legal-hold workflow")
    if manifest["evidence_id"] != "sha256:" + manifest["content_sha256"]:
        raise EvidenceError("evidence_id must be derived from content_sha256")

def build_manifest(content: bytes, metadata: Mapping[str, Any], *, now: datetime) -> dict[str, Any]:
    """Build a manifest from bytes and reviewed metadata; content is not stored."""
    if not isinstance(content, bytes):
        raise EvidenceError("content must be bytes")
    if len(content) > MAX_EVIDENCE_BYTES:
        raise EvidenceError("evidence exceeds the 10 MiB limit")
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise EvidenceError("now must be timezone-aware")
    required = {
        "source_id", "collection_request_id", "source_url", "acquired_at", "captured_by",
        "identity_authorization_ref", "policy_decision_ref", "emergency_state_ref",
        "compliance_review_ref", "audit_event_ref", "source_license", "data_classification",
        "content_type", "retention_days", "legal_hold",
    }
    missing = required - set(metadata)
    unknown = set(metadata) - required
    if missing or unknown:
        raise EvidenceError(f"metadata fields mismatch; missing={sorted(missing)}, unknown={sorted(unknown)}")
    acquired = _parse_time(metadata["acquired_at"])
    if acquired > now.astimezone(timezone.utc) + MAX_FUTURE_SKEW:
        raise EvidenceError("acquired_at is too far in the future")
    digest = hashlib.sha256(content).hexdigest()
    manifest = {
        "manifest_version":"1.0",
        "evidence_id":"sha256:" + digest,
        **dict(metadata),
        "content_sha256":digest,
        "content_size":len(content),
        "state":"captured",
    }
    validate_manifest(manifest)
    return manifest

def verify_artifact(content: bytes, manifest: Mapping[str, Any]) -> bool:
    """Verify byte digest and size. This does not authenticate the source or custodian."""
    validate_manifest(manifest)
    if not isinstance(content, bytes):
        raise EvidenceError("content must be bytes")
    digest = hashlib.sha256(content).hexdigest()
    return len(content) == manifest["content_size"] and digest == manifest["content_sha256"]
