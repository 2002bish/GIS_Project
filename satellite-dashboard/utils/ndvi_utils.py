# utils/ndvi_utils.py

import rasterio
import numpy as np

def load_bands(red_band_path, nir_band_path):
    with rasterio.open(red_band_path) as red_src, rasterio.open(nir_band_path) as nir_src:
        red_band = red_src.read(1).astype('float32')
        nir_band = nir_src.read(1).astype('float32')
    return red_band, nir_band

def calculate_ndvi(red_band, nir_band):
    np.seterr(divide='ignore', invalid='ignore')
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    ndvi[np.isnan(ndvi)] = 0
    return ndvi
