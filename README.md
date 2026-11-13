# OptiPacker for Claude

A Claude skill and Claude Code plugin for project-scoped packing proposals, ROI comparisons and what-if scenarios. Available tools depend on the deployed connector, your organization role and your consent.

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
- “Compare the ROI of these packing options before I choose one, and show the cashflow chart.”
- “What if annual demand falls? Keep the original scenario beside that preview.”
- “Save this ROI scenario and give me its review link. I will decide about demand planning later.”
- “Create this custom returnable box from my supplied specification, then compare packing this part in it.”

Claude recommends catalogue containers first. Custom container creation requires an organization administrator and supplied engineering facts. It creates a container record for packing, not a manufactured design. The connector lists accessible definitions; it does not track physical stock counts.

STL transfer needs file/code tools and HTTPS access to the signed storage URL. Before saving, Claude asks for source units and measured part weight, shows material options, and requires a material and cost choice. Enter a part price or explicitly accept the shown raw-material estimate, which excludes manufacturing. Completion prepares the retained mesh for the website viewer and packing. The current limit is 4 MiB with closed geometry.

An older connection needs renewed consent for `models:write`, `containers:write` or `projects:write`. Existing grants keep their original permissions. Refresh the connector's tools list after an upgrade, then start a new chat. Older chats can retain the earlier tool list.

ROI retrieval, comparison and financial images require optional `roi:read` consent. Saving requires `roi:write` and current project write access. Existing connections must reconnect to grant them. ROI comparisons reuse saved packing and consume no proposal run. What-if is a preview until explicitly saved. Unadopted options can be compared, then adopted on the website before saving an operational ROI analysis. Demand planning remains a separate website action.

Native PNG images are returned in tool results. In Claude web, expand the visualization tool result to open the image preview. A separate image attachment in the assistant's final answer depends on the client; the skill directs Claude to the tool preview when it has not created that attachment.

Preparation, catalogue reads and imports consume no proposal run. A completed comparison consumes one run even when no feasible option exists. Before the run, a member of your organization confirms or declines the effective engineering checks on the OptiPacker review page that Claude links. A run waits with `engineering_check_pending` until a member confirms, and a decline returns its reason. Claude reports estimates, unknown costs and search limits. Proposal adoption remains on the OptiPacker website.

## Build and verify

```sh
python -m unittest discover -s tests
python scripts/package_skill.py dist/optipacker.zip
```

The ZIP contains an `optipacker/` folder with `SKILL.md`, references and the upload helper. Python's standard library is sufficient. Credentials and uploaded parts belong to your session and account and are never part of this repository.
