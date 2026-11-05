# Agent instructions

- Hashes prove byte consistency only; never claim authenticity, truth, non-repudiation, trusted time or legal chain of custody.
- Do not add network collection, source retrieval, storage backends, encryption, signatures or WORM claims without a separate reviewed design.
- Initial profile accepts public non-personal artifacts only; reject personal or sensitive data.
- Require source, collection, policy, identity, emergency-stop, compliance and audit references.
- Enforce size and retention ceilings; never increase source-declared retention.
- Never fabricate evidence, timestamps, reviewer identities, approvals, signatures or provenance references.
- Do not store real OSINT content, personal data, credentials or confidential incident records in this public repository.
- Treat chain events as metadata; do not embed sensitive details.
- Run python -m unittest discover -s tests -v before committing.
