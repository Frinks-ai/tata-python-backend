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
