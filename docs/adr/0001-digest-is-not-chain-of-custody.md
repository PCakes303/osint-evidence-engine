# ADR 0001: Digest integrity is not legal chain of custody

- Status: accepted
- Date: 2026-11-02

## Context

Evidence systems need reproducible integrity metadata, but local hashes alone do not authenticate sources, actors, timestamps or storage administrators.

## Decision

The first implementation creates content-addressed manifests and deterministic hash-linked event metadata only. It does not persist content, sign events, anchor checkpoints, provide trusted timestamps, encrypt evidence or manage legal holds. The initial public profile rejects personal/sensitive data.

## Consequences

- Hashes are integrity links, not signatures or proof of truth.
- Production use requires private storage, identity, audit, compliance, emergency-stop, retention and external checkpoint integrations.
- No legal chain-of-custody claim is permitted.
