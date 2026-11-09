# STL attachment transfer

This flow needs `models:write`, file/code tools with access to the attachment and outbound HTTPS access to the returned storage URL. If transfer is unavailable, use the OptiPacker website upload and resume from the saved part ID.

1. Resolve the project and ask for the source units (`mm`, `cm`, `m` or `in`) and measured weight in g. Get the intended part name.
2. Run `python scripts/upload_stl.py inspect /absolute/path/part.stl` from this skill folder. It reports `originalFileName`, `byteLength` and `sha256` without reading engineering facts from the file.
3. Call `prepare_stl_upload` with those facts, `projectId`, `name`, `sourceLengthUnit`, `measuredWeightG` and `idempotencyKey`. The server currently accepts bounded, closed STL geometry. Use the runtime schema for the current size limit.
4. If the response says `awaiting_upload`, save its JSON to a private temporary ticket file and run `python scripts/upload_stl.py upload /absolute/path/part.stl --ticket /absolute/path/ticket.json`. The helper PUTs the original bytes using the returned headers. Do not expose the signed URL in the chat or repository. Delete the temporary ticket after transfer.
5. Call `complete_stl_upload` with `projectId` and `uploadId`. If preparation already says `completed`, proceed directly to this call. If a PUT response is uncertain, try completion before starting another upload.
6. Show the saved part's dimensions, weight, volume and retained source checksum. Use its `modelId` and revision in `prepare_proposal` with the selected containers.

The server verifies file identity and geometry and retains the STL for packing. Invalid geometry needs correction or a website import path. For an expired reservation use a new idempotency key. Reuse an upload ID after an uncertain completion response to avoid creating duplicate parts.

If cleanup has removed the reservation after a completed import, discover the saved part in `get_project_context` before starting another import.
