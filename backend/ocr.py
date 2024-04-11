import os
import re
import Levenshtein
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

class OCR_detect():
    def __init__(self):
        super().__init__()

    # Similarity Score between the input number plate and the output of OCR
    def calculate_similarity_score(self,input_plate, ocr_output):
        # Remove special characters
        # input_plate = remove_special_characters(input_plate)
        ocr_output = self.remove_special_characters(ocr_output)

        # Convert both strings to uppercase for case-insensitive comparison
        input_plate = input_plate.upper()
        ocr_output = ocr_output.upper()

        # Calculate Levenshtein distance
        distance = Levenshtein.distance(input_plate, ocr_output)

        # Calculate similarity score as a percentage
        max_length = max(len(input_plate), len(ocr_output))
        similarity_score = ((max_length - distance) / max_length) * 100

        return similarity_score


    def remove_special_characters(self, s):
        return re.sub(r'[^a-zA-Z0-9]', '', s)

    def rotate_image(self,image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

    def compute_skew(self, src_img):

        if len(src_img.shape) == 3:
            h, w, _ = src_img.shape
        elif len(src_img.shape) == 2:
            h, w = src_img.shape
        else:
            w = 0
            h = 0
            print('upsupported image type')

        img = cv2.medianBlur(src_img, 3)

        edges = cv2.Canny(img,  threshold1 = 30,  threshold2 = 100, apertureSize = 3, L2gradient = True)

        lines = cv2.HoughLinesP(edges, 1, math.pi/180, 30, minLineLength=w / 4.0, maxLineGap=h/4.0)
        angle = 0.0
        if lines is not None:
            nlines = lines.size
            cnt = 0
            for x1, y1, x2, y2 in lines[0]:
                ang = np.arctan2(y2 - y1, x2 - x1)

                if math.fabs(ang) <= 30: # excluding extreme rotations
                    angle += ang
                    cnt += 1

            if cnt == 0:
                return 0.0
            return (angle / cnt)*180/math.pi

        # Continue with your code to process the lines
        else:
            print("No lines detected.")


    def deskew(self, path):
        src_img  = cv2.imread(path)
        # cv2.imshow('deskew_image',src_img)
        return self.rotate_image(src_img, self.compute_skew(src_img))
    def deskew_modified(self, img):
        # src_img  = cv2.imread(path)
        # cv2.imshow('deskew_image',src_img)
        return self.rotate_image(img, self.compute_skew(img))

    def OCR(self, output_directory,reader,input_np):
        p = output_directory
        l = {}
        npd_cropped_data = pd.DataFrame(columns=['npd_cropped_image_path','npd_cropped_image_filename','OCR_Output','OCR_Similarity'])
        data = {}
        data_list = []
        sim_score = 0
        for item in os.listdir(p):
            # l[item] = perform_ocr(p+item)
            corrected_img = self.deskew(p+item)
            t = self.perform_ocr(corrected_img,reader)
            # t = perform_ocr_tesseract(corrected_img)
            if not t == None:
                # i = cv2.imread(p+item)
                # cv2_imshow(corrected_img)
                t = self.remove_special_characters(t)
                sim_score = self.calculate_similarity_score(input_np,t)
                print(f"OCR Output: {t} | Similarity Score: {sim_score:.2f}%")

            else:
                sim_score = 0
                print('Cannot perform OCR')
            # Storing the data
            data = {'npd_cropped_image_path':p + item,'npd_cropped_image_filename':item,
                        'OCR_Output':t,'OCR_Similarity': f'{sim_score:.2f}%'}
            data_list.append(data)

        npd_cropped_data = pd.DataFrame(data_list)
        npd_cropped_data.to_csv(output_directory+'/npd_cropped_data.csv', index=False)

    def OCR_modified(self,reader,input_np,img_cropped):
        # l[item] = perform_ocr(p+item)
        corrected_img = self.deskew_modified(img_cropped)
        t = self.perform_ocr(corrected_img,reader)
        # t = perform_ocr_tesseract(corrected_img)
        if not t == None:
            # i = cv2.imread(img_path)
            # cv2_imshow(corrected_img)
            t = self.remove_special_characters(t)
            print(f"OCR Output: {t}")
        else:
            t = ''
            print('Cannot perform OCR')
        return t

    def perform_ocr(self,img,reader):
        
        if len(reader.readtext(img)):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # cv2_imshow(gray)
            try:
                text = reader.readtext(gray)[0][-2]
                return text
            except Exception as e:
                print(e)
                return ''

        return 