# Pyradiomics: Feature Extraction Toolkit
## Overview
Pyradiomics is a feature extractor designed for radiomics analysis.
## Getting Started with Data Preprocessing
### Step 1: Define the Region of Interest (ROI)
To demarcate the ROI, employ the LabelMe annotation tool to label your dataset, resulting in JSON-formatted files.
**Installation:**
Ensure Python and pip are installed on your system. Then, install LabelMe using the following command:
```bash
pip install labelme
```

### Step 2: Convert JSON to Dataset
Transform the annotated JSON files into usable datasets using the `labelme_json_to_dataset` utility.
**Location:**
The tool is typically found at `D:\ProgramData\miniconda3\envs\labelme\Scripts\labelme_json_to_dataset.exe`.
**Conversion Script:**
To batch convert all JSON files in a directory, use the following batch script `json_to_dataset.bat`. Make sure to adjust the path to match your actual environment.
```batch
@echo off
for %%i in (*.json) do "D:\ProgramData\miniconda3\envs\rm\Scripts\labelme_json_to_dataset.exe" "%%i"
pause
```
**Note:**
Remember to update the script with the correct path to the `labelme_json_to_dataset` executable in your environment.

### Step 3: Prepare Your Images
The 'Image Preprocessing' folder contains essential codes for preparing your images for analysis. Here's what you need to do:
1. **Standardize Image Filenames:**
   Rename the image files to match the parent folder's name for consistency and easier management.
2. **Create Mask Files:**
   Generate mask files that correspond to your images, which are necessary for feature extraction.
3. **Convert to Grayscale:**
   If your images are not in grayscale, convert them to grayscale using the provided codes, as many radiomics features require monochromatic images.
4. **Copy Images to a Target Folder:**
   If you need to move images to a specific directory, utilize the `copy_file.py` script to facilitate this process.
**Instructions:**
- Navigate to the 'Image Preprocessing' folder to access the preprocessing codes.
- Follow the steps outlined in the code comments to execute each preprocessing task.
- Ensure that you have the necessary permissions to modify and move files within your file system.
By following these steps, you will have your images and masks ready for feature extraction with Pyradiomics.


## Extract Features with Pyradiomics
### Step 1: Install Pyradiomics Package
Begin by installing the Pyradiomics library using the pip command:
```bash
pip install pyradiomics
```
### Step 2: Execute Feature Extraction
To perform feature extraction, execute the `feature_extract.py` script. The extracted features will be saved in a file named `features.csv`.
**Important:**
- Ensure you update the paths to the image and mask files within the `feature_extract.py` script to reflect the correct locations on your system.
- Verify that the image and mask files are correctly preprocessed before running the feature extraction script.
By following these steps, you will be able to extract a comprehensive set of radiomics features from your medical images using Pyradiomics.

## Advanced Analysis: Feature Filtering and Evaluation
The `Feature Filtering and Analysis.ipynb` Jupyter Notebook is equipped with the necessary code to filter and analyze the extracted features. The process includes the following key steps:
### Step 1: Data Splitting
- **Dataset Division:** Partition your dataset into training and testing subsets to ensure that the model's performance can be accurately evaluated.
### Step 2: Feature Selection
- **Relevance Identification:** Utilize statistical methods such as the T-test and Lasso regularization, as well as machine learning-based feature selection techniques, to identify the most pertinent features for your analysis.
### Step 3: Classification
- **Feature Classification:** Implement the RandomForestClassifier to classify the selected features into two distinct classes, facilitating the subsequent analysis of feature importance and predictive power.
### Step 4: Result Visualization
- **Performance Metrics:** Visualize the classification results using a confusion matrix to understand the true positives, false positives, true negatives, and false negatives.
- **ROC Curve:** Plot the Receiver Operating Characteristic (ROC) curve to assess the classifier's performance and to determine the area under the curve (AUC), which indicates the classifier's ability to distinguish between classes.
- **Additional Charts:** Explore other visualizations as needed to gain further insights into the feature set and classification outcomes.
By working through the `Feature Filtering and Analysis.ipynb` notebook, you will be able to refine your feature set, build a predictive model, and interpret the results in a meaningful way. Ensure that you adjust parameters and paths within the notebook to fit your specific dataset and analysis requirements.

