##Go through a list of files and reproject them to a standard projection

#Import ArcGIS Scripts
import sys, arcpy
import os
#Set the working environment
arcpy.env.workspace = "C:/Temp/"

#Now read the list of files to reproject and the list of file locations --> MUST MATCH ONE TO ONE
#Open the two files
in_list_loc = "C:/Tim_Goudge/Research_Data/Jezero/in_shp_files_list_5-18-2013.txt"
out_list_loc = "C:/Tim_Goudge/Research_Data/Jezero/out_shp_files_list_5-18-2013.txt"
in_list = open(in_list_loc,'r')
out_list = open(out_list_loc,'r')
#Count the number of lines in the two files
in_list_length = len(in_list.readlines())
out_list_length = len(out_list.readlines())
#Set both files back to start for later reading
in_list.seek(0)
out_list.seek(0)
#Now make sure the two files have the same lengths
if in_list_length != out_list_length:
	sys.exit("Length of input and output files does not match. Quitting.")
#Now get lists of all the files
in_list_temp = in_list.read()
in_file_list = in_list_temp.split('\n')
out_list_temp = out_list.read()
out_file_list = out_list_temp.split('\n')

#Now assign the location of the output projection
out_proj_loc = "C:/Tim_Goudge/Research_Data/Jezero/TAG_JEZERO_MAPPING_PROJ.prj"

#Now loop through each file and reproject it.
for i in range(0,in_list_length):
	try:
		#Get the input and output shapefiles from the list
		in_shp = in_file_list[i]
		out_shp = out_file_list[i]
		
		#Reproject the input shapefile
		arcpy.Project_management(in_shp, out_shp, out_proj_loc)
		
		print "Successful " + in_shp
	except:
		print "Not Successful " + in_shp
		print(arcpy.GetMessages())
		
