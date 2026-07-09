from pathlib import Path

import pytest

from tests.ai_toolkit.install_skills.fakes import FakeCopierInstaller, FakeNpxInstaller


@pytest.fixture
def fake_npx() -> FakeNpxInstaller:
    return FakeNpxInstaller()


@pytest.fixture
def fake_copier() -> FakeCopierInstaller:
    return FakeCopierInstaller()


@pytest.fixture
def skills_dir(tmp_path: Path) -> Path:
    d = tmp_path / "skills"
    d.mkdir()
    return d


@pytest.fixture
def target_dir(tmp_path: Path) -> Path:
    d = tmp_path / "agents" / "skills"
    d.mkdir(parents=True)
    return d


@pytest.fixture
def sample_yaml(tmp_path: Path) -> Path:
    content = """
skills:
  - forging-blocks-org/forging-blocks/tree/main/skills/forging-blocks-maintenance
  - owner/repo/some-skill
"""
    p = tmp_path / "skills.yaml"
    p.write_text(content)
    return p
