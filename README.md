# AIUpscaleGUI

- Using [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) repository for upscaling images. 
- I am using Automatic111 WebUI for Stable Diffusion. Because of my low VRAM I can not upscale my images so I made a GUI for upscaling my outputs. As I can see from the options in WebUI, it is using Real-ESRGAN as default.

## Requirements
- Currently Windows os is supported.
- Git has to be in PATH.
- Tested with Python 3.10.6 and used Tkinter for GUI. As a note for Python 3.10.6 version Tkinter comes as default library. You can easily test it with these commands:

### Check Tkinter Module
- From command line enter ```python``` command and press Enter button.
- Write ```import tkinter``` command and press Enter button. If there are no errors. You are ready to go.
- Write ```exit()``` command and press Enter button to exit.

## Usage
- Open terminal or cmd and clone the repository and get into folder ```git clone https://github.com/alpertunga-bile/AIUpscaleGUI.git & cd AIUpscaleGUI```
- Open the GUI with ```python main.py``` command.
- Press the ***Startup*** button. If you do not have the [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) repository it is going to handled by GUI. Wait for ***Installation is complete!!! You can continue*** text above the button. You can check the process from your terminal or cmd. 
- After the installation progress, choose your input and output directories.
- Then select which model and attributes you want to use.
- After selecting them, press ***Initialize*** button and wait for ***DONE!!!*** text to appear under the button.

### Model Names And Attributes 
- Currently RealESRGAN_x4plus,
            RealESRNet_x4plus,
            RealESRGAN_x4plus_anime_6B,
            RealESRGAN_x2plus,
            realesr-general-x4v3 models can be used. You dont have to download them, script will handle this.
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
