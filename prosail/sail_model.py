#!/usr/bin/env python
import numpy as np
import scipy

from prospect_d import run_prospect

def run_prosail(n, cab, car,  cbrown, cw, cm, lai, lidfa, hspot,
                tts, tto, psi, ant=0.0, alpha=40., prospect_version="5", 
                typelidf=2, lidfb=0., factor="SDR",
                rsoil0=None, rsoil=None, psoil=None,
                soil_spectrum1=None, soil_spectrum2=None):
    """Run the PROSPECT_5B and SAILh radiative transfer models. The soil
    model is a linear mixture model, where two spectra are combined together as

         rho_soil = rsoil*(psoil*soil_spectrum1+(1-psoil)*soil_spectrum2)
    By default, ``soil_spectrum1`` is a dry soil, and ``soil_spectrum2`` is a
    wet soil, so in that case, ``psoil`` is a surface soil moisture parameter.
    ``rsoil`` is a  soil brightness term. You can provide one or the two
    soil spectra if you want.  The soil spectra must be defined
    between 400 and 2500 nm with 1nm spacing.

    Parameters
    ----------
    n: float
        Leaf layers
    cab: float
        leaf chlorophyll concentration
    car: float
        leaf carotenoid concentration
    cbrown: float
        senescent pigment
    cw: float
        equivalent leaf water
    cm: float
        leaf dry matter
    lai: float
        leaf area index
    lidfa: float
        a parameter for leaf angle distribution. If ``typliedf``=2, average
        leaf inclination angle.
    tts: float
        Solar zenith angle
    tto: float
        Sensor zenith angle
    psi: float
        Relative sensor-solar azimuth angle ( saa - vaa )
    ant: float
        leaf anthocyanin concentration (default set to 0)
    alpha: float
        The alpha angle (in degrees) used in the surface scattering
        calculations. By default it's set to 40 degrees.
    prospect_version: str
        Which PROSPECT version to use. We have "5" and "D"
    typelidf: int, optional
        The type of leaf angle distribution function to use. By default, is set
        to 2.
    lidfb: float, optional
        b parameter for leaf angle distribution. If ``typelidf``=2, ignored
    factor: str, optional
        What reflectance factor to return:
        * "SDR": directional reflectance factor (default)
        * "BHR": bi-hemispherical r. f.
        * "DHR": Directional-Hemispherical r. f. (directional illumination)
        * "HDR": Hemispherical-Directional r. f. (directional view)
        * "ALL": All of them
    rsoil0: float, optional
        The soil reflectance spectrum
    rsoil: float, optional
        Soil scalar 1 (brightness)
    psoil: float, optional
        Soil scalar 2 (moisture)
    soil_spectrum1: 2101-element array
        First component of the soil spectrum
    soil_spectrum2: 2101-element array
        Second component of the soil spectrum
    Returns
    --------
    A reflectance factor between 400 and 2500 nm


    """

    factor = factor.upper()
    if factor not in ["SDR", "BHR", "DHR", "HDR", "ALL"]:
        raise ValueError, "'factor' must be one of SDR, BHR, DHR, HDR or ALL"

    if soil_spectrum1 is not None:
        assert (len(soil_spectrum1) == 2101)
    else:
        soil_spectrum1 = spectral_libs.rsoil1

    if soil_spectrum2 is not None:
        assert (len(soil_spectrum1) == 2101)
    else:
        soil_spectrum2 = spectral_libs.rsoil2

    if rsoil0 is None:
        if (rsoil is None) or (psoil is None):
            raise ValueError, "If rsoil0 isn't define, then rsoil and psoil" + \
                              " need to be defined!"
        rsoil0 = rsoil * (
        psoil * soil_spectrum1 + (1. - psoil) * soil_spectrum2)

    wv, refl, trans = run_prospect (n, cab, car,  cbrown, cw, cm, ant=ant, 
                 prospect_version=prospect_version,  
                 nr=nr, kab=kab, kcar=kcar, kbrown=kbrown, kw=kw, 
                 km=km, kant=kant, alpha=alpha)
    
    rho = sail(refl, trans, lai, lidfa, lidfb, rsoil0, hspot, tts, tto, psi,
               typelidf)

    if factor == "SDR":
        return rho[0, :]
    elif factor == "BHR":
        return rho[1, :]
    elif factor == "DHR":
        return rho[2, :]
    elif factor == "HDR":
        return rho[3, :]
    elif factor == "ALL":
        return rho


def run_sail(refl, trans, lai, lidfa, hspot, tts, tto, psi,
             typelidf=2, lidfb=0., factor="SDR",
             rsoil0=None, rsoil=None, psoil=None,
             soil_spectrum1=None, soil_spectrum2=None):
    """Run the SAILh radiative transfer model. The soil model is a linear
    mixture model, where two spectra are combined together as

         rho_soil = rsoil*(psoil*soil_spectrum1+(1-psoil)*soil_spectrum2)

    By default, ``soil_spectrum1`` is a dry soil, and ``soil_spectrum2`` is a
    wet soil, so in that case, ``psoil`` is a surface soil moisture parameter.
    ``rsoil`` is a  soil brightness term. You can provide one or the two
    soil spectra if you want. The soil spectra, and leaf spectra must be defined
    between 400 and 2500 nm with 1nm spacing.

    Parameters
    ----------
    refl: 2101-element array
        Leaf reflectance
    trans: 2101-element array
        leaf transmittance
    lai: float
        leaf area index
    lidfa: float
        a parameter for leaf angle distribution. If ``typliedf``=2, average
        leaf inclination angle.
    hspot: float
        The hotspot parameter
    tts: float
        Solar zenith angle
    tto: float
        Sensor zenith angle
    psi: float
        Relative sensor-solar azimuth angle ( saa - vaa )
    typelidf: int, optional
        The type of leaf angle distribution function to use. By default, is set
        to 2.
    lidfb: float, optional
        b parameter for leaf angle distribution. If ``typelidf``=2, ignored
    factor: str, optional
        What reflectance factor to return:
        * "SDR": directional reflectance factor (default)
        * "BHR": bi-hemispherical r. f.
        * "DHR": Directional-Hemispherical r. f. (directional illumination)
        * "HDR": Hemispherical-Directional r. f. (directional view)
        * "ALL": All of them
    rsoil0: float, optional
        The soil reflectance spectrum
    rsoil: float, optional
        Soil scalar 1 (brightness)
    psoil: float, optional
        Soil scalar 2 (moisture)
    soil_spectrum1: 2101-element array
        First component of the soil spectrum
    soil_spectrum2: 2101-element array
        Second component of the soil spectrum

    Returns
    --------
    Directional surface reflectance between 400 and 2500 nm


    """
    factor = factor.upper()
    if factor not in ["SDR", "BHR", "DHR", "HDR", "ALL"]:
        raise ValueError, '\'factor\' must be one of SDR, BHR, DHR, HDR or ALL'

    if soil_spectrum1 is not None:
        assert (len(soil_spectrum1) == 2101)
    else:
        soil_spectrum1 = spectral_libs.rsoil1

    if soil_spectrum2 is not None:
        assert (len(soil_spectrum1) == 2101)
    else:
        soil_spectrum2 = spectral_libs.rsoil2

    if rsoil0 is None:
        if (rsoil is None) or (psoil is None):
            raise ValueError, "If rsoil0 isn't defined, then rsoil " + \
                              "and psoil need to be defined!"
        rsoil0 = rsoil * (psoil * soil_spectrum1 +
                          (1. - psoil) * soil_spectrum2)
    rho = sail(refl, trans, lai, lidfa, lidfb, rsoil0, hspot, tts, tto, psi,
               typelidf)

    if factor == "SDR":
        return rho[0, :]
    elif factor == "BHR":
        return rho[1, :]
    elif factor == "DHR":
        return rho[2, :]
    elif factor == "HDR":
        return rho[3, :]
    elif factor == "ALL":
        return rho



