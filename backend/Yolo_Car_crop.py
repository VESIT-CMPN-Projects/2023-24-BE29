import os
import cv2
import time
import shutil
import numpy as np
import pandas as pd
from ultralytics import YOLO

class Car_crop():
    def __init__(self):
        super().__init__()

    # delete intermediate files
    def delete_intermediate(self):
    # Specify the path to the directory you want to delete
        directory_path = "runs/detect/predict"

        # Use shutil.rmtree() to delete the directory and its contents
        try:
            shutil.rmtree(directory_path)
            print(f"Directory '{directory_path}' and its contents have been deleted successfully.")
        except FileNotFoundError:
            print(f"Directory '{directory_path}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

# Video to frame conversion (with unnecessary frame discarding)
    def video_to_frames(self,video_path, output_directory, frames_per_second, model, npd_model):
        # Storing this frames_data
        frames_data =  pd.DataFrame(columns=['frame_name','frame_path', 'timestamp'])
        data = {}
        data_list = []
        start_time = time.perf_counter()

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        # Get video properties
        frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total frames in the video

        # Calculate the interval at which frames should be extracted
        frame_interval = int(frame_rate / frames_per_second)
        

        # Extract and save frames
        frame_count = 0
        frame_number = 0
        

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if frame_number % frame_interval == 0:
                frame_path = os.path.join(output_directory + '/frames', f'frame_{frame_count:04d}.jpg')
                cv2.imwrite(frame_path, frame)
                # Calling YOLO Function
                self.YOLO_Car_Crop_modified(frame_path, output_directory, model, npd_model)
                # Printing timestamp
                timestamp = (frame_number / frame_rate) if frame_number < total_frames else -1
                # print(f'Timestamp of frame {frame_number}: {timestamp:.2f} seconds')
                # data_list = []
                data = {'frame_name':'frame_'+f'{frame_count:04d}','frame_path':frame_path,
                        'timestamp':f'{timestamp:.2f}'+f'{frame_count%frame_rate}'}
                data_list.append(data)
                frame_count += 1

            frame_number += 1

            if frame_number >= total_frames:  # Break the loop when all frames are processed
                break
        end_time = time.perf_counter()
        frames_data = pd.DataFrame(data_list)
        frames_data.to_csv(output_directory+'/frames_data.csv', index=False)
        # print(f"Extracted {frame_count} frames")
        print(f"Total Time: {end_time-start_time:.2f}")

        cap.release()

# Object (Car) Detection
    def YOLO_Car_Crop(self,frame, output_directory, model, npd_model):
    # Start Time
        start_time = time.perf_counter()
        coord = []

        # Input image location
        frame_name = os.path.basename('/frames/' + frame)
        frame_name = frame_name.split('.')[0]

        # Creating a text file for all the detected objects with thier normalized coordinates
        pred = model.predict(frame, save=True, save_txt=True)

        labels = pred[0].names
        txt_path = "runs/detect/predict/labels/"+frame_name+".txt"
        # This condition is because when model doesn't finds any object it does not create the txt file
        if os.path.exists(txt_path):
            lis = open(txt_path,"r").readlines()

            # Extracting the coordinates of cars only
            for li in lis:
                l = li.split()
                # Checking whether the cropped segnment is a Car or not
                if int(l[0]) == 2:
                    coord.append([float(l[1]), float(l[2]), float(l[3]), float(l[4])])

            # coord
            img = cv2.imread(frame)
            # Checking is there any car in the frame
            contains_car = any(float(sublist.split()[0]) == 2 for sublist in lis)
            if contains_car == False:
                if os.path.exists(frame):
                    os.remove(frame)
                    print(f"File '{frame}' has been deleted. Does not have any cars in it!")
                else:
                    print(f"File '{frame}' does not exist.")

        # Denormalizing the co-ordinates of the bounding boxes
            h, w = img.shape[0], img.shape[1]
            pos = []

            for c in coord:
                c[0] *= w
                c[1] *= h
                c[2] *= w
                c[3] *= h
                # Getting the co-ordinates of Top-Left and Bottom-Right in pos
                pos.append([(int(c[0] - c[2]/2), int(c[1] - c[3]/2)), (int(c[0] + c[2]/2), int(c[1] + c[3]/2))])
                print(f'Pos = {pos}')
            mask = np.zeros(img.shape[:2], np.uint8)

            for p in pos:
                mask[p[0][1]: p[1][1], p[0][0]:p[1][0]] = 255
                print(f'Mask = {mask}')

                new_image = cv2.bitwise_and(img, img, mask=mask)

                # Saving all the cropped images in the given directory
            count = 0
            npd_data =  pd.DataFrame(columns=['frame_name','frame_path', 'timestamp'])
            # # Car Cropped List
            # cropped_data_list = []
            for p in pos:
                ci = img[p[0][1]:p[1][1], p[0][0]:p[1][0]]
                print(f'Ci = {ci}')
                npd_img, cropped_npd_img = self.number_plate_detection(ci, npd_model)
                car_image_path =  output_directory +'/car_cropped/'+ frame_name +'_npd_'+str(count)+'.jpeg'
                npd_cropped_path =  output_directory +'/npd_cropped/'+ frame_name +'_npd_cropped_'+str(count)+'.jpeg'
                cv2.imwrite(car_image_path, npd_img)

        # if cropped_npd_img != []:
                if np.any(cropped_npd_img):
                    cv2.imwrite(npd_cropped_path, cropped_npd_img) # type: ignore
                count = count + 1
    # Frame had noting in it so Delete it
            else:
                if os.path.exists(frame):
                    print(f"File '{frame}' Contains car in it.")
                else:
                    print(f"File '{frame}' does not exist.")

            end_time = time.perf_counter()
            
            print(f"Total Time For Cropping : {end_time - start_time:.2f}")

    def YOLO_Car_Crop_modified(self, frame, output_directory, model, npd_model):
        # Start Time
        start_time = time.perf_counter()
        coord = []

        # Input image location
        frame_name = os.path.basename('/frames/' + frame)
        frame_name = frame_name.split('.')[0]

        # Creating a text file for all the detected objects with thier normalized coordinates
        pred = model.predict(frame, save=True, save_txt=True)

        labels = pred[0].names
        txt_path = "runs/detect/predict/labels/" + frame_name + ".txt"
        # This condition is because when model doesn't finds any object it does not create the txt file
        if os.path.exists(txt_path):
            lis = open(txt_path, "r").readlines()

            # Extracting the coordinates of cars only
            for li in lis:
                l = li.split()
                # Checking whether the cropped segnment is a Car or not
                if int(l[0]) == 2:
                    coord.append([float(l[1]), float(l[2]), float(l[3]), float(l[4])])

            # coord
            img = cv2.imread(frame)
            # Checking is there any car in the frame
            contains_car = any(float(sublist.split()[0]) == 2 for sublist in lis)
            if contains_car == False:
                if os.path.exists(frame):
                    os.remove(frame)
                    print(f"File '{frame}' has been deleted. Does not have any cars in it!")
                else:
                    print(f"File '{frame}' does not exist.")

            # Denormalizing the co-ordinates of the bounding boxes
            h, w = img.shape[0], img.shape[1]
            pos = []

            for c in coord:
                c[0] *= w
                c[1] *= h
                c[2] *= w
                c[3] *= h
                # Getting the co-ordinates of Top-Left and Bottom-Right in pos
                pos.append([(int(c[0] - c[2] / 2), int(c[1] - c[3] / 2)), (int(c[0] + c[2] / 2), int(c[1] + c[3] / 2))])
                # print(f'Pos = {pos}')
            mask = np.zeros(img.shape[:2], np.uint8)

            for p in pos:
                mask[p[0][1]: p[1][1], p[0][0]:p[1][0]] = 255
                # print(f'Mask = {mask}')

                new_image = cv2.bitwise_and(img, img, mask=mask)

                # Saving all the cropped images in the given directory
            count = 0
            npd_data = pd.DataFrame(columns=['frame_name', 'frame_path', 'timestamp'])
            # # Car Cropped List
            # cropped_data_list = []
            for p in pos:
                ci = img[p[0][1]: p[1][1], p[0][0]:p[1][0]]
                # print(f'Ci= {ci}')
                # npd_img, cropped_npd_img = self.number_plate_detection(ci, npd_model)
                car_image_path = output_directory + '/car_cropped/' + frame_name + '_npd_' + str(count) + '.jpeg'
                # npd_cropped_path = output_directory + '/npd_cropped/' + frame_name + '_npd_cropped_' + str(
                #     count) + '.jpeg'
                # print(f'P  = {p}')
                # Open the file in write mode
                txt_filename = output_directory + '/car_cropped_txt/' + frame_name + '_npd_' + str(count) + '.txt'
                with open(txt_filename, 'w') as file:
    # Write each coordinate pair to the file
                    for coordinate in p:
                        file.write(f"{coordinate[0]},{coordinate[1]}\n")
                cv2.imwrite(car_image_path, ci)

                # if cropped_npd_img != []:
                # if np.any(cropped_npd_img):
                #     cv2.imwrite(npd_cropped_path, cropped_npd_img)  # type: ignore
                count = count + 1
            # Frame had noting in it so Delete it
            else:
                if os.path.exists(frame):
                    print(f"File '{frame}' Contains car in it.")
                else:
                    print(f"File '{frame}' does not exist.")

            end_time = time.perf_counter()

            print(f"Total Time For Cropping : {end_time - start_time:.2f}")


    def number_plate_detection(self,img, model):

        pred_df = pd.DataFrame()
        pred = model(img, size=1280, augment=False)
        new_image = []

        for i, row in pred.pandas().xyxy[0].iterrows():
        # If number Plate is not there then break through the loop
            if row['confidence'] < model.conf: break
            # mask = np.zeros((img.height, img.width), np.uint8)

            mask = np.zeros(img.shape[:2], np.uint8)
            mask[int(row['ymin']):int(row['ymax']), int(row['xmin']):int(row['xmax'])] = 255

            new_image = cv2.bitwise_and(img, img, mask=mask)
            new_image = new_image[int(row['ymin']):int(row['ymax']), int(row['xmin']):int(row['xmax'])]
        # cv2.imshow(new_image) # type: ignore

        return img, new_image

cc = Car_crop()
cc.delete_intermediate()
