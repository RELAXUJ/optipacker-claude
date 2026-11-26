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

## Updates

The skill checks its version in each conversation. It passes its version to `get_project_context`, and the server compares it with the version of this repository. If a newer version exists, Claude tells you once and gives the steps for your client.

- Claude Code: turn on auto-update once. Open `/plugin`, select Marketplaces, select optipacker and turn on auto-update. Later versions then install at startup. To update now, run `claude plugin marketplace update optipacker` and `claude plugin update optipacker@optipacker`, then `/reload-plugins`. Claude can run these commands for you after you agree.
- Claude web and desktop: download the latest [optipacker.zip](https://github.com/RELAXUJ/optipacker-claude/releases/latest/download/optipacker.zip). In Customize > Skills, delete the optipacker skill, upload the ZIP and turn it on.

The connector runs on the OptiPacker server, so it needs no update. Claude tells you when your tool list is older than the server, or when a request needs a permission that your connection does not hold. Then reconnect the connector and start a new chat.

## Requests to try

- “Which returnable containers can I use for this project? Show internal dimensions, payload limits and prices.”
- “Save this STL in my selected project. The source units are mm and the measured part weight is 120 g.”
- “Recommend a returnable container for this part, run the packing comparison, and explain why.”
- “Compare the recommended packing with the current saved configuration.”
- “Compare the ROI of these packing options before I choose one, and show the cashflow chart.”
- “What if annual demand falls? Keep the original scenario beside that preview.”
- “Save this ROI scenario and give me its review link. I will decide about demand planning later.”
- “Create this custom returnable box from my supplied specification, then compare packing this part in it.”
- “Check whether our decision policy lets you adopt the recommended option. Adopt it only if every rule passes.”

Claude recommends catalogue containers first. Custom container creation requires an organization administrator and supplied engineering facts. It creates a container record for packing, not a manufactured design. The connector lists accessible definitions; it does not track physical stock counts.

STL transfer needs file/code tools and HTTPS access to the signed storage URL. Before saving, Claude asks for source units and measured part weight, shows material options, and requires a material and cost choice. Enter a part price or explicitly accept the shown raw-material estimate, which excludes manufacturing. Completion prepares the retained mesh for the website viewer and packing. The current limit is 4 MiB with closed geometry.

An older connection needs renewed consent for `models:write`, `containers:write`, `projects:write` or `proposals:adopt`. Existing grants keep their original permissions. Refresh the connector's tools list after an upgrade, then start a new chat. Older chats can retain the earlier tool list.

ROI retrieval, comparison and financial images require optional `roi:read` consent. Saving requires `roi:write` and current project write access. Existing connections must reconnect to grant them. ROI comparisons reuse saved packing and consume no proposal run. What-if is a preview until explicitly saved. Unadopted options can be compared. An option needs an adoption before you save an operational ROI analysis. A member adopts on the website, or Claude adopts the recommended option with `proposals:adopt`. Demand planning remains a separate website action.

Native PNG images are returned in tool results. In Claude web, expand the visualization tool result to open the image preview. A separate image attachment in the assistant's final answer depends on the client; the skill directs Claude to the tool preview when it has not created that attachment.

Preparation, catalogue reads and imports consume no proposal run. A completed comparison consumes one run even when no feasible option exists. Before the run, a member of your organization confirms or declines the effective engineering checks on the OptiPacker review page that Claude links. If the four check values, the part revision, the supplied trays and the explicit coverage entries equal the active standing profile of the part, the quote needs no review. A run waits with `engineering_check_pending` until a member confirms, and a decline returns its reason. Claude reports estimates, unknown costs and search limits. A member adopts a proposal option on the OptiPacker website. With the optional `proposals:adopt` consent, Claude adopts only the recommended option of a run, inside the decision policy that your organization administrator sets. You get a notice and a mail of each adoption.

## Build and verify

For unattended work, request an unattended connection during consent. An organization administrator approves and renews its UTC end date in Settings, Connected agents. Approved unattended runs require a standing engineering profile, and unattended connections cannot adopt packing. A daily source watch records changes to adopted packing without starting a run or changing the packing. `list_agent_events` reads pending checks, finished runs, source changes and ending profiles within the connection's projects. See the skill's [connection and events reference](plugins/optipacker/skills/optipacker/references/unattended-and-events.md).

```sh
python -m unittest discover -s tests
python scripts/package_skill.py dist/optipacker.zip
```

To publish a version, raise it in `plugin.json`, the `marketplace.json` entry and the version lines of `SKILL.md`, and commit. Then run `python scripts/publish_release.py --notes "What changed."`. The script refuses version marks that differ and a version that already has a release. It pushes the files to `main` of the public repository, tags the version and creates the release with the ZIP. Add `--dry-run` to stop before the push.

The ZIP contains an `optipacker/` folder with `SKILL.md`, references and the upload helper. Python's standard library is sufficient. Credentials and uploaded parts belong to your session and account and are never part of this repository.
