from osgeo import ogr
from osgeo import osr
import glob,os
import magic

'This takes as input a directory containing all the files including shapefile *.prj'
def reproject_from_native_to_WGS84(container_directory):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    os.chdir(container_directory)
    for file in glob.glob("*.shp"):
        presumed_shapefile = magic.from_file(container_directory + file)
        if presumed_shapefile.lower().startswith('esri shapefile'):
            dataset = driver.Open(container_directory + file)
            layer = dataset.GetLayer()
            inSpatialRef = layer.GetSpatialRef()
            outSpatialRef = osr.SpatialReference()
            outSpatialRef.ImportFromEPSG(4326)

            # create the CoordinateTransformation
            coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

            # create the output layer
            outputShapefile = container_directory + '/' + r'transform_4326.shp'
            if os.path.exists(outputShapefile):
                driver.DeleteDataSource(outputShapefile)
            outDataSet = driver.CreateDataSource(outputShapefile)
            outLayer = outDataSet.CreateLayer("transform_4326", geom_type=ogr.wkbMultiPolygon)

        else:
            #exception
            pass