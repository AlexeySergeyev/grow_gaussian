import numpy as np
from astropy.modeling import models
from photutils import CircularAperture, CircularAnnulus, aperture_photometry

def GaussModel(a=1000, x=50, y=50, sx=5, sy=5, theta=0, ratio=None):
    """
    Get a 2D Gaussian model with parameters a, x, y, sx, sy, theta.
    """
    if ratio is not None:
        sy = sx * ratio

    model = models.Gaussian2D(amplitude=a, x_mean=x, y_mean=y, x_stddev=sx, y_stddev=sy, theta=theta)

    return model

def add_noise(data, noise=0.1):
    """
    Add noise to data.
    """
    return data + np.random.normal(0, noise, data.shape)


def Model2Data(model, x0, x1, y0, y1, noise=0):
    """
    Generate data from a 2D model.
    """
    x = np.arange(x0, x1, 1)
    y = np.arange(y0, y1, 1)
    X, Y = np.meshgrid(x, y)
    data = model(X, Y)

    if noise > 0:
        data = add_noise(data, noise)

    return x, y, data

def AperturePhotometry(data, x, y, r=5, dr=2):
    """
    Perform aperture photometry on data.
    """
    positions = [(x, y)]
    aperture = CircularAperture(positions, r)
    annulus_aperture = CircularAnnulus(positions, r_in=r, r_out=r+dr)
    apers = [aperture, annulus_aperture]
    phot_table = aperture_photometry(data, apers)

    return phot_table    