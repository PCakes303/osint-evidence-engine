# Security Policy

This repository hashes caller-supplied bytes and validates public evidence metadata. It does not collect, persist, encrypt, sign, timestamp with a trusted authority or provide tamper-proof storage.

## Reporting

Do not publish exploitable vulnerability details, credentials, personal data or confidential evidence in public issues. Use GitHub private vulnerability reporting or a private security advisory only if enabled for this repository. No dedicated private reporting address is published here; configure an owner-approved private channel if GitHub private reporting is unavailable.

## Security invariants

- Reject personal and sensitive evidence in the initial public profile.
- Bound payload size and retention.
- Verify every digest and chain link before relying on it.
- Treat actor IDs, source metadata and references as untrusted until authenticated by external systems.
- Hash chains are not signatures or trusted timestamps.
- Keep actual evidence in private, access-controlled storage outside this public repository.
