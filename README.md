# OSINT Evidence Engine

Portfolio ID: osint-evidence  
Maturity: scaffolded evidence-manifest and integrity-verification library.

Preserve provenance metadata, content digests, timestamps, source references and deterministic chain-of-custody records for authorized public-information artifacts.

## Safety boundary

This scaffold hashes caller-supplied bytes and validates evidence metadata and event-chain integrity. It does not fetch, collect, persist, encrypt, sign, timestamp with a trusted authority, or make evidence tamper-proof. SHA-256 detects byte mismatch only when the expected digest is independently trusted.

The initial profile accepts only public, non-personal evidence with a current source review, bounded size and retention, and required collection, identity, policy, emergency-stop, compliance and audit references. Personal or sensitive data is rejected. Legal holds are not implemented.

## Quick start

Python 3.10+:

    python -m pip install -r requirements-dev.txt
    python -m unittest discover -s tests -v

See docs/EVIDENCE-CONTRACT.md, docs/THREAT-MODEL.md and docs/INTEGRATION-GATES.md.

## No chain-of-custody claim

A locally computed hash chain is not a digital signature, trusted timestamp, immutable/WORM storage, proof of source authenticity, proof of truth, or legal chain-of-custody certification. Production use requires authenticated ingestion, signed checkpoints, external anchoring, private storage, access controls, retention/legal-hold operations and independent review.

## Licensing

This repository follows the ecosystem's scoped mixed-license policy: original source code and machine-readable contracts are designated Apache-2.0; original human-readable documentation is designated CC BY 4.0. Third-party material retains upstream terms. Datasets, evidence, fixtures, sample payloads, media, and material with uncertain provenance are not blanket-licensed. File-level provenance and redistribution-rights review remains required before release. See [LICENSE.md](LICENSE.md).
