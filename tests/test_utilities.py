import unittest
from hypothesis import given
from hypothesis.strategies import floats
from random import random
import sys
sys.path.append('..')
from undulator.utilities import wavelength2energy

hc = 1.2398419739640718e-06


class TestWavelength2Energy(unittest.TestCase):

    def test_1nm(self):
        '''
        1nm photon
        '''
        E = wavelength2energy(1e-9)
        self.assertAlmostEqual(E, 1239.8419739640717)

    @given(exmpl=floats(
        min_value=1e-15,
        exclude_min=True,
        allow_infinity=False,
        ))
    def test_back_conversion_works(self, exmpl):
        '''
        Convert to energy with wavelength2energy, then convert back to
        wavelength.  Should get the same number.
        '''
        new_wavelength = hc / wavelength2energy(exmpl)
        self.assertAlmostEqual(new_wavelength / exmpl, 1.0)

    def test_no_negative_wavelengths(self):
        '''
        Negative wavelength input should raise an error
        '''
        with self.assertRaises(ValueError):
            wavelength2energy(-1e-9)

    def test_no_zero_wavelengths(self):
        '''
        Zero wavelength input should raise an error
        Wavelengths less than 1e-15 are considered to be zero
        '''
        with self.assertRaises(ValueError):
            wavelength2energy(0.9e-15)
        with self.assertRaises(ValueError):
            wavelength2energy(0)


if __name__=='__main__':
    unittest.main()
