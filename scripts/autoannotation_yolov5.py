import os 
import random
import cv2
import torch

# img_dir = "/home/frinks1/Downloads/DP/Heidelberg/ratio_test/negative_images/"

# img_dir = "/home/frinks1/Downloads/DP/ACC_NEW/data_fromsite/frame_annotations/"
img_dir = "/home/frinks1/Meraj/circle_detection/testing/data/test_Images"

DETECT_ONLY_AFTER_CX =  0 ## 245
DETECT_ONLY_AFTER_CY = 0
SCORE_THRESHOLD_BAG, IOU_THRESHOLD_BAG =  0.5, 0.25 # 0.15,0.3 #### FOR 0.5 some detections are missing
SCORE_THRESHOLD_TAG, IOU_THRESHOLD_TAG = 0.1, 0.3 # 0.7, 0.3 iou low value gives good result

ISRATIO = False
DO_TAG = False



BAG_MODEL_WEIGHT = "/home/frinks1/Meraj/circle_detection/training/yolov5s_training_results/yolov5m_460AUG_data3/weights/best.pt" ### ultratech deployed

TAG_MODEL_WEIGHT = "/home/frinks1/Downloads/DP/Heidelberg/label_tag/yolov5l_training_results_data/training_backup_1966dt_coco_hype_adam_ULTRATECH/weights/best.pt" ### ultratech deployed



### crop exp
RANDOM_NAME = ['23','r34','4e','sa','sf5','sdf2','awd','hfg','c5g','sfg','sef4','kj','vp','chmbt','rey','lil','fghgh','neo','34f']



### -------------------------------------- function to run detection ---------------------------------------------------------
def detectx (frame_batch, model):
    # frame = [frame]
    # print(f"[INFO] Detecting. . . ")
    results = model(frame_batch, augment=True)

    batch_results = []

    for ir in range(len(results)):

        labels, cordinates = results.xyxyn[ir][:, -1], results.xyxyn[ir][:, :-1]

        batch_results.append((labels,cordinates))

    # print(f"len of batch_result: {len(batch_results)}")
    # print(batch_results)

    return batch_results


#### -------------------------------------- to save annotaions in txt file

def save_annotations(img, BBox,class_id, frame_name):
    
    xmin, ymin, xmax, ymax = BBox

    file_name = frame_name.split('/')[-1].split('.')[0]
    output_dir  = "./auto_annotations"
    os.makedirs(output_dir, exist_ok= True)

    filex = open(f"{output_dir}/{file_name}.txt",'w')

    #### writing the annotaion in normalised yolo format ---> class_id x y w h 

    filex.write(f'{class_id} '+str((((xmin+xmax)/2)/img.shape[1]))+' '+str((((ymin+ymax)/2)/img.shape[0]))+' '+str(((xmax-xmin)/img.shape[1]))+' '+str(((ymax-ymin)/img.shape[0]))+'\n')

    filex.close()





### ------------------------------------ to plot the BBox and results --------------------------------------------------------
def update_rects_plot_bbox(batch_results,imgs_rgb,classes, FRAME_COUNTER, vidc_name,SCORE_THRESHOLD):

    # print(f"[INFO] Updating rects. . . ")


    """
    --> This function takes results, frame and classes
    --> results: contains labels and coordinates predicted by model on the given frame
    --> classes: contains the strting labels

    """
    # print(imgs_rgb)
    imgs_results=[]
    rects_master = []
    x_mid = []


    output_dir  = "./auto_annotations"
    os.makedirs(output_dir, exist_ok= True)

    
    for im in range(len(imgs_rgb)):
        # image_h, image_w, _ = frame.shape  
        # 
         
        file_name = vidc_name.split('/')[-1].split('.')[0]
        filex = open(f"{output_dir}/{file_name}.txt",'w')


        
        frame = imgs_rgb[im]
        labels, cord = batch_results[im]
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        x_mid.append(x_shape//2)

        
        rects =[] ### rects per image


        # print(f"[INFO] Total {n} detections. . . ")
        # print(f"[INFO] Looping through all detections. . . ")


        ### looping through the detections per image
        for i in range(n):
            row = cord[i]
            if row[4] >= SCORE_THRESHOLD: ### threshold value for detection. We are discarding everything below this value
                # print(f"[INFO] Extracting BBox coordinates. . . ")
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape) ## BBOx coordniates
                # startX, startY, endX, endY = x1,y1,x2,y2

                class_id_int = int(labels[i])
                text_d = classes[int(labels[i])]

                cx = int((x1+x2)/2.0)
                cy = int((y1+y2)/2.0)

                xmin, ymin, xmax, ymax = x1, y1, x2, y2
                



                filex.write(f'{class_id_int} '+str((((xmin+xmax)/2)/frame.shape[1]))+' '+str((((ymin+ymax)/2)/frame.shape[0]))+' '+str(((xmax-xmin)/frame.shape[1]))+' '+str(((ymax-ymin)/frame.shape[0]))+'\n')



                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) ## BBox
                

                    
                cv2.putText(frame, text_d + f" {round(float(row[4]),2)}", (x1, y1-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,255,0), 2)

                rects.append((x1,y1,x2,y2))

                os.makedirs(f"./detection_Onimages", exist_ok= True)
                cv2.imwrite(f"./detection_Onimages/{file_name}_{FRAME_COUNTER}.jpg",frame)
            


            ## print(row[4], type(row[4]),int(row[4]), len(text_d))


        filex.close() ### closing the txt file

        imgs_results.append(frame)
        rects_master.append(rects)

    return imgs_results, rects_master, x_mid


################ --------    main area ------------------------


print(f"[INFO] Loading model... ")

if DO_TAG:
model = torch.hub.load(f'./yolov5', 'custom', source='local', path=GP.weights_path, force_reload=True)    model.conf = SCORE_THRESHOLD_TAG ### setting up confidence threshold
    model.iou = IOU_THRESHOLD_TAG ## setting up iou threshold
    SCORE_THRESHOLD = SCORE_THRESHOLD_TAG
else:
    model =  torch.hub.load('/home/frinks1/Meraj/circle_detection/training/yolov5', 'custom', source ='local', path=BAG_MODEL_WEIGHT,force_reload=True) ### lastm_label_bag.pt--good result,  The repo is stored locally
    model.conf = SCORE_THRESHOLD_BAG ### setting up confidence threshold
    model.iou = IOU_THRESHOLD_BAG ## setting up iou threshold
    SCORE_THRESHOLD = IOU_THRESHOLD_BAG
classes = model.names ### class names in string format

# img_master=[]

#### looping through the images 

print(os.listdir(img_dir))
FRAME_COUNTER = 1

for i in os.listdir(img_dir):
    img_master=[]

    full_path = os.path.join(img_dir,i)
    vidc_name = full_path
    print(full_path)

    img = cv2.imread(full_path)
    img_master.append(img)
    # cv2.namedWindow("img",cv2.WINDOW_NORMAL)

    # while True:

    #     cv2.imshow("img", img)


    #     if cv2.waitKey(1) == ord("q"):
    #         break
    batch_results = detectx(frame_batch=img_master, model = model)

    img_master, rects_master, x_mid = update_rects_plot_bbox(batch_results=batch_results, imgs_rgb = img_master, classes= classes, FRAME_COUNTER= FRAME_COUNTER, vidc_name= vidc_name,SCORE_THRESHOLD=SCORE_THRESHOLD)

    FRAME_COUNTER+=1
