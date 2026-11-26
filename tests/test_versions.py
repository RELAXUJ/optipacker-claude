import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "plugin_versions.py"
spec = importlib.util.spec_from_file_location("plugin_versions", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VersionTest(unittest.TestCase):
    def test_every_version_mark_names_the_same_version(self):
        versions = module.read_versions()
        self.assertEqual(len(set(versions.values())), 1, versions)
        self.assertRegex(module.checked_version(), r"^\d+\.\d+\.\d+$")

    def test_the_skill_asks_for_the_version_check_on_the_first_context_call(self):
        skill = module.SKILL.read_text(encoding="utf-8")
        self.assertIn("## Check the skill and connector versions", skill)
        self.assertIn("connector.skill.status", skill)
        self.assertIn("updateSteps.claudeCode", skill)
        self.assertIn("updateSteps.claudeWeb", skill)


if __name__ == "__main__":
    unittest.main()
