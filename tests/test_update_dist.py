import json
from pathlib import Path

import pytest

from scripts import update_dist


def write_config(path: Path, content: object) -> None:
    path.write_text(json.dumps(content), encoding="utf-8")


def test_load_schema_versions_returns_supported_and_development_versions(tmp_path: Path) -> None:
    config_path = tmp_path / "schemas.json"
    write_config(
        config_path,
        {"latest": "3.2", "supported": ["3.2"], "development": ["3.3", "3.4"]},
    )

    assert update_dist.load_schema_versions(config_path) == ("3.2", "3.3", "3.4")


def test_load_schema_versions_rejects_non_object_config(tmp_path: Path) -> None:
    config_path = tmp_path / "schemas.json"
    write_config(config_path, ["3.2"])

    with pytest.raises(ValueError, match="Expected an object"):
        update_dist.load_schema_versions(config_path)


@pytest.mark.parametrize(
    ("content", "category"),
    [
        ({"development": []}, "supported"),
        ({"supported": "3.2", "development": []}, "supported"),
        ({"supported": [], "development": "3.3"}, "development"),
        ({"supported": [3.2], "development": []}, "supported"),
    ],
)
def test_load_schema_versions_rejects_invalid_version_lists(
    tmp_path: Path,
    content: object,
    category: str,
) -> None:
    config_path = tmp_path / "schemas.json"
    write_config(config_path, content)

    with pytest.raises(ValueError, match=category):
        update_dist.load_schema_versions(config_path)


@pytest.mark.parametrize(
    "content",
    [
        {"supported": [], "development": []},
        {"supported": ["3.2"], "development": ["3.2"]},
    ],
)
def test_load_schema_versions_rejects_empty_or_duplicate_versions(
    tmp_path: Path,
    content: object,
) -> None:
    config_path = tmp_path / "schemas.json"
    write_config(config_path, content)

    with pytest.raises(ValueError, match="non-empty and unique"):
        update_dist.load_schema_versions(config_path)


def test_update_distributions_combines_every_configured_version(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_config(
        tmp_path / "schemas.json",
        {"supported": ["3.2"], "development": ["3.3"]},
    )
    calls: list[tuple[Path, Path]] = []

    def record_combination(input_path: Path, output_path: Path) -> None:
        calls.append((input_path, output_path))

    monkeypatch.setattr(update_dist, "combine_schema", record_combination)

    outputs = update_dist.update_distributions(tmp_path)

    assert calls == [
        (tmp_path / "3.2/itop_design.xsd", tmp_path / "dist/3.2/itop_design.xsd"),
        (tmp_path / "3.3/itop_design.xsd", tmp_path / "dist/3.3/itop_design.xsd"),
    ]
    assert outputs == tuple(output_path for _, output_path in calls)


def test_main_reports_updated_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output_path = tmp_path / "dist/3.2/itop_design.xsd"

    def return_output(repository_root: Path) -> tuple[Path, ...]:
        assert repository_root == tmp_path.resolve()
        return (output_path,)

    monkeypatch.setattr(update_dist, "update_distributions", return_output)

    exit_code = update_dist.main(["--repository-root", str(tmp_path)])

    assert exit_code == 0
    assert f"Updated: {output_path}" in capsys.readouterr().out


def test_main_reports_generation_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def raise_error(_repository_root: Path) -> tuple[Path, ...]:
        raise OSError("generation failed")

    monkeypatch.setattr(update_dist, "update_distributions", raise_error)

    exit_code = update_dist.main(["--repository-root", str(tmp_path)])

    assert exit_code == 1
    assert "Error: generation failed" in capsys.readouterr().err
