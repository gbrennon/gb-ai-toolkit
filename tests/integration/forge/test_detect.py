import os
import subprocess
import tempfile
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parents[3]


def run_detect(
    repo_dir: Path, extra_env: dict[str, str] | None = None
) -> subprocess.CompletedProcess:
    env = {**os.environ, "GIT_DIR": str(repo_dir / ".git")}
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        ["uv", "run", "--directory", str(PROJECT_DIR), "forge-detect"],
        capture_output=True,
        text=True,
        cwd=str(repo_dir),
        env=env,
    )


def run_detect_json(repo_dir: Path) -> dict:
    env = {**os.environ, "GIT_DIR": str(repo_dir / ".git")}
    result = subprocess.run(
        ["uv", "run", "--directory", str(PROJECT_DIR), "forge-detect", "--json"],
        capture_output=True,
        text=True,
        cwd=str(repo_dir),
        env=env,
    )
    import json

    return json.loads(result.stdout)


@pytest.mark.integration
class TestForgeDetectIntegration:
    @pytest.fixture(autouse=True)
    def clean_git_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        for key in list(os.environ.keys()):
            if key.startswith("GIT_"):
                monkeypatch.delenv(key, raising=False)

    def test_github_https(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://github.com/owner/repo.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.returncode == 0
            assert result.stdout.strip() == "github"

    def test_codeberg_https(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://codeberg.org/u/r.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.stdout.strip() == "codeberg"

    def test_gitlab_https(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://gitlab.com/o/p.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.stdout.strip() == "gitlab"

    def test_bitbucket_https(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://bitbucket.org/o/r.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.stdout.strip() == "bitbucket"

    def test_gitea_https(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://gitea.com/o/r.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.stdout.strip() == "gitea"

    def test_ssh_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "git@github.com:o/r.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.stdout.strip() == "github"

    def test_github_enterprise_subdomain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                [
                    "git",
                    "remote",
                    "add",
                    "origin",
                    "https://github.mycompany.com/o/r.git",
                ],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.stdout.strip() == "github"

    def test_unknown_forge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://myhost.com/o/r.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.stdout.strip() == "unknown"

    def test_no_remote(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            result = run_detect(repo)
            assert result.returncode == 1
            assert "No git remote found" in result.stderr

    def test_env_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "myremote", "https://gitlab.com/o/p.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo, extra_env={"REMOTE": "myremote"})
            assert result.stdout.strip() == "gitlab"

    def test_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://github.com/o/r.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            data = run_detect_json(repo)
            assert data["forge"] == "github"
            assert data["remote"] == "origin"
            assert "github.com" in data["url"]

    def test_prefers_tracked_upstream_over_origin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://github.com/fork/repo.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            bare = Path(tmp) / "bare"
            subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", "init"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "push", str(bare), "main"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "remote", "add", "upstream", str(bare)],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "fetch", "upstream"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "branch", "-u", "upstream/main"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            code = (
                "from ai_toolkit.forge.api import get_main_remote; "
                "print(get_main_remote())"
            )
            env = {**os.environ, "GIT_DIR": str(repo / ".git")}
            result = subprocess.run(
                ["uv", "run", "--directory", str(PROJECT_DIR), "python", "-c", code],
                capture_output=True,
                text=True,
                cwd=str(repo),
                env=env,
            )
            assert result.stdout.strip() == "upstream"

    def test_falls_back_to_origin_when_no_tracked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://bitbucket.org/o/r.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "remote", "add", "upstream", "https://gitlab.com/o/p.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.stdout.strip() == "bitbucket"

    def test_falls_back_to_first_remote(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "remote", "add", "first", "https://codeberg.org/o/r.git"],
                cwd=repo,
                check=True,
                capture_output=True,
            )
            result = run_detect(repo)
            assert result.stdout.strip() == "codeberg"
