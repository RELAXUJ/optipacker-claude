# Custom returnable container

Use a catalogue recommendation first. If the member requests a custom definition, get the target project, name, internal and external dimensions in mm, wall thickness in mm, tare weight in g, maximum part payload in g, returnability and specification evidence. Ask for an optional unit price when known. For the material, call `list_materials` with `use: container` and let the member choose; pass its `materialId`. A `materialName` alone leaves the material empty in the website container form. Do not invent a payload rating from dimensions or material.

## Price and supplier

Give the price as `unitPriceUsd`, or as `unitPrice { amount, currency }` in the currency of its source (USD, EUR, GBP, CAD, JPY, AUD, CHF or CZK). The server converts it with the stored daily rate and returns `priceEntry` with the rate. If no rate is stored, ask the member for a USD price. Pass `priceEvidence` with the source of the price.

To record who sells the box, call `list_suppliers` first. Link a matching supplier with its `supplierId`. If none matches, call `create_supplier` with the name, address, ISO country code and `sourceEvidence`. An active supplier with the same name refuses the create and names its `supplierId`. New purchase orders of the box preselect the linked supplier.

If the price or the supplier comes from a web page or a document, show the values to the member. Ask whether to use them or whether the member gives their own before you write them. When the page shows more than one price, ask which one, with or without VAT.

To add or change the price, the supplier or the material of a saved project box, call `update_container`; do not create a second container. `supplierId: null` removes the link.

Each container answer has an image of the box and `webUrl`, the page of the box on the website. Show both to the member. `get_visualization` with `kind: container` draws a saved box again.

Call `create_container` only when the connected tool is present. It requires `containers:write` and an organization administrator. A member without that role can ask an administrator to create the definition or choose a verified catalogue container.

Use a new idempotency key for a changed specification. Reuse the same key when the response is uncertain. Show the returned specification and its evidence. The record describes the supplied box; manufacturing design, supplier verification and physical load testing remain engineering work.

Pass the returned `container.containerId` and the selected part's `modelId` to `prepare_proposal`. If `checks.status` is `confirmed`, a standing profile confirmed the checks, so run the proposal. Otherwise give the member `checks.reviewUrl` for the website check of the effective checks. Run the proposal after a member confirms them. Explain fit and costs from the saved result, including missing prices. Do not call a box perfect or claim a global optimum from a bounded search.
