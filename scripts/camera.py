import cv2

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3000)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 3000)
cam.set(cv2.CAP_PROP_EXPOSURE, 250)

BASE_PATH = "/home/poop/frinks/skh/camera_backend"

while True:
    ret, frame = cam.read()
    if not ret:
        break
    if frame.max() == 0:
        continue
    cv2.imwrite(f"{BASE_PATH}/images/upload.bmp", frame)
    break

cam.release()
