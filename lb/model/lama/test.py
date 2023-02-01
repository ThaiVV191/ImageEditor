import cv2
import hydra
import numpy as np
import torch
import yaml
from PIL import Image
from omegaconf import OmegaConf
from saicinpainting.training.trainers import load_checkpoint

device = 'cpu'
checkpoint_path = '/home/thaivv/ImageEditor/lb/model/lama/weight/model/best.ckpt'
config = '/home/thaivv/ImageEditor/lb/model/lama/weight/config.yaml'
image_path = '/home/thaivv/ImageEditor/lb/model/lama/4.png'
mask_path = '/home/thaivv/ImageEditor/lb/model/lama/4_mask001.png'

def load_image(fname, mode='RGB', return_orig=False):
    img = np.array(Image.open(fname).convert(mode))
    if img.ndim == 3:
        img = np.transpose(img, (2, 0, 1))
    out_img = img.astype('float32') / 255
    if return_orig:
        return out_img, img
    else:
        return out_img
    
@hydra.main(config_path="./configs/prediction", config_name="default.yaml")
def main(predict_config: OmegaConf):
    with open(config, 'r') as f:
        train_config = OmegaConf.create(yaml.safe_load(f))
    train_config.training_model.predict_only = True
    model = load_checkpoint(train_config, checkpoint_path, strict=False, map_location='cpu')
    model.eval()
    model.to(device)
    image = load_image(image_path, mode='RGB')
    mask = np.expand_dims(load_image(mask_path, mode='L'),axis=0)   
    batch = dict()
    batch['image'] = torch.unsqueeze(torch.tensor(image),dim=0).to(device)
    batch['mask'] = torch.unsqueeze(torch.tensor(mask),dim=0).to(device)
    with torch.no_grad():  
        batch = model(batch) 
        cur_res = batch['inpainted'][0].permute(1, 2, 0).detach().cpu().numpy()
        cur_res = np.clip(cur_res * 255, 0, 255).astype('uint8')
        cur_res = cv2.cvtColor(cur_res, cv2.COLOR_RGB2BGR)
        cv2.imwrite('/home/thaivv/ImageEditor/lama/check.png', cur_res)




if __name__ == '__main__':
    main()