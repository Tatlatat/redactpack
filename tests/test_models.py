from redactpack.models import Finding, severity_meets_threshold, severity_rank


def test_severity_ordering_and_thresholds():
    assert severity_rank("low") < severity_rank("medium") < severity_rank("high") < severity_rank("critical")
    assert severity_meets_threshold("critical", "critical") is True
    assert severity_meets_threshold("high", "critical") is False
    assert severity_meets_threshold("medium", "low") is True


def test_finding_safe_dict_excludes_raw_value_and_bruteforceable_hash():
    finding = Finding(
        detector="email",
        label="Email address",
        severity="medium",
        confidence=0.95,
        file="app.log",
        line=3,
        start=10,
        end=27,
        value="alice@example.com",
        placeholder="[REDACTED:EMAIL:1]",
    )

    safe = finding.to_safe_dict()

    assert "alice@example.com" not in str(safe)
    assert "value" not in safe
    assert "value_hash" not in safe
    assert safe["placeholder"] == "[REDACTED:EMAIL:1]"
