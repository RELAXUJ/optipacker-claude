"""Read the four version marks of the OptiPacker plugin and check that they agree.

The marks are the plugin manifest, the marketplace entry, the version line of SKILL.md
and the skillVersion that SKILL.md tells Claude to pass to get_project_context.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / "plugins" / "optipacker" / ".claude-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
SKILL = ROOT / "plugins" / "optipacker" / "skills" / "optipacker" / "SKILL.md"
VERSION = re.compile(r"^\d{1,4}\.\d{1,4}\.\d{1,4}$")


def read_versions():
    """Answer each version mark by its name. A missing mark is None."""
    manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    entry = next((plugin for plugin in marketplace.get("plugins", []) if plugin.get("name") == "optipacker"), {})
    skill = SKILL.read_text(encoding="utf-8")
    stated = re.search(r"This is skill version (\S+?)\.\s", skill)
    passed = re.search(r'skillVersion: "([^"]+)"', skill)
    return {
        "plugin.json": manifest.get("version"),
        "marketplace.json": entry.get("version"),
        "SKILL.md version line": stated.group(1) if stated else None,
        "SKILL.md skillVersion": passed.group(1) if passed else None,
    }


def checked_version():
    """Answer the plugin version, or raise ValueError when a mark is missing, malformed or different."""
    versions = read_versions()
    values = set(versions.values())
    if len(values) != 1 or None in values:
        raise ValueError(f"The version marks differ: {versions}")
    version = values.pop()
    if not VERSION.match(version):
        raise ValueError(f"The version {version} is not major.minor.patch")
    return version


if __name__ == "__main__":
    print(checked_version())
