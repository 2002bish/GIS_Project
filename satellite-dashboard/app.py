import os
import numpy as np
import rasterio
from flask import Flask, render_template, request, jsonify, send_from_directory
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'tif', 'tiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Utility function to read a raster image
def read_raster(file_path):
    with rasterio.open(file_path) as src:
        return src.read(1), src.transform  # Read the first band

# Calculate NDVI
def calculate_ndvi(red_band, nir_band):
    return (nir_band - red_band) / (nir_band + red_band)

# Calculate EVI (Enhanced Vegetation Index)
def calculate_evi(blue_band, red_band, nir_band):
    # EVI formula
    L = 1  # Canopy background adjustment value
    C1 = 6  # Coefficient for the blue band
    C2 = 7.5  # Coefficient for the red band
    G = 2.5  # Gain factor
    evi = G * (nir_band - red_band) / (nir_band + C1 * blue_band - C2 * red_band + L)
    return evi

# Calculate NDBI (Normalized Difference Built-up Index)
def calculate_ndbi(swir_band, nir_band):
    return (swir_band - nir_band) / (swir_band + nir_band)

# Route to upload images and process them
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get uploaded files
        red_band_file = request.files['red_band']
        green_band_file = request.files['green_band']
        blue_band_file = request.files['blue_band']
        nir_band_file = request.files['nir_band']
        
        # Save files to the server
        red_band_path = os.path.join(app.config['UPLOAD_FOLDER'], 'red_band.tif')
        green_band_path = os.path.join(app.config['UPLOAD_FOLDER'], 'green_band.tif')
        blue_band_path = os.path.join(app.config['UPLOAD_FOLDER'], 'blue_band.tif')
        nir_band_path = os.path.join(app.config['UPLOAD_FOLDER'], 'nir_band.tif')

        red_band_file.save(red_band_path)
        green_band_file.save(green_band_path)
        blue_band_file.save(blue_band_path)
        nir_band_file.save(nir_band_path)

        # Read raster data
        red_band, _ = read_raster(red_band_path)
        green_band, _ = read_raster(green_band_path)
        blue_band, _ = read_raster(blue_band_path)
        nir_band, _ = read_raster(nir_band_path)

        # Calculate indices
        ndvi = calculate_ndvi(red_band, nir_band)
        evi = calculate_evi(blue_band, red_band, nir_band)

        # Generate heatmap for NDVI
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
        ax.set_title("NDVI Heatmap")
        plt.colorbar(ax.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1), ax=ax)
        plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'ndvi_heatmap.png'))
        plt.close()

        # Generate heatmap for EVI
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(evi, cmap='YlGn', vmin=-0.5, vmax=1)
        ax.set_title("EVI Heatmap")
        plt.colorbar(ax.imshow(evi, cmap='YlGn', vmin=-0.5, vmax=1), ax=ax)
        plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'evi_heatmap.png'))
        plt.close()

        # Display results on the dashboard
        return render_template('result.html', ndvi_image='ndvi_heatmap.png', evi_image='evi_heatmap.png')

    return render_template('index.html')


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
