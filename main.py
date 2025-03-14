# Collin Campagna, A01312964
# collinacampagne@gmail.com
# Created May 06, 2024
# Submitted May 24, 2024
# Updated: 07/30/2024

# Created for Planetary Remote Sensing under the supervision of Ramin Azar and Joshua MacDougall (BCIT GIS Faculty).

# INFO: This tool automates the classification of pixels within aerial imagery. 
# The output is a classified raster and a table with the percentages of pixels within each class.
# ***IMPORTANT*** In order to run this tool, ArcGIS Pro Deep Learning Libraries must be installed for the relevant version of ArcGIS Pro on the machine. 
# This script was written and used using ArcGIS Pro 3.2. Updates may need to be made for subsequent versions of ArcGIS. 

# ===================================================================================================================================================
# Imports:
# ===================================================================================================================================================

import arcpy
from arcpy.ia import *
import sys
import math
import os
import traceback


# ===================================================================================================================================================
# Establishing the class types and parameters. 
# ===================================================================================================================================================

class Toolbox(object):

    def __init__(self):  
        self.label = "DLAutomation"
        self.alias = "Deep Learning Automation"
        self.tools = [DLAutomation]

class DLAutomation(object):
    def __init__(self):
        self.label = "Image Segmentation"
        self.description = "Takes an image and performs a Segment Mean Shift"
        
    def getParameterInfo(self):
        # Image Input
        Image = arcpy.Parameter(
            displayName="Input Image",
            name="roads",
            datatype="GPRasterLayer", 
            parameterType="Required",
            direction="Input")
        
        Image.filter.list = ["Raster"]
        # Model Training Input
        TrainingData = arcpy.Parameter(
            displayName="TrainDLModel",
            name="Train Deep Learning Model",
            datatype="DEFolder", 
            parameterType="Required",
            direction="Input")

        parameter = [Image, TrainingData]
        
        return parameter
    
# ===================================================================================================================================================
# Establish appropriate licenses are checked out (image analyst)
# ===================================================================================================================================================

    def isLicensed(self):
            return True

    def update(self, parameter):
        if parameter[0].altered:
            parameter[1].value = arcpy.ValidateFieldName(parameter[1].value, parameter[0].value)
        return

    
    def updateMessages(self, parameter):
        return

# ==============================================================================================
# Execute the tools
# ==============================================================================================

    def execute(self, parameter, messages):
        # Check out Image Analyst license:
        arcpy.CheckOutExtension("ImageAnalyst") 

        # Process: Segment Mean Shift of 3-band aerial imagery.
        Image = parameter[0].valueAsText
        Spectral = "18.5"
        Spatial = "10"
        MinSegSize = "20"


        SMS = arcpy.SegmentMeanShift(Image, Spectral, Spatial, MinSegSize)
        SMS.save(arcpy.env.workspace)

# ===================================================================================================================================================
        # create a folder for the model definition output. 
# ===================================================================================================================================================
       
        out_folder = "models"
        parent_dir = arcpy.env.workspace
        path = os.path.join(parent_dir, out_folder)

        TrainingData = parameter[1].valueAsText
        max_epochs = 20
        model_type = "UNET"
        batch_size = 8
        arg = "IGNORE_CLASSES 'false';"
        backbone_model = "RESNET34" 
        validation_percent = 10
        stop_training = "STOP_TRAINING"
        freeze = "UNFREEZE_MODEL"

        # Train the model. Uses U-NET method and Resnet34 backbone. 
        model = arcpy.TrainDeepLearningModel(TrainingData, path, max_epochs, model_type, 
            batch_size, arg, backbone_model,
            validation_percent, stop_training, freeze)
        model.save(os.path.join("DLModel.emd"))
        
# ===================================================================================================================================================
# Run a DL pixel classification after training the model. 
# ===================================================================================================================================================

        args = "padding 56; batch_size 4; tile_size 224"
        processingMode = "PROCESS_AS_MOSAICKED_IMAGE"

        DLClassRaster = arcpy.ClassifyPixelsUsingDeepLearning(SMS, model, args, processingMode)
        DLClassRaster.save(arcpy.env.workspace)
        
# ===================================================================================================================================================
# Perform a Summarize Categorical Raster function on the output raster
# ===================================================================================================================================================

        outTableName = "ClassSummary.csv"
        outTable = os.path.join(parent_dir, outTableName)

        ClassSummary = arcpy.ia.SummarizeCategoricalRaster(DLClassRaster, outTable)

# ===================================================================================================================================================
# Calculate the percent of pixels in each class 
# ===================================================================================================================================================


        fields = arcpy.ListFields(ClassSummary)
        numFields = len(fields) - 1
        with arcpy.da.SearchCursor(ClassSummary,"*" ) as cursor:
            for row in cursor:
                rowSum = sum(row[1:])

                classValue += row[0]

            if rowSum != 0:
                classValue= [value / rowSum for value in row[1:numFields]]
            

    # establish percentage for individual classes
        classPercent = classValue * 100
        print(classPercent)


    # No. Pixels in each class from SCR operation
    # (Class pixels / Total pixels) * 100
    # output .xls file.
# ===================================================================================================================================================

    def postExecute(self, parameter):
        return