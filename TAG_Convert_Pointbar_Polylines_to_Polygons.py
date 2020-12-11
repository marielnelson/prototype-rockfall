#Importing standard library modules
import sys, string, os, arcpy, glob, gc, shutil, numpy
#Set the working environment
gc.collect()
arcpy.env.workspace = "C:/Temp/"
arcpy.env.overwriteOutput = True

#SETUP THE INPUT PATH AND FILE NAME
inpath="C:/Users/tag2646/Desktop/Goudge_Working/Projects/Rio_Grande/Shapefiles/TAG_Pointbar_Mapping/"
in_shp_name="TAG_Mapped_Rio_Grande_Bar_Areas_12_1946_Polyline.shp"
in_shp = inpath + in_shp_name
out_shp = inpath + in_shp_name.split("Polyline.shp")[0] + "Polygon.shp"

#Make temporary folders to store the split up bar edges and perpindiculars
try:
    os.mkdir(inpath+"temp_single_image/")
    os.mkdir(inpath+"temp_single_image_unsplit_lines/")
    os.mkdir(inpath+"temp_single_image_polygons/")
except OSError:
    print OSError

#Get all the unique values from this shapefile
temp_datatable = arcpy.da.TableToNumPyArray(in_shp,('Image_ID'))
unique_image_ids = numpy.unique(temp_datatable['Image_ID']).tolist()
unique_image_ids_length = len(unique_image_ids)

#Now loop through each image, and extract those associated lines, unsplit, and convert to polygons
for i in range(0, unique_image_ids_length):
    try:
        #Get the image ID and set up some names
        temp_image_id = unique_image_ids[i]
        temp_lines_name = inpath+"temp_single_image/"+"temp_lines_"+temp_image_id+".shp"
        temp_unsplit_lines_name = inpath+"temp_single_image_unsplit_lines/"+"temp_unsplit_lines_"+temp_image_id+".shp"
        temp_polygons_name = inpath+"temp_single_image_polygons/"+"temp_polygons_"+temp_image_id+".shp"

        #Select all the lines with this image ID
        arcpy.MakeFeatureLayer_management(in_shp,"tempFtlyr")
        arcpy.SelectLayerByAttribute_management(in_layer_or_view="tempFtlyr",selection_type="NEW_SELECTION",where_clause=("\"Image_ID\" = '" + temp_image_id + "'"))
        arcpy.CopyFeatures_management("tempFtlyr",temp_lines_name)
        arcpy.Delete_management("tempFtlyr")

        #Now unsplit those lines
        arcpy.UnsplitLine_management(temp_lines_name,temp_unsplit_lines_name)

        #Now covnert them to a polygon amd add image ID back
        arcpy.FeatureToPolygon_management(temp_unsplit_lines_name,temp_polygons_name)
        arcpy.AddField_management(temp_polygons_name,"Image_ID","TEXT",50)
        arcpy.CalculateField_management(temp_polygons_name,"Image_ID",("\"" + temp_image_id + "\""),"PYTHON_9.3")
    except Exception, ErrorDesc:
        print "Error creating individual polygons."
        print ErrorDesc


#Now merge all the polygons into one
all_polygon_list = glob.glob(inpath+"temp_single_image_polygons/temp_polygons_*.shp")
polygon_python_list = []
for ind_polygon in all_polygon_list:
    polygon_python_list.append(ind_polygon)

try:
    arcpy.Merge_management(polygon_python_list,out_shp)  
except Exception, ErrorDesc:
    print "Error merging polygons."
    print ErrorDesc

#Now delete the temporary folders
try:
    shutil.rmtree(inpath+"temp_single_image/")
    shutil.rmtree(inpath+"temp_single_image_unsplit_lines/")
    shutil.rmtree(inpath+"temp_single_image_polygons/")
except OSError:
    print OSError

print "DONE CREATING POLYGONS!!!"

    


