from unittest.mock import patch

import pytest

from ai_toolkit.install_hooks.main import install, main
from ai_toolkit.install_hooks.installers.native_enforcement_installer import (
    NativeEnforcementInstaller,
)
from ai_toolkit.install_hooks.installers.pi_hooks_installer import PiHooksInstaller

pytestmark = pytest.mark.unit


class TestInstall:
    def test_install_returns_zero_when_all_succeed(self):
        with (
            patch.object(PiHooksInstaller, "install", return_value=True),
            patch.object(NativeEnforcementInstaller, "install", return_value=True),
        ):
            code = install("all")

        assert code == 0

    def test_install_returns_one_when_an_installer_fails(self):
        with (
            patch.object(PiHooksInstaller, "install", return_value=False),
            patch.object(NativeEnforcementInstaller, "install", return_value=True),
        ):
            code = install("all")

        assert code == 1


class TestMain:
    def test_main_returns_zero_for_valid_agent(self):
        with (
            patch.object(PiHooksInstaller, "install", return_value=True),
            patch.object(NativeEnforcementInstaller, "install", return_value=True),
        ):
            code = main(["--agent", "opencode"])

        assert code == 0
