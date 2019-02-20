'''
Provides the *Undulator* class for calculations of various properties
of undulator radiation.
'''
from undulator.ebeam import sig, sigp, beamgamma, m
from undulator.utilities import wavelength2energy
c = 299792458.0

from collections import namedtuple
from math import pi
from typing import Dict

Str2Float = Dict[str, float]

class Undulator:
    '''
    Given the properties of an electron beam and an undulator, this class
    provides multiple methods for calculating the properties of the emitted
    undulator light.

    Initialise an Undulator class with the following:

    Args:
        insdev: A dictionary containing details of the insertion device.
        beam: A dictionary containing details of the electron beam.

    insdev:
        * period: The period of the magnetic field
        * Kmax: The maximum value of the K parameter
        * Np: The number of periods of the magnetic field
        * L: The effective magnetic length of the device
    beam:
        * energy: The energy of the beam (eV).
        * betax: The horizontal beta function at the centre of the undulator (m).
        * betay: The horizontal beta function at the centre of the undulator (m).
        * emitx: The horiztonal emittance (m.rad)
        * emity: The horiztonal emittance (m.rad)
        * espread: The fractional RMS spread of the beam energy
    '''
    def __init__(self, insdev: Str2Float, beam: Str2Float) -> None:
        '''
        >>> insdev = {'period': 15e-3, 'Kmax': 1.38, 'Np': 111, 'L': 15e-3*111}
        >>> beam = {
        ...     'energy': 3e9,
        ...     'betax': 9,
        ...     'betay': 4.7,
        ...     'emitx': 350e-12,
        ...     'emity': 8e-12,
        ...     'espread': 0.8e-3
        ... }
        >>> ID = Undulator(insdev=insdev, beam=beam)
        >>> print(ID.beam)
        beam(energy=3000000000.0, betax=9, betay=4.7, emitx=3.5e-10, emity=8e-12, espread=0.0008)
        >>> print(ID.insdev)
        insdev(period=0.015, Kmax=1.38, Np=111, L=1.665)
        '''
        self.insdev = objectdict(insdev)
        self.beam = objectdict(beam)

    def __repr__(self) -> str:
        insdev_repr = repr(self.insdev.asdict())
        beam_repr = repr(self.beam.asdict())
        return 'Undulator(' + insdev_repr + ', ' + beam_repr + ')'

    def lamda_n(self, n: int=1, theta: float=0):
        '''
        Calculate the wavelength of the nth harmonic
        '''
        if n>50:
            raise ValueError('Harmonics higher than 50 are likely to be' +
                    'non-physical')
        gamma = beamgamma(self.beam.energy)
        unscaled = self.insdev.period / (2 * n * gamma**2)
        return unscaled * (1 + self.insdev.Kmax**2 + (gamma*theta)**2)

    def energy_n(self, n: int=1, theta: float=0) -> float:
        '''
        Calculate the photon energy of the nth harmonic
        '''
        return wavelength2energy(self.lamda_n(n=n, theta=theta))

    def d2l_dtheta2(self, n: int=1) -> float:
        return self.insdev.period / n

    def dl_dgamma(self, n: int=1) -> float:
        gamma = beamgamma(self.beam.energy)
        return -(1+self.insdev.Kmax**2)*self.insdev.period / (n*gamma**3)

    def spectralwidth_ebeam(self, n: int=1) -> float:
        beam = self.beam
        gamma = beamgamma(beam.energy)
        sigp_y_sqr = sigp(beam.emity, beam.betay)**2
        dgamma = beam.energy * beam.espread / m
        disp_term = 0.5 * self.d2l_dtheta2(n) * sigp_y_sqr
        energy_term = self.dl_dgamma(n)* gamma * dgamma/gamma
        return (disp_term**2 + energy_term**2)**0.5

    def spectralwidth_undulator(self, n: int=1, theta: float=0) -> float:
        magic_num = 0.225079 # solve sinc(pi.N.x) = sqrt(0.5)
        return magic_num * self.lamda_n(n, theta) / (n * self.insdev.Np)

    def spectralwidth_total(self, n: int=1, theta: float=0) -> float:
        ebeam = self.spectralwidth_ebeam(n)
        undulator = self.spectralwidth_undulator(n, theta)
        return (ebeam**2 + undulator**2)**0.5

    def difflimited_spot(self, n: int=1) -> float:
        '''
        https://www.cockcroft.ac.uk/wp-content/uploads/2014/12/CLarke-Lecture-3.pdf
        '''
        L = self.insdev.L
        return (1/(4*pi)) * (self.lamda_n(n=n, theta=0) * L)**0.5

    def difflimited_div(self, n: int=1) -> float:
        '''
        https://www.cockcroft.ac.uk/wp-content/uploads/2014/12/CLarke-Lecture-3.pdf
        '''
        L = self.insdev.L
        return (self.lamda_n(n=n, theta=0) / L)**0.5

    def source_spot(self, plane: str, n: int=1, theta: float=0) -> float:
        if plane == 'y':
            beta = self.beam.betay
            emit = self.beam.emity
        elif plane == 'x':
            beta = self.beam.betax
            emit = self.beam.emitx
        else:
            raise ValueError("'plane' must be 'x' or 'y'")
        insdev = self.insdev
        gamma = beamgamma(self.beam.energy)
        osc_amplitude = insdev.period*insdev.Kmax / (2*pi*gamma)
        spot_sqr = self.difflimited_spot(n=n)**2
        spot_sqr += sig(emit, beta)**2
        spot_sqr += osc_amplitude**2
        spot_sqr += (1/12) * sigp(emit, beta)**2 * insdev.L**2
        return spot_sqr**0.5

    def source_div(self, plane: str, n: int=1, theta: float=0) -> float:
        if plane == 'y':
            beta = self.beam.betay
            emit = self.beam.emity
        elif plane == 'x':
            beta = self.beam.betax
            emit = self.beam.emitx
        else:
            raise ValueError("'plane' must be 'x' or 'y'")
        spot_sqr = self.difflimited_div(n=n)**2
        spot_sqr += sigp(emit, beta)**2
        return spot_sqr**0.5

    def brightness(self, n: int=1, theta: float=0) -> float:
        sigx = self.source_spot('x', n, theta)
        sigxp = self.source_div('x', n, theta)
        sigy = self.source_spot('y', n, theta)
        sigyp = self.source_div('y', n, theta)
        centre_freq = c / self.lamda_n(n)
        high_freq = c / (self.lamda_n(n) - self.spectralwidth_total(n))
        delta_f = high_freq - centre_freq
        frac_freqdiff = delta_f / centre_freq
        return 1 / (sigx * sigxp * sigy * sigyp * frac_freqdiff)


class objectdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


if __name__=="__main__":
    import doctest
    doctest.testmod()

