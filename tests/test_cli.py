import json

from redactpack.cli import main


def test_cli_scan_returns_nonzero_when_critical_findings_meet_threshold(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "auth.log").write_text("Authorization: Bearer abcdef1234567890abcdef1234567890", encoding="utf-8")
    out = tmp_path / "out"

    exit_code = main(["scan", str(source), "--out", str(out), "--fail-on", "critical"])

    assert exit_code == 1
    report = json.loads((out / "redactpack-report.json").read_text(encoding="utf-8"))
    assert report["counts_by_severity"]["critical"] == 1


def test_cli_honors_policy_fail_on_when_flag_is_omitted(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "app.log").write_text("contact alice@example.com", encoding="utf-8")
    policy = tmp_path / "policy.json"
    policy.write_text('{"fail_on": "low"}', encoding="utf-8")
    out = tmp_path / "out"

    exit_code = main(["scan", str(source), "--out", str(out), "--policy", str(policy)])

    assert exit_code == 1


def test_cli_rejects_non_object_policy_json_cleanly(tmp_path, capsys):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "app.log").write_text("contact alice@example.com", encoding="utf-8")
    policy = tmp_path / "policy.json"
    policy.write_text("[]", encoding="utf-8")

    exit_code = main(["scan", str(source), "--out", str(tmp_path / "out"), "--policy", str(policy)])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "JSON object" in captured.err
    assert "Traceback" not in captured.err


def test_cli_detectors_lists_builtin_detectors(capsys):
    exit_code = main(["detectors"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "email" in output
    assert "bearer_token" in output


def test_cli_benchmark_reports_recall(capsys):
    exit_code = main(["benchmark"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "overall_recall" in output
    assert "missed" in output


def test_cli_benchmark_default_corpus_works_outside_repo(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    exit_code = main(["benchmark"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "redactpack.data/corpus.json" in output
