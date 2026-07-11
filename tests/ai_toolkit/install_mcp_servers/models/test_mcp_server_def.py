import pytest

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef


class TestMcpServerDef:
    @pytest.mark.unit
    def test_construct_when_given_all_fields_then_sets_attributes(self) -> None:
        server = McpServerDef(
            name="test-server",
            command="npx",
            args=("-y", "some-package"),
            env=(("KEY", "value"),),
            server_type=None,
            url=None,
            disabled=False,
        )
        assert server.name == "test-server"
        assert server.command == "npx"
        assert server.args == ("-y", "some-package")
        assert server.env == (("KEY", "value"),)
        assert server.server_type is None
        assert server.url is None
        assert server.disabled is False

    @pytest.mark.unit
    def test_construct_when_http_server_then_has_null_command_and_url(self) -> None:
        server = McpServerDef(
            name="github",
            command=None,
            args=(),
            env=(),
            server_type="streamableHttp",
            url="https://api.githubcopilot.com/mcp/",
            disabled=False,
        )
        assert server.command is None
        assert server.url == "https://api.githubcopilot.com/mcp/"
        assert server.server_type == "streamableHttp"

    @pytest.mark.unit
    def test_immutable_when_constructed_then_cannot_modify(self) -> None:
        server = McpServerDef(
            name="fixed",
            command="npx",
            args=(),
            env=(),
            server_type=None,
            url=None,
            disabled=False,
        )
        with pytest.raises(AttributeError):
            server.name = "changed"  # pyright: ignore[reportAttributeAccessIssue]

    @pytest.mark.unit
    def test_construct_when_disabled_then_flag_is_true(self) -> None:
        server = McpServerDef(
            name="off",
            command="npx",
            args=(),
            env=(),
            server_type=None,
            url=None,
            disabled=True,
        )
        assert server.disabled is True
