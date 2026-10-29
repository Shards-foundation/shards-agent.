#!/usr/bin/env python3
"""Apply the Shards Agent distribution identity to an upstream Hermes checkout.

This deliberately preserves upstream code identifiers, URLs for upstream services,
the original MIT LICENSE, and historical attribution. Run after merging the target
repository's bootstrap history into the upstream checkout.
"""
from __future__ import annotations

import json
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()


def replace_once(text: str, old: str, new: str) -> str:
    return text.replace(old, new, 1) if old in text else text


readme = ROOT / "README.md"
text = readme.read_text()
text = text.replace('alt="Hermes Agent"', 'alt="Shards Agent"')
text = replace_once(text, "assets/banner.png", "assets/shards-banner.svg")
text = replace_once(text, "# Hermes Agent ☤", "# Shards Agent")
text = replace_once(
    text,
    '  <a href="https://hermes-agent.nousresearch.com/">Hermes Agent</a> | <a href="https://hermes-agent.nousresearch.com/">Hermes Desktop</a>',
    '  <a href="https://github.com/Shards-foundation/shards-agent.">Shards Agent</a> | <a href="https://github.com/Shards-foundation/shards-agent.">Source repository</a>',
)
text = text.replace(
    "https://github.com/NousResearch/hermes-agent/blob/main/LICENSE",
    "https://github.com/Shards-foundation/shards-agent./blob/main/LICENSE",
)
text = text.replace(
    "https://img.shields.io/badge/Built%20by-Nous%20Research-blueviolet?style=for-the-badge",
    "https://img.shields.io/badge/Distribution-Shards%20Foundation-black?style=for-the-badge",
)
text = text.replace('alt="Built by Nous Research"', 'alt="Distributed by Shards Foundation"')
text = replace_once(
    text,
    "**The self-improving AI agent built by [Nous Research](https://nousresearch.com).**",
    "**Shards Agent** is the Shards Foundation distribution of Hermes Agent, originally created by [Nous Research](https://nousresearch.com). It retains the upstream agent capabilities while this repository develops Shards-specific integrations.",
)
text = text.replace(
    '<a href="https://nousresearch.com"><img src="https://img.shields.io/badge/Distribution-Shards%20Foundation-black?style=for-the-badge" alt="Distributed by Shards Foundation"></a>',
    '<a href="https://github.com/Shards-foundation/shards-agent."><img src="https://img.shields.io/badge/Distribution-Shards%20Foundation-black?style=for-the-badge" alt="Distributed by Shards Foundation"></a>',
)
readme.write_text(text)

# Keep translated documentation intact while replacing its visible product title
# and image alt text where those exact upstream strings are present.
for path in ROOT.glob("README*.md"):
    if path.name == "README.md":
        continue
    translated = path.read_text()
    translated = translated.replace('alt="Hermes Agent"', 'alt="Shards Agent"')
    translated = replace_once(translated, "assets/banner.png", "assets/shards-banner.svg")
    translated = re.sub(r"(?m)^# Hermes Agent(?:\s+.*)?$", "# Shards Agent", translated, count=1)
    path.write_text(translated)

pyproject = ROOT / "pyproject.toml"
text = pyproject.read_text()
text = replace_once(text, 'name = "hermes-agent"', 'name = "shards-agent"')
text = replace_once(
    text,
    'description = "The self-improving AI agent — creates skills from experience, improves them during use, and runs anywhere"',
    'description = "Shards Agent — Shards Foundation distribution of the self-improving AI agent"',
)
text = replace_once(text, 'authors = [{ name = "Nous Research" }]', 'authors = [{ name = "Shards Foundation" }]\n# Derived from Hermes Agent by Nous Research; see LICENSE and upstream attribution.')
text = text.replace("hermes-agent[", "shards-agent[")
text = replace_once(
    text,
    'hermes-agent = "agent.legacy_cli:main"',
    'shards-agent = "agent.legacy_cli:main"\nhermes-agent = "agent.legacy_cli:main"  # Compatibility alias for existing users.',
)
if 'shards = "hermes_cli.main:main"' not in text:
    text = replace_once(
        text,
        'hermes = "hermes_cli.main:main"',
        'shards = "hermes_cli.main:main"\nhermes = "hermes_cli.main:main"  # Compatibility alias for existing users.',
    )
text = text.replace(
    "Building wheels or sdists for hermes-agent is not supported.",
    "Building wheels or sdists for shards-agent is not supported.",
)
pyproject.write_text(text)

package_json = ROOT / "package.json"
if package_json.exists():
    data = json.loads(package_json.read_text())
    data["name"] = "shards-agent"
    data["repository"] = {
        "type": "git",
        "url": "git+https://github.com/Shards-foundation/shards-agent..git",
    }
    data["bugs"] = {"url": "https://github.com/Shards-foundation/shards-agent./issues"}
    data["homepage"] = "https://github.com/Shards-foundation/shards-agent.#readme"
    package_json.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

branding = ROOT / "SHARDS_BRANDING.md"
branding.write_text("""# Shards Agent

Shards Agent is the Shards Foundation distribution of Hermes Agent, originally created by Nous Research.

- Destination repository: https://github.com/Shards-foundation/shards-agent.
- Upstream project: https://github.com/NousResearch/hermes-agent
- Licence: MIT. The original upstream LICENSE and copyright notices remain intact.
- Python distribution: shards-agent.
- Primary CLI alias: shards-agent.
- Compatibility CLI aliases: hermes and hermes-agent.

The upstream project history is retained. Technical identifiers and URLs that are part of
the upstream runtime or refer to upstream-operated services are intentionally preserved
where changing them would break compatibility or point to a service that does not exist.
""")

banner = ROOT / "assets" / "shards-banner.svg"
banner.parent.mkdir(parents=True, exist_ok=True)
banner.write_text("""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="360" viewBox="0 0 1600 360" role="img" aria-labelledby="title desc">
<title id="title">Shards Agent</title><desc id="desc">Shards Agent, an open source AI agent distribution by Shards Foundation.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#080808"/><stop offset="1" stop-color="#202020"/></linearGradient><linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff0a3"/><stop offset=".45" stop-color="#d4af37"/><stop offset="1" stop-color="#8b6a14"/></linearGradient></defs>
<rect width="1600" height="360" rx="22" fill="url(#bg)"/><path d="M0 300 L390 0 M1160 360 L1540 0" stroke="#d4af37" stroke-opacity=".16" stroke-width="2"/>
<g transform="translate(110 75)"><path d="M90 0 L165 45 L140 132 L55 175 L0 120 L25 35 Z" fill="none" stroke="url(#gold)" stroke-width="8" stroke-linejoin="round"/><path d="M25 35 L95 70 L165 45 M95 70 L55 175 M95 70 L140 132 M0 120 L95 70" fill="none" stroke="url(#gold)" stroke-width="6" stroke-linejoin="round"/><path d="M95 70 L119 103 L84 127 Z" fill="url(#gold)"/></g>
<text x="350" y="165" fill="#f5f5f5" font-family="Inter,Arial,sans-serif" font-size="78" font-weight="750" letter-spacing="5">SHARDS AGENT</text>
<text x="356" y="222" fill="#d4af37" font-family="Inter,Arial,sans-serif" font-size="26" font-weight="600" letter-spacing="6">AUTONOMOUS AI · OPEN SOURCE · SHARDS FOUNDATION</text>
<path d="M355 254 H1030" stroke="#d4af37" stroke-opacity=".7" stroke-width="2"/>
</svg>
""")

test = ROOT / "tests" / "shards" / "test_distribution_metadata.py"
test.parent.mkdir(parents=True, exist_ok=True)
test.write_text('''"""Contract tests for the Shards Agent distribution metadata."""
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
''')

# Rebrand user-visible product names throughout tracked text files while
# retaining the upstream MIT licence, explicit origin attribution, and URLs
# for services/repos operated by Nous Research.
tracked = subprocess.run(
    ["git", "ls-files", "-z"],
    cwd=ROOT,
    check=True,
    stdout=subprocess.PIPE,
).stdout.split(b"\0")
text_suffixes = {
    ".md", ".rst", ".txt", ".py", ".sh", ".ps1", ".cmd", ".bat",
    ".toml", ".yaml", ".yml", ".json", ".ts", ".tsx", ".js", ".jsx",
    ".html", ".css", ".xml", ".ini", ".cfg", ".env", ".properties",
}
skip_paths = {
    "LICENSE",
    "SHARDS_BRANDING.md",
    "scripts/shards_rebrand.py",
    "pyproject.toml",
    "package.json",
    "uv.lock",
    "flake.lock",
    ".github/workflows/shards-upstream-migration.yml",
    "tests/shards/test_distribution_metadata.py",
}
for raw_path in tracked:
    if not raw_path:
        continue
    rel = raw_path.decode("utf-8", errors="surrogateescape")
    if rel in skip_paths or rel.endswith("package-lock.json"):
        continue
    path = ROOT / rel
    if not path.is_file() or path.suffix.lower() not in text_suffixes:
        continue
    try:
        original = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    if "\0" in original:
        continue

    if rel == "README.md":
        lines = []
        for line in original.splitlines(keepends=True):
            # Preserve the one explicit sentence crediting the original project.
            if "originally created by [Nous Research]" not in line:
                line = line.replace("Hermes Agent", "Shards Agent")
                line = line.replace("Hermes Desktop", "Shards Desktop")
            lines.append(line)
        updated = "".join(lines)
    else:
        updated = original.replace("Hermes Agent", "Shards Agent")
        updated = updated.replace("Hermes Desktop", "Shards Desktop")

    # Documentation commands are rebranded, but upstream repository and service
    # URLs remain untouched so attribution links never point to a fake endpoint.
    if path.suffix.lower() in {".md", ".rst", ".txt"}:
        doc_lines = []
        for line in updated.splitlines(keepends=True):
            if (
                "github.com/NousResearch/hermes-agent" not in line
                and "hermes-agent.nousresearch.com" not in line
            ):
                line = re.sub(r"\bhermes-agent\b", "shards-agent", line)
            doc_lines.append(line)
        updated = "".join(doc_lines)

    if rel == ".github/CODEOWNERS":
        updated = updated.replace("@NousResearch/hermes-agent-core", "@Shards-inc")
    if updated != original:
        path.write_text(updated, encoding="utf-8")

print(f"Applied Shards branding to {ROOT}")
