m = 510998.94626861025

def sigy(ebeam):
    '''
    >>> sigy({'energy': 3e9, 'emitx': 340e-12, 'emity': 8e-12, 'betax': 9, 'betay': 4.7, 'espread': 0.8e-3})
    6.131883886702356e-06
    '''
    try:
        return ebeam['sigy']
    except KeyError:
        return (ebeam['emity'] * ebeam['betay'])**0.5

def sigyp(ebeam):
    '''
    >>> sigyp({'energy': 3e9, 'emitx': 340e-12, 'emity': 8e-12, 'betax': 9, 'betay': 4.7, 'espread': 0.8e-3})
    1.3046561461068843e-06
    '''
    try:
        return ebeam['sigyp']
    except KeyError:
        return (ebeam['emity'] / ebeam['betay'])**0.5

def sigx(ebeam):
    '''
    >>> sigx({'energy': 3e9, 'emitx': 340e-12, 'emity': 8e-12, 'betax': 9, 'betay': 4.7, 'espread': 0.8e-3})
    5.5317266743757324e-05
    '''
    try:
        return ebeam['sigx']
    except KeyError:
        return (ebeam['emitx'] * ebeam['betax'])**0.5

def sigxp(ebeam):
    '''
    >>> sigxp({'energy': 3e9, 'emitx': 340e-12, 'emity': 8e-12, 'betax': 9, 'betay': 4.7, 'espread': 0.8e-3})
    6.1463629715285915e-06
    '''
    try:
        return ebeam['sigxp']
    except KeyError:
        return (ebeam['emitx'] / ebeam['betax'])**0.5
    
def beamgamma(ebeam):
    '''
    >>> beamgamma({'energy': 3e9, 'emitx': 340e-12, 'emity': 8e-12, 'betax': 9, 'betay': 4.7, 'espread': 0.8e-3})
    5870.85359354739
    '''
    try:
        return ebeam['gamma']
    except KeyError:
        return ebeam['energy'] / m

if __name__ == "__main__":
    import doctest
    doctest.testmod()