from redactpack.detectors import default_detectors, scan_text


def detector_ids(text):
    return {finding.detector for finding in scan_text(text, default_detectors(), file="sample.log")}


def join_secret(*parts):
    return "".join(parts)


def test_detects_core_pii_and_secret_formats():
    text = """
    user alice@example.com connected from 192.168.1.10
    AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
    api_key = "rp_1234567890abcdef1234567890abcdef"
    card 4242 4242 4242 4242
    ssn 123-45-6789
    callback https://example.com/hook?token=secret123&safe=yes
    """ + "\n".join(
        [
            "Authorization: Bearer " + join_secret("bt_", "live_", "1234567890abcdefghijklmnop"),
            "github token " + join_secret("github_", "pat_", "11ABCDEFG0abcdefghijklmnopqrstuvwxyzABCDE1234567890abcd"),
            "stripe key " + join_secret("sk_", "test_", "4eC39HqLyjWDarjtT1zdp7dc"),
            "slack " + join_secret("xoxb", "-123456789012", "-123456789012", "-abcdefghijklmnopqrstuvwx"),
        ]
    )

    found = detector_ids(text)

    assert "email" in found
    assert "ipv4" in found
    assert "bearer_token" in found
    assert "aws_access_key" in found
    assert "github_token" in found
    assert "stripe_key" in found
    assert "slack_token" in found
    assert "generic_api_key" in found
    assert "credit_card" in found
    assert "us_ssn" in found
    assert "url_sensitive_query" in found


def test_luhn_rejects_invalid_credit_card_number():
    text = "not a real card 4242 4242 4242 4241"
    found = detector_ids(text)
    assert "credit_card" not in found
