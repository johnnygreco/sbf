# Third-party
import numpy as np
from scipy import ndimage


__all__ = [
    'compute_azimuthal_average',
    'compute_power_spectrum',
    'compute_k_values'
]

def compute_azimuthal_average(image, num_radial_bins=50):
    """
    Compute radial profile of image.

    Parameters
    ----------
    image : `~numpy.ndarray`
        Input image.
    num_radial_bins : int
        Number of radial bins in profile.

    Returns
    -------
    radial_mean : `~numpy.ndarray`
        Mean intensity within each annulus.
    radial_err : `~numpy.ndarray`
        Standard error on the mean: sigma / sqrt(N).
    """
    ny, nx = image.shape
    yy, xx = np.mgrid[:ny, :nx]
    center = np.array(image.shape) / 2

    r = np.hypot(xx - center[1], yy - center[0])
    rbin = (num_radial_bins * r/r.max()).astype(np.int)

    radial_mean = ndimage.mean(
        image, labels=rbin, index=np.arange(1, rbin.max() + 1))

    radial_stddev = ndimage.standard_deviation(
        image, labels=rbin, index=np.arange(1, rbin.max() + 1))

    npix = ndimage.sum(np.ones_like(image), labels=rbin,
                       index=np.arange(1, rbin.max() + 1))

    radial_err = radial_stddev / np.sqrt(npix)

    return radial_mean, radial_err


def compute_power_spectrum(data):
    """
    Compute the two-dimensional power spectrum.

    Parameters
    ----------
    data : `~numpy.ndarray`
        Data from which to compute the power spectrum.

    Returns
    -------
    ps :  `~numpy.ndarray`
        Two-dimensional power spectrum of `data`.
    """
    fft = np.fft.fftshift(np.fft.fft2(data))
    ps = np.abs(fft)**2
    return ps


def compute_k_values(window_length, num_radial_bins=45):
    """
    Compute azimuthally-averaged wavenumbers.

    Parameters
    ----------
    window_length : int
        Window size (bandwidth).
    num_radial_bins : int (optional).
        Number of radial bins.

    Returns
    -------
    k :  `~numpy.ndarray`
        Azimuthal-averaged wavenumbers.
    """
    k = np.fft.fftshift(np.fft.fftfreq(window_length))
    kx, ky = np.meshgrid(k, k)
    k = np.sqrt(kx**2 + ky**2)
    k, _ = azimuthal_average(k, num_radial_bins)
    return k
