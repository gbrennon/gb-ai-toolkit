import json
import subprocess
import sys
from unittest.mock import patch

import pytest

from ai_toolkit.forge_issue.main import (
    gh_comment,
    gh_create,
    gh_label_add,
    gh_label_remove,
    gh_list,
    gh_view,
    main,
)


class TestGhList:
    def test_lists_issues(self) -> None:
        with patch("ai_toolkit.forge_issue.main.gh_run") as mock_run:
            mock_run.return_value = [
                {
                    "number": 1,
                    "title": "Fix",
                    "state": "open",
                    "user": "alice",
                    "labels": ["bug"],
                    "created_at": "",
                },
            ]

            result = gh_list("owner", "repo", "open", None)

            mock_run.assert_called_once()
            assert "state=open" in str(mock_run.call_args)
            assert result[0]["title"] == "Fix"

    def test_filters_by_label(self) -> None:
        with patch("ai_toolkit.forge_issue.main.gh_run") as mock_run:
            mock_run.return_value = []

            gh_list("owner", "repo", "open", "bug")

            args_str = str(mock_run.call_args)
            assert "bug" in args_str


class TestGhView:
    def test_views_issue_and_comments(self) -> None:
        with (
            patch("ai_toolkit.forge_issue.main.gh_run_single") as single,
            patch("ai_toolkit.forge_issue.main.gh_run") as multi,
        ):
            single.return_value = {
                "number": 1,
                "title": "Fix",
                "state": "open",
                "body": "desc",
                "user": "alice",
                "labels": ["bug"],
                "created_at": "",
            }
            multi.return_value = [
                {"id": 1, "user": "bob", "body": "comment", "created_at": ""},
            ]

            issue, comments = gh_view("owner", "repo", "1")

            assert issue["title"] == "Fix"
            assert comments[0]["user"] == "bob"


class TestGhCreate:
    def test_creates_issue(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = json.dumps(
                {"number": 42, "title": "Fix", "html_url": "https://x"}
            )

            result = gh_create("o", "r", "Fix", "body", ["bug"])

            cmd = mock_run.call_args[0][0]
            assert "--body" in cmd
            assert result["number"] == 42


class TestGhComment:
    def test_adds_comment(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = json.dumps(
                {"id": 99, "html_url": "https://x"}
            )

            result = gh_comment("o", "r", "1", "nice")

            cmd = mock_run.call_args[0][0]
            assert "--body" in cmd
            assert result["id"] == 99


class TestGhLabel:
    def test_add(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "[]"

            gh_label_add("o", "r", "1", "bug")

            cmd = mock_run.call_args[0][0]
            assert "labels" in str(cmd)
            assert "bug" in str(cmd)

    def test_remove(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""

            gh_label_remove("o", "r", "1", "bug")

            cmd = mock_run.call_args[0][0]
            assert "DELETE" in str(cmd)


class TestCmdList:
    def test_github(self, capsys) -> None:
        with (
            patch.object(
                sys, "argv", ["forge-issue", "list", "o/r", "--state", "open"]
            ),
            patch("ai_toolkit.forge_issue.main.gh_list") as mock_list,
            patch(
                "ai_toolkit.forge_issue.main.parse_remote_ref",
                return_value=("github.com", "o", "r", "1"),
            ),
        ):
            mock_list.return_value = [
                {
                    "number": 1,
                    "title": "Fix",
                    "state": "open",
                    "user": "alice",
                    "labels": [],
                    "created_at": "",
                },
            ]

            main()
            out = capsys.readouterr().out

            assert "#1" in out
            assert "Fix" in out

    def test_no_issues(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["forge-issue", "list", "o/r"]),
            patch("ai_toolkit.forge_issue.main.gh_list", return_value=[]),
            patch(
                "ai_toolkit.forge_issue.main.parse_remote_ref",
                return_value=("github.com", "o", "r", "1"),
            ),
        ):
            main()
            out = capsys.readouterr().out
            assert "No issues" in out


class TestCmdView:
    def test_github(self, capsys) -> None:
        with (
            patch.object(
                sys, "argv", ["forge-issue", "view", "https://github.com/o/r/issues/1"]
            ),
            patch("ai_toolkit.forge_issue.main.gh_view") as mock_view,
        ):
            mock_view.return_value = (
                {
                    "number": 1,
                    "title": "Fix",
                    "state": "open",
                    "body": "desc",
                    "user": "alice",
                    "labels": ["bug"],
                    "created_at": "",
                },
                [{"id": 1, "user": "bob", "body": "LGTM", "created_at": ""}],
            )

            main()
            out = capsys.readouterr().out

            assert "#1" in out
            assert "Fix" in out
            assert "bob" in out
            assert "LGTM" in out


class TestCmdCreate:
    def test_github(self, capsys) -> None:
        with (
            patch.object(
                sys,
                "argv",
                ["forge-issue", "create", "o/r", "My Issue", "--label", "bug"],
            ),
            patch("ai_toolkit.forge_issue.main.gh_create") as mock_create,
            patch(
                "ai_toolkit.forge_issue.main.parse_remote_ref",
                return_value=("github.com", "o", "r", "1"),
            ),
            patch.object(sys, "stdin") as mock_stdin,
        ):
            mock_stdin.read.return_value = "Issue body"
            mock_create.return_value = {
                "number": 42,
                "title": "My Issue",
                "html_url": "https://github.com/o/r/issues/42",
            }

            main()
            out = capsys.readouterr().out

            assert "#42" in out
            assert "My Issue" in out


class TestCmdComment:
    def test_github(self, capsys) -> None:
        with (
            patch.object(
                sys,
                "argv",
                ["forge-issue", "comment", "https://github.com/o/r/issues/1"],
            ),
            patch("ai_toolkit.forge_issue.main.gh_comment") as mock_c,
            patch.object(sys, "stdin") as mock_stdin,
        ):
            mock_stdin.read.return_value = "Nice work"
            mock_c.return_value = {"id": 99, "html_url": "https://x"}

            main()
            out = capsys.readouterr().out

            assert "99" in out


class TestCmdLabel:
    def test_add(self, capsys) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "forge-issue",
                    "label",
                    "https://github.com/o/r/issues/1",
                    "add",
                    "ready-for-agent",
                ],
            ),
            patch("ai_toolkit.forge_issue.main.gh_label_add"),
        ):
            main()
            out = capsys.readouterr().out
            assert "added" in out

    def test_remove(self, capsys) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "forge-issue",
                    "label",
                    "https://github.com/o/r/issues/1",
                    "remove",
                    "wontfix",
                ],
            ),
            patch("ai_toolkit.forge_issue.main.gh_label_remove"),
        ):
            main()
            out = capsys.readouterr().out
            assert "removed" in out


class TestMainDispatch:
    def test_no_args(self) -> None:
        with patch.object(sys, "argv", ["forge-issue"]):
            with pytest.raises(SystemExit):
                main()

    def test_unknown_command(self) -> None:
        with patch.object(sys, "argv", ["forge-issue", "unknown"]):
            with pytest.raises(SystemExit):
                main()
