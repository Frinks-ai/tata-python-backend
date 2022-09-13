import cv2
import torch
import numpy as np
from dexi_model import DexiNed


# Function to normalise image
def image_normalization(img, img_min=0, img_max=255,
                        epsilon=1e-12):
    img = np.float32(img)
    # whenever an inconsistent image
    img = (img - np.min(img)) * (img_max - img_min) / \
        ((np.max(img) - np.min(img)) + epsilon) + img_min
    return img


def load_model(checkpoint_path, device):
    # Initialising mdoel
    model = DexiNed().to(device)
    # Loading model
    model.load_state_dict(torch.load(checkpoint_path,
                                     map_location=device))
    model.eval()
    return model


# Prediction
def predict(model, image, device):
    # getting image shape
    img_shape = image.shape[:-1]
    # Preprocessing
    image = cv2.resize(image, (352, 352))
    img = np.array(image, dtype=np.float32)
    # Subtracting mean bgr values
    img -= [103.939, 116.779, 123.68]
    # Properly reshaping
    img = img[np.newaxis, ...]
    img = img.transpose((0, 3, 1, 2))
    img = torch.from_numpy(img.copy()).float()
    img = img.to(device)
    # Prediction
    preds = model(img)
    # Post processing
    tensor = torch.sigmoid(preds[6]).cpu().detach().numpy()
    fuse = np.uint8(image_normalization(tensor))
    fuse = cv2.bitwise_not(fuse)
    fuse = cv2.resize(fuse[0, 0], (img_shape[1], img_shape[0]))
    fuse = fuse.astype(np.uint8)
    return fuse


# def main(img_path, model_path, device="cuda"):
#     img = cv2.imread(img_path, cv2.IMREAD_COLOR)
#     model = load_model(model_path, device)
#     final = predict(model, img, device)
#     return final


# if __name__ == "__main__":
#     checkpoint_path = "/home/poop/10_model.pth"
#     final = main(
#         "/home/amal/Frinks/molbio/DexiNed/data/download (19).png", checkpoint_path)
#     while True:
#         cv2.imshow("final", final)
#         k = cv2.waitKey(1)
#         if k == ord(" "):
#             break
