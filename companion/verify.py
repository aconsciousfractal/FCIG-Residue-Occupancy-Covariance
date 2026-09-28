"""Verify the entire companion using only Python's standard library.

Run: python -B verify.py
No files are written. Redirect stdout to retain the deterministic JSON receipt.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parent
CERTIFICATES=tuple(f"certificates/band_{i:02d}.json" for i in range(3,17))+(
    "certificates/depth2.json","certificates/urn_monotonicity.json",
    "certificates/column_anchors.json","certificates/small_cutoffs.json")

def require(condition,message):
    if not condition:raise ArithmeticError(message)

def check_integrity(root=ROOT):
    manifest=json.loads((root/"MANIFEST.json").read_text(encoding="utf-8"))
    require(manifest["schema"]=="residue-occupancy-companion-v1","Manifest schema")
    entries=manifest["files"]
    expected=set(CERTIFICATES)|{"band_check.py","urn_check.py","math_checks.py",
        "verify.py","test_companion.py","README.md","CERTIFICATE_MAP.md","PROVENANCE.json"}
    require(set(entries)==expected,"Complete fixed companion inventory")
    actual={p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
            and "__pycache__" not in p.parts and p.name!="MANIFEST.json"}
    require(actual==expected,"No omitted or unexpected companion file")
    for name,record in entries.items():
        path=PurePosixPath(name)
        require(not path.is_absolute() and ".." not in path.parts,"Relative paths only")
        content=(root/name).read_bytes()
        require(hashlib.sha256(content).hexdigest()==record["sha256"]
                and len(content)==record["bytes"],"File integrity: "+name)
    return len(entries)

def main():
    files=check_integrity()
    import band_check,urn_check,math_checks
    bands=band_check.check_all()
    urns=urn_check.check_all()
    direct=math_checks.check_all()
    require(bands["total_grid_equalities"]==47696 and urns["rational_identity_checks"]==4056,
            "Complete interpolation grids")
    require(bands["total_integer_coefficients"]==35664 and urns["integer_coefficients"]==3120,
            "Complete coefficient arrays")
    result=dict(status="PASS",inventory_files=files,certificate_files=len(CERTIFICATES),
        exact_grid_equalities=51752,stored_integer_coefficients=38784,
        finite_boundary_fractions=bands["small_depth_equalities"]+urns["small_cutoff_exact_checks"],
        band_checks=bands,urn_checks=urns,direct_checks=direct,
        scope="Exact certificate identities and finite controls supporting the written proofs; not formal proof-assistant verification.")
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()

