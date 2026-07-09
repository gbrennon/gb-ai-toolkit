from ai_toolkit.install_agent_rules.parsing.load_rules_dir import load_rules_entries


class TestLoadRulesEntries:
    def test_with_numbered_files_then_returns_sorted(self) -> None:
        files = {
            "00-base.md": "# Base",
            "10-tools.md": "# Tools",
            "05-middle.md": "# Middle",
        }
        rules = load_rules_entries(files)
        assert [r.order for r in rules] == [0, 5, 10]
        assert [r.name for r in rules] == ["base", "middle", "tools"]

    def test_with_empty_dict_then_returns_empty_list(self) -> None:
        assert load_rules_entries({}) == []

    def test_with_non_md_files_then_ignores_them(self) -> None:
        files = {
            "00-base.md": "# Base",
            "readme.txt": "# Readme",
            "99-end.md": "# End",
        }
        rules = load_rules_entries(files)
        assert len(rules) == 2
        assert [r.name for r in rules] == ["base", "end"]

    def test_without_number_prefix_then_ignored(self) -> None:
        files = {
            "00-base.md": "# Base",
            "random.md": "# Random",
        }
        rules = load_rules_entries(files)
        assert len(rules) == 1
        assert rules[0].name == "base"