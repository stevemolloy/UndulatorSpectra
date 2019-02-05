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


class InsertionDevice:
    def __init__(self, Kmax, lamda_w, Np, L):
        self.Kmax = Kmax
        self.lamda_w = lamda_w
        self.Np = Np
        self.L = L
        
    def __repr__(self):
        terms = [
            f'Kmax={self.Kmax}',
            f'Period={self.lamda_w*1e3} mm',
            f'Ncells={self.Np}'
        ]
        return f'InsertionDevice:: ' + ' '.join(terms)
        

class ElectronBeam:
    def __init__(self, energy, emittance, beta, espread=0):
        self.E = energy
        self.gamma0 = self.E / m
        self.emitx = emittance['x']
        self.emity = emittance['y']
        self.betax = beta['x']
        self.betay = beta['y']
        self.espread = espread
        
    def __repr__(self):
        terms = [
            f'{self.E*1e-9} GeV',
            f'ex={self.emitx} ey={self.emity}',
            f'bx={self.betax} by={self.betay}'
        ]
        return f'ElectronBeam:: ' + ' '.join(terms)
    
    def sigy(self):
        return (self.emity * self.betay)**0.5
    
    def sigyp(self):
        return (self.emity / self.betay)**0.5
    
    def sigx(self):
        return (self.emitx * self.betax)**0.5
    
    def sigxp(self):
        return (self.emitx / self.betax)**0.5


class Beamline:
    def __init__(self, undulator, electronbeam):
        self.undulator = undulator
        self.beam = electronbeam
        
    def __repr__(self):
        return f'{self.undulator}\n{self.beam}'
        
    def lamda_n(self, n=1, theta=0):
        undulator = self.undulator
        beam = self.beam
        unscaled = undulator.lamda_w / (2 * n * beam.gamma0**2) 
        return unscaled * (1 + undulator.Kmax**2 + (beam.gamma0*theta)**2)
    
    def energy_n(self, n=1, theta=0):
        return wavelength2energy(self.lamda_n(n=n, theta=theta))
    
    def d2l_dtheta2(self, n=1):
        return self.undulator.lamda_w / n
    
    def dl_dgamma(self, n=1):
        undulator = self.undulator
        beam = self.beam
        return -(1+undulator.Kmax**2)*undulator.lamda_w / (n*beam.gamma0**3)
    
    def spectralwidth_ebeam(self, n=1):
        beam = self.beam
        sigp_y_sqr = beam.emity / beam.betay
        gamma0 = beam.gamma0
        dgamma = beam.E * beam.espread / m
        disp_term = 0.5*abs(self.d2l_dtheta2(n))*sigp_y_sqr
        energy_term = abs(self.dl_dgamma(n))* gamma0 * dgamma/gamma0
        return disp_term + energy_term
    
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
        return (self.lamda_n(n=n, theta=theta) * undulator.L)**0.5
    
    # TODO: Fix this
    def difflimited_div(self, n=1, theta=0):
        undulator = self.undulator
        return (self.lamda_n(n=n, theta=theta) / undulator.L)**0.5 / (2*pi)
    
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

if __name__=="__main__":
    print(m, hc)