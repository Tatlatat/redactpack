from redactpack.detectors import default_detectors
from redactpack.policy import Policy
from redactpack.redactor import redact_text


def test_redaction_uses_stable_typed_placeholders_for_repeated_values():
    text = "Email alice@example.com then alice@example.com again"

    result = redact_text(text, default_detectors(), Policy.default(), file="note.txt")

    assert result.text == "Email [REDACTED:EMAIL:1] then [REDACTED:EMAIL:1] again"
    assert len(result.findings) == 2
    assert {finding.placeholder for finding in result.findings} == {"[REDACTED:EMAIL:1]"}


def test_overlap_resolution_prefers_higher_severity_longer_match():
    token = "".join(["bt_", "live_", "1234567890abcdefghijklmnop"])
    text = "Authorization: Bearer " + token

    result = redact_text(text, default_detectors(), Policy.default(), file="auth.log")

    assert "[REDACTED:BEARER_TOKEN:1]" in result.text
    assert token not in result.text
    assert sum(1 for finding in result.findings if finding.detector == "bearer_token") == 1


def test_allowlist_skips_matching_values():
    policy = Policy.default(allowlist=[r"alice@example\.com"])
    result = redact_text("alice@example.com bob@example.com", default_detectors(), policy, file="mail.log")

    assert "alice@example.com" in result.text
    assert "[REDACTED:EMAIL:1]" in result.text
    assert all(finding.value != "alice@example.com" for finding in result.findings)
