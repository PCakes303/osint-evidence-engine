import hashlib
import unittest
from datetime import datetime, timedelta, timezone
from osint_evidence.records import EvidenceError, build_manifest, validate_manifest, verify_artifact
from tests.helpers import metadata

class EvidenceRecordTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(timezone.utc)
        self.content = b'{"synthetic":true,"records":3}'
        self.meta = metadata(self.now)

    def test_builds_content_addressed_manifest(self):
        manifest = build_manifest(self.content, self.meta, now=self.now)
        digest = hashlib.sha256(self.content).hexdigest()
        self.assertEqual(manifest["content_sha256"], digest)
        self.assertEqual(manifest["evidence_id"], "sha256:" + digest)
        self.assertEqual(manifest["content_size"], len(self.content))
        self.assertEqual(manifest["state"], "captured")

    def test_artifact_digest_verifies(self):
        manifest = build_manifest(self.content, self.meta, now=self.now)
        self.assertTrue(verify_artifact(self.content, manifest))
        self.assertFalse(verify_artifact(b"tampered", manifest))

    def test_manifest_id_must_match_digest(self):
        manifest = build_manifest(self.content, self.meta, now=self.now)
        manifest["evidence_id"] = "sha256:" + ("0"*64)
        with self.assertRaisesRegex(EvidenceError, "derived"):
            validate_manifest(manifest)

    def test_personal_data_is_rejected(self):
        meta = dict(self.meta)
        meta["data_classification"] = "personal"
        with self.assertRaises(EvidenceError):
            build_manifest(self.content, meta, now=self.now)

    def test_legal_hold_is_rejected_without_hold_workflow(self):
        meta = dict(self.meta)
        meta["legal_hold"] = True
        with self.assertRaises(EvidenceError):
            build_manifest(self.content, meta, now=self.now)

    def test_payload_size_is_bounded(self):
        with self.assertRaisesRegex(EvidenceError, "10 MiB"):
            build_manifest(b"x" * (10_485_761), self.meta, now=self.now)

    def test_unknown_metadata_fields_rejected(self):
        meta = dict(self.meta)
        meta["unreviewed_field"] = "secret"
        with self.assertRaisesRegex(EvidenceError, "fields mismatch"):
            build_manifest(self.content, meta, now=self.now)

    def test_future_acquisition_time_rejected(self):
        meta = dict(self.meta)
        meta["acquired_at"] = (self.now+timedelta(minutes=2)).isoformat()
        with self.assertRaisesRegex(EvidenceError, "future"):
            build_manifest(self.content, meta, now=self.now)

    def test_naive_acquisition_time_rejected(self):
        meta = dict(self.meta)
        meta["acquired_at"] = self.now.replace(tzinfo=None).isoformat()
        with self.assertRaises(EvidenceError):
            build_manifest(self.content, meta, now=self.now)

    def test_embedded_credentials_in_source_url_rejected(self):
        meta = dict(self.meta)
        meta["source_url"] = "https://user:secret@example.org/"
        with self.assertRaisesRegex(EvidenceError, "HTTPS"):
            build_manifest(self.content, meta, now=self.now)

    def test_retention_is_bounded(self):
        meta = dict(self.meta)
        meta["retention_days"] = 366
        with self.assertRaises(EvidenceError):
            build_manifest(self.content, meta, now=self.now)

    def test_empty_or_invalid_source_license_rejected(self):
        meta = dict(self.meta)
        meta["source_license"] = ""
        with self.assertRaises(EvidenceError):
            build_manifest(self.content, meta, now=self.now)

if __name__ == "__main__":
    unittest.main()
