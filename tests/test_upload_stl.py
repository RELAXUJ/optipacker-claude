import importlib.util
import hashlib
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/optipacker/skills/optipacker/scripts/upload_stl.py"
spec = importlib.util.spec_from_file_location("upload_stl", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UploadTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.file = Path(self.directory.name) / "part.stl"
        self.file.write_bytes(b"solid part\nendsolid part\n")
        self.ticket = {"status": "awaiting_upload", "method": "PUT",
                       "uploadUrl": "https://storage.googleapis.com/bucket/object?signature=secret",
                       "headers": {"Content-Type": "application/octet-stream",
                                   "Content-Length": str(self.file.stat().st_size),
                                   "x-goog-if-generation-match": "0"}}

    def test_inspection_and_request_preserve_attachment_bytes(self):
        facts = module.inspect(self.file)
        self.assertEqual(facts["sha256"], hashlib.sha256(self.file.read_bytes()).hexdigest())
        self.assertEqual(facts["byteLength"], self.file.stat().st_size)
        request = module.ticket_request(self.file, self.ticket)
        self.assertEqual(request.data, self.file.read_bytes())
        self.assertEqual(request.method, "PUT")

    def test_refuses_foreign_hosts_http_credentials_and_changed_file(self):
        for url in ("https://attacker.example/", "http://storage.googleapis.com/",
                    "https://storage.googleapis.com.attacker.example/", "https://user@storage.googleapis.com/"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                module.ticket_request(self.file, {**self.ticket, "uploadUrl": url})
        self.file.write_bytes(b"changed")
        with self.assertRaises(ValueError):
            module.ticket_request(self.file, self.ticket)

    def test_refuses_redirects_and_unexpected_headers(self):
        with self.assertRaises(ValueError):
            module.NoRedirect().redirect_request(None, None, 302, "redirect", {}, "https://attacker.example")
        ticket = {**self.ticket, "headers": {**self.ticket["headers"], "Authorization": "token"}}
        with self.assertRaises(ValueError):
            module.ticket_request(self.file, ticket)


if __name__ == "__main__":
    unittest.main()
