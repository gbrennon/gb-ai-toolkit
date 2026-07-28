import json
import os
import subprocess
from unittest.mock import patch

import pytest

from ai_toolkit.forge.api import (
    fj_api_url,
    fj_get,
    fj_patch,
    fj_post,
    get_remote_host,
    gh_post,
    gh_post_list,
    gh_run,
    gh_run_single,
    is_github,
    parse_remote_ref,
)


class TestGetRemoteHost:
    def test_detects_from_git(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = (
                "ssh://git@codeberg.org/gbrennon/ai-toolkit.git\n"
            )

            assert get_remote_host() == "codeberg.org"

    def test_https_url(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "https://github.com/owner/repo.git\n"

            assert get_remote_host() == "github.com"

    def test_git_fails(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 1

            assert get_remote_host() is None


class TestParseRemoteRef:
    def test_github_url(self) -> None:
        h, o, r, n = parse_remote_ref("https://github.com/owner/repo/pull/42")
        assert (h, o, r, n) == ("github.com", "owner", "repo", "42")

    def test_forgejo_url(self) -> None:
        h, o, r, n = parse_remote_ref("https://codeberg.org/o/r/issues/7")
        assert (h, o, r, n) == ("codeberg.org", "o", "r", "7")

    @patch("ai_toolkit.forge.api.get_remote_host", return_value="my.host")
    def test_owner_repo_number(self, _) -> None:
        h, o, r, n = parse_remote_ref("o/r/42")
        assert (h, o, r, n) == ("my.host", "o", "r", "42")

    def test_invalid(self) -> None:
        with pytest.raises(ValueError):
            parse_remote_ref("bad")


class TestIsGithub:
    def test_yes(self) -> None:
        assert is_github("github.com")
        assert is_github("api.github.com")

    def test_no(self) -> None:
        assert not is_github("codeberg.org")
        assert not is_github("")


class TestGhRun:
    def test_parses_ndjson(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = '{"id":1}\n{"id":2}\n'
            mock_run.return_value.stderr = ""

            assert gh_run(["x"]) == [{"id": 1}, {"id": 2}]

    def test_empty(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""

            assert gh_run(["x"]) == []

    def test_error(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "fail"

            with pytest.raises(SystemExit):
                gh_run(["x"])

    def test_single(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = '{"a": 1}'

            assert gh_run_single(["x"]) == {"a": 1}

    def test_single_error(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "fail"

            with pytest.raises(SystemExit):
                gh_run_single(["x"])


class TestGhPost:
    def test_post(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = '{"id": 42}'

            result = gh_post(["api", "/test"], '{"body": "hi"}')

            cmd = mock_run.call_args[0][0]
            assert "--body" in cmd
            idx = cmd.index("--body")
            assert cmd[idx + 1] == '{"body": "hi"}'
            assert result == {"id": 42}

    def test_post_error(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "fail"

            with pytest.raises(SystemExit):
                gh_post(["api", "/test"], "data")

    def test_post_list(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = '{"n":1}\n{"n":2}\n'

            result = gh_post_list(["x"], "body")

            assert result == [{"n": 1}, {"n": 2}]


class TestFjApi:
    def test_url(self) -> None:
        assert (
            fj_api_url("codeberg.org", "o/r/issues")
            == "https://codeberg.org/api/v1/repos/o/r/issues"
        )

    def test_get(self) -> None:
        with (
            patch.object(subprocess, "run") as mock_run,
            patch.dict(os.environ, {}, clear=True),
        ):
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = '{"ok": true}'

            result = fj_get("https://h/api/v1/repos/o/r")

            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd[0] == "curl"
            assert "-H" not in cmd
            assert result == {"ok": True}

    def test_get_with_token(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "{}"

            with patch.dict(
                os.environ, {"FORGEJO_TOKEN": "tok", "FJ_TOKEN": ""}, clear=True
            ):
                fj_get("https://h/api/v1/repos/o/r")

            cmd = mock_run.call_args[0][0]
            assert "-H" in cmd

    def test_get_with_fj_token(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "{}"

            with patch.dict(
                os.environ, {"FORGEJO_TOKEN": "", "FJ_TOKEN": "ftok"}, clear=True
            ):
                fj_get("https://h/api/v1/repos/o/r")

            cmd = mock_run.call_args[0][0]
            assert "-H" in cmd
            idx = cmd.index("-H")
            assert "ftok" in cmd[idx + 1]

    def test_get_error(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "err"

            with patch.dict(os.environ, {}, clear=True):
                with pytest.raises(SystemExit):
                    fj_get("https://h/api/v1/repos/o/r")

    def test_post(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = '{"id": 1}'

            result = fj_post("https://h/api/v1/repos/o/r/issues", {"title": "x"})

            cmd = mock_run.call_args[0][0]
            assert "-X" in cmd
            idx = cmd.index("-X")
            assert cmd[idx + 1] == "POST"
            assert "-d" in cmd
            didx = cmd.index("-d")
            assert json.loads(cmd[didx + 1]) == {"title": "x"}
            assert result == {"id": 1}

    def test_post_error(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "err"

            with patch.dict(os.environ, {}, clear=True):
                with pytest.raises(SystemExit):
                    fj_post("https://h/api/v1/repos/o/r", {})

    def test_patch(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = '{"ok": true}'

            result = fj_patch("https://h/api/v1/repos/o/r/i/1", {"state": "closed"})

            cmd = mock_run.call_args[0][0]
            assert "-X" in cmd
            idx = cmd.index("-X")
            assert cmd[idx + 1] == "PATCH"
            assert result == {"ok": True}
