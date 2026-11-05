import unittest
from osint_evidence.chain import append_event, create_event, verify_chain
from osint_evidence.records import EvidenceError
from tests.helpers import event_time

class EvidenceChainTests(unittest.TestCase):
    def test_empty_chain_is_valid(self):
        self.assertTrue(verify_chain(()))

    def test_append_and_verify_hash_chain(self):
        events = append_event((), event_id="event-001", timestamp=event_time(0), event_type="captured", actor_id="collector-1", details={"source":"synthetic"})
        events = append_event(events, event_id="event-002", timestamp=event_time(1), event_type="verified", actor_id="reviewer-1", details={"result":"pass"})
        self.assertTrue(verify_chain(events))
        self.assertEqual(events[1]["previous_hash"], events[0]["event_hash"])

    def test_tampered_event_detected(self):
        events = append_event((), event_id="event-001", timestamp=event_time(0), event_type="captured", actor_id="collector-1", details={"source":"synthetic"})
        tampered = [dict(events[0])]
        tampered[0]["details_sha256"] = "0"*64
        with self.assertRaisesRegex(EvidenceError, "hash mismatch"):
            verify_chain(tampered)

    def test_reordered_events_detected(self):
        events = append_event((), event_id="event-001", timestamp=event_time(0), event_type="captured", actor_id="collector-1", details={"source":"synthetic"})
        events = append_event(events, event_id="event-002", timestamp=event_time(1), event_type="verified", actor_id="reviewer-1", details={"result":"pass"})
        with self.assertRaises(EvidenceError):
            verify_chain(tuple(reversed(events)))

    def test_duplicate_event_id_rejected(self):
        first = create_event(event_id="event-001", timestamp=event_time(0), event_type="captured", actor_id="collector-1", details={})
        second = create_event(event_id="event-001", timestamp=event_time(1), event_type="verified", actor_id="reviewer-1", details={}, previous_hash=first["event_hash"])
        with self.assertRaisesRegex(EvidenceError, "duplicate"):
            verify_chain([first,second])

    def test_non_monotonic_timestamps_rejected(self):
        first = create_event(event_id="event-001", timestamp=event_time(2), event_type="captured", actor_id="collector-1", details={})
        second = create_event(event_id="event-002", timestamp=event_time(1), event_type="verified", actor_id="reviewer-1", details={}, previous_hash=first["event_hash"])
        with self.assertRaisesRegex(EvidenceError, "not monotonic"):
            verify_chain([first,second])

    def test_append_rejects_corrupt_existing_chain(self):
        first = create_event(event_id="event-001", timestamp=event_time(0), event_type="captured", actor_id="collector-1", details={})
        broken = dict(first)
        broken["event_hash"] = "f"*64
        with self.assertRaises(EvidenceError):
            append_event([broken], event_id="event-002", timestamp=event_time(1), event_type="verified", actor_id="reviewer-1", details={})

    def test_event_details_are_hashed_not_embedded(self):
        event = create_event(event_id="event-001", timestamp=event_time(0), event_type="captured", actor_id="collector-1", details={"private":"do-not-store"})
        self.assertNotIn("private", event)
        self.assertIn("details_sha256", event)

    def test_event_timestamp_must_be_timezone_aware(self):
        with self.assertRaisesRegex(EvidenceError, "timezone"):
            create_event(event_id="event-001", timestamp="2026-11-02T12:00:00", event_type="captured", actor_id="collector-1", details={})

if __name__ == "__main__":
    unittest.main()
