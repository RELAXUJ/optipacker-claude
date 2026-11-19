# Cost gaps before a run

An unknown cost lowers the precision of the result. An option with an unknown cost gets no comparable cost and no rank. Its known total leaves out the unknown cost, so the real cost is higher. If no option has complete costs, the outcome is unranked.

## Ask before the run

1. Before the first preparation, ask the member about these costs: one-time charges, washing, maintenance, disposal, handling, switching, residual value and logistics.
2. After each preparation, read `costGaps.unknown` to the member. Name the cost type and its item, for example "washing of the catalogue blister".
3. Explain `costGaps.effect` in plain words. For example: "Without the blister washing cost, OptiPacker cannot rank the options. The totals leave that cost out, so the real cost is higher."
4. Offer the ways of `closeWith` for each gap. Let the member choose.
5. If the member gives an amount or an exclusion, prepare again with it. Each preparation saves a new quote.
6. If the member accepts the gaps, run the quote. Tell the member that the result can stay unranked.

Never fill a value, a zero or an exclusion yourself. Never derive the cost of one piece from an annual total. An exclusion needs the member's reason.

## Ways to close a gap

| `closeWith` | Ask the member for | Input |
|---|---|---|
| `amount`, `overrides.costOptions.additionalCosts` | Handling, switching or residual value in USD for each calendar year, with evidence. | `category`, `year`, `amount` (`{value, unit: "usd"}`), `evidence`. Handling needs each programme year with parts. |
| `amount`, `overrides.materialAssumptions` | The cost of one piece for the named `field`: wash price for each wash, maintenance for each year, disposal for each discarded piece, or the annual replacement fraction. | One entry for each role (`sourceType`) with `values` and `evidence`. A catalogue blister and a supplied tray use the role `insert`. |
| `amount`, `website_project_logistics` | The project logistics settings. | No MCP input. The member enters them on the website. |
| `not_applicable`, `costScope` | A reason why the cost type does not apply. | `costScope.notApplicable` and `costScope.reason`. |
| `not_applicable`, `overrides.costOptions.coverage` | A reason why the cost does not apply. | An entry `{category, status: "not-applicable", evidence}`. Without `materialId`, it covers each item without a recorded or library value. With a value of `materialIds`, it covers that container only. |
| `accept_gap` | The member's acceptance. | No input. |

`overrides.materialAssumptions` replaces the default roles. Copy the `container` and `pallet` entries of `reviewBrief.materialAssumptions` into the array, then add the `insert` entry. Otherwise the container and pallet lose their library estimates.

## Read the forecast

- `estimates` lists container and pallet costs from the operating library. Call them estimates.
- The same cost type can be an estimate for one item and unknown for another item. For example, the container washing is a library estimate and the blister washing is unknown. Name the item each time.
- `condition: returnable_blister`: the gap applies if the fitted catalogue blister is returnable.
- `condition: blister_with_unpriced_charge`: a catalogue tooling charge has no price. Only acceptance closes it. The website review names the charge.
- `condition: project_logistics_incomplete`: the run calculates logistics from the project logistics settings.
- An annual total of washing, maintenance or disposal has no input in MCP or on the website. Ask for the cost of one piece, or for acceptance of the gap.
- The forecast holds no figure. The run can still find a gap, for example a container without a price.
