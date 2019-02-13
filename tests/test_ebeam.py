import unittest
from hypothesis import given
from hypothesis.strategies import floats
import sys
sys.path.append('..')
from undulator.ebeam import sig, sigp, beamgamma, m


class TestSigFunction(unittest.TestCase):

    def test_maxiv_y_params(self):
        '''
        Test MAX-IV y plane params.
        assertAlmostEquals because of float comparison
        '''
        self.assertAlmostEqual(sig(8e-12, 4.7), 6.131884e-6)

    def test_maxiv_x_params(self):
        '''
        Test MAX-IV x plane params.
        assertAlmostEquals because of float comparison
        '''
        self.assertAlmostEqual(sig(340e-12, 9.0), 5.531727e-5)

    @given(val=floats(max_value=0, exclude_max=True))
    def test_negative_emit_valueerror(self, val):
        '''Negative emit value is an error'''
        with self.assertRaises(ValueError):
            sig(val, 1)

    @given(val=floats(max_value=0, exclude_max=True))
    def test_negative_beta_valueerror(self, val):
        '''Negative beta value is an error'''
        with self.assertRaises(ValueError):
            sig(1, val)


class TestSigpFunction(unittest.TestCase):

    def test_maxiv_y_params(self):
        '''
        Test MAX-IV y plane params.
        assertAlmostEquals because of float comparison
        '''
        self.assertAlmostEqual(sigp(8e-12, 4.7), 1.304656e-6)

    def test_maxiv_x_params(self):
        '''
        Test MAX-IV x plane params.
        assertAlmostEquals because of float comparison
        '''
        self.assertAlmostEqual(sigp(340e-12, 9.0), 6.146363e-6)

    @given(val=floats(max_value=0, exclude_max=True))
    def test_negative_emit_valueerror(self, val):
        '''Negative emit value is an error'''
        with self.assertRaises(ValueError):
            sig(val, 1)

    @given(val=floats(max_value=0, exclude_max=True))
    def test_negative_beta_valueerror(self, val):
        '''Negative beta value is an error'''
        with self.assertRaises(ValueError):
            sig(1, val)


class TestBeamGammaFunction(unittest.TestCase):

    def test_maxiv_params(self):
        self.assertAlmostEqual(beamgamma(3e9), 5870.853593, places=5)
        self.assertAlmostEqual(beamgamma(1.5e9), 2935.426797, places=5)

    def test_restframe_gamma(self):
        self.assertEqual(beamgamma(m), 1.0)

    @given(val=floats(max_value=m, exclude_max=True))
    def test_nonphysical_energy(self, val):
        '''Hypothesis ensures that val<m'''
        with self.assertRaises(ValueError):
            beamgamma(val)


if __name__=='__main__':
    unittest.main()
