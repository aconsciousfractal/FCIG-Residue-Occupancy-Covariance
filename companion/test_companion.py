"""Meaningful corruption and boundary controls; run with unittest in either mode."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import band_check
import urn_check
import verify

ROOT=Path(__file__).resolve().parent

class CompanionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def cert(self,name):
        return json.loads((ROOT/"certificates"/name).read_text())

    def band_mutation(self,mutator):
        c=self.cert("band_03.json");mutator(c)
        path=self.root/"band.json";path.write_text(json.dumps(c))
        with self.assertRaises((ArithmeticError,KeyError)):
            band_check.check_one(path,3)

    def test_inventory(self):
        self.assertEqual(verify.check_integrity(),26)

    def test_missing_file(self):
        target=self.root/"copy"
        shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns("__pycache__"))
        (target/"certificates/band_16.json").unlink()
        with self.assertRaises(ArithmeticError):verify.check_integrity(target)

    def test_missing_file_and_manifest_entry(self):
        target=self.root/"copy"
        shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns("__pycache__"))
        f=target/"MANIFEST.json";m=json.loads(f.read_text())
        del m["files"]["certificates/band_16.json"]
        f.write_text(json.dumps(m));(target/"certificates/band_16.json").unlink()
        with self.assertRaises(ArithmeticError):verify.check_integrity(target)

    def test_hash_corruption(self):
        target=self.root/"copy"
        shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns("__pycache__"))
        with (target/"certificates/band_03.json").open("ab") as f:f.write(b" ")
        with self.assertRaises(ArithmeticError):verify.check_integrity(target)

    def test_missing_band_case(self):
        self.band_mutation(lambda c:c["cases"].pop())

    def test_duplicate_band_case(self):
        self.band_mutation(lambda c:c["cases"].append(copy.deepcopy(c["cases"][0])))

    def test_missing_residue(self):
        self.band_mutation(lambda c:c["affine_types"].pop())

    def test_altered_domain(self):
        self.band_mutation(lambda c:c.__setitem__("shift",133))

    def test_reduced_degree(self):
        self.band_mutation(lambda c:c.__setitem__("coefficient_degree",c["coefficient_degree"]-1))

    def test_nonpositive_scale(self):
        self.band_mutation(lambda c:c.__setitem__("scale",0))

    def test_negative_coefficient(self):
        self.band_mutation(lambda c:c["cases"][0]["negative_scaled_B_at_shift_plus_y"].__setitem__(0,-1))

    def test_positive_but_false_identity(self):
        def alter(c):c["cases"][0]["negative_scaled_B_at_shift_plus_y"][0]+=1
        self.band_mutation(alter)

    def test_changed_geometry(self):
        def alter(c):c["affine_types"][0]["entries"][0]["A"]+=1
        self.band_mutation(alter)

    def test_urn_wrong_domain(self):
        c=self.cert("urn_monotonicity.json")["cases"][0];c["shift"]=15
        with self.assertRaises(ArithmeticError):urn_check.inspect_case(c,1,3,16,1)

    def test_anchor_wrong_sign(self):
        c=self.cert("column_anchors.json")["cases"][0];c["sign"]=1
        with self.assertRaises(ArithmeticError):
            urn_check.inspect_case(c,c["degree_x"],c["degree_parameter"],40,-1)

    def test_missing_urn_profile(self):
        certdir=self.root/"certificates";certdir.mkdir()
        for name in ("urn_monotonicity.json","column_anchors.json","small_cutoffs.json"):
            shutil.copyfile(ROOT/"certificates"/name,certdir/name)
        c=self.cert("urn_monotonicity.json");c["cases"].pop()
        (certdir/"urn_monotonicity.json").write_text(json.dumps(c))
        with patch.object(urn_check,"ROOT",self.root):
            with self.assertRaises(ArithmeticError):urn_check.check_all()

    def test_modified_finite_fraction(self):
        certdir=self.root/"certificates";certdir.mkdir()
        c=self.cert("depth2.json");c[0]["covariances"][2]["numerator"]+=1
        (certdir/"depth2.json").write_text(json.dumps(c))
        with patch.object(band_check,"ROOT",self.root):
            with self.assertRaises(ArithmeticError):band_check.small_depth()

if __name__=="__main__":unittest.main()

