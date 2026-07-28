import json
import os
import subprocess
import sys
from unittest.mock import patch

import pytest

from ai_toolkit.fetch_pr_review.main import (
    fj_fetch_comments,
    fj_fetch_pr,
    fj_fetch_reviews,
    fj_get,
    gh_fetch_comments,
    gh_fetch_pr,
    gh_fetch_reviews,
    gh_run,
    gh_run_single,
    is_github,
    main,
    parse_remote_ref,
    render,
)


class TestParseRef:
    def test_github_url(self) -> None:
        host, owner, repo, num = parse_remote_ref(
            "https://github.com/owner/repo/pull/42"
        )
        assert host == "github.com"
        assert (owner, repo, num) == ("owner", "repo", "42")

    def test_github_url_pulls(self) -> None:
        host, owner, repo, num = parse_remote_ref(
            "https://github.com/owner/repo/pulls/42"
        )
        assert host == "github.com"
        assert (owner, repo, num) == ("owner", "repo", "42")

    def test_forgejo_url(self) -> None:
        host, owner, repo, num = parse_remote_ref(
            "https://codeberg.org/gbrennon/ai-toolkit/pulls/1"
        )
        assert host == "codeberg.org"
        assert (owner, repo, num) == ("gbrennon", "ai-toolkit", "1")

    @patch(
        "ai_toolkit.forge.api.get_remote_host",
        return_value="codeberg.org",
    )
    def test_owner_repo_number(self, mock_host) -> None:
        host, owner, repo, num = parse_remote_ref("owner/repo/42")
        assert host == "codeberg.org"
        assert (owner, repo, num) == ("owner", "repo", "42")

    @patch(
        "ai_toolkit.forge.api.get_remote_host",
        return_value=None,
    )
    def test_owner_repo_number_no_remote(self, mock_host) -> None:
        host, owner, repo, num = parse_remote_ref("owner/repo/42")
        assert host == ""
        assert (owner, repo, num) == ("owner", "repo", "42")

    def test_invalid_ref(self) -> None:
        with pytest.raises(ValueError, match="Unrecognized"):
            parse_remote_ref("https://example.com/not/a/pr")

    def test_invalid_short(self) -> None:
        with pytest.raises(ValueError, match="Expected owner/repo/number or full URL"):
            parse_remote_ref("bad")


class TestIsGithub:
    def test_github(self) -> None:
        assert is_github("github.com")
        assert is_github("api.github.com")

    def test_not_github(self) -> None:
        assert not is_github("codeberg.org")
        assert not is_github("")


class TestGhBackend:
    def test_gh_run_parses_ndjson(self) -> None:
        mock_output = (
            '{"id": 1, "user": {"login": "alice"}}\n'
            '{"id": 2, "user": {"login": "bob"}}\n'
        )
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = mock_output
            mock_run.return_value.stderr = ""

            result = gh_run(["api", "/test"])

            assert result == [
                {"id": 1, "user": {"login": "alice"}},
                {"id": 2, "user": {"login": "bob"}},
            ]

    def test_gh_run_empty(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""

            assert gh_run(["api", "/test"]) == []

    def test_gh_run_exits_on_error(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "not found"

            with pytest.raises(SystemExit):
                gh_run(["api", "/test"])

    def test_gh_run_single(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = json.dumps({"title": "Fix", "state": "open"})

            result = gh_run_single(["api", "/test"])

            assert result == {"title": "Fix", "state": "open"}

    def test_gh_fetch_pr(self) -> None:
        with patch("ai_toolkit.fetch_pr_review.main.gh_run_single") as mock_fn:
            mock_fn.return_value = {
                "title": "Fix",
                "state": "open",
                "body": "desc",
                "user": "alice",
            }

            result = gh_fetch_pr("owner", "repo", "42")

            mock_fn.assert_called_once_with(
                [
                    "api",
                    "/repos/owner/repo/pulls/42",
                    "--jq",
                    "{title, state, body, user: .user.login}",
                ]
            )
            assert result == {
                "title": "Fix",
                "state": "open",
                "body": "desc",
                "user": "alice",
            }

    def test_gh_fetch_reviews(self) -> None:
        with patch("ai_toolkit.fetch_pr_review.main.gh_run") as mock_fn:
            mock_fn.return_value = [
                {
                    "id": 1,
                    "user": "alice",
                    "state": "APPROVED",
                    "body": "LGTM",
                    "submitted_at": "2024-01-01",
                },
            ]

            result = gh_fetch_reviews("owner", "repo", "42")

            mock_fn.assert_called_once_with(
                [
                    "api",
                    "/repos/owner/repo/pulls/42/reviews",
                    "--jq",
                    ".[] | {id, user: .user.login, state, body, submitted_at}",
                    "--paginate",
                ]
            )
            assert result == [
                {
                    "id": 1,
                    "user": "alice",
                    "state": "APPROVED",
                    "body": "LGTM",
                    "submitted_at": "2024-01-01",
                },
            ]

    def test_gh_fetch_comments(self) -> None:
        with patch("ai_toolkit.fetch_pr_review.main.gh_run") as mock_fn:
            mock_fn.return_value = [
                {
                    "id": 1,
                    "user": "bob",
                    "path": "src/main.py",
                    "line": 10,
                    "body": "fix this",
                    "commit_id": "abc",
                },
            ]

            result = gh_fetch_comments("owner", "repo", "42")

            mock_fn.assert_called_once_with(
                [
                    "api",
                    "/repos/owner/repo/pulls/42/comments",
                    "--jq",
                    ".[] | {id, user: .user.login, path, line, body, commit_id}",
                    "--paginate",
                ]
            )
            assert result == [
                {
                    "id": 1,
                    "user": "bob",
                    "path": "src/main.py",
                    "line": 10,
                    "body": "fix this",
                    "commit_id": "abc",
                },
            ]


class TestFjBackend:
    def test_fj_get_no_auth(self) -> None:
        with (
            patch.object(subprocess, "run") as mock_run,
            patch.dict(os.environ, {}, clear=True),
        ):
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = json.dumps({"title": "Fix"})

            result = fj_get("https://codeberg.org/api/v1/repos/o/r/pulls/1")

            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd[:2] == ["curl", "-s"]
            assert cmd[-1] == ("https://codeberg.org/api/v1/repos/o/r/pulls/1")
            assert result == {"title": "Fix"}

    def test_fj_get_with_token(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "{}"

            with patch.dict(
                os.environ,
                {"FORGEJO_TOKEN": "my-token", "FJ_TOKEN": ""},
                clear=True,
            ):
                fj_get("https://codeberg.org/api/v1/repos/o/r/pulls/1")

            cmd = mock_run.call_args[0][0]
            assert "-H" in cmd
            idx = cmd.index("-H")
            assert "my-token" in cmd[idx + 1]

    def test_fj_get_with_fj_token(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "{}"

            with patch.dict(
                os.environ,
                {"FORGEJO_TOKEN": "", "FJ_TOKEN": "fj-token"},
                clear=True,
            ):
                fj_get("https://codeberg.org/api/v1/repos/o/r/pulls/1")

            cmd = mock_run.call_args[0][0]
            assert "-H" in cmd
            idx = cmd.index("-H")
            assert "fj-token" in cmd[idx + 1]

    def test_fj_get_exits_on_error(self) -> None:
        with patch.object(subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 1

            with pytest.raises(SystemExit):
                fj_get("https://codeberg.org/api/v1/repos/o/r/pulls/1")

    def test_fj_fetch_pr(self) -> None:
        with patch("ai_toolkit.fetch_pr_review.main.fj_get") as mock_get:
            mock_get.return_value = {
                "title": "Fix bug",
                "state": "open",
                "body": "desc",
                "user": {"login": "alice"},
            }

            result = fj_fetch_pr("codeberg.org", "owner", "repo", "42")

            mock_get.assert_called_once_with(
                "https://codeberg.org/api/v1/repos/owner/repo/pulls/42"
            )
            assert result == {
                "title": "Fix bug",
                "state": "open",
                "body": "desc",
                "user": "alice",
            }

    def test_fj_fetch_reviews(self) -> None:
        with patch("ai_toolkit.fetch_pr_review.main.fj_get") as mock_get:
            mock_get.return_value = [
                {
                    "id": 1,
                    "user": {"login": "bob"},
                    "state": "APPROVED",
                    "body": "LGTM",
                    "submitted_at": "2024-01-01",
                },
            ]

            result = fj_fetch_reviews("codeberg.org", "owner", "repo", "42")

            mock_get.assert_called_once_with(
                "https://codeberg.org/api/v1/repos/owner/repo/pulls/42/reviews"
            )
            assert result == [
                {
                    "id": 1,
                    "user": "bob",
                    "state": "APPROVED",
                    "body": "LGTM",
                    "submitted_at": "2024-01-01",
                },
            ]

    def test_fj_fetch_reviews_empty(self) -> None:
        with patch("ai_toolkit.fetch_pr_review.main.fj_get") as mock_get:
            mock_get.return_value = {}

            result = fj_fetch_reviews("codeberg.org", "owner", "repo", "42")

            assert result == []

    def test_fj_fetch_comments(self) -> None:
        with patch("ai_toolkit.fetch_pr_review.main.fj_get") as mock_get:
            mock_get.return_value = [
                {
                    "id": 1,
                    "user": {"login": "bob"},
                    "path": "src/main.py",
                    "line": 10,
                    "body": "fix this",
                    "commit_id": "abc",
                },
            ]

            result = fj_fetch_comments("codeberg.org", "owner", "repo", "42")

            mock_get.assert_called_once_with(
                "https://codeberg.org/api/v1/repos/owner/repo/pulls/42/comments"
            )
            assert result == [
                {
                    "id": 1,
                    "user": "bob",
                    "path": "src/main.py",
                    "line": 10,
                    "body": "fix this",
                    "commit_id": "abc",
                },
            ]


class TestRender:
    def test_with_reviews_and_comments(self, capsys) -> None:
        pr = {"title": "Fix bug", "state": "open", "body": "desc", "user": "alice"}
        reviews = [
            {"user": "bob", "state": "APPROVED", "body": "LGTM", "submitted_at": ""},
        ]
        comments = [
            {
                "user": "bob",
                "path": "src/main.py",
                "line": 42,
                "body": "rename this",
                "commit_id": "x",
            },
        ]

        render(pr, reviews, comments)
        out = capsys.readouterr().out

        assert "# PR Review: Fix bug" in out
        assert "bob (APPROVED)" in out
        assert "LGTM" in out
        assert "src/main.py:42" in out
        assert "rename this" in out
        assert "Total findings: 2" in out

    def test_empty(self, capsys) -> None:
        pr = {"title": "Fix", "state": "open", "body": "", "user": "alice"}

        render(pr, [], [])
        out = capsys.readouterr().out

        assert "_No review summaries found._" in out
        assert "_No inline comments found._" in out
        assert "Total findings: 0" in out


class TestMain:
    def test_no_args(self) -> None:
        with patch.object(sys, "argv", ["fetch-pr-review"]):
            with pytest.raises(SystemExit):
                main()

    def test_github_dispatch(self) -> None:
        with (
            patch.object(
                sys, "argv", ["fetch-pr-review", "https://github.com/o/r/pull/1"]
            ),
            patch("ai_toolkit.fetch_pr_review.main.gh_fetch_pr") as pr_fn,
            patch("ai_toolkit.fetch_pr_review.main.gh_fetch_reviews") as rv,
            patch("ai_toolkit.fetch_pr_review.main.gh_fetch_comments") as cm,
        ):
            pr_fn.return_value = {
                "title": "Fix",
                "state": "open",
                "body": "",
                "user": "alice",
            }
            rv.return_value = []
            cm.return_value = []

            main()

            pr_fn.assert_called_once()
            rv.assert_called_once()
            cm.assert_called_once()

    def test_forgejo_dispatch(self) -> None:
        with (
            patch.object(
                sys, "argv", ["fetch-pr-review", "https://codeberg.org/o/r/pulls/1"]
            ),
            patch("ai_toolkit.fetch_pr_review.main.fj_fetch_pr") as pr_fn,
            patch("ai_toolkit.fetch_pr_review.main.fj_fetch_reviews") as rv,
            patch("ai_toolkit.fetch_pr_review.main.fj_fetch_comments") as cm,
        ):
            pr_fn.return_value = {
                "title": "Fix",
                "state": "open",
                "body": "",
                "user": "alice",
            }
            rv.return_value = []
            cm.return_value = []

            main()

            pr_fn.assert_called_once()
            rv.assert_called_once()
            cm.assert_called_once()

    def test_forgejo_no_host_exits(self) -> None:
        with (
            patch.object(sys, "argv", ["fetch-pr-review", "o/r/1"]),
            patch("ai_toolkit.forge.api.get_remote_host", return_value=""),
            pytest.raises(SystemExit),
        ):
            main()
