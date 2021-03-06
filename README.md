# TopoMapVisualiser
PYQGIS script for creating and styling elevation data using a DEM within QGIS 3X.


The TopoMapVisualiser script is a quick and simple method of visualising topographic features derived from a DEM. It applies a custom single band pseudocolor render to the DEM layer, whcih is draped over a hillshade layer to create a 3-dimensional look. Contours are also drawn at two intervals: 100 meters and 400 meters. The contour layers are symbolised appropriately, emphasising the 400-meter contours as important steps in elevation. TopoMapVisualiser also makes the most of the QuickOSM plugin to extract natural peaks within the extent of the supplied DEM. These are programitally styled and added to the topographic map to give extra detail to the visualisation. For more information on QuickOSM and instructions for installing the plugin in QGIS see here: https://docs.3liz.org/QuickOSM/.

This script was designed using elevatinon data for Victoria, Australia, however it is designed to work with other terrain datasets with different elevation ranges.
Please change the various filepath and attribute fields to suit your workspace before running the script.


![image](https://user-images.githubusercontent.com/72475218/136927883-fdc21d78-94f3-4120-b87b-1f2ed6e2f868.png)


The output can be visualised in 3D using QGIS 3D map view layout by selecting the DEM as the elevation source and adjusting the elevation scale accordingly.

![image](https://user-images.githubusercontent.com/72475218/136885890-fcc68223-3e0c-4b72-9f8c-c350aa1c06fa.png)


A sample DEM for the Victorian Alps is included, allowing you to test your own implementation.
