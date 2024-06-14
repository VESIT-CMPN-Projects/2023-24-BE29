# Imports
from backend.Yolo_Car_crop import Car_crop
from backend.ocr import OCR_detect
from backend.car_model_predict import Car_model
from backend.car_color_predict import Car_color
from backend.get_coords import GetCoords
from backend.tracking import run_tracker
import os
import cv2
import time
import torch
import sqlite3
import easyocr
import numpy as np
import pandas as pd
from ultralytics import YOLO
import os
from PIL import Image

# UI Imports
import sys
from PyQt5.QtWidgets import QApplication
from frontend.SignUp import SignUpPage
from frontend.Login import LoginPage
from frontend.Dashboard import DashboardPage
from frontend.db import GetCarDetails

# Flask
# from flask import Flask, render_template, redirect, request

from werkzeug.utils import secure_filename
# Create an instance of the GetCarDetails class
car_det = GetCarDetails()

# Backend Instances
cc = Car_crop()
ocr = OCR_detect()
cmp = Car_model()
color = Car_color()
getcord = GetCoords()
from tensorflow.keras.models import load_model
# Trial 
from keras.layers import TFSMLayer


# Taking input from the UI
# input_numplate = GetNumberPlate()
# Storing data in this folder
path = 'Data/'
# Car Model Predition Model
car_model = 'Models/SW_Classification_EfficientNet'
# car_model = TFSMLayer('Models/SW_Classification_EfficientNet', call_endpoint='serving_default')
# car_model = 'Models/SW_Classification_EfficientNet'

# Car Color Prediction Model
car_color_model = 'Models/Car_Color_model_4'

# This list is not exaustive
model_names = ['swift', 'wagonr']
color_list = ['black', 'blue','red','white']
# Load the saved model
# car_model_efficientNet = TFSMLayer('Models/SW_Classification_EfficientNet', call_endpoint='serving_default') 
car_model_efficientNet = load_model(car_model,compile=False)
print('Initialized Car Model Prediction')
car_color_efficientNet = load_model(car_color_model,compile=False)
print('Initialized Car Color Prediction')
# Initialize easyOCR
reader = easyocr.Reader(['en'])
# Initialize Yolo model instance
npd_model_path = 'Models/YOLOv5 Licence Plate Detector/licence_plate_detection_model_weights.pt'
print('Initialized npd_model')
model = YOLO("yolov8m.pt")
print('Initialized YOLO for Object Detection')
model_npd = torch.hub.load('ultralytics/yolov5', 'custom', path=npd_model_path)


def execute_models():
# Call the get_last_number_plate() method to retrieve the last number plate from the database
    input_np = car_det.get_last_number_plate()
    input_color = car_det.get_last_color()
    input_model = car_det.get_last_model()
    # Parameter inputs
    
    # Location of the input video
    # video_path = 'E:/Carmodelflow/MSD_Dir/MSD_Dir/video/Trim_8_5PM.mp4'
    
    
    # camera = input('Select Camera:')
    if input_color == 'red':
        video_path = 'video/Trim_4_5PM.mp4'
        print('VESIT Main Entrance Selected')
        frames_per_second = 5
    elif input_color == 'white':
        video_path = 'video/Engg_entrance.mp4'
        print('VESIT Engineering Entrance Selected')
        frames_per_second = 2
    else:
        video_path = 'video/Trim_4_5PM.mp4'
        frames_per_second = 5

    # video_path = '/content/drive/MyDrive/BE Project Group 29/Trimmed Clips/test_video1.mp4'
    # Locating output Directory
    # output_directory = "E:/Carmodelflow/MSD_Dir/MSD_Dir/Data/Tanmay1"
    output_directory = "Data/Footages"
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(output_directory+'/frames/', exist_ok=True)
    os.makedirs(output_directory+'/car_cropped/', exist_ok=True)
    # Comment later
    os.makedirs(output_directory+'/npd_cropped/', exist_ok=True)
    os.makedirs(output_directory+'/car_cropped_txt/', exist_ok=True)

    start_time = time.perf_counter()

    cc.video_to_frames(video_path, output_directory, frames_per_second, model, model_npd)
    cc.delete_intermediate()

    directory = output_directory+ "/car_cropped"

    # List all files in the directory
    files = os.listdir(directory)

    # Filter only image files (you can add more image extensions if needed)
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    images_data = []
    # Create a dictionary to store image data
    for image_file in image_files:
        deleted = False
        # Construct the full path to the image
        image_path = os.path.join(directory, image_file)
        # image =np.array(Image.open(image_path))
        image = cv2.imread(image_path)
        npd_img, cropped_npd_img = cc.number_plate_detection(image, model_npd)

            # sim_score = sim_score
        model_label, model_confidence = cmp.predict_car_class(car_model_efficientNet,
                                                            image_path, model_names)


        # For Car color
        color_label, color_confidence = color.predict_car_color(car_color_efficientNet,
                                                                image_path, color_list)
        if color_label != input_color or model_label != input_model:
            os.remove(image_path)
            print('The car color or model is not same as of the stolen car')
            deleted = True
        else:
            print(f"Label = {model_label} | confidence = {model_confidence}")
            print(f"Label = {color_label} | confidence = {color_confidence}")

        # Get initial values for color, model, and number plate
        if deleted == False:
            numplate = None
            sim_score = 0
            if np.any(cropped_npd_img):
                numplate=ocr.OCR_modified(reader,input_np,cropped_npd_img)
                sim_score = ocr.calculate_similarity_score(input_np,numplate)
                sim_score = sim_score/100

            image_data = {
                'image_name': image_file,
                'color': color_label,
                'color_confidence':color_confidence,
                'model': model_label,
                'model_confidence': model_confidence,
                'number_plate': numplate,
                'np_similarity_score': sim_score,
            }

            # Append the initial image data to the list
            images_data.append(image_data)
        # List of Remaining Images
    files = os.listdir(directory)
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    txt_directory = output_directory+ "/car_cropped_txt"
    first_frame_centers = []
    last_frame_centers = []
    if image_files != []:
        first_frame_centers, last_frame_centers = getcord.get_coords(image_files_list=image_files,txt_dir=txt_directory)
        
        first_frame_centers_lst = []
        for tup in first_frame_centers:
            for cord in tup:
                first_frame_centers_lst.append(cord)
        
        last_frame_centers_lst = []
        for tup in last_frame_centers:
            for cord in tup:
                last_frame_centers_lst.append(cord)
        
        first_frame_centers = first_frame_centers_lst
        last_frame_centers = last_frame_centers_lst
    else:
        print('No Car found')
        
    print("Final................................................................................................")
    # print(images_data)
    print(f'Image Files List: {image_files}')
    print(f'Start Frame: {list(first_frame_centers)}')
    print(f'End Frame {list(last_frame_centers)}')
    run_tracker(list(first_frame_centers),list(last_frame_centers))
    framesdata=pd.DataFrame(images_data)
    framesdata.to_csv("Data/Footages/ReIddata.csv")


if __name__ == '__main__':
    # UI 
    app = QApplication(sys.argv)
    # UI Pages Instances
    signup_page = SignUpPage()
    login_page = LoginPage()
    dashboard_page = DashboardPage()

    signup_page.show_login_signal.connect(login_page.show)
    login_page.show_signup_signal.connect(signup_page.show)
    login_page.login_successful.connect(dashboard_page.show)
    dashboard_page.submit_from_signal.connect(execute_models) 
    login_page.show()
    # bc.execute_models
    sys.exit(app.exec_())


