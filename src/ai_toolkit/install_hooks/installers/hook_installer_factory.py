from collections.abc import Sequence

from ai_toolkit.install_hooks.installers.hook_installer import HookInstaller
from ai_toolkit.install_hooks.installers.native_enforcement_installer import (
    NativeEnforcementInstaller,
)
from ai_toolkit.install_hooks.installers.pi_hooks_installer import PiHooksInstaller

_NATIVE_AGENTS: tuple[str, ...] = ("opencode", "cline", "omp")


class HookInstallerFactory:
    """Resolve an agent selector to the ordered hook installers to run."""

    @classmethod
    def create(cls, agent: str) -> Sequence[HookInstaller]:
        if agent == "all":
            return [PiHooksInstaller.create()] + [
                NativeEnforcementInstaller.create(name)
                for name in _NATIVE_AGENTS
            ]
        if agent == "pi":
            return [PiHooksInstaller.create()]
        return [NativeEnforcementInstaller.create(agent)]
