import cv2
from deviation import anomalies
from parts_detection import main_detection
from dimesioning_new import dimensioning_parts
from positioning import positioning_parts
from deviation import anomalies
import time
import socketio


sio = socketio.Client()

try:
    sio.connect("http://localhost:9000")
except Exception as e:
    print('Socket is unable to connect to the BASE_URL!!!')

@sio.on('automobile-input')
def on_message(data):
    print("hiiii")
    GLOBAL_SWITCH[0] = True

IMAGE_PATH = '/home/frinks1/molebio-backend/result/images/automobile.bmp'
GLOBAL_SWITCH = [False]

def main():
    while True:
        if GLOBAL_SWITCH[0]==False:
            continue
        start=time.time()
        final_result={}
        frame=cv2.imread(IMAGE_PATH)
        image,labels_dict=main_detection(IMAGE_PATH) ## for image
        # print(f'part_detection---{labels_dict}')
        position_dict,dimension_dict=dimensioning_parts(frame,labels_dict)
        print(f'position_detection---{position_dict}')
        print(f'dimension_detection---{dimension_dict}')
        relative_position=positioning_parts(frame,position_dict)
        print(f'relative_position---{relative_position}')
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
        
        end=time.time()
        final_result["total_time"] = end-start
        
        sio.emit("automobile-output", final_result  )
        GLOBAL_SWITCH[0]=False
###################################################################

main()


