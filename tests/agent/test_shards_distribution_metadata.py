"""Contract tests for the Shards Agent distribution metadata."""
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[2]


def test_python_distribution_uses_shards_agent_name():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    assert project["name"] == "shards-agent"


def test_shards_cli_entrypoint_exists_with_upstream_compatibility_alias():
    scripts = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["scripts"]
    assert scripts["shards"] == "hermes_cli.main:main"
    assert scripts["shards-agent"] == "agent.legacy_cli:main"
    assert scripts["hermes-agent"] == "agent.legacy_cli:main"


def test_upstream_mit_license_and_attribution_are_preserved():
    license_text = (ROOT / "LICENSE").read_text()
    attribution = (ROOT / "SHARDS_BRANDING.md").read_text()
    assert "MIT License" in license_text
    assert "Nous Research" in license_text
    assert "originally created by Nous Research" in attribution


def test_shards_branding_assets_and_readme_are_present():
    assert (ROOT / "assets" / "shards-banner.svg").is_file()
    assert "Shards Agent" in (ROOT / "README.md").read_text()
