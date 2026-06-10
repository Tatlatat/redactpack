import json
import os
import zipfile

import pytest

from redactpack.policy import Policy
from redactpack.scanner import scan_path


def test_scan_path_mirrors_directory_and_writes_reports(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "app.log").write_text("contact alice@example.com\n", encoding="utf-8")
    out = tmp_path / "out"

    result = scan_path(source, out, Policy.default())

    assert result.exit_code == 0
    assert (out / "app.log").read_text(encoding="utf-8") == "contact [REDACTED:EMAIL:1]\n"
    report = json.loads((out / "redactpack-report.json").read_text(encoding="utf-8"))
    assert report["input_path"] == "bundle"
    assert report["output_path"] == "out"
    assert report["counts_by_detector"]["email"] == 1
    assert "alice@example.com" not in (out / "redactpack-report.json").read_text(encoding="utf-8")
    assert "review aid" in (out / "redactpack-summary.md").read_text(encoding="utf-8")


def test_scan_path_preserves_crlf_bytes_in_sanitized_files(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "app.log").write_bytes(b"contact alice@example.com\r\n")
    out = tmp_path / "out"

    scan_path(source, out, Policy.default())

    assert (out / "app.log").read_bytes() == b"contact [REDACTED:EMAIL:1]\r\n"


def test_dry_run_writes_reports_but_not_sanitized_files(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "app.log").write_text("token Bearer abcdef1234567890abcdef1234567890\n", encoding="utf-8")
    out = tmp_path / "out"

    result = scan_path(source, out, Policy.default(), dry_run=True)

    assert result.exit_code == 1
    assert not (out / "app.log").exists()
    assert (out / "redactpack-report.json").exists()


def test_zip_output_contains_sanitized_files_and_reports(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "app.log").write_text("alice@example.com\n", encoding="utf-8")
    out = tmp_path / "out"

    result = scan_path(source, out, Policy.default(), make_zip=True)

    assert result.zip_path is not None
    with zipfile.ZipFile(result.zip_path) as archive:
        names = set(archive.namelist())
    assert "app.log" in names
    assert "redactpack-report.json" in names


def test_binary_files_are_skipped_and_reported(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "blob.bin").write_bytes(b"\x00\xff\x00")
    out = tmp_path / "out"

    result = scan_path(source, out, Policy.default())

    assert result.report.skipped_files == ["blob.bin"]
    assert not (out / "blob.bin").exists()


def test_zip_name_appends_suffix_for_dotted_output_directory(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "app.log").write_text("alice@example.com\n", encoding="utf-8")
    out = tmp_path / "out.v1"

    result = scan_path(source, out, Policy.default(), make_zip=True)

    assert result.zip_path == tmp_path / "out.v1.zip"
    assert result.zip_path.exists()


def test_output_directory_inside_input_is_rejected(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "app.log").write_text("alice@example.com\n", encoding="utf-8")

    with pytest.raises(ValueError, match="outside the input"):
        scan_path(source, source / "out", Policy.default())


def test_symlink_files_are_skipped_not_followed(tmp_path):
    source = tmp_path / "bundle"
    source.mkdir()
    outside = tmp_path / "outside.log"
    outside.write_text("outside alice@example.com\n", encoding="utf-8")
    link = source / "outside-link.log"
    try:
        os.symlink(outside, link)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")
    out = tmp_path / "out"

    result = scan_path(source, out, Policy.default())

    assert result.report.skipped_files == ["outside-link.log"]
    assert not (out / "outside-link.log").exists()


def test_unreadable_files_are_skipped_and_reports_are_still_written(tmp_path, monkeypatch):
    source = tmp_path / "bundle"
    source.mkdir()
    (source / "locked.log").write_text("alice@example.com\n", encoding="utf-8")
    out = tmp_path / "out"
    original_read_bytes = type(source).read_bytes

    def fake_read_bytes(path):
        if path.name == "locked.log":
            raise PermissionError("denied")
        return original_read_bytes(path)

    monkeypatch.setattr(type(source), "read_bytes", fake_read_bytes)

    result = scan_path(source, out, Policy.default())

    assert result.report.skipped_files == ["locked.log"]
    assert (out / "redactpack-report.json").exists()
    assert not (out / "locked.log").exists()
