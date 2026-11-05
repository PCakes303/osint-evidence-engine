# Staging Status — osint-evidence-engine

- Portfolio ID: osint-evidence
- Canonical registry position: 22 of 32 (21st component; master is position 1)
- GitHub owner: PCakes303
- Intended visibility: public
- Remote repository: https://github.com/PCakes303/osint-evidence-engine (public; main).
- Staging state: deployed; all 25 staged paths match the public remote by path and Git blob SHA.
- Maturity: evidence manifest and hash-chain validation only; no storage.
- License: scoped mixed-license policy included in staged LICENSE.md; file-level provenance clearance remains required.
- Dependencies: osint-collection, audit-provenance, secure-supply-chain, emergency-control, compliance-governance (declared only).
- Implemented in this staging packet: Draft 2020-12 evidence manifest and chain schemas; content SHA-256 manifest builder/verifier; deterministic hash-linked event chain; synthetic tests; Python 3.10–3.12 CI.
- Not implemented: source collection, durable storage, encryption, signatures, trusted timestamps, external checkpoint anchoring, retention service, legal holds, personal-data processing or legal chain-of-custody certification.
- Remote CI: https://github.com/PCakes303/osint-evidence-engine/actions/runs/41989265888 passed on Python 3.10, 3.11 and 3.12 (21 tests).
- Deployment verification: 25/25 paths and blob SHAs match master staging; remote CI is green on all three Python versions.
- Required before production: satisfy every gate in docs/INTEGRATION-GATES.md, including authenticated provenance, trusted timestamping, storage, retention and independent legal/evidence review.
