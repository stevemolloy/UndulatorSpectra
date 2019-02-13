undulator module
================
This is the module containing the vast majority of the physics complexity.

Spectral properties
-------------------
The wavelength, :math:`\lambda_n`, of a particular harmonic, :math:`n`, when viewed with an angle, :math:`\theta`, with respect to the forward direction is calculated as follows.

.. math:: \lambda_n = \frac{\lambda_w}{2n\gamma_0^2}\left(1 + K_{max}^2 + \gamma_0^2\theta^2\right)

From this, the photo energy, :math:`E_\gamma`, can be calculated (where :math:`h`, :math:`c`, and :math:`e`, are the usual physical constants).

.. math:: E_\gamma = \frac{hc}{e}\frac{1}{\lambda_n}

There are two primary contributors to the width of each spectral line: the finite number of undulator periods, and the spread of the beam parameters that appear in that expression (i.e., the electron energy and divergence).

Beam contribution
-----------------
The width, :math:`\sigma_{\lambda_{n,b}}`, due to the electron beam parameter spreads is calculated from a Taylor expansion of the :math:`\lambda_n` expression.

.. math:: \Delta\lambda_n = \frac{\partial\lambda_n}{\partial \gamma} \Bigr|_{\substack{\gamma=\gamma_0}} \cdot \Delta\gamma + \frac{\partial\lambda_n}{\partial\Theta}\Bigr|_{\substack{\Theta=0}}\cdot\Delta\Theta + \frac{1}{2}\frac{\partial^2\lambda_n}{\partial\Theta^2}\Bigr|_{\substack{\Theta=0}}\cdot\Delta\Theta^2

.. math:: \frac{\partial\lambda_n}{\partial \gamma}\Bigr|_{\substack{\gamma=\gamma_0}} = -\frac{1}{n\gamma_0^3}\left(1+K_w^2\right)\lambda_w

.. math:: \frac{\partial\lambda_n}{\partial\Theta}\Bigr|_{\substack{\Theta=0}}=\frac{\Theta\lambda_w}{n}\Bigr|_{\substack{\Theta=0}} = 0

.. math:: \frac{\partial^2\lambda_n}{\partial\Theta^2}\Bigr|_{\substack{\Theta=0}}=\frac{\lambda_w}{n}

To calculate the RMS spread, it is assumed that the distributions of the energy-spread and the angular divergence are uncorrelated, and so can be added in quadrature.

.. math:: \sigma_{\lambda_{n,b}}^2 = \left(-\frac{1}{n}\frac{1}{\gamma_0^3}\left(1+K_w^2\right)\lambda_w\cdot\Delta\gamma\right)^2 + \left(\frac{1}{2}\frac{1}{n}\lambda_w\cdot\Delta\Theta^2\right)^2

Undulator contribution
----------------------
The energy spectrum, :math:`\frac{dW_n}{d\omega}`, of the :math:`n`-th harmonic goes as follows.

.. math:: \frac{dW_n}{d\omega} \propto \left(\frac{\sin\left(\pi N_p \frac{\Delta\omega_n}{\omega_1}\right)}{\pi N_p \frac{\Delta\omega_n}{\omega_n}}\right)^2

In many texts, the width of the spectrum due to the :math:`\frac{\sin\left(Nx\right)}{Nx}` is often approximated as the point at which this function first passes through zero.  This solution results in, :math:`\frac{\Delta\omega_n}{\omega_n}=\pm\frac{1}{nN_p}`.  Unfortunately this does not match well with the RMS widths used elsewhere in the code, and so a different point is chosen.

.. math:: \frac{\sin\left(Nx\right)}{Nx} = \sqrt{\frac{1}{2}} \Longrightarrow \frac{\Delta\omega_n}{\omega_n}=\frac{0.225079}{N_p}

This results in a spectral width, :math:`\sigma_{\lambda_{n,u}}`, due to the finite number of periods in the undulator of,
.. math:: \sigma_{\lambda_{n,u}} = 0.225079\frac{1}{nN_p}\lambda_n

Total spectral width
--------------------
The beam contribution and the undulator contribution should be convoluted to optain the total width, however it is enough to add the contributions in quadrature.

.. math:: \sigma_{\lambda_{n,total}}^2 = \left(-\frac{1}{n}\frac{1}{\gamma_0^3}\left(1+K_w^2\right)\lambda_w\cdot\Delta\gamma\right)^2 + \left(\frac{1}{2}\frac{1}{n}\lambda_w\cdot\Delta\Theta^2\right)^2 + \left(0.225079\frac{1}{nN_p}\lambda_n\right)^2

Transverse Size
===============
The transverse size of the apparent source of the undulator light is a combination of the diffraction limited spot size and the transverse size fna divergence of the electron beam as it transits the undulator."

Diffraction limited source size
-------------------------------
The diffraction limited spot size, :math:`\sigma_{diff}`, can be shown to be the following.

.. math:: \sigma_{diff} = \frac{1}{2\pi}\sqrt{\frac{1}{2}\lambda_nL}

With the diffraction limited divergence, :math:`\sigma'_{diff}`, being.

.. math:: \sigma'_{diff} = \frac{1}{2\pi}\sqrt{\frac{1}{2}\frac{\lambda_n}{L}}

Total source size
-----------------
The total source size is the quadrature sum of several components:
1. The diffraction limited source size, :math:`\sigma_{diff}`, as given above.
2. The RMS size, :math:`\sigma_{b:x,y,x',y'}`, of the electron bunch in that plane of motion.
3. The average change in size of the bunch (in that plane of motion) as it traverses the undulator.  Note this is only true with the assumption that the electron beam optics lead to a waist within the undulator.
4. The apparent increase in size due to the oscillating path of the bunch within the undulator.

Note that the divergence of the electron beam is not affected by the undulator, and so only the first two points apply to the apparent source divergence.

.. math:: \sigma_{x,y}^2 = \sigma_{diff}^2 +  \sigma_{b:x,y}^2 + \frac{1}{3}\left(\frac{1}{2}\sigma_{x',y'}L\right)^2 + \left(\frac{\lambda_wK_{max}}{2\pi\gamma_0}\right)^2

.. math:: \sigma_{x',y'}^2 = \sigma_{diff}'^2 +  \sigma_{b:x',y'}^2

Methods
=======
.. automodule:: undulator.undulator
   :members:
   :undoc-members:
   :show-inheritance:
