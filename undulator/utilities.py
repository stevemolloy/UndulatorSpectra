hc = 1.2398419739640718e-06

def wavelength2energy(wavelength: float) -> float:
    '''
    Calculate the energy of a photon of a given wavelength

    Parameters:
        wavelength: The photon wavelength (m)

    Returns:
        Photon energy (eV)

    Examples
    --------
    >>> wavelength2energy(1e-9)
    1239.8419739640717
    '''
    if wavelength < 0:
        raise ValueError('Negative wavelengths are unphysical')
    if wavelength < 1e-15:
        raise ValueError(
                'Wavelengths less than 1e-15 m could' +
                'lead to floating point errors'
                )
    if wavelength == float('inf'):
        raise ValueError('Infinite wavelengths are unphysical')
    return hc / wavelength

if __name__ == "__main__":
    import doctest
    doctest.testmod()
