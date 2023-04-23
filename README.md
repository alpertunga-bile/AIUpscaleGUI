# AIUpscaleGUI

- Using [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) repository for upscaling images. 
- I am using Automatic111 WebUI for Stable Diffusion. Because of my low VRAM I can not upscale my images so I made a GUI for upscaling my outputs. As I can see from the options in WebUI, it is using Real-ESRGAN as default.

## Requirements
- Git has to be in PATH variable.
- Tested with Python 3.10.6 and used Tkinter for GUI. As a note for Python 3.10.6 version Tkinter comes as default library. You can easily test it with these commands:

### Check Tkinter Module
- From command line enter ```python``` command and press Enter button.
- Write ```import tkinter``` command and press Enter button. If there are no errors. You are ready to go.
- Write ```exit()``` command and press Enter button to exit.

## Usage
- [x] In ***Startup*** and ***Initialize*** parts, check the progress on terminal. GUI will be freeze in that time.
- Open terminal or cmd and clone the repository and get into folder ```git clone https://github.com/alpertunga-bile/AIUpscaleGUI.git & cd AIUpscaleGUI```
- Open the GUI with ```python main.py``` command.
- Press the ***Startup*** button. If you do not have the [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) repository it is handled by application. Application is creating virtual environment inside the repo's folder and installing modules to it. So python modules are going to be installed on virtual environment not to the default one. Wait for ***Installation is complete!!! You can continue*** text above the button or look to the terminal. You can check the process from your terminal.
- After the installation progress, choose your input and output directories.
- Then select which model and attributes you want to use.
- After selecting them, press ***Initialize*** button and wait for ***DONE!!!*** text to appear under the button or in terminal.

### Model Names And Attributes 
- Currently RealESRGAN_x4plus, RealESRNet_x4plus, RealESRGAN_x4plus_anime_6B, RealESRGAN_x2plus, realesr-general-x4v3 models can be used. You dont have to download them, script will handle this.
- x2, x3 and x4 scales are supported.
- You can open and close face enhancement feature.

## Examples
- RealESRGAN_x4plus model, x4 scale and face enhancement are used.
- 512x512 images are created with NeverEndingDreamBakedVAE model, model hash is 64b14b6ca5. CodeFormer is used for face restoration. 

512x512                    |  2048x2048
:-------------------------:|:-------------------------:
![00024-3324991962](https://user-images.githubusercontent.com/76731692/233845862-bc77ede8-421b-4076-a31d-29b5ba4f109d.png) | ![00024-3324991962_out](https://user-images.githubusercontent.com/76731692/233845891-49a4df16-82b1-409e-bcea-2fdeac65044e.png)

512x512                    |  2048x2048
:-------------------------:|:-------------------------:
![00067-1531602356](https://user-images.githubusercontent.com/76731692/233845865-5379d7c0-d6b4-4396-86ff-3b2a82bcbb32.png) | ![00067-1531602356_out](https://user-images.githubusercontent.com/76731692/233845997-6fad9e31-ae50-430f-86cf-b98ddd7a0ad3.png)
