import cv2
from deviation import anomalies
from parts_detection import main_detection
from dimesioning_new import dimensioning_parts
from positioning import positioning_parts
import time
import socketio
import os
from dotenv import load_dotenv
import torch
from model import U2NETP
from dexi_model import DexiNed


load_dotenv()



device = "cuda" if torch.cuda.is_available() else "cpu"

###################################################
######YOLO MODEL

model = torch.hub.load(f'./yolov5', 'custom', source='local',path=f'{os.getenv("MODEL_BASE")}/best.pt', force_reload=True) 
# model = torch.hub.load(f'./yolov5', 'custom', source='local',path='/home/rishabh/frinks/tata_comms/tata_demo/best.pt', force_reload=True) 

model.eval()



#####################################################
######SPRING MODEL

spring_dir = f'{os.getenv("MODEL_BASE")}/u2netp.pth'

# spring_dir ='/home/rishabh/frinks/tata_comms/tata_demo/share_u2net/u2netp.pth'

model_spring = U2NETP(3, 1)

if torch.cuda.is_available():
    model_spring.load_state_dict(torch.load(spring_dir))
    model_spring.cuda()
else:
    model_spring.load_state_dict(torch.load(
        spring_dir, map_location=torch.device('cpu')))

model_spring.eval()

####################################################
####### DEXINED MODEL


model_dim = DexiNed().to(device)

model_dim.load_state_dict(torch.load(f'{os.getenv("MODEL_BASE")}/10_model.pth',
                                     map_location=device))

# model_dim.load_state_dict(torch.load('/home/rishabh/frinks/tata_comms/tata_demo/10_model.pth',
#                                      map_location=device))

model_dim.eval()


####################################################

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

#################################################################


def main():

    print("Model loaded inside main")
    while True:
        if GLOBAL_SWITCH[0] == False:
            continue


        start = time.time()
        final_result = {}

        frame = cv2.imread(IMAGE_PATH)

        # frame = cv2.imread(im_path)


        image, final_coords = main_detection(frame,model)  # for image
        # print(f'part_detection---{final_coords}')
        position_dict, dimension_dict = dimensioning_parts(frame, final_coords,model_spring,model_dim)
        # print(f'position_detection---{position_dict}')
        # print(f'dimension_detection---{dimension_dict}')
        relative_position = positioning_parts(frame, position_dict)
        # print(f'relative_position---{relative_position}')
        position_dev, parts_absent = anomalies(
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
                        if key[:-1]=='torsion_spring' and position_dev[key]>1.2:
                            final_result[key] = [1,0.9515492550818216, dimension_dict[key]]

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




# image_dir='/home/rishabh/Downloads/tmp/tmp'

# for img in sorted(os.listdir(image_dir)):
#     print('image----------------------------------',img)
#     image_path=image_dir+'/'+img
#     main(image_path)
