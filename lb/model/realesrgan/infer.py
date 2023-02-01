import argparse
import cv2
import glob
import torch
import time
import onnxruntime as rt
import numpy as np
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
from utils import RealESRGANer
from srvggnet import SRVGGNetCompact


def main():
    # model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    # netscale = 4
    # model_path = '/home/thaivv/ImageEditor/lb/model/realesrgan/weight/RealESRGAN_x4plus.pth'
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
    # img_path = '/home/thaivv/ImageEditor/output.jpg'
    # img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # output, _ = upsampler.enhance(img, outscale=outscale)
    # # print(output.shape)
    # cv2.imwrite('output_test2.png', output)

    model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
    netscale = 4
    wdn_model_path = '/home/thaivv/ImageEditor/lb/model/realesrgan/weight/realesr-general-wdn-x4v3.pth'
    model_path = '/home/thaivv/ImageEditor/lb/model/realesrgan/weight/realesr-general-x4v3.pth'
    denoise_strength = 0.5
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
    img_path = '/home/thaivv/ImageEditor/output.jpg'
    in_image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    output, _ = upsampler.enhance(in_image, outscale=outscale)
    cv2.imwrite('output_test3.png', output)
    
    # img_path = '/home/thaivv/ImageEditor/output.jpg'
    # img_ = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # sess = rt.InferenceSession('/home/thaivv/ImageEditor/realesrgan-x4.onnx', providers=['CPUExecutionProvider'])
    # img = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)
    # img = np.transpose(img, (2, 0, 1))
    # img = np.expand_dims(img, axis=0)
    # in_mat = img.astype(np.float32)
    # # in_mat = in_mat/255
    # start_time = time.time()
    # input_name = sess.get_inputs()[0].name
    # # output_name = sess.get_outputs()[0].name
    # # in_mat = torch.tensor(in_mat).to('cpu')
    # output = sess.run(None, {input_name: in_mat})[0]
    # elapsed_time = time.time() - start_time
    # print(elapsed_time)
    # output = np.transpose(output, (0, 2, 3, 1))
    # output = output[0]
    # output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    # h,w = img_.shape[:2]
    # output_alpha = cv2.resize(output, (w , h), interpolation=cv2.INTER_LINEAR)
    # cv2.imwrite('output_test4.png', output_alpha)






if __name__ == '__main__':
    main()