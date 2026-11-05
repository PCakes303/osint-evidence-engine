from datetime import datetime, timedelta, timezone

def metadata(now=None):
    now = now or datetime.now(timezone.utc)
    return {
        "source_id":"example.public-api","collection_request_id":"synthetic-request-001",
        "source_url":"https://api.example.org/catalog","acquired_at":now.isoformat().replace("+00:00","Z"),
        "captured_by":"synthetic-collector-1","identity_authorization_ref":"identity-review-1",
        "policy_decision_ref":"policy-decision-1","emergency_state_ref":"emergency-state-1",
        "compliance_review_ref":"compliance-review-1","audit_event_ref":"audit-event-1",
        "source_license":"CC-BY-4.0","data_classification":"public","content_type":"application/json",
        "retention_days":30,"legal_hold":False
    }

def event_time(offset=0):
    return (datetime.now(timezone.utc)+timedelta(seconds=offset)).isoformat().replace("+00:00","Z")
