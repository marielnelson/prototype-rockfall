#Importing standard library modules
import sys, string, os, arcpy, glob
import shutil
#Set the working environment
arcpy.env.workspace = "C:/Temp/"

#SETUP THE INPUT PATH
inpath="C:/Users/tag2646/Desktop/Goudge_Working/Projects/Schorghofer_RSLs/*/"
temp_DEM_list = glob.glob(inpath+"*DEM.tif")
dummy_base_path = os.path.dirname(temp_DEM_list[0])


#Copy the dummy DEM here
arcpy.CopyRaster_management("C:/Users/tag2646/Desktop/Goudge_Working/Scripts_Tools_etc/Python_Scripts/A-DEM.tif",dummy_base_path+"/A-DEM.tif")
shutil.copyfile("C:/Users/tag2646/Desktop/Goudge_Working/Scripts_Tools_etc/Python_Scripts/A-DEM.prj",dummy_base_path+"/A-DEM.prj")

#Get the list of DEMs and DRGs
in_DEM_raster_list = glob.glob(inpath+"*DEM.tif")
in_DRG_raster_list = glob.glob(inpath+"*DRG.tif")

#Loop through and assign projections, buildpyramids, and stretch DEMs. Also
#   mask data < -15000 to NaN
for in_raster in in_DEM_raster_list:
    raster = in_raster
    projection = in_raster.split(".tif")[0] + ".prj"
    out_mask_name = in_raster.split(".tif")[0] + "_masked.tif"
    try:
        arcpy.DefineProjection_management(raster, projection)
        arcpy.BuildPyramids_management(raster)
        arcpy.CalculateStatistics_management(raster,"1","1","-32767")
        where_clause = "VALUE >= -15000"
        # Check out the ArcGIS Spatial Analyst extension license
        arcpy.CheckOutExtension("Spatial")
        out_mask_data = arcpy.sa.Con(raster, raster, "", where_clause)
        out_mask_data.save(out_mask_name)
        print "Successful: "+raster
    except Exception, ErrorDesc:
        print "Not Successful: "+raster
        print ErrorDesc

print "DONE DEM"

#Loop through and assign projections, buildpyramids, and stretch DRGs.
for in_raster_2 in in_DRG_raster_list:
    raster_2 = in_raster_2
    projection_2 = in_raster_2.split(".tif")[0] + ".prj"
    try:
        arcpy.DefineProjection_management(raster_2, projection_2)
        arcpy.BuildPyramids_management(raster_2)
        arcpy.CalculateStatistics_management(raster_2,"1","1","0")
        print "Successful: "+raster_2
    except Exception, ErrorDesc:
        print "Not Successful: "+raster_2
        print ErrorDesc

print "DONE DRG"

#Get list of masked DEMs
in_masked_DEM_raster_list = glob.glob(inpath+"*DEM_masked.tif")

#Loop through and assign projections, buildpyramids, and stretch masked DEMs.
for in_raster_3 in in_masked_DEM_raster_list:
    raster_3 = in_raster_3
    projection_3 = in_raster_3.split("_masked.tif")[0] + ".prj"
    try:
        arcpy.DefineProjection_management(raster_3, projection_3)
        arcpy.BuildPyramids_management(raster_3)
        arcpy.CalculateStatistics_management(raster_3,"1","1","-32767")
        print "Successful: "+raster_3
    except Exception, ErrorDesc:
        print "Not Successful: "+raster_3
        print ErrorDesc


arcpy.Delete_management(dummy_base_path+"/A-DEM.tif")
arcpy.Delete_management(dummy_base_path+"/A-DEM_masked.tif")
print "DONE MASKED DEMs"

