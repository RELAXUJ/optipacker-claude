# OptiPacker for Claude

A Claude skill and Claude Code plugin for working with project-scoped OptiPacker packing proposals. Available tools depend on the deployed connector and your consent. The extended upload and container tools are implemented on OptiPacker's development branch and require a production release before they appear on optipacker.com.

## Claude web and desktop

1. Download [optipacker.zip](https://github.com/RELAXUJ/optipacker-claude/releases/latest/download/optipacker.zip).
2. Enable code execution and file creation in Claude's capabilities, then upload the ZIP in Skills and enable it. Your organization's settings may control custom skill access. See [Anthropic's installation guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
3. Add a custom connector with MCP server URL `https://optipacker.com/api/mcp`.
4. Sign in to OptiPacker and select the projects and permissions you want Claude to use. Read the consent page before allowing access.

The skill teaches the workflow. The connector provides account access. Each is installed separately in Claude web and desktop.

## Claude Code

```text
/plugin marketplace add RELAXUJ/optipacker-claude
/plugin install optipacker@optipacker
```

Open `/mcp` to authenticate the OptiPacker server. The plugin includes the remote HTTP connector and the skill. See [Anthropic's marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces).

## Requests to try

- “Which returnable containers can I use for this project? Show internal dimensions, payload limits and prices.”
- “Save this STL in my selected project. The source units are mm and the measured part weight is 120 g.”
- “Recommend a returnable container for this part, run the packing comparison, and explain why.”
- “Compare the recommended packing with the current saved configuration.”
- “Create this custom returnable box from my supplied specification, then compare packing this part in it.”

Claude recommends catalogue containers first. Custom container creation requires an organization administrator and supplied engineering facts. It creates a container record for packing, not a manufactured design. The connector lists accessible definitions; it does not track physical stock counts.

STL transfer needs file/code tools and HTTPS access to the signed storage URL. Claude asks for source units and measured part weight. The current import path accepts STL files up to 4 MiB and requires closed geometry. An older connection needs renewed consent for `models:write` or `containers:write`; existing grants keep their original permissions.

Preparation, catalogue reads and imports consume no proposal run. A completed comparison consumes one run even when no feasible option exists. The member confirms the effective engineering checks before the run. Claude reports estimates, unknown costs and search limits. Proposal adoption remains on the OptiPacker website.

## Build and verify

```sh
python -m unittest discover -s tests
python scripts/package_skill.py dist/optipacker.zip
```

The ZIP contains an `optipacker/` folder with `SKILL.md`, references and the upload helper. Python's standard library is sufficient. Credentials and uploaded parts belong to your session and account and are never part of this repository.
