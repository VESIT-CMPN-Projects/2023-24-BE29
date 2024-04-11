# Imports
from backend.Yolo_Car_crop import Car_crop
from backend.ocr import OCR_detect
from backend.car_model_predict import Car_model
from backend.car_color_predict import Car_color
from backend.get_coords import GetCoords

import os
import cv2
import time
import torch
import easyocr
import numpy as np
import pandas as pd
from ultralytics import YOLO
import os
from PIL import Image



from tensorflow.keras.models import load_model


cc = Car_crop()
ocr = OCR_detect()
cmp = Car_model()
color = Car_color()
getcord = GetCoords()
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
input_np = 'MH43AB5586'
input_color = 'white'
input_model = 'swift'

# Initialize Yolo model instance
npd_model_path = 'Models/YOLOv5 Licence Plate Detector/licence_plate_detection_model_weights.pt'

model = YOLO("yolov8m.pt")
model_npd = torch.hub.load('ultralytics/yolov5', 'custom', path=npd_model_path)


def get_video_length(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video file.")
            return None
        
        # Get the total number of frames and frame rate
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = cap.get(cv2.CAP_PROP_FPS)

        # Calculate the duration in seconds
        duration = total_frames / frame_rate

        # Release the video capture object
        cap.release()

        return duration
    except Exception as e:
        print(f"Error occurred while getting video length: {e}")
        return None

'''Implementation '''


# Parameter inputs
frames_per_second = 3

# Defining the directory name
# dir_name = "tanmay"
# Location of the input video
# video_path = 'E:/Carmodelflow/MSD_Dir/MSD_Dir/video/Trim_8_5PM.mp4'
video_path = 'video/Engg_entrance.mp4'
# video_path = '/content/drive/MyDrive/BE Project Group 29/Trimmed Clips/test_video1.mp4'
# Locating output Directory
# output_directory = "E:/Carmodelflow/MSD_Dir/MSD_Dir/Data/Tanmay1"
output_directory = "Data/Footages"
os.makedirs(output_directory, exist_ok=True)
os.makedirs(output_directory+'/frames/', exist_ok=True)
os.makedirs(output_directory+'/car_cropped/', exist_ok=True)
# Comment later
# os.makedirs(output_directory+'/npd_cropped/', exist_ok=True)
os.makedirs(output_directory+'/car_cropped_txt/', exist_ok=True)


initial_time = time.perf_counter()

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
# first_frame_centers, last_frame_centers = getcord.get_coords(image_files_list=image_files,txt_dir=txt_directory)

print("Final................................................................................................")
# print(images_data)
# print(f'Image Files List: {image_files}')
# print(f'Start Frame: {first_frame_centers}')
# print(f'End Frame {last_frame_centers}')
framesdata=pd.DataFrame(images_data)
framesdata.to_csv("Data/Footages/ReIddata.csv")

final_time = time.perf_counter()
print(f'Video Name: {video_path}')
print(f'Video Length: {get_video_length(video_path)}')
print(f'Total Time taken by the entire Process: {final_time- initial_time:.2f}')
