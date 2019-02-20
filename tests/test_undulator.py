import unittest
from hypothesis import given
from hypothesis.strategies import integers
from math import pi
import sys
sys.path.append('..')
from undulator.undulator import Undulator


def quadrature_sum(*args):
    return sum(v**2 for v in args)**0.5


class TestSigFunction(unittest.TestCase):

    def setUp(self):
        self.insdev = {
                'period': 18e-3,
                'Kmax': 1.38,
                'Np': 111,
                'L': 18e-3*111
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

    def test_nanomax_lamdan(self):
        '''
        Make sure the harmonic matches the NanoMAX params
        '''
        actual_value = self.ID.lamda_n()
        expected_value = 0.7583967046157e-9
        self.assertAlmostEqual(actual_value/expected_value, 1.0)

    def test_nanomax_energyn(self):
        '''
        Make sure the harmonic matches the NanoMAX params
        '''
        actual_value = self.ID.energy_n()
        expected_value = 1634.81983296
        self.assertAlmostEqual(actual_value, expected_value)

    @given(val=integers(min_value=1, max_value=50))
    def test_harmonic_wavelengths(self, val):
        expected_value = self.ID.lamda_n(n=1) / val
        actual_value = self.ID.lamda_n(n=val)
        self.assertAlmostEqual(expected_value/actual_value, 1)

    @given(val=integers(min_value=1, max_value=50))
    def test_harmonic_energy(self, val):
        expected_value = self.ID.energy_n(n=1) * val
        actual_value = self.ID.energy_n(n=val)
        self.assertAlmostEqual(expected_value/actual_value, 1)

    @given(val=integers(min_value=1, max_value=50))
    def test_spectralwidth_undulator(self, val):
        expected_value = (0.225079/(val*self.ID.insdev.Np)) * self.ID.lamda_n(n=val)
        actual_value = self.ID.spectralwidth_undulator(n=val)
        self.assertAlmostEqual(expected_value/actual_value, 1)

    @given(val=integers(min_value=1, max_value=50))
    def test_diffspotsize(self, val):
        spotsize = self.ID.difflimited_spot(n=val)
        actual_value = (spotsize *4*pi)**2
        expected_value = self.ID.lamda_n(n=val) * self.ID.insdev.L
        self.assertAlmostEqual(expected_value/actual_value, 1)

    @given(val=integers(min_value=1, max_value=50))
    def test_diffspotdiv(self, val):
        spotsize = self.ID.difflimited_div(n=val)
        actual_value = spotsize**2
        expected_value = self.ID.lamda_n(n=val) / self.ID.insdev.L
        self.assertAlmostEqual(expected_value/actual_value, 1)

    def test_sourcespot_plane_must_be_right(self):
        '''
        Test all latin input chars except lowercase 'x' and 'y'
        '''
        alfa = 'abcdefghijkjlmnopqrstuvwz'
        for c in alfa + alfa.upper() + 'XY':
            with self.assertRaises(ValueError):
                self.ID.source_spot(plane=c)


if __name__=='__main__':
    unittest.main()
