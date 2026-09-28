"""Build from a clean source copy without installing any dependency."""
from pathlib import Path
import argparse
import hashlib
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "Covariance_Signs_for_Residue_Class_Occupancy.pdf"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Require exact distributed PDF bytes")
    args = parser.parse_args()
    engine = shutil.which("pdflatex")
    if not engine:
        raise SystemExit("pdflatex is not installed or not on PATH.")
    version = subprocess.check_output([engine, "--version"], text=True, encoding="utf-8")
    cmd = [engine]
    if "miktex" in version.lower():
        cmd += ["-disable-installer"]
    cmd += ["-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
            "-file-line-error", "main.tex"]
    env = dict(os.environ, SOURCE_DATE_EPOCH="1790373600")
    with tempfile.TemporaryDirectory(prefix="residue-occupancy-build-") as tmp:
        build = Path(tmp)
        shutil.copyfile(ROOT / "paper/Covariance_Signs_for_Residue_Class_Occupancy.tex", build / "main.tex")
        for i in range(2):
            q = subprocess.run(cmd, cwd=build, env=env, capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
            if q.returncode:
                print(q.stdout)
                print(q.stderr)
                raise SystemExit("LaTeX pass " + str(i + 1) + " failed.")
        pdf = (build / "main.pdf").read_bytes()
        if args.check:
            if pdf != (ROOT / "paper" / NAME).read_bytes():
                raise SystemExit("PDF differs. Check engine, fonts, packages, source and epoch; "
                                 "no cross-toolchain identity is promised.")
            print("PASS: byte-identical PDF")
        else:
            output = ROOT / "build"
            output.mkdir(exist_ok=True)
            (output / NAME).write_bytes(pdf)
            print((output / NAME).resolve())
        print("SHA256: " + hashlib.sha256(pdf).hexdigest())


if __name__ == "__main__":
    main()
