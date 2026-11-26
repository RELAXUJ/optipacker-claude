"""Publish the committed plugin version to the public repository and create its GitHub release.

Run from integrations/claude:  python scripts/publish_release.py --notes "What changed."
Add --dry-run to stop before the push and the release.

The script checks the version marks, runs the package tests and refuses a version that has a release.
It refuses package files that differ from origin/development. It copies them into a clone of the public repository,
commits and tags the version, pushes main and the tag, builds optipacker.zip and creates the release with it.
Claude Code installs update from main. Claude web and desktop download the ZIP of the latest release.
deploy:prod refuses a web release whose plugin version has no release (scripts/check-claude-plugin-published.mjs).
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "RELAXUJ/optipacker-claude"


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command, cwd, check=True):
    print("+", " ".join(command))
    return subprocess.run(command, cwd=cwd, check=check, text=True, capture_output=not check)


def committed_package_files():
    """Answer the tracked files of the package. Refuse changes that are not on origin/development.

    The release then equals the package of origin/development, which the next server build reads.
    """
    status = subprocess.run(["git", "status", "--porcelain", "--", "."], cwd=ROOT, check=True, text=True, capture_output=True)
    if status.stdout.strip():
        sys.exit(f"Commit the package changes first:\n{status.stdout}")
    run(["git", "fetch", "origin", "development"], ROOT)
    if run(["git", "diff", "--quiet", "origin/development", "HEAD", "--", "."], ROOT, check=False).returncode != 0:
        sys.exit("The package differs from origin/development. Push the package commits, or update this checkout.")
    listed = subprocess.run(["git", "ls-files", "-z", "--", "."], cwd=ROOT, check=True, text=True, capture_output=True)
    return [Path(name) for name in listed.stdout.split("\0") if name]


def copy_package(files, clone):
    for entry in clone.iterdir():
        if entry.name == ".git":
            continue
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    for relative in files:
        target = clone / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)


def publish(notes, dry_run):
    version = load("plugin_versions").checked_version()
    tag = f"v{version}"
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], ROOT)
    if run(["gh", "release", "view", tag, "--repo", REPOSITORY], ROOT, check=False).returncode == 0:
        sys.exit(f"{REPOSITORY} already has the release {tag}. Raise the version first.")
    files = committed_package_files()
    with tempfile.TemporaryDirectory() as directory:
        clone = Path(directory) / "public"
        run(["gh", "repo", "clone", REPOSITORY, str(clone), "--", "--depth", "1"], ROOT)
        copy_package(files, clone)
        run(["git", "add", "-A"], clone)
        if run(["git", "diff", "--cached", "--quiet"], clone, check=False).returncode == 0:
            sys.exit("The public repository already holds these files. Nothing to publish.")
        run(["git", "commit", "-m", f"release: OptiPacker for Claude {version}", "-m", notes], clone)
        run(["git", "tag", tag], clone)
        archive = Path(directory) / "optipacker.zip"
        load("package_skill").build(archive)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        if dry_run:
            run(["git", "show", "--stat", "--format=%s", "HEAD"], clone)
            print(f"Dry run: {tag} is ready and not pushed. ZIP SHA-256 {digest}")
            return
        run(["git", "push", "origin", "HEAD:main", tag], clone)
        run(["gh", "release", "create", tag, str(archive), "--repo", REPOSITORY,
             "--title", f"OptiPacker for Claude {version}", "--notes", notes], ROOT)
        print(f"Published {tag}. ZIP SHA-256 {digest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--notes", required=True, help="Release notes: what changed for the user.")
    parser.add_argument("--dry-run", action="store_true", help="Stop before the push and the release.")
    arguments = parser.parse_args()
    publish(arguments.notes, arguments.dry_run)
