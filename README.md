Satellite Dashboard for GIS Project
Overview

The Satellite Dashboard is a GIS-based web application that processes and visualizes satellite image data. Built using Flask and other Python libraries, the dashboard provides users with interactive capabilities to analyze satellite data, focusing on key vegetation indices like NDVI, SAVI, and NDWI. The app supports uploading satellite images in TIFF format, performing analysis, and generating heatmaps of key indices to facilitate environmental monitoring.



Installation
Prerequisites:

Ensure that you have the following installed on your system:

Python 3.7+

pip (Python package manager)

Step 1: Clone the Repository

To get started, clone the repository:

git clone https://github.com/2002bish/GIS_Project.git
cd GIS_Project/satellite-dashboard

Step 2: Install Dependencies

Create a virtual environment (optional but recommended) and install the required dependencies:

python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt


The requirements.txt contains the necessary dependencies:

Flask: For creating the web application.

rasterio: For reading and processing satellite images (TIFF format).

numpy: For array manipulations.

matplotlib: For creating heatmaps and plots.

pandas: For data handling and export functionality.

Flask-Uploads: To handle file uploads from the user.

Step 3: Run the Application

Once the dependencies are installed, start the Flask application:

python app.py


The app will start a development server on http://127.0.0.1:5000/. You can access it by opening this URL in your browser.

Usage
1. Upload Satellite Images

Open the application in your browser (http://127.0.0.1:5000/).

Use the file input to upload one or more TIFF satellite images. Each image must contain Red, Green, Blue, and NIR bands for processing.
