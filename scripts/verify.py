"""Verify package integrity, exact mathematics, and rejection controls."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inventory(root):
    result = {}
    for f in root.rglob("*"):
        rel = f.relative_to(root)
        if rel.parts[0] in {".git", "build"} or "__pycache__" in rel.parts:
            continue
        require(not f.is_symlink(), "Symlinks are not package payloads: " + rel.as_posix())
        if f.is_file() and rel.as_posix() != "MANIFEST.json":
            result[rel.as_posix()] = f
    return result


def check_integrity(root=ROOT):
    data = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    require(data["schema"] == "residue-occupancy-package-v1", "Package schema")
    entries = data["files"]
    require(isinstance(entries, dict) and bool(entries), "Nonempty file map")
    for name in entries:
        p = PurePosixPath(name)
        require(bool(name) and not p.is_absolute() and ".." not in p.parts
                and "\\" not in name and ":" not in name and p.as_posix() == name,
                "Canonical relative paths only")
    actual = inventory(root)
    require(set(actual) == set(entries), "Exact package inventory")
    for name, f in actual.items():
        content = f.read_bytes()
        require(len(content) == entries[name]["bytes"]
                and hashlib.sha256(content).hexdigest() == entries[name]["sha256"],
                "Package integrity: " + name)
    if "MANIFEST_SHA256.txt" in entries:
        expected = "".join(entries[name]["sha256"] + "  " + name + "\n"
                           for name in sorted(entries) if name != "MANIFEST_SHA256.txt")
        require((root / "MANIFEST_SHA256.txt").read_text(encoding="utf-8") == expected,
                "Readable manifest agrees with the JSON inventory")
    return len(entries) + 1


def run(args, cwd):
    q = subprocess.run([sys.executable, "-B"] + (["-O"] if sys.flags.optimize else []) + args,
                       cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if q.returncode:
        raise RuntimeError(q.stdout + q.stderr)
    return q.stdout, q.stderr


def main():
    files = check_integrity()
    receipt, _ = run(["verify.py"], ROOT / "companion")
    _, ctests = run(["-m", "unittest", "-v", "test_companion"], ROOT / "companion")
    _, ptests = run(["-m", "unittest", "discover", "-s", "tests",
                    "-p", "test_package.py", "-v"], ROOT)
    require(re.search(r"Ran 17 tests", ctests) is not None, "Complete companion tests")
    require(re.search(r"Ran 4 tests", ptests) is not None, "Complete package controls")
    proof = json.loads(receipt)
    require(proof["status"] == "PASS", "Companion verdict")
    corollaries, _ = run(["scripts/check_corollaries.py"], ROOT)
    derived = json.loads(corollaries)
    require(derived["status"] == "PASS", "Corollary controls")
    print(json.dumps(dict(status="PASS", package_files=files,
                         companion_tests=17, package_controls=4, companion_receipt=proof,
                         corollary_checks=derived),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
