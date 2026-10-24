import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    'extract_features', Path(__file__).resolve().parents[1] / '5.feature_extract.py'
)
extract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extract)


class PairingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.images = Path(self.temp.name) / 'images'
        self.masks = Path(self.temp.name) / 'masks'
        self.images.mkdir()
        self.masks.mkdir()

    def test_equal_counts_do_not_hide_different_case_ids(self):
        (self.images / 'patient_a_img.png').touch()
        (self.masks / 'patient_b_mask.png').touch()
        with self.assertRaisesRegex(ValueError, 'Unmatched case IDs'):
            extract.pair_files(self.images, self.masks)

    def test_pairing_uses_case_ids_and_is_deterministic(self):
        for case in ('case_b', 'case_a'):
            (self.images / f'{case}_img.png').touch()
            (self.masks / f'{case}_mask.png').touch()
        pairs = extract.pair_files(self.images, self.masks)
        self.assertEqual([row[0] for row in pairs], ['case_a', 'case_b'])
        for case, image, mask in pairs:
            self.assertEqual(image.name, f'{case}_img.png')
            self.assertEqual(mask.name, f'{case}_mask.png')

    def test_empty_input_is_an_error(self):
        with self.assertRaisesRegex(ValueError, 'No .* files'):
            extract.pair_files(self.images, self.masks)


if __name__ == '__main__':
    unittest.main()
