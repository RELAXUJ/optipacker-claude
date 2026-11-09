"""Inspect an attachment or transfer its unchanged bytes using an OptiPacker upload ticket."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

MAX_BYTES = 4 * 1024 * 1024
STORAGE_HOSTS = {"storage.googleapis.com", "firebasestorage.googleapis.com"}


def attachment(path):
    source = Path(path)
    if source.suffix.lower() != ".stl":
        raise ValueError("Choose an STL attachment.")
    if not 0 < source.stat().st_size <= MAX_BYTES:
        raise ValueError("The attachment exceeds the 4 MiB import limit or is empty.")
    data = source.read_bytes()
    if not 0 < len(data) <= MAX_BYTES:
        raise ValueError("The attachment changed while it was being read.")
    return data


def inspect(path):
    data = attachment(path)
    return {"originalFileName": Path(path).name, "byteLength": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def ticket_request(path, ticket):
    data = attachment(path)
    value = ticket.get("structuredContent", ticket)
    if value.get("status") != "awaiting_upload" or value.get("method") != "PUT":
        raise ValueError("The ticket must be an awaiting_upload response from prepare_stl_upload.")
    url = value.get("uploadUrl")
    if not isinstance(url, str):
        raise ValueError("The ticket has no upload URL.")
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname not in STORAGE_HOSTS
            or parsed.username or parsed.password or parsed.port not in (None, 443)
            or parsed.fragment):
        raise ValueError("The ticket must use an HTTPS Google Storage upload URL.")
    headers = value.get("headers")
    if not isinstance(headers, dict) or not all(isinstance(k, str) and isinstance(v, str)
                                              for k, v in headers.items()):
        raise ValueError("The ticket has invalid upload headers.")
    normalized = {key.lower(): val for key, val in headers.items()}
    if (normalized.get("content-length") != str(len(data))
            or normalized.get("content-type") != "application/octet-stream"
            or normalized.get("x-goog-if-generation-match") != "0"
            or set(normalized) != {"content-length", "content-type", "x-goog-if-generation-match"}):
        raise ValueError("The ticket does not match the attachment or immutable upload headers.")
    return urllib.request.Request(url, data=data, headers=headers, method="PUT")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Upload redirects are refused. Prepare a new ticket.")


def upload(path, ticket_path):
    ticket = json.loads(Path(ticket_path).read_text(encoding="utf-8-sig"))
    if not isinstance(ticket, dict):
        raise ValueError("The ticket must be a JSON object.")
    request = ticket_request(path, ticket)
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=60) as response:
            if response.status not in (200, 201, 204):
                raise ValueError("Storage did not accept the upload. Try completion before retrying.")
    except urllib.error.URLError as error:
        raise ValueError("Upload was not confirmed. Try complete_stl_upload before starting another import.") from error
    return {"uploaded": True, "next": "complete_stl_upload"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("inspect").add_argument("file")
    transfer = commands.add_parser("upload")
    transfer.add_argument("file")
    transfer.add_argument("--ticket", required=True)
    args = parser.parse_args()
    try:
        result = inspect(args.file) if args.command == "inspect" else upload(args.file, args.ticket)
        print(json.dumps(result))
    except (OSError, ValueError, TypeError, KeyError):
        print("The STL operation failed. Check the attachment and ticket; try completion after an uncertain transfer.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
