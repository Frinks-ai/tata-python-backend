import cv2
from deviation import anomalies
from parts_detection import main_detection
from dimesioning_new import dimensioning_parts
from positioning import positioning_parts
from deviation import anomalies
import time

def main(img_path):

    final_result={}
    frame=cv2.imread(img_path)
    image,labels_dict=main_detection(img_path) ## for image
    # print(f'part_detection---{labels_dict}')
    position_dict,dimension_dict=dimensioning_parts(frame,labels_dict)
    # print(f'position_detection---{position_dict}')
    # print(f'dimension_detection---{dimension_dict}')
    relative_position=positioning_parts(frame,position_dict)
    # print(f'relative_position---{relative_position}')
    dimension_dev, position_dev,parts_absent=anomalies(dimension_dict, relative_position)
    # print(f'dimension_deviation---{dimension_dev}')
    # print(f'position_deviation---{position_dev}')
    # print(f'parts absent----{parts_absent}')
    for key in parts_absent:
        final_result[key]=[0]
        
    for key in position_dev.keys():
        if key in dimension_dict.keys():
            final_result[key] =[1,position_dev[key],dimension_dict[key]]
        else:
            final_result[key]=[1,position_dev[key]]
    
    print(f'final_result-----{final_result}')
###################################################################

start=time.time()

main('/home/rishabh/frinks/tata_comms/tata_demo/283.bmp')

end=time.time()

print(f"time----{end-start}")

