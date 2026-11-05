# Integration Gates Before Production Evidence Handling

1. Verify source approval and terms with osint-source-registry and osint-collection.
2. Authenticate collector, reviewer and downstream actor identities.
3. Verify policy decision and emergency-stop state at ingestion and export.
4. Obtain compliance/privacy review and classify the payload; deny personal or sensitive data in the initial profile.
5. Use a private encrypted evidence store with access control, retention, deletion and legal-hold workflow.
6. Anchor signed chain checkpoints outside the storage administrator's control.
7. Integrate audit-provenance for attributable events and secure-supply-chain for artifact/build provenance.
8. Validate content types, malware scan, size, parser isolation and transformation reproducibility.
9. Test truncation, replay, hash mismatch, chain reorder, clock skew, storage corruption and unauthorized access.
10. Obtain independent security and legal review before asserting evidentiary or chain-of-custody sufficiency.

A successful local hash verification is not proof of authenticity, truth or legal sufficiency.
