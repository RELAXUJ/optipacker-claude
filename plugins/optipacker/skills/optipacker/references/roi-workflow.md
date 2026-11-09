# Packing, ROI and what-if

Use the advertised input schemas. Existing connections need renewed consent for `roi:read` and, when saving is requested, `roi:write`. These scopes are optional on the consent page. Project access and current write permissions still apply.

## Start with the decision

For a new project, compare feasible packing options and their programme costs and financial outcomes. For an existing operation, ask whether the member wants savings against a saved baseline and use its verified identity. Two alternative designs alone do not establish savings against current operations.

After `get_proposal`, select a few relevant options. Call `compare_roi_scenarios` with up to five named scenarios. A source is either `{ "kind": "proposal", "proposalId": "<returned ID>", "revision": 1, "candidateId": "<returned option ID>" }` or `{ "kind": "analysis", "analysisId": "<saved analysis ID>" }`. Copy the actual returned revision. Do not substitute a container ID for a candidate ID.

The comparison reuses saved packing. It does not run optimization, consume another proposal allowance, adopt an option or write project data. Keep unavailable costs and missing financial metrics visible. Compare the financial period, demand and cost assumptions before identifying a preferred result.

## What-if

Add only the requested `whatIf` fields, or the advertised volume-profile override, to a scenario. Follow the tool schema for names, ranges and units. Ask for a missing assumption rather than inventing it. Keep a named unchanged scenario beside the changed one when explaining impact.

When returned assumptions include `demandByYear`, change demand through the full `volumeProfile` override. `whatIf.annualDemand` is for scalar-demand analyses without a yearly profile. Preserve the requested programme years and use fixed yearly counts that satisfy the advertised schema.

Monetary what-if inputs are USD, including fixed income per part, freight and loading charges. Ask for USD amounts or use a verified exchange rate supplied by OptiPacker. Do not pass an organization-currency amount unchanged as USD.

For replacement changes, read `assumptions.materials[]` and copy the intended row's `materialId`. Each row includes its name, returnability, effective replacement fraction and loading-unit quantity. Set `whatIf.returnableSystemCosts.bomReplacementRates` with that ID and the requested annual fraction from 0 to 1. For example, a requested 10% tray replacement rate uses `{"returnableSystemCosts":{"bomReplacementRates":{"<returned tray materialId>":0.10}}}` inside `whatIf`. A tray design ID, embedded insert ID, container ID or row name is not a BOM `materialId`. Unknown material IDs are rejected. A single-use material must keep fraction 1; another per-material value is rejected. If `assumptions.materialsTruncated` is true, use the website for unlisted materials rather than guessing their IDs.

The global `whatIf.returnableSystemCosts.replacementRate` changes non-insert BOM rows, such as containers and pallets. It preserves insert and protective tray rates. Use a per-material override to change an insert or tray, or to change just one container or pallet. Keep all other rows unchanged unless the member requested a wider change.

Packing capacity is not a financial what-if field. Select another evaluated packing candidate for a layout change. Re-run packing only when the geometry, clearances, rotations or container scope changes.

The returned average annual net cashflow, ROI, investment and break-even belong to the stated programme and cost coverage. They are not automatically savings against current packing. A preview does not apply assumptions to the project.

`cumulativeReturnRoi` is a decimal ratio: `0.25` means 25%. `combinedRoiPercent` and `irrPercent` are already percentages. Use `cashflowGranularity` for the period labels.

## Images in chat

Call `get_visualization` with `kind: "roi"` and the same scenarios to obtain a comparison chart. Use `kind: "packing"` with the saved proposal reference and candidate ID for stored part position bounds. The MCP returns an image content block plus accessible metadata. Show the image with its figures and review link. Tray bodies and cavities are not drawn. Retain returned `packingContext`, including the protective tray specification and engineering pending status, beside images, financial previews and saved ROI.

In Claude web, direct the member to expand the tool result to open its native image preview. Use "attached" or "below" only for a separate message attachment you have created. Keep the figures and review link in the response when the client shows the image only in the tool preview.

If the response says the image is unavailable, use its reason and link. Do not make up a layout for a bulk estimate or describe a bounds view as a mesh render. Rendering an image uses no proposal allowance run.

## Save and hand off

Use `get_roi_analysis` to read a saved analysis. Use `save_roi_scenario` only after the member requests a named save. Pass the scenario and a new idempotency key. Retry the same request with the same key. A changed scenario needs a different key.

An unadopted proposal option returns `adoption_required`. Give its website review link so the member can choose and adopt packing. Do not silently adopt it. After a successful save, return the saved analysis link and offer further what-if work or the demand-planning handoff.

Demand planning requires a saved, complete analysis with a valid packing basis. Follow the returned next actions and website validation. It remains separate from saving ROI and from ordering.
