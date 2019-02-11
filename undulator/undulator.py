from .ebeam import sigy, sigyp, sigx, sigxp, beamgamma
from .utilities import wavelength2energy

from math import pi
m = 510998.94626861025

def lamda_n(insdev, beam, n=1, theta=0):
    unscaled = insdev['lamda_w'] / (2 * n * beamgamma(beam)**2) 
    return unscaled * (1 + insdev['Kmax']**2 + (beamgamma(beam)*theta)**2)

def energy_n(insdev, beam, n=1, theta=0):
    return wavelength2energy(lamda_n(insdev, beam, n=n, theta=theta))

def d2l_dtheta2(insdev, n=1):
    return insdev['lamda_w'] / n

def dl_dgamma(insdev, beam, n=1):
    return -(1+insdev['Kmax']**2)*insdev['lamda_w'] / (n*beamgamma(beam)**3)

def spectralwidth_ebeam(insdev, beam, n=1):
    sigp_y_sqr = sigyp(beam)**2
    gamma0 = beamgamma(beam)
    dgamma = beam['energy'] * beam['espread'] / m
    disp_term = 0.5 * d2l_dtheta2(insdev, n) * sigp_y_sqr
    energy_term = dl_dgamma(insdev, beam, n)* gamma0 * dgamma/gamma0
    return (disp_term**2 + energy_term**2)**0.5

def spectralwidth_undulator(insdev, beam, n=1, theta=0):
    magic_num = 0.225079 # solve sinc(pi.N.x) = sqrt(0.5)
    return magic_num * lamda_n(insdev, beam, n, theta) / (n * insdev['Np'])

def spectralwidth_total(insdev, beam, n=1, theta=0):
    ebeam = spectralwidth_ebeam(insdev, beam, n)
    undulator = spectralwidth_undulator(insdev, beam, n, theta)
    return (ebeam**2 + undulator**2)**0.5

# TODO: Fix this
def difflimited_spot(insdev, beam, n=1, theta=0):
    return (0.5 * lamda_n(insdev, beam, n=n, theta=theta) * insdev['L'])**0.5

# TODO: Fix this
def difflimited_div(insdev, beam, n=1, theta=0):
    return (0.5 * lamda_n(insdev, beam, n=n, theta=theta) / insdev['L'])**0.5 / (2*pi)

def source_spot_y(insdev, beam, n=1, theta=0):
    osc_amplitude = insdev['lamda_w']*insdev['Kmax'] / (2*pi*beamgamma(beam))
    spot_sqr = difflimited_spot(insdev, beam, n=n, theta=theta)**2
    spot_sqr += sigy(beam)**2
    spot_sqr += osc_amplitude**2
    spot_sqr += (1/12) * sigyp(beam)**2 * insdev['L']**2
    return spot_sqr**0.5

def source_spot_x(insdev, beam, n=1, theta=0):
    osc_amplitude = insdev['lamda_w']*insdev['Kmax'] / (2*pi*beamgamma(beam))
    spot_sqr = difflimited_spot(insdev, beam, n=n, theta=theta)**2
    spot_sqr += sigx(beam)**2
    spot_sqr += osc_amplitude**2
    spot_sqr += (1/12) * sigxp(beam)**2 * insdev['L']**2
    return spot_sqr**0.5

def source_div_y(insdev, beam, n=1, theta=0):
    spot_sqr = difflimited_div(insdev, beam, n=n, theta=theta)**2
    spot_sqr += sigyp(beam)**2
    return spot_sqr**0.5

def source_div_x(insdev, beam, n=1, theta=0):
    spot_sqr = difflimited_div(insdev, beam, n=n, theta=theta)**2
    spot_sqr += sigxp(beam)**2
    return spot_sqr**0.5

def brightness(insdev, beam, n=1, theta=0):
    sigx = source_spot_x(insdev, beam, n, theta)
    sigxp = source_div_x(insdev, beam, n, theta)
    sigy = source_spot_y(insdev, beam, n, theta)
    sigyp = source_div_y(insdev, beam, n, theta)
    centre_freq = c / lamda_n(insdev, beam, n)
    high_freq = c / (lamda_n(insdev, beam, n) - spectralwidth_total(insdev, beam, n))
    delta_f = high_freq - centre_freq
    frac_freqdiff = delta_f / centre_freq
    return 1 / (sigx * sigxp * sigy * sigyp * frac_freqdiff)

def brightness_max(insdev, beam, n=1, theta=0):
    sigx = difflimited_spot(insdev, beam, n, theta)
    sigy = sigx
    sigxp = difflimited_div(insdev, beam, n, theta)
    sigyp = sigxp
    centre_freq = c / lamda_n(insdev, beam, n)
    high_freq = c / (lamda_n(insdev, beam, n) - spectralwidth_undulator(insdev, beam, n))
    delta_f = high_freq - centre_freq
    frac_freqdiff = delta_f / centre_freq
    return 1 / (sigx * sigxp * sigy * sigyp * frac_freqdiff)

if __name__=="__main__":
    print(m, hc)
