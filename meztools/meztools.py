from typing import Optional, Tuple, Union
import aplpy
from astropy.io import fits
from astropy.io.fits import HDUList
import matplotlib.pyplot as plt


# Light speed in km/s
_C = 299792.458


class MEZTools:
    def __init__(self, fitsfile: str) -> None:
        self.fitsfile = fitsfile

    def pixTovel(
        self,
        outname: str,
        w0: float,
        scale: float,
        vsys: float = 0.0,
        crsum: int = None,
        ccsum: int = None,
        save: bool = False
    ) -> HDUList:
        """Convert the wavelenght and pixels into velocity and arcsec, respectively."""

        hdu = fits.open(self.fitsfile)
        header = hdu[0].header

        if crsum is None or ccsum is None:
            if "CCDSUM" in header:
                binning = header["CCDSUM"]
                ccsum = float(binning[0])
                crsum = float(binning[2])
            elif "CBIN" in header or "RBIN" in header:
                ccsum = float(header["CBIN"])
                crsum = float(header["RBIN"])
            else:
                raise ValueError(
                    "You must specify 'crsum' or 'ccsum' if binning information is not in header."
                )

        ax1 = 2
        ax2 = 1
        if header["DISPAXIS"] == 2:
            ax1 = 1
            ax2 = 2

        header[f"CRVAL{ax1}"] = -(header[f"NAXIS{ax1}"] / 2.0) * scale * crsum
        header[f"CRPIX{ax1}"] = 0
        header[f"CD{ax1}_{ax1}"] = scale * crsum
        header[f"CDELT{ax1}"] = scale * crsum
        dv = (header[f"CDELT{ax2}"] / w0) * _C
        header[f"CDELT{ax2}"] = dv
        header[f"CD{ax2}_{ax2}"] = dv
        v0 = (header[f"CRVAL{ax2}"] - w0) / w0 * _C + header["VLSR"] - vsys
        header[f"CRVAL{ax2}"] = v0

        header["VSYS"] = (vsys, "Systemic velocity.")

        if save:
            hdu.writeto(outname, overwrite=True)

        return hdu

    def vcut(self):
        pass


def plotOneSpec(
    fitsfile: Union[str, HDUList],
    outfile: Optional[str] = "spec_vel",
    dimensions: Tuple[int] = [1, 0],
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    show: bool = True,
    save: bool = False,
    xlabel: str = "X axis",
    ylabel: str = "Y axis",
    xspacing: Optional[float] = None,
    yspacing: Optional[float] = None,
    recenter: Optional[Tuple[float]] = None,
) -> None:
    """Funtion to plot a spectrum."""

    if isinstance(fitsfile, str):
        hdu = fits.open(fitsfile)
    if isinstance(fitsfile, HDUList):
        hdu = fitsfile
        del fitsfile

    fig = aplpy.FITSFigure(hdu, dimensions=dimensions)
    fig.show_grayscale(invert=True, vmin=vmin, vmax=vmax)
    fig.set_theme("publication")

    fig.axis_labels.set_xtext(xlabel)
    fig.axis_labels.set_ytext(ylabel)

    fig.tick_labels.set_font(size=11)
    if xspacing is not None:
        fig.ticks.set_xspacing(xspacing)
    if yspacing is not None:
        fig.ticks.set_yspacing(yspacing)

    if recenter is not None:
        fig.recenter(recenter[0], recenter[1], width=recenter[2], height=recenter[3])

    if save and not show:
        fig.savefig(f"{outfile}_vel.pdf")

    if show:
        plt.show()
