import pytest

from ai_toolkit.install_hooks.installers.hook_installer_factory import (
    HookInstallerFactory,
)
from ai_toolkit.install_hooks.installers.native_enforcement_installer import (
    NativeEnforcementInstaller,
)
from ai_toolkit.install_hooks.installers.pi_hooks_installer import PiHooksInstaller

pytestmark = pytest.mark.unit


class TestHookInstallerFactory:
    def test_pi_selects_pi_installer(self):
        installers = HookInstallerFactory.create("pi")

        assert len(installers) == 1
        assert isinstance(installers[0], PiHooksInstaller)

    def test_native_agent_selects_native_installer(self):
        for agent in ("opencode", "cline", "omp"):
            installers = HookInstallerFactory.create(agent)

            assert len(installers) == 1
            assert isinstance(installers[0], NativeEnforcementInstaller)

    def test_all_selects_pi_then_native(self):
        installers = HookInstallerFactory.create("all")

        assert len(installers) == 4
        assert isinstance(installers[0], PiHooksInstaller)
        assert all(
            isinstance(installer, NativeEnforcementInstaller)
            for installer in installers[1:]
        )
