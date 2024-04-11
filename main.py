# Imports
from backend.Yolo_Car_crop import Car_crop
from backend.ocr import OCR_detect
from backend.car_model_predict import Car_model
from backend.car_color_predict import Car_color
import os
import cv2
import time
import yaml
import math
import torch
# import rembg
import random
import shutil
import easyocr
import numpy as np
import pandas as pd
from PIL import Image
from ultralytics import YOLO

# Deep Learning Models
from glob import glob
from pandas import read_csv
import matplotlib.pyplot as plt

## deep learning
from keras.models import Sequential
from keras.preprocessing import image
# from tensorflow.keras.models import Model
# from tensorflow.keras import regularizers
from tensorflow.keras.models import load_model
# from tensorflow.keras.applications import efficientnet
# from keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.preprocessing.image import img_to_array, load_img
# from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, BatchNormalization, Flatten, Input, Conv1D, Conv2D, MaxPooling2D


cc = Car_crop()
ocr = OCR_detect()
cmp = Car_model()
color = Car_color()
# Storing data in this folder 
path = 'Data/'

# Car Model Predition Model
car_model = 'Models/SW_Classification_EfficientNet'
# Car Color Prediction Model
car_color_model = 'Models/Car_Color_model_4'
# This list is not exaustive
model_names = ['swift', 'wagonr']
color_list = ['black', 'blue','red','white']
# Load the saved model
car_model_efficientNet = load_model(car_model)
car_color_efficientNet = load_model(car_color_model)
# Initialize easyOCR
reader = easyocr.Reader(['en'])
input_np = 'MH43BE1907'

# Initialize Yolo model instance
npd_model_path = 'Models/YOLOv5 Licence Plate Detector/licence_plate_detection_model_weights.pt'

model = YOLO("yolov8m.pt")
model_npd = torch.hub.load('ultralytics/yolov5', 'custom', path=npd_model_path)


'''Implementation ''' 
# Parameter inputs
frames_per_second = int(input("Enter Number of Frames per second:"))

# Defining the directory name
dir_name = input("Enter Directory Name to Store cropped images: ")
# Location of the input video
video_path = 'video/Trim_8_5PM.mp4'
# video_path = '/content/drive/MyDrive/BE Project Group 29/Trimmed Clips/test_video1.mp4'
# Locating output Directory
output_directory = path + dir_name
os.makedirs(output_directory, exist_ok=True)
os.makedirs(output_directory+'/frames/', exist_ok=True)
os.makedirs(output_directory+'/car_cropped/', exist_ok=True)
os.makedirs(output_directory+'/npd_cropped/', exist_ok=True)

start_time = time.perf_counter()

cc.video_to_frames(video_path, output_directory, frames_per_second, model, model_npd)
cc.delete_intermediate()

ocr.OCR_modified(output_directory,reader,input_np)

# Storing Car Cropped Data
car_cropped_data = pd.DataFrame(columns = ['car_cropped_image_path','car_cropped_image_filename','car_color','color_confidence','car_model','model_confidence'])
data = {}
data_list = []
for filename in os.listdir(output_directory+'/car_cropped'):
    model_confidence = 0
    model_label = ''
    color_confidence = 0
    color_label = ''
    # Check if the current item is a file (not a directory)
    if os.path.isfile(os.path.join(output_directory+'/car_cropped', filename)):
        # For Car Model
        model_label, model_confidence = cmp.predict_car_class(car_model_efficientNet,output_directory+'/car_cropped/'+filename,model_names)
        # Process the file or perform any desired operation
        print(f"Label = {model_label} | confidence = {model_confidence}")
        # For Car color
        color_label, color_confidence = color.predict_car_color(car_color_efficientNet,output_directory+'/car_cropped/'+filename,color_list)
        # Process the file or perform any desired operation
        print(f"Label = {color_label} | confidence = {color_confidence}")
    # Store the color and model data into the system
    data = {'car_cropped_image_path':output_directory+'/car_cropped/'+filename,'car_cropped_image_filename':filename,
                    'car_color':color_label,'color_confidence': f'{color_confidence:.2f}%','car_model':model_label,'model_confidence':f'{model_confidence:.2f}%'}
    data_list.append(data)
car_cropped_data = pd.DataFrame(data_list)
car_cropped_data.to_csv(output_directory+'/car_cropped_data.csv', index=False)



end_time = time.perf_counter()
print(f"Total Time For Entire Process : {end_time - start_time:.2f}")