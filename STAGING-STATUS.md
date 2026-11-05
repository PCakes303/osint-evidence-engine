# Staging Status — osint-evidence-engine

- Portfolio ID: osint-evidence
- Canonical registry position: 22 of 32 (21st component; master is position 1)
- GitHub owner: PCakes303
- Intended visibility: public
- Remote repository: not yet created; the connected GitHub integration cannot create repositories.
- Staging state: initial scaffold prepared in the master repository; matrix validated.
- Maturity: evidence manifest and hash-chain validation only; no storage.
- License: scoped mixed-license policy included in staged LICENSE.md; file-level provenance clearance remains required.
- Dependencies: osint-collection, audit-provenance, secure-supply-chain, emergency-control, compliance-governance (declared only).
- Implemented in this staging packet: Draft 2020-12 evidence manifest and chain schemas; content SHA-256 manifest builder/verifier; deterministic hash-linked event chain; synthetic tests; Python 3.10–3.12 CI.
- Not implemented: source collection, durable storage, encryption, signatures, trusted timestamps, external checkpoint anchoring, retention service, legal holds, personal-data processing or legal chain-of-custody certification.
- Staging CI: master workflow run 41514862252 passed 21 tests on Python 3.10, 3.11 and 3.12.
- Required before remote deployment: owner creates public repository PCakes303/osint-evidence-engine, then the staging product files are pushed and repository CI verified.
- Required before production: satisfy every gate in docs/INTEGRATION-GATES.md.
