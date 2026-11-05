# Evidence Manifest and Provenance Contract v1.0

## Manifest

A manifest describes caller-supplied bytes using a content SHA-256 digest, byte size, content type, source reference, acquisition timestamp, source license, collection request, identity/policy/emergency/compliance/audit references, data classification and retention limit.

The evidence ID is derived as sha256:<content digest>. The library does not persist the payload. The caller must keep bytes in a separate private, access-controlled evidence store.

## Initial profile

- Public, non-personal data only.
- HTTPS source URLs without embedded credentials.
- Source and collection references must be supplied by upstream reviewed components.
- Maximum payload size: 10 MiB.
- Retention ceiling: 365 days and never above the source-declared ceiling.
- Legal hold is not supported; manifests with legal_hold=true are rejected.
- No personal/sensitive data, secrets or confidential incident material in public repository fixtures.

## Chain-of-custody metadata

Events contain event ID, timestamp, event type, actor ID, digest of event details, previous event hash and current event hash. Canonical JSON with sorted keys and compact separators is SHA-256 hashed. Events are ordered, IDs unique, timestamps monotonic and previous hashes linked.

Details are hashed, not embedded. Actor IDs and timestamps are claims until authenticated by external identity and trusted timestamp services.

## Integrity semantics

- Artifact digest detects byte changes relative to a trusted manifest.
- Event-chain verification detects changed, reordered or duplicated events within the supplied chain.
- A hash chain does not prevent truncation unless a trusted checkpoint is anchored independently.
- A hash chain is not a signature, trusted timestamp, source authenticity proof, proof of truth, immutable storage guarantee or legal chain-of-custody certification.
