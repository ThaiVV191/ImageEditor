# ImageEditor
This is my final project, with the idea of creating a photo editing application that applies AI with a simple and easy-to-use interface. The application includes operations such as image flipping, rotation, zooming, shrinking, adding text to images, Adjust the image temperature, brightness, darkness, contrast, and add additional filters such as Gaussian blur, box blur, and median blur..., along with AI tasks such as image inpainting and image super resolution. The model used for image inpainting is [LaMa](https://github.com/advimman/lama), and the model used for image super resolution is [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN). Follow the instructions to set up the weight file as in the author's guide.
The steps to run the project:
```bash 
git clone git@github.com:ThaiVV191/ImageEditor.git
pip install -r requirements.txt
sh run.sh
```
Video demo image super resolution, image inpainting:

https://user-images.githubusercontent.com/109791557/227111670-0e93b64c-5218-4c8b-914f-2dc543589932.mp4

