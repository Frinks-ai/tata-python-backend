import os 
import random
import cv2
import torch

weights='/home/rishabh/frinks/tata_comms/tata_demo/best.pt'


### -------------------------------------- function to run detection ---------------------------------------------------------
def detectx (frame, model):
    frame = [frame]
    print(f"[INFO] Detecting. . . ")
    results = model(frame)
    
    print(f'results:{results}')

    labels, cordinates = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    return labels, cordinates



###################################################################################################

### ------------------------------------ to plot the BBox and results --------------------------------------------------------
def plot_boxes(results, frame,classes,frame_no):

    """
    --> This function takes results, frame and classes
    --> results: contains labels and coordinates predicted by model on the given frame
    --> classes: contains the strting labels
    """
    labels, cord = results
    print(f'labels:{labels}')
    print(f'shape:{labels.shape}')

    lb=labels.tolist()
    print(f'lb:---{lb}')

    indices = [i for i, x in enumerate(lb) if x == 2]
    
    n = len(labels)

    x_shape, y_shape = frame.shape[1], frame.shape[0]

    print(f"[INFO] Total {n} detections. . . ")
    print(f"[INFO] Looping through all detections. . . ")


    ### looping through the detections
    cars_coords=[]

    if len(indices)>0:
      
      for i in indices:
        row = cord[i]
        x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
        cars_coords.append([x1,y1,x2,y2])

      print(f'cars_coords---{cars_coords}')

      cars_coords=np.array(cars_coords)

      idx=indices[cars_coords[:,3].argmax()]

      new_row = cord[idx]
    
      if new_row[4] >= 0.55:
        
        x1, y1, x2, y2 = int(new_row[0]*x_shape), int(new_row[1]*y_shape), int(new_row[2]*x_shape), int(new_row[3]*y_shape)
      
        text_d = 'car'



          # print(f'len of text_d{len(text_d)}')
            
          # if text_d == 'car' and labels.count('car')==1:
          #   print('yes we got the car')
          #   print(f"[INFO] Extracting BBox coordinates. . . ")
          #   # x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape) ## BBOx coordniates
            
        if y2>=1100 and y2<=1300:
          cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) ## BBox
          cv2.rectangle(frame, (x1, y1-20), (x2, y1), (0, 255,0), -1) ## for text label background  
          cv2.putText(frame, text_d + f" {round(float(row[4]),2)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,255,255), 2)
          bbox_coords.append([x1,y1,x2,y2]) 
          
          cropped_img=frame[y1:y2,x1:x2]

          cv2.imwrite(f'/content/drive/MyDrive/results_yolo/res_{frame_no}.png' , cropped_img)




          # elif text_d == 'car' and labels.count('car')>1:
          #   print('There is more than one car')
          #   print(f"[INFO] Extracting BBox coordinates. . . ")
          #   x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape) ## BBOx coordniates

    else:
      pass





    return frame

#############################################################################################################

### ---------------------------------------------- Main function -----------------------------------------------------

# def main(img_path=None, vid_path=None,vid_out =None):

def main(img_path=None, vid_path=None,vid_out=None):

    print(f"[INFO] Loading model... ")
    ## loading the custom trained model
    # model =  torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt',force_reload=True) ## if you want to download the git repo and then run the detection
    # model =  torch.hub.load('C:/Users/coder/Downloads/youtube_zero/yolov5_deploy/yolov5-master', 'custom', source ='local', path='last.pt',force_reload=True) ### The repo is stored locally

    model = torch.hub.load(f'./yolov5', 'custom', source='local', path=weights, force_reload=True)   ### setting up confidence threshold

    # classes = model.names ### class names in string format

    print(f"names of classes: {classes}")

    if img_path != None:
        print(f"[INFO] Working with image: {img_path}")
        frame = cv2.imread(img_path)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        results = detectx(frame, model = model) ### DETECTION HAPPENING HERE    

        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        frame = plot_boxes(results, frame,classes = classes)

        while True:
           # frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

            cv2.imwrite("final_output.jpg",frame) ## if you want to save he output result.

    elif vid_path !=None:
        print(f"[INFO] Working with video: {vid_path}")

        ## reading the video
        cap = cv2.VideoCapture(vid_path)


        if vid_out: ### creating the video writer if video output path is given

            # by default VideoCapture returns float instead of int
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            codec = cv2.VideoWriter_fourcc(*'mp4v') ##(*'XVID')

            out = cv2.VideoWriter(vid_out, codec, fps, (width, height))
    

        # assert cap.isOpened()
        frame_no = 1

        while True:
          
          # start_time = time.time()
          ret, frame = cap.read()
            
          if ret :
            
            if (frame_no%frame_skip ==0) and (frame_no >after_frame):
              
              print(f"[INFO] Working with frame {frame_no} ")

              frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
              results = detectx(frame, model = model)
              frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
              frame = plot_boxes(results, frame,classes = classes,frame_no=frame_no)
      
            if vid_out:
              print(f"[INFO] Saving output video. . . ")
              out.write(frame)
                  
              frame_no += 1

          else:
            print(" Video completed!!!")
            break

                
        
        print(f"[INFO] Clening up. . . ")
        ### releaseing the writer
        
        out.release()

##########################################################################################################

### -------------------  calling the main function-------------------------------

# main(vid_path="/content/drive/MyDrive/cropped/result.mp4",vid_out="/content/drive/MyDrive/results_yolo/result7_skip4_jsl.mp4")

# main(vid_path="/content/result1.mp4",vid_out="car_result.mp4") ### for custom video
# main(vid_path=0,vid_out="webcam_facemask_result.mp4") #### for webcam

main(img_path="crowd_mask181.jpg") ## for image
