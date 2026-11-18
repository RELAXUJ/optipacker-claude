# Unattended connections and agent events

Use the tools and schemas advertised by the connected server. If it omits `list_agent_events`, use the website's notifications and agent review pages.

## Choose the connection

A personal connection remains available for interactive work. To request unattended access, the member selects "Run this assistant without me (unattended connection)" on the consent page. That choice removes `proposals:adopt` from the selected permissions. Other selected permissions remain.

An organization administrator opens Settings, Connected agents, and approves the request with a last day in UTC. Until approval, it works as a personal connection. An approval lasts up to 90 days. The administrator can renew it before the end date. After it ends, the member connects again and an administrator approves the new request. A revoked connection also needs a new sign-in and consent.

For the same member and client, a new personal consent replaces earlier personal grants. An unattended request replaces earlier requested or approved unattended grants. The two kinds can coexist. Check the named connection before asking the member to reconnect.

## Start an unattended run

An approved unattended connection starts a proposal run only through a standing engineering profile. The profile must match the part revision, all four engineering checks, the supplied trays and the explicit coverage entries of the prepared quote. Evidence text does not count. Its approver must still have an approver role, and its end date must still allow preparation. Give the member the website review link when a profile needs approval or renewal. Never claim to approve checks or renew access in chat.

Approval and profiles do not remove the paid-run requirement. A completed calculation uses one proposal run. Start one only within the member's requested task and budget. Preserve one idempotency key when retrying the same request. A source-change notice gives no permission to calculate again.

Requested and approved unattended connections cannot adopt a proposal option. Use the website review link for a member decision. A personal connection can use `adopt_proposal_option` only with its consent scope and the organization's decision policy. The current policy still requires the first adoption and no existing active or outdated packing.

## Read events

Call `list_agent_events` with no arguments and `projects:read` consent. The answer contains:

- `connection`: whether this connection is unattended, with `endsAt` when it is.
- `waitingQuotes`: up to 50 live quotes waiting for engineering checks. Each has a website review link and `thisConnection`.
- `finishedRuns`: up to 50 saved or released agent runs from the latest 100 organization run records. A saved run names its proposal and revision. A released run saved no result and used no allowance run.
- `changes`: up to 50 change records for adopted packing, naming the project, part, proposal revision, source kinds and detection time.
- `endingProfiles`: up to 50 profiles that have ended or end within 30 days.

Each list covers only projects this connection can currently read. `truncated` means the answer shows a bounded subset. The answer holds no cost figures, member names or grant IDs. Use the saved proposal tools for authorized result details.

Summarize events that need attention and link to the website. `thisConnection: false` means another connection owns a waiting quote. `run_proposal` returns `not_found` for that quote; do not retry it through this connection. An ended profile needs a member's website action.

Each connection has six event calls per 60-minute window. Poll only when the member asks for ongoing checks, with at least ten minutes between calls. On `rate_limited`, wait for the stated retry time. Event reads consume no proposal run.

## Explain a source-change notice

Once a day, OptiPacker compares adopted packing sources with their current state. Source kinds are project inputs, part, container, pallet, blister catalogue, baseline packing and baseline packing result. The case timeline shows "Change detected" and the changed source labels. The adopter gets an app notice. Pending notices are grouped into at most one email per adopter per UTC day; later pending items can appear on a later day.

The notice leaves adopted packing unchanged and starts no run. Explain which source changed, read its current facts when authorized, and ask for the member's next action. For a requested recalculation, prepare a fresh quote and follow its engineering checks and allowance. Never treat a notice as approval to replace existing packing.
