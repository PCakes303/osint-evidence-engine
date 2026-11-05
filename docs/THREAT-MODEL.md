# Threat Model

## Assets

- Evidence byte integrity and source provenance metadata.
- Acquisition and transformation event ordering.
- Privacy, confidentiality and retention of evidence payloads.
- Trustworthy references to collection, policy, identity, emergency, compliance and audit decisions.

## Threats and controls

| Threat | Reference control | Remaining requirement |
|---|---|---|
| Artifact modification | SHA-256 digest and size verification | Independently trusted manifest and protected storage |
| Event modification/reordering | Canonical hash chain and monotonic timestamps | Signed checkpoints and external anchoring |
| Chain truncation | Explicitly documented limitation | Independently retained checkpoint roots |
| False actor/source claim | Required external identity/source references | Cryptographic signatures and authenticated ingestion |
| Sensitive data leakage | Public-only data classification and no payload storage | Private encrypted evidence vault and access control |
| Retention overrun | Bounded retention field | Durable lifecycle/deletion/legal-hold service |
| Malformed/oversized evidence | Schema limits and 10 MiB ceiling | Streaming ingestion, quotas and malware scanning |
| Fabricated timestamp | Timezone validation only | Trusted timestamp service and authenticated source capture |

## Non-goals

No network collection, persistence, encryption, signing, trusted timestamping, legal hold, retention service, WORM storage or legal chain-of-custody certification is implemented.
