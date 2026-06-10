import json

import pytest

from redactpack.policy import Policy, load_policy


def test_default_policy_has_conservative_failure_threshold():
    policy = Policy.default()
    assert policy.fail_on == "critical"
    assert "email" not in policy.disabled_detectors


def test_load_policy_from_json(tmp_path):
    path = tmp_path / "policy.json"
    path.write_text(
        json.dumps(
            {
                "disabled_detectors": ["ipv4"],
                "allowlist": ["example\\.internal"],
                "custom_literals": [{"literal": "ACME-CUSTOMER-123", "label": "customer_id", "severity": "medium"}],
                "fail_on": "high",
            }
        ),
        encoding="utf-8",
    )

    policy = load_policy(path)

    assert policy.disabled_detectors == {"ipv4"}
    assert policy.allowlist_patterns == ["example\\.internal"]
    assert policy.custom_literals[0]["literal"] == "ACME-CUSTOMER-123"
    assert policy.fail_on == "high"


def test_invalid_policy_severity_is_rejected(tmp_path):
    path = tmp_path / "bad-policy.json"
    path.write_text(json.dumps({"fail_on": "severe"}), encoding="utf-8")

    with pytest.raises(ValueError, match="fail_on"):
        load_policy(path)


def test_non_object_policy_json_is_rejected(tmp_path):
    path = tmp_path / "bad-shape.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON object"):
        load_policy(path)


def test_invalid_allowlist_regex_is_rejected_at_load(tmp_path):
    path = tmp_path / "bad-allowlist.json"
    path.write_text(json.dumps({"allowlist": ["[unclosed"]}), encoding="utf-8")

    with pytest.raises(ValueError, match="allowlist"):
        load_policy(path)
