import argparse
import cv2
import glob
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
from utils import RealESRGANer
from srvggnet import SRVGGNetCompact

def main():
    # model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
    # netscale = 2
    # model_path = '/home/thaivv@kaopiz.local/Documents/Real-ESRGAN/weights/RealESRGAN_x2plus.pth'
    # dni_weight = None
    # tile = 0
    # tile_pad = 10
    # pre_pad = 0
    # half = False
    # gpu_id = 0
    # outscale = 1
    # upsampler = RealESRGANer(
    #     scale=netscale,
    #     model_path=model_path,
    #     dni_weight=dni_weight,
    #     model=model,
    #     tile=tile,
    #     tile_pad=tile_pad,
    #     pre_pad=pre_pad,
    #     half=half,
    #     gpu_id=gpu_id)
    # img_path = '/home/thaivv@kaopiz.local/Documents/ImageEditor/output.jpg'
    # img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # output, _ = upsampler.enhance(img, outscale=outscale)
    # cv2.imwrite('output_test2.png', output)

    model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
    netscale = 4
    wdn_model_path = '/home/thaivv@kaopiz.local/Documents/Real-ESRGAN/weights/realesr-general-wdn-x4v3.pth'
    model_path = '/home/thaivv@kaopiz.local/Documents/Real-ESRGAN/weights/realesr-general-x4v3.pth'
    denoise_strength = 0.3
    model_path =  [model_path, wdn_model_path]
    dni_weight = [denoise_strength, 1 - denoise_strength]
    tile = 0
    tile_pad = 10
    pre_pad = 0
    half = False
    gpu_id = 0
    outscale = 1
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=dni_weight,
        model=model,
        tile=tile,
        tile_pad=tile_pad,
        pre_pad=pre_pad,
        half=half,
        gpu_id=gpu_id)
    img_path = '/home/thaivv@kaopiz.local/Documents/ImageEditor/output.jpg'
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    output, _ = upsampler.enhance(img, outscale=outscale)
    cv2.imwrite('output_test1.png', output)






if __name__ == '__main__':
    main()