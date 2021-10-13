from qgis.core import *
from qgis import processing

# Define filepath to DEM file (please direct the filepath to your local machine).
rasterLyr = QgsRasterLayer("C:\\Users\\YOUR_FILEPATH_HERE\\DEM.tif", "DEM") 
rasterLyr.isValid() 

# Access raster band attribute statistics (elevation).
stats = rasterLyr.dataProvider().bandStatistics(1, QgsRasterBandStats.All)

# Create elevation groups which color rendering will be applied to.
# Maximum elevation value.
min = stats.minimumValue
# Minimum elevation value.
max = stats.maximumValue
# Range of elevation values.
range = max - min
# Find 25% of range.
quater = range//4
# Define lower range (25%).
lowerRange = min + quater
# Define mid-point range (50%).
half = range//2
middle = min + half
# Define upper range (75%).
upperRange = max - quater


# Push QGIS colour shader and set to interpolated.
fnc = QgsColorRampShader()
fnc.setColorRampType(QgsColorRampShader.Interpolated)

# Set interpolated colour ramp by assigning each group of elevation values a colour. RGBA values used to set lower transparency.
lst = [QgsColorRampShader.ColorRampItem(min, QColor(43,131,186,190), str(min)),\
    QgsColorRampShader.ColorRampItem(lowerRange, QColor (171,221,164, 190), str(lowerRange)),\
    QgsColorRampShader.ColorRampItem(middle, QColor(255,255,191,190), str(middle)),\
    QgsColorRampShader.ColorRampItem(upperRange, QColor(253,174,97,190), str(upperRange)),\
    QgsColorRampShader.ColorRampItem(max, QColor(215,25,28,190), str(max))]
fnc.setColorRampItemList(lst)

# Push QGIS shader and apply render to DEM layer.
shader = QgsRasterShader()
shader.setRasterShaderFunction(fnc)
renderer = QgsSingleBandPseudoColorRenderer(rasterLyr.dataProvider(), 1, shader)
rasterLyr.setRenderer(renderer)



# Define filepath for first contour layer (larger interval). Please change to a suitable filepath on your local machine.
contourFn = 'C:\\Users\\YOUR_FILEPATH_HERE\\ContoursLarge.shp'

# Parameters dictionary for first contour process. Change interval if necessary.
parametersC = {'INPUT': rasterLyr,
            'BAND': 1,
            'INTERVAL': 400,
            'FIELD_NAME': 'Band 1',
            'CREATE_3D': 0,
            'IGNORE_NODATA': 1,
            'NODATA': 0,
            'OFFSET': 0,
            'OUTPUT': contourFn}
            
# Run contour processing tool.
contourResult = processing.run("gdal:contour", parametersC)

# Add first contour output as a vector layer.
contourLyr = QgsVectorLayer(contourFn, "Contours_400m", "ogr")
# Set colour and transparency of contours.
contourLyr.renderer().symbol().setColor(QColor(8,8,8,150))
contourLyr.triggerRepaint()

# Define filepath for second contour layer (smaller interval). Please change to a suitable filepath on your local machine.
contourFn2 = 'C:\\Users\\YOUR_FILEPATH_HERE\\ContoursSmall.shp'

# Parameters dictionary for second contour process. Change interval if necessary.
parametersC2 = {'INPUT': rasterLyr,
            'BAND': 1,
            'INTERVAL': 100,
            'FIELD_NAME': 'Band 1',
            'CREATE_3D': 0,
            'IGNORE_NODATA': 1,
            'NODATA': 0,
            'OFFSET': 0,
            'OUTPUT': contourFn2}

# Run contour processing tool.
contourResult2 = processing.run("gdal:contour", parametersC2)

# Add second contour output as a vector layer.
contourLyr2 = QgsVectorLayer(contourFn2, "Contours_100m", "ogr")
# Set colour and greater transparency of contours.
contourLyr2.renderer().symbol().setColor(QColor(8,8,8,60))
contourLyr2.triggerRepaint()

# Define filepath for hillshade layer. Please change to a suitable filepath on your local machine.
hillshadeFn = 'C:\\Users\\YOUR_FILEPATH_HERE\\Hillshade.tif'

# Parameters dictionary for hillshade operation.
parametersH = {'INPUT': rasterLyr,
            'BAND': 1,
            'Z_FACTOR': 1,
            'AZIMUTH': 300,
            'OUTPUT': hillshadeFn}

# Run hillshade processing tool.
hillshadeResult = processing.run("gdal:hillshade", parametersH)
# Add result as raster layer.
hillshadeLayer = QgsRasterLayer(hillshadeFn, "Hillshade")

# Add all map layers. Do not change order as hillshade needs to be drawn first, followed by the DEM and finally the two contour layers.
QgsProject.instance().addMapLayers([hillshadeLayer])
QgsProject.instance().addMapLayers([rasterLyr])
QgsProject.instance().addMapLayers([contourLyr2])
QgsProject.instance().addMapLayers([contourLyr])

# Define the extent for the QuickOSM query builder tool set to the supplied DEM layer.
extent = rasterLyr.extent()
# Run a query in Overpass API and generate a download URL for natural peaks layer.
results = processing.run("quickosm:buildqueryextent", 
                        {"KEY":"natural", 
                         "VALUE":"peak", 
                         "EXTENT":extent})

# Establish filepath for OSM layer. Please change to a suitable folder on your local machine.
osmFn = 'C:\\Users\\YOUR_FILEPATH_HERE\\OSMPeaks.shp'
# Use the file downloader native tool to save the OSM layer to the filepath specified above.
osm = processing.run("native:filedownloader", 
                        {'URL':results['OUTPUT_URL'], 
                         'OUTPUT': osmFn})
# Establish the OSM layer as a vector layer in the workspace.
osmPeaks = QgsVectorLayer(osmFn, "Peaks", "ogr")

# Style the OSM peak point layer as black crosses.
osmPeaks.renderer().symbol().setColor(QColor("black"))
osmPeaks.renderer().symbol().symbolLayer(0).setShape(QgsSimpleMarkerSymbolLayerBase.CrossFill)
osmPeaks.triggerRepaint()
# Finally, add the OSM data to the map layer instance.
QgsProject().instance().addMapLayer(osmPeaks)
