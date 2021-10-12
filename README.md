# TopoMapVisualiser
PYQGIS script for creating and styling elevation data using a DEM.


The TopoMapVisualiser script is a quick and simple method of visualising topographic features derived from a DEM. It applies a custom single band pseudocolor render to the DEM layer overlayed on a hillshade layer to create a 3-dimensional look. Contours are also drawn at two intervals: 100 meters and 400 meters.

This script was designed for use elevatinon data for Victoria, Australia, however it can be easily adapted to suit larger elevation ranges.

Please change the various filepath and attribute fields to suit your workspace before running the script.

![image](https://user-images.githubusercontent.com/72475218/136885623-e96fa103-e4fc-4d2b-aad9-9f23c7a388e4.png)


The output can be visualised in 3D using QGIS 3D map view layout by selecting the DEM as the elevation source and adjusting the elevation scale accordingly.

![image](https://user-images.githubusercontent.com/72475218/136885890-fcc68223-3e0c-4b72-9f8c-c350aa1c06fa.png)


Sample data is included to test the implementation of this script.
