# Custom returnable container

Use a catalogue recommendation first. If the member requests a custom definition, get the target project, name, internal and external dimensions in mm, wall thickness in mm, tare weight in g, maximum part payload in g, returnability and specification evidence. Ask for an optional unit price in USD and material name when known. Do not invent a payload rating from dimensions or material.

Call `create_container` only when the connected tool is present. It requires `containers:write` and an organization administrator. A member without that role can ask an administrator to create the definition or choose a verified catalogue container.

Use a new idempotency key for a changed specification. Reuse the same key when the response is uncertain. Show the returned specification and its evidence. The record describes the supplied box; manufacturing design, supplier verification and physical load testing remain engineering work.

Pass the returned `container.containerId` and the selected part's `modelId` to `prepare_proposal`. Give the member `checks.reviewUrl` for the website check of the effective checks. Run the proposal after a member confirms them. Explain fit and costs from the saved result, including missing prices. Do not call a box perfect or claim a global optimum from a bounded search.
