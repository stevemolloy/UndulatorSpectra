import unittest
from hypothesis import given
import sys
sys.path.append('..')
from undulator.undulator import Undulator


class TestSigFunction(unittest.TestCase):

    def setUp(self):
        self.insdev = {
                'period': 15e-3,
                'Kmax': 1.38,
                'Np': 111,
                'L': 15e-3*111
                }
        self.beam = {
            'energy': 3e9,
            'betax': 9,
            'betay': 4.7,
            'emitx': 350e-12,
            'emity': 8e-12,
            'espread': 0.8e-3
        }
        self.ID = Undulator(insdev=self.insdev, beam=self.beam)

    def test_beam_attribute_references(self):
        '''
        Sanity check of the insdev and beam parameters
        '''
        for key, val in self.insdev.items():
            val_in_ID = getattr(self.ID.insdev, key)
            self.assertEqual(val_in_ID, val)

        for key, val in self.beam.items():
            val_in_ID = getattr(self.ID.beam, key)
            self.assertEqual(val_in_ID, val)


if __name__=='__main__':
    unittest.main()
