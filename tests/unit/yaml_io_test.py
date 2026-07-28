import re
from pathlib import Path

import pytest

from yaml_io import read_yaml


class TestReadYaml:
    def test_returns_parsed_sequence(self, tmp_path: Path) -> None:
        path = tmp_path / "data.yml"
        path.write_text("- a: 1\n  b: 2\n")

        assert read_yaml(path) == [{"a": 1, "b": 2}]

    def test_returns_parsed_mapping(self, tmp_path: Path) -> None:
        path = tmp_path / "data.yml"
        path.write_text("key: value\n")

        assert read_yaml(path) == {"key": "value"}

    def test_raises_for_empty_file(self, tmp_path: Path) -> None:
        path = tmp_path / "empty.yml"
        path.write_text("")

        with pytest.raises(ValueError, match=re.escape(str(path))):
            read_yaml(path)

    def test_raises_for_yaml_null_document(self, tmp_path: Path) -> None:
        path = tmp_path / "null.yml"
        path.write_text("null\n")

        with pytest.raises(ValueError, match=re.escape(str(path))):
            read_yaml(path)
