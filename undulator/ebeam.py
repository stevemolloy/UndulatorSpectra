m = 510998.94626861025

def sig(emit: float, beta: float) -> float:
    '''
    Calculate the RMS size of a beam

    Args:
        emit: The beam emittance (m.rad).
        beta: The beam beta function (m).

    Returns:
        RMS beam size

    Examples
    --------
    >>> sig(8e-12, 4.7)
    6.131883886702356e-06
    '''
    return (emit * beta)**0.5

def sigp(emit: float, beta: float) -> float:
    '''
    Calculate the RMS divergence of a beam

    Args:
        emit: The beam emittance (m.rad).
        beta: The beam beta function (m).

    Returns:
        RMS beam divergence

    Examples
    --------
    >>> sigp(8e-12, 4.7)
    1.3046561461068843e-06
    '''
    return (emit / beta)**0.5

def beamgamma(energy: float) -> float:
    '''
    Calculate the relativistic gamma-factor of a beam

    Args:
        energy: The beam energy (eV).

    Returns:
        Relativistic gamma-factor

    Examples
    --------
    >>> beamgamma(3e9)
    5870.85359354739
    '''
    return energy / m

if __name__ == "__main__":
    import doctest
    doctest.testmod()
