from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qimage2ndarray
import numpy as np
import cv2
import torch
from PIL import Image
device = torch.device(f'cuda' if torch.cuda.is_available() else 'cpu')

def ceil_modulo(x, mod):
    if x % mod == 0:
        return x
    return (x // mod + 1) * mod


def pad_img_to_modulo(img, mod):
    channels, height, width = img.shape
    out_height = ceil_modulo(height, mod)
    out_width = ceil_modulo(width, mod)
    return np.pad(img, ((0, 0), (0, out_height - height), (0, out_width - width)), mode='symmetric')


def load_image(image, mode='RGB', return_orig=False):
    img = np.array(image.convert(mode))
    
    if img.ndim == 3:
        img = np.transpose(img, (2, 0, 1))
    out_img = img.astype('float32') / 255
    if return_orig:
        return out_img, img
    else:
        return out_img


def lama(self, pixmap, black):
    image = Image.fromarray(qimage2ndarray.rgb_view(pixmap.toImage()))
    mask = Image.fromarray(qimage2ndarray.rgb_view(black.toImage()))
    
    image = load_image(image, mode='RGB')    
    mask = np.expand_dims(load_image(mask, mode='L'),axis=0)
    image = pad_img_to_modulo(image, 8)
    mask = pad_img_to_modulo(mask, 8)
    batch = dict()
    batch['image'] = torch.unsqueeze(torch.tensor(image),dim=0).to(device)
    batch['mask'] = torch.unsqueeze(torch.tensor(mask),dim=0)
    batch['mask'] = ((batch['mask'] > 0) * 1).to(device)
    with torch.no_grad():  
        batch = self.modelLama(batch) 
        cur_res = batch['inpainted'][0].permute(1, 2, 0).detach().cpu().numpy()
        cur_res = np.clip(cur_res * 255, 0, 255).astype('uint8')
        cur_res = cv2.cvtColor(cur_res, cv2.COLOR_RGB2BGR)
    pixmap = convertCVtoPixmap(cur_res)
    updateView(self, pixmap)


def superResolution(self, pixmap):
    image = converPixmapToCV(pixmap)
    output, _ = self.upsampler.enhance(image, outscale=self.outscale)
    pixmap_new =  convertCVtoPixmap(output)
    updateView(self, pixmap_new)

def inpainting(self):
    pass

def updateView(self, pixmap):
    self.scene.clear()
    self.scene.addPixmap(pixmap)
    self.pixmap = pixmap

def convertCVtoPixmap( rotated_image):
    return QPixmap.fromImage(QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0],rotated_image.shape[1] * rotated_image.shape[2], QImage.Format_RGB888).rgbSwapped())

def convertPILtoPixmap( rotated_image):
    np_image = np.array(rotated_image)
    qimage = qimage2ndarray.array2qimage(np_image)
    pixmap = QPixmap.fromImage(qimage)
    return pixmap

def converPixmapToCV(pixmap):
    image_data = qimage2ndarray.rgb_view(pixmap.toImage())
    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
    return image_data