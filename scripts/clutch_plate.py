import cv2
from deviation import anomalies
from parts_detection import main_detection
from dimesioning_new import dimensioning_parts
from positioning import positioning_parts
import time
import socketio
import os
from dotenv import load_dotenv

load_dotenv()

sio = socketio.Client()

try:
    sio.connect(os.getenv("BASE_URL"))
except Exception as e:
    print('Socket is unable to connect to the BASE_URL!!!')


@sio.on('input')
def on_message(data):
    print("input called")
    GLOBAL_SWITCH[0] = True


IMAGE_PATH = f'{os.getenv("IMAGE_BASE")}/upload.bmp'
GLOBAL_SWITCH = [False]


def main():
    print("Model loaded inside main")
    while True:
        if GLOBAL_SWITCH[0] == False:
            continue
        start = time.time()
        final_result = {}
        frame = cv2.imread(IMAGE_PATH)
        image, final_coords = main_detection(IMAGE_PATH)  # for image
        print(f'part_detection---{final_coords}')
        position_dict, dimension_dict = dimensioning_parts(frame, final_coords)
        print(f'position_detection---{position_dict}')
        print(f'dimension_detection---{dimension_dict}')
        relative_position = positioning_parts(frame, position_dict)
        print(f'relative_position---{relative_position}')
        dimension_dev, position_dev, parts_absent = anomalies(
            dimension_dict, relative_position)
        # print(f'dimension_deviation---{dimension_dev}')
        # print(f'position_deviation---{position_dev}')
        # print(f'parts absent----{parts_absent}')
        try:
            if len(position_dict) > 8:
                for key in parts_absent:
                    final_result[key] = [0]

                for key in position_dev.keys():
                    if key in dimension_dict.keys():
                        final_result[key] = [
                            1, position_dev[key], dimension_dict[key]]
                    else:
                        final_result[key] = [1, position_dev[key]]

                print(f'final_result-----{final_result}')

        except:
            print('part placed is not correct')

        end = time.time()
        final_result["total_time"] = end-start

        sio.emit("output", final_result)
        GLOBAL_SWITCH[0] = False
###################################################################


main()
