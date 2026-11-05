# Contributing

Contributions may improve evidence manifest validation, deterministic hashing, chain verification, documentation and synthetic tests. Any storage, signing, collection, encryption or legal-hold integration requires a separate threat model and architecture decision.

## Development

- Python 3.10+
- Install: python -m pip install -r requirements-dev.txt
- Test: python -m unittest discover -s tests -v

Changes to digest canonicalization, event ordering, source references, retention or data classification require positive, negative and boundary tests. Never commit real evidence payloads or personal data.
