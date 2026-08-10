#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from lxml import etree

from itop_schema.combine import combine_schema


def load_schema_versions(config_path: Path) -> tuple[str, ...]:
    raw_config: object = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw_config, dict):
        raise ValueError(f"Expected an object in {config_path}")

    config = cast(dict[str, object], raw_config)
    versions: list[str] = []
    for category in ("supported", "development"):
        configured_versions = config.get(category)
        if not isinstance(configured_versions, list):
            raise ValueError(f"Expected a list of version strings for {category!r}")
        for configured_version in cast(list[object], configured_versions):
            if not isinstance(configured_version, str):
                raise ValueError(f"Expected a list of version strings for {category!r}")
            versions.append(configured_version)

    if not versions or len(versions) != len(set(versions)):
        raise ValueError("Configured schema versions must be non-empty and unique")
    return tuple(versions)


def update_distributions(repository_root: Path) -> tuple[Path, ...]:
    versions = load_schema_versions(repository_root / "schemas.json")
    outputs: list[Path] = []
    for version in versions:
        output_path = repository_root / "dist" / version / "itop_design.xsd"
        combine_schema(repository_root / version / "itop_design.xsd", output_path)
        outputs.append(output_path)
    return tuple(outputs)


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Update all configured distribution schemas.")
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root containing schemas.json",
    )
    return parser


def main(arguments: list[str] | None = None) -> int:
    repository_root = create_argument_parser().parse_args(arguments).repository_root.resolve()
    try:
        outputs = update_distributions(repository_root)
    except (OSError, ValueError, etree.LxmlError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    for output in outputs:
        print(f"Updated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
