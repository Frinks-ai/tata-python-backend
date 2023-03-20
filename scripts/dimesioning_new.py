import cv2
from spring_model import pred_unet
import numpy as np
# from direct_test import load_model, predict
import torch
import os
from dotenv import load_dotenv
from direct_test import predict

load_dotenv()


def dimensioning_parts(frame, bboxcoords,model_spring,model_dim):

    position_dict = {}

    dimension_dict = {}

    device = "cuda" if torch.cuda.is_available() else "cpu"

    for old_key, old_value in bboxcoords.items():

        if old_key == 'torsion_spring':

            count_spring = 0
            for key, coord in old_value.items():

                image = frame[coord[1]-10:coord[3]+10, coord[0]-10:coord[2]+10]
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                imask = pred_unet(model_spring,image)
                gray = cv2.cvtColor(imask, cv2.COLOR_BGR2GRAY)
                M = cv2.moments(gray)
                if (M['m00'] != 0):
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    new_cX = cX+coord[0]-10
                    new_cY = cY+coord[1]-10

                count_spring += 1
                position_dict[key] = (new_cX, new_cY)

            # if count_spring<4:
            #     print(f"{}")

        if old_key == 'rivet_top':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]
                image = predict(model_dim, image, device=device)

                circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20,
                                           param1=50, param2=30, minRadius=27, maxRadius=42)

                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for x, i in enumerate(circles[0, :]):
                        value = (i[0]+coord[0], i[1]+coord[1])
                        size = i[2]

                        position_dict[key] = value

                        dimension_dict[key] = size/12

                else:
                    value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                    position_dict[key] = value

                    dimension_dict[key] = 34/12

        if old_key == 'rivet_inner':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]
                image = predict(model_dim, image, device=device)
                circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20,
                                           param1=50, param2=30, minRadius=35, maxRadius=44)

                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for x, i in enumerate(circles[0, :]):
                        value = (i[0]+coord[0], i[1]+coord[1])
                        size = i[2]

                        position_dict[key] = value

                        dimension_dict[key] = size/12

                else:
                    value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                    position_dict[key] = value

                    dimension_dict[key] = 37/12

        if old_key == 'rivet_bottom':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]

                value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                position_dict[key] = value

        if old_key == 'stop_pin':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]
                image = predict(model_dim, image, device=device)
                circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20,
                                           param1=50, param2=30, minRadius=10, maxRadius=30)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for x, i in enumerate(circles[0, :]):
                        value = (i[0]+coord[0], i[1]+coord[1])
                        size = i[2]

                        position_dict[key] = value

                        dimension_dict[key] = size/12

                else:
                    value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                    position_dict[key] = value

                    dimension_dict[key] = 25/12

        if old_key == 'central_hub':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]
                image = predict(model_dim, image, device=device)
                circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 126,
                                           param1=150, param2=22, minRadius=95, maxRadius=120)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for x, i in enumerate(circles[0, :]):
                        value = (i[0]+coord[0], i[1]+coord[1])
                        size = i[2]

                        position_dict[key] = value

                        dimension_dict[key] = size/12

                else:
                    value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                    position_dict[key] = value

                    dimension_dict[key] = 110/12

        if old_key == 'outer_clip':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]

                value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                position_dict[key] = value

        if old_key == 'inner_clip':

            for key, coord in old_value.items():

                image = frame[coord[1]:coord[3], coord[0]:coord[2]]

                value = ((coord[0]+coord[2])/2, (coord[1]+coord[3])/2)

                position_dict[key] = value

    return position_dict, dimension_dict


# print(position_dict)
# print(dimension_dict)
