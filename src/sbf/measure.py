# Standard library
import pickle
from copy import deepcopy

# Third-party
import numpy as np
from scipy import optimize
from scipy.interpolate import interp1d
from scipy.signal import fftconvolve
from astropy.convolution import convolve_fft

# Project
from . import utils

__all__ = [
    'measure',
    'SBFResults'
]


class SBFResults(object):
    """
    Class to hold all the results from the SBF calculation.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_pickle(self, file_name):
        """Pickle results object."""
        pkl_file = open(file_name, 'wb')
        pickle.dump(self, pkl_file)
        pkl_file.close()

    @staticmethod
    def from_pickle(file_name):
        """Load pickle of results object."""
        pkl_file = open(file_name, 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()
        return data

    def copy(self):
        """Create deep copy of results object."""
        return deepcopy(self)


def measure(
    normed_res_image,
    psf,
    mask=None,
    k_range=[0.01, 0.4],
    fit_param_guess=[100, 50],
    num_radial_bins=45,
    use_sigma=False,
    **kwargs
):
    """
    Measure surface brightness fluctuations in the normalized residual image.

    Parameters
    ----------

    Returns
    -------
    """
    res_image = normed_res_image.copy()

    # zero-pad psf before calculating its FT to increase its frequency
    # sampling rate to match that of the object mask.
    psf_padded = np.pad(
        psf, (res_image.shape[0] - psf.shape[0])//2, 'constant')
    psf_padded /= psf_padded.sum()

    # if a mask is given, convolve its power spectrum with the psf
    if mask is not None:
        res_image[mask.astype(bool)] = 0.0
        mask = (~mask.astype(bool)).astype(float)
        npix = mask.sum()
        ps_mask = utils.compute_power_spectrum(mask)
        ps_2d_psf = convolve_fft(ps_psf, ps_mask, boundary='fill',
                              normalize_kernel=True)
    else:
        npix = np.product(res_image.shape)
        ps_2d_psf = utils.compute_power_spectrum(psf_padded)

    # compute power spectra of image
    psu_2d_image = utils.compute_power_spectrum(res_image)

    # compute azimuthal averages
    ps_image, ps_image_err = utils.azimuthal_average(ps_2d_image,
                                                     num_radial_bins)
    ps_psf, _ = utils.azimuthal_average(ps_2d_psf, num_radial_bins)

    # compute wave numbers
    wavenumbers = utils.compute_k_values(res_image.shape[0], num_radial_bins)

    # apply cut on wave number
    k_cut = (wavenumbers >= k_range[0]) & (wavenumbers <= k_range[1])
    ps_image = ps_image[k_cut]
    ps_psf = ps_psf[k_cut]
    ps_image_err = ps_image_err[k_cut]
    wavenumbers = wavenumbers[k_cut]

    # define fitting function: psf(k)*p0 + p1
    psf_k = interp1d(wavenumbers, ps_psf)
    fit_function = lambda k, p0, p1: psf_k(k) * p0 + p1

    # perform fit
    sigma = ps_image_err if use_sigma else None
    popt, pcov = optimize.curve_fit(
        fit_function, wavenumbers, ps_image, p0=fit_param_guess,
        sigma=sigma, **kwargs)

    # consolidate results
    results = SBFResults(ps_2d_image=ps_2d_image,
                         ps_2d_psf=ps_2d_psf,
                         ps_image=ps_image,
                         ps_image_err=ps_image_err,
                         ps_psf=ps_psf,
                         npix=npix,
                         k=wavenumbers,
                         p=popt,
                         cov=pcov,
                         fit_func=fit_func)

    return results
