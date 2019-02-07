from scipy.constants import c, e, electron_mass, h, pi
hc = h*c/e
m = electron_mass*c**2 / e

def wavelength2energy(lamda):
    return hc / lamda

def lamda_n(E, Keff, lamda_w, theta=0, n=1):
    unscaled = lamda_w / (2 * n * gamma0**2)
    return unscaled * (1 + Keff**2 + (gamma0*theta)**2)

def photonEnergy_n(E, Keff, lamba_w, theta=0, n=1):
    ln = lamda_n(E, Keff, lamda_w, theta=0, n=1)
    return wavelength2energy(ln)

def sigy(ebeam):
    try:
        return ebeam['sigy']
    except KeyError:
        return (ebeam['emity'] * ebeam['betay'])**0.5

def sigyp(ebeam):
    try:
        return ebeam['sigyp']
    except KeyError:
        return (ebeam['emity'] / ebeam['betay'])**0.5

def sigx(ebeam):
    try:
        return ebeam['sigx']
    except KeyError:
        return (ebeam['emitx'] * ebeam['betax'])**0.5

def sigxp(ebeam):
    try:
        return ebeam['sigxp']
    except KeyError:
        return (ebeam['emitx'] / ebeam['betax'])**0.5
    
def beamgamma(ebeam):
    try:
        return ebeam['gamma']
    except KeyError:
        return ebeam['energy']/m

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
    dgamma = beam['E'] * beam['espread'] / m
    disp_term = 0.5 * d2l_dtheta2(insdev, n) * sigp_y_sqr
    energy_term = dl_dgamma(insdev, beam, n)* gamma0 * dgamma/gamma0
    return (disp_term**2 + energy_term**2)**0.5

def spectralwidth_undulator(self, n=1, theta=0):
    magic_num = 0.225079 # solve sinc(pi.N.x) = sqrt(0.5)
    return magic_num * self.lamda_n(n, theta) / (n * self.undulator.Np)

def spectralwidth_total(self, n=1, theta=0):
    ebeam = self.spectralwidth_ebeam(n)
    undulator = self.spectralwidth_undulator(n, theta)
    return (ebeam**2 + undulator**2)**0.5

# TODO: Fix this
def difflimited_spot(self, n=1, theta=0):
    undulator = self.undulator
    return (0.5 * self.lamda_n(n=n, theta=theta) * undulator.L)**0.5

# TODO: Fix this
def difflimited_div(self, n=1, theta=0):
    undulator = self.undulator
    return (0.5 * self.lamda_n(n=n, theta=theta) / undulator.L)**0.5 / (2*pi)

def source_spot_y(self, n=1, theta=0):
    beam = self.beam
    undulator = self.undulator
    osc_amplitude = undulator.lamda_w*undulator.Kmax / (2*pi*beam.gamma0)
    spot_sqr = self.difflimited_spot(n=n, theta=theta)**2
    spot_sqr += beam.sigy()**2
    spot_sqr += osc_amplitude**2
    spot_sqr += (1/12) * beam.sigyp()**2 * undulator.L**2
    return spot_sqr**0.5

def source_spot_x(self, n=1, theta=0):
    beam = self.beam
    undulator = self.undulator
    osc_amplitude = undulator.lamda_w*undulator.Kmax / (2*pi*beam.gamma0)
    spot_sqr = self.difflimited_spot(n=n, theta=theta)**2
    spot_sqr += beam.sigx()**2
    spot_sqr += osc_amplitude**2
    spot_sqr += (1/12) * beam.sigxp()**2 * undulator.L**2
    return spot_sqr**0.5

def source_div_y(self, n=1, theta=0):
    beam = self.beam
    spot_sqr = self.difflimited_div(n=n, theta=theta)**2
    spot_sqr += beam.sigyp()**2
    return spot_sqr**0.5

def source_div_x(self, n=1, theta=0):
    beam = self.beam
    spot_sqr = self.difflimited_div(n=n, theta=theta)**2
    spot_sqr += beam.sigxp()**2
    return spot_sqr**0.5

def brightness(self, n=1, theta=0):
    sigx = self.source_spot_x(n, theta)
    sigxp = self.source_div_x(n, theta)
    sigy = self.source_spot_y(n, theta)
    sigyp = self.source_div_y(n, theta)
    centre_freq = c / self.lamda_n(n)
    high_freq = c / (self.lamda_n(n) - self.spectralwidth_total(n))
    delta_f = high_freq - centre_freq
    frac_freqdiff = delta_f / centre_freq
    return 1 / (sigx * sigxp * sigy * sigyp * frac_freqdiff)

def brightness_max(self, n=1, theta=0):
    sigx = self.difflimited_spot(n, theta)
    sigy = sigx
    sigxp = self.difflimited_div(n, theta)
    sigyp = sigxp
    centre_freq = c / self.lamda_n(n)
    high_freq = c / (self.lamda_n(n) - self.spectralwidth_undulator(n))
    delta_f = high_freq - centre_freq
    frac_freqdiff = delta_f / centre_freq
    return 1 / (sigx * sigxp * sigy * sigyp * frac_freqdiff)

_name__=="__main__":
print(m, hc)
