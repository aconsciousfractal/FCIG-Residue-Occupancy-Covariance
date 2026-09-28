"""Four adverse controls for the package inventory (not mathematical tests)."""
from pathlib import Path
import hashlib
import importlib.util
import json
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "package_verify", Path(__file__).resolve().parents[1] / "scripts/verify.py")
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class PackageControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "payload.txt").write_bytes(b"original\n")
        self.data = {"schema": "residue-occupancy-package-v1", "files": {"payload.txt": {
            "bytes": 9, "sha256": hashlib.sha256(b"original\n").hexdigest()}}}
        self.save()

    def save(self):
        (self.root / "MANIFEST.json").write_text(json.dumps(self.data), encoding="utf-8")

    def test_corruption_rejected(self):
        (self.root / "payload.txt").write_bytes(b"changed!\n")
        with self.assertRaisesRegex(ValueError, "integrity"):
            verify.check_integrity(self.root)

    def test_missing_file_rejected(self):
        (self.root / "payload.txt").unlink()
        with self.assertRaisesRegex(ValueError, "inventory"):
            verify.check_integrity(self.root)

    def test_unexpected_file_rejected(self):
        (self.root / "unexpected.txt").write_text("extra", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "inventory"):
            verify.check_integrity(self.root)

    def test_escape_path_rejected(self):
        self.data["files"] = {"../outside.txt": self.data["files"]["payload.txt"]}
        self.save()
        with self.assertRaisesRegex(ValueError, "relative paths"):
            verify.check_integrity(self.root)


if __name__ == "__main__":
    unittest.main()

