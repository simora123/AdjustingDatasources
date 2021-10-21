#-------------------------------------------------------------------------------
# Name:       Change_Data_Source.py
# Purpose:    Loop through all workspaces that house mxds for service publishing.
#             Changes the data source from our old server ARCGIS to ARCGIS1. Then saves
#
# Author:      Joseph Simora - Senior GIS Analyst
#              jsimora@ycpc.org
#
# Created:     09/30/2021
#-------------------------------------------------------------------------------


import arcpy, os, shutil
from arcpy import env

#wrkspc = arcpy.GetParameterAsText(0)
wrkspc = r'H:\GIS\GIS_Server_Replacement\Test\hazard_mitigation'

dirlist = []

# Create text file for logging results of script
# Update to directory on SCTF server
file = wrkspc + "\\" + "{}".title().format(wrkspc.split("\\")[-1]) + " Folder MXDS.txt"
# Open text file in write mode and log results of script
report = open(file,'w')

# Define functions
def message(report,message):
    """ Write a message to a text file
    report is the text file to write the messages to
    report should be defined as report = open(path to file, mode)
    message is the string to write to the file
    """
    timeStamp = time.strftime("%b %d %Y %H:%M:%S")
    report.write("{} {} \n".format(timeStamp,message))
    print ("{}: ".format(timeStamp) + message)

for root, dirs, files in os.walk(wrkspc):
    for subdirs in dirs:
        if subdirs.endswith('gdb'):
            pass
        else:
            if subdirs == "ARCDB1":
                pass
            else:
                dirlist.append(os.path.join(root, subdirs))

for dir in dirlist:
    arcpy.env.workspace = dir
    mxdList = arcpy.ListFiles("*.mxd")
    if len(mxdList) != 0:
        ARCDB1_Folder = os.path.join(dir, "ARCDB1")
        isFile = os.path.exists(ARCDB1_Folder)
        if isFile == True:
            shutil.rmtree(ARCDB1_Folder)

        os.mkdir(ARCDB1_Folder)

        arcpy.AddMessage("******* " + str(dir) + " *******")
        message(report, "******* " + str(dir) + " *******")

        for mxd in mxdList:
            try:
                message(report, str(mxd))
                arcpy.AddMessage(str(mxd))
            except:
                message(report, "MXD - SYNTAX ERROR")
                pass
            mxdPath = os.path.join(dir, mxd)
            mxdObject = arcpy.mapping.MapDocument(mxdPath)
            Total = 0

            for lyr in arcpy.mapping.ListLayers(mxdObject):
                if lyr.supports("DATASOURCE"):
                    #print str(lyr.dataSource)
                    if str(lyr.dataSource).startswith(r"C:\Users"):
                        #print str(lyr.dataSource)

                        Root = os.path.join(str(lyr.dataSource.split("\\")[0]),"\\",str(lyr.dataSource.split("\\")[1]),"jsimora.YCPC",str(lyr.dataSource.split("\\")[3]),str(lyr.dataSource.split("\\")[4]),\
                        str(lyr.dataSource.split("\\")[5]), "Desktop10.6", str(lyr.dataSource.split("\\")[7]))
                        #print Root
                        lyrTruncate = str(lyr.dataSource.split("\\")[-2])
                        lyrTruncate_Final = str(lyrTruncate.split(".")[-1])
                        if lyrTruncate_Final == 'Land_Base' or lyrTruncate_Final == 'Transportation' or lyrTruncate_Final == 'WaterSystems' or lyrTruncate_Final == 'YCDES':
                            message (report, "\tLayer: " + lyr.name)
                            message(report, "\t OLD SOURCE: " + os.path.join(str(lyr.dataSource.split("\\")[-3]),str(lyr.dataSource.split("\\")[-2]), str(lyr.dataSource.split("\\")[-1])))
                            arcpy.AddMessage("\t OLD SOURCE: " + os.path.join(str(lyr.dataSource.split("\\")[-3]),str(lyr.dataSource.split("\\")[-2]), str(lyr.dataSource.split("\\")[-1])))
                            lyrConnection = str(lyr.dataSource.split("\\")[-3])
                            lyrConnectionTemp1 = lyrConnection.split("@")[-1]
                            lyrConnectionTemp2 = lyrConnectionTemp1.split(".")[0]
                            if lyrConnectionTemp2 == 'York':
                                lyrConnectionFinal = lyrConnection.split("@")[0] + "@" + lyrConnectionTemp2 + "1.sde"
                            if lyrConnectionTemp2 != 'York':
                                lyrConnectionTemp3 = str(lyrConnectionTemp2.split("_")[0]) + "1_" + str(lyrConnectionTemp2.split("_")[-1]) + ".sde"
                                lyrConnectionFinal = lyrConnection.split("@")[0] + "@" + lyrConnectionTemp3
                            #print lyrConnectionFinal

                            lyrDataset = str(lyr.dataSource.split("\\")[-2])
                            lyrDatasetTemp1 = lyrDataset.split(".")[0]
                            lyrDatasetFinal = lyrDatasetTemp1 + "1." + lyrDataset.split(".")[1] + "." + lyrDataset.split(".")[2]
                            #print lyrDatasetFinal

                            lyrSource = str(lyr.dataSource.split("\\")[-1])
                            lyrSourceTemp1 = lyrSource.split(".")[0]
                            if lyrSourceTemp1 == 'York':
                                lyrSourceFinal = lyrSourceTemp1 + "1." + lyrSource.split(".")[1] + "." + lyrSource.split(".")[2]
                            if lyrSourceTemp1 != 'York':
                                lyrSourceTemp2 = lyrSourceTemp1.split("_")[0] + "1_" + lyrSourceTemp1.split("_")[-1]
                                lyrSourceFinal = lyrSourceTemp2 + "." + lyrSource.split(".")[1] + "." + lyrSource.split(".")[2]

                            #print lyrSourceFinal + "\n"

                            lyrPath = os.path.join(Root,lyrConnectionFinal)
                            #print lyrPath + "\n"

                            lyr.replaceDataSource(lyrPath, "SDE_WORKSPACE", lyrSourceFinal, "")
                            message(report, "\t NEW SOURCE: " + os.path.join(lyrConnectionFinal, lyrDatasetFinal, lyrSourceFinal) + "\n")
                            arcpy.AddMessage("\t NEW SOURCE: " + os.path.join(lyrConnectionFinal, lyrDatasetFinal, lyrSourceFinal) + "\n")
                            Total = Total + 1

                        else:
                            message (report, "\tLayer: " + lyr.name)
                            message(report, "\t OLD SOURCE: " + os.path.join(str(lyr.dataSource.split("\\")[-2]), str(lyr.dataSource.split("\\")[-1])))
                            arcpy.AddMessage("\t OLD SOURCE: " + os.path.join(str(lyr.dataSource.split("\\")[-2]), str(lyr.dataSource.split("\\")[-1])))
                            #Root = lyr.dataSource.split("\\")[0]
                            lyrPath = os.path.join(Root, str(lyr.dataSource.split("\\")[-2]),str(lyr.dataSource.split("\\")[-1]))
                            #print lyrPath
                            lyrDataset = str(lyr.dataSource.split("\\")[-2])
                            lyrDatasetTemp1 = lyrDataset.split("@")[-1]
                            if lyrDatasetTemp1.split(".")[0] == 'York':
                                lyrDatasetTemp2 = lyrDatasetTemp1.split("_")[0]
                                lyrDatasetTemp3 = lyrDatasetTemp2.split(".")[0] + "1." + lyrDatasetTemp2.split(".")[-1]
                                lyrDatasetFinal = lyrDataset.split("@")[0] + "@" + lyrDatasetTemp3
                                #print lyrDatasetFinal
                                lyrSource = str(lyr.dataSource.split("\\")[-1])
                                lyrSourceTemp1 = lyrSource.split(".")[0]
                                second = lyrSourceTemp1.split("_")[0]
                                final = second + "1" + "." + lyrSource.split(".")[-2] + "." + lyrSource.split(".")[-1]
                            else:
                                lyrDatasetTemp2 = lyrDatasetTemp1.split(".")[0]
                                lyrDatasetTemp3 = lyrDatasetTemp2.split("_")[0] + "1_" + lyrDatasetTemp2.split("_")[-1]
                                lyrDatasetFinal = lyrDataset.split("@")[0] + "@" + lyrDatasetTemp3 + ".sde"

                                lyrSource = str(lyr.dataSource.split("\\")[-1])
                                lyrSourceTemp1 = lyrSource.split(".")[0]
                                second = lyrSourceTemp1.split("_")[0]
                                final = second + "1_" + lyrSourceTemp1.split("_")[-1] + "." + lyrSource.split(".")[-2] + "." + lyrSource.split(".")[-1]

                            Final = os.path.join(Root, lyrDatasetFinal)
                            #print os.path.join(Final, final)

                            lyr.replaceDataSource(Final, "SDE_WORKSPACE", final, "")
                            message (report, "\t NEW SOURCE: " + os.path.join(lyrDatasetFinal, final) + "\n")
                            arcpy.AddMessage("\t NEW SOURCE: " + os.path.join(lyrDatasetFinal, final) + "\n")
                            Total = Total + 1

            if Total != 0:
                message (report, "\t Found a Total of {} Data Source Changes. Saving MXD to ARCDB1 Folder\n".format(Total))
                arcpy.AddMessage("\t Found a Total of {} Data Source Changes. Saving MXD to ARCDB1 Folder\n".format(Total))
                mxdObject.saveACopy(os.path.join(ARCDB1_Folder, mxd))
                #mxdObject.save()
                del mxdObject
            else:
                message (report, "\t Found {} Data Source Changes. :(\n".format(Total))
                arcpy.AddMessage("\t Found {} Data Source Changes. :(\n".format(Total))
                del mxdObject

        if Total == 0:
            shutil.rmtree(ARCDB1_Folder)

    else:
        pass

message (report, "Script Complete")
arcpy.AddMessage("Script Complete")

report.close()
#End of Script




