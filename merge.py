#!/usr/bin/env python3
"""Merge ROS workspace compile_commands.json files into a workspace-level database."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
OUTPUT = BUILD / "compile_commands.json"


def load_compile_commands(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"{path} does not contain a JSON array")
    return data


def key_for_entry(entry: dict[str, Any]) -> tuple[Any, Any, Any]:
    return (entry.get("directory"), entry.get("file"), entry.get("command"))


def main() -> int:
    if not BUILD.exists() or not BUILD.is_dir():
        raise SystemExit(f"Build directory not found: {BUILD}")

    compile_files = sorted(BUILD.glob("*/compile_commands.json"))
    if not compile_files:
        raise SystemExit("No compile_commands.json files found under build/*")

    merged: list[dict[str, Any]] = []
    seen: set[tuple[Any, Any, Any]] = set()

    for compile_file in compile_files:
        commands = load_compile_commands(compile_file)
        for entry in commands:
            key = key_for_entry(entry)
            if key not in seen:
                merged.append(entry)
                seen.add(key)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as out_file:
        json.dump(merged, out_file, indent=2)
        out_file.write("\n")

    print(f"Merged {len(compile_files)} compile_commands.json files into {OUTPUT}")
    print(f"Total entries: {len(merged)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
