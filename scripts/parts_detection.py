import os 
import random
from typing import final
import cv2
import torch
import math
from direct_test import load_model,predict

weights='/home/frinks1/best.pt'


### -------------------------------------- function to run detection ---------------------------------------------------------
def detectx (frame, model):
    frame = [frame]
    print(f"[INFO] Detecting. . . ")
    results = model(frame)

    # print(f'results:{results}')

    labels, cordinates = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    return labels,cordinates

#############################################################################################################

def plot_boxes(results,frame):

    labels, cord = results

    lb=labels.tolist()

    coords=cord.tolist()

    print(f'labels:{lb}')

    # print(f'coords---{(coords)}')

    string_labels=[]

    for x in lb:
        if x==0:
            string_labels.append('central_hub')
        elif x==1:
            string_labels.append('outer_clip')
        elif x==2:
            string_labels.append('inner_clip')
        elif x==3:
            string_labels.append('torsion_spring')
        elif x==4:
            string_labels.append('rivet_inner')
        elif x==5:
            string_labels.append('stop_pin')
        elif x==6:
            string_labels.append('rivet_top')
        elif x==7:
            string_labels.append('rivet_bottom')

    n = len(string_labels)

    x_shape, y_shape = frame.shape[1], frame.shape[0]

    print(f"[INFO] Total {n} detections. . . ")
    print(f"[INFO] Looping through all detections. . . ")


    labels_dict={}


    # if len(indices)>0:

    for i in range(n):
        row=coords[i]
        label=string_labels[i]
        if row[4]>0.75:
            x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
            if len(labels_dict)==0 or label not in labels_dict.keys():
                labels_dict[label]=[]
                labels_dict[label].append([x1,y1,x2,y2])

            else:
                labels_dict[label].append([x1,y1,x2,y2])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # print(f'bboxcoords:{labels_dict}')

    # print(f'length---{len(labels_dict)}')

    # print(f'person_coords---{labelled_coords}')


    return frame,labels_dict

def check_slopes(labels_dictionary):

    bboxcoords={}

    for key,value in labels_dictionary.items():
        if key=='central_hub':
            val=((value[0][0]+value[0][2])/2,(value[0][1]+value[0][3])/2)
                
    slopes={}
    for key, value in labels_dictionary.items():
        for coord in value:
            slope=math.degrees(math.atan2(val[1]-coord[1],val[0]-coord[0]))
            if len(slopes)==0 or key not in slopes.keys():
                slopes[key]=[]
                slopes[key].append(int(slope))
            else:
                slopes[key].append(int(slope))
    
        slopes[key]=[i[0] for i in sorted(enumerate(slopes[key]), key=lambda x:x[1])]

    for key,values in slopes.items():
        bboxcoords[key]=[labels_dictionary[key][index] for index in values]

    return bboxcoords
###############################################################################################################

def main_detection(img_path):

    print(f"[INFO] Loading model... ")

    final_coords={}

    model = torch.hub.load(f'/home/frinks1/tata-python-backend/scripts/yolov5', 'custom', source='local', path='/home/frinks1/best.pt', force_reload=True)   ### setting up confidence threshold
    if img_path != None:
        print(f"[INFO] Working with image: {img_path}")
        frame = cv2.imread(img_path)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)        
        results = detectx(frame, model = model) ### DETECTION HAPPENING HERE    
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        frame,labels_dict = plot_boxes(results,frame)
        bboxcoords=check_slopes(labels_dict)
        cv2.imwrite("/home/frinks1/molebio-backend/result/images/automobile_result.bmp",frame)
        for key,values in bboxcoords.items():
            for i,coord in enumerate(values):
                if key not in final_coords.keys():    
                    final_coords[key]={}
                    final_coords[key][f'{key}{i}']=coord
                else:
                    final_coords[key][f'{key}{i}']=coord

    return frame,final_coords

    
##########################################################################################################


# main_detection(img_path="/home/rishabh/frinks/tata_comms/tata_demo/2000.bmp") ## for image
