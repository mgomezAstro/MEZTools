# MEZTools

Package that transform pixels and wavelengths into position and velocity, respectively, taking into account the plate scale of the detector.

### Installation
`python install setup.py`

### Usage
```python
from meztools import MEZTools

pv = MEZTools(outname:str, w0: float, scale:float, vsys: float)
pv.pixTovel()
# scale => Plate-scale at binning 1x1.
# w0 => Reference wavelength.
# vsys => Systemic velocity, when available.
```