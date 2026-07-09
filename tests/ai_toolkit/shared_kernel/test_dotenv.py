from pathlib import Path

import pytest

from ai_toolkit.shared_kernel.dotenv import load_dotenv


class TestLoadDotenv:
    @pytest.mark.unit
    def test_load_when_file_does_not_exist_then_returns_empty(
        self,
        tmp_path: Path,
    ) -> None:
        result = load_dotenv(tmp_path / "nope.env")
        assert result == {}

    @pytest.mark.unit
    def test_load_when_file_empty_then_returns_empty(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / ".env"
        p.write_text("")
        result = load_dotenv(p)
        assert result == {}

    @pytest.mark.unit
    def test_load_when_file_has_key_value_pairs_then_returns_dict(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / ".env"
        p.write_text("GITHUB_TOKEN=ghp_abc\nFORGEJO_ACCESS_TOKEN=xyz\n")
        result = load_dotenv(p)
        assert result == {
            "GITHUB_TOKEN": "ghp_abc",
            "FORGEJO_ACCESS_TOKEN": "xyz",
        }

    @pytest.mark.unit
    def test_load_when_values_are_quoted_then_strips_quotes(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / ".env"
        p.write_text('KEY="double"\nOTHER=\'single\'\n')
        result = load_dotenv(p)
        assert result == {"KEY": "double", "OTHER": "single"}

    @pytest.mark.unit
    def test_load_when_file_has_comments_and_blanks_then_skips_them(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / ".env"
        p.write_text("# comment\n\nKEY=val\n  \n# another\n")
        result = load_dotenv(p)
        assert result == {"KEY": "val"}

    @pytest.mark.unit
    def test_load_when_file_has_trailing_spaces_then_strips(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / ".env"
        p.write_text("  KEY  =  val  \n")
        result = load_dotenv(p)
        assert result == {"KEY": "val"}
