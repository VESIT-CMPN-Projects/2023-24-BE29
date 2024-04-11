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

# Deep learning 
from keras.preprocessing import image

class Car_color():
    def __init__(self) -> None:
        super().__init__()
    
    def predict_car_color(self, model, image_path,colorlist):
        '''
        This function will predict the class of an image and display the result.
        '''
        # Load and preprocess the image
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.  # Normalize the image

        # Make predictions
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)
        predicted_label = colorlist[predicted_class]
        confidence = np.max(prediction)

        # Display the result
        # plt.imshow(img)
        # plt.title(f'Predicted: {predicted_label} | Confidence: {confidence:.4f}')
        # plt.show()
        # print(f'Predicted: {predicted_label} | Confidence: {confidence:.4f}')
        return predicted_label,confidence