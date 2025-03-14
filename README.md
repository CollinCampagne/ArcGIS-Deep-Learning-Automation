# ArcGIS-Deep-Learning-Automation
This repository highlights the automation process for classifying raster imagery with predetermined training sites, and classification numbers resulting in a classified image, and a table of class percentages. 

## About
This script was created for Planetary Remote Sensing and the British Columbia Institute of Technology. The objective of this script is to obtain the most accurate classification of open source aerial RGB imagery. While traditional supervised machine-learning classification methods are effective at classifying 30 meter 8+ band imagery (such as Maximum Likelihood), aerial imagery is more common and easily accessible while being higher resolution. Because of these factors, being able to perform advanced analyses on it while minimizing the amount of time performing spectral enhancements ( like adjusting for haze and shadows) is greatly beneficial. Through analysis, ArcGIS Pro's Deep Learning Libraries allow for using advanced machine-learned models that more accurately classify images, reducing the amount of post-classification processes. 

This project takes a 20km^2 study area based around Coquitlam, British Columbia, and classifies surfaces into six different classes with different runoff and permeability characteristics. This lays the groundwork for future analyses, where the specific permeability and other hydrologic qualities to be applied to these surfaces, however accounting for these is outside of the scope of this project. 

### A note on ArcGIS DL Framework
In order to use this script, ArcGIS Pro Deep learning libraries must be installed in order to create models and perform DL pixel classifications. Download them here:
https://github.com/Esri/deep-learning-frameworks
These libraries are the easiest ways to integrate Pytorch, Keras, Tensorflow, and other machine learning methods into Pro in my experience, in large part due to ArcGIS Pro's method of training models. *The model creation and classification takes hours to complete. Times will vary based on the dedicated GPU memory the user has, but may take up to 10 hours with a standard, 4-gb GPU. 

** Methodology
The process for model training, followed by classification, is not straightforward. In this version of the script, the user submits two dependencies: 

1: The image to be classified. *Note: performing segmentation on the raster beforehand greatly enhances the accuracy of the classified raster,*

2: Training Areas, created by the user. 

With these inputs, the script creates a model using the training sites as inputs, then performs a Support Vector Machine classification on the image. After the creation of the classified image, the Summarize Categorical Raster tool is ran, which counts all of the pixels in each class. Using the sum, the scrip outputs a second table that calculates the percentage value for each class. 

** Conclusion
With the percentages of permeable surfaces, the tool may be run again using historical imagery of the same area. This will give the user the ability to see the amount of surface permeability changes over time as areas continue to be developed. 

** Future Updates:
Because of the time limitations and expectations of this project, the ability to perform hydrologic analysis is not accounted for. Having the script automatically perform modelling based on the rates of which water can be absorbed into each surface would create a specialized and practical tool for use by land developers and policy makers. Additionally, being able to model the surface with the input of elevation and volume of water would help in this task. 
