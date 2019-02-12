ebeam module
============
This module assumes that the beam has a waist at the centre of the undulator, and that the dispersion has been nulled for this section of the accelerator, and so the spot size in any of the transverse planes of motion can be calculated directly.

.. math:: \sigma_{x,y}=\sqrt{\epsilon_{x,y}\beta_{x,y}}
.. math:: \sigma'_{x,y}=\sqrt{\frac{\epsilon_{x,y}}{\beta_{x,y}}}

Lastly, this module provides a function to calculate the relativistic gamma of a beam of electrons.

.. math:: \gamma = \frac{E}{mc^2}

Functions
---------
.. automodule:: undulator.ebeam
   :members:
   :undoc-members:
   :show-inheritance:
