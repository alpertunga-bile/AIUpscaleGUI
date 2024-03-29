# AIUpscaleGUI

<p align="center">
  <img src=https://user-images.githubusercontent.com/76731692/234883310-86fceaa3-45b3-4870-83ca-3642b98ccf20.gif alt="animated" />
</p>

- Using [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) repository for upscaling images.
- I am using Automatic111 WebUI for Stable Diffusion. Because of my low VRAM I can not upscale my images so I made a GUI for upscaling my outputs. As I can see from the options in WebUI, it is using Real-ESRGAN as default.
- I have another repository about prompts. Briefly you can parse prompts from Markdown files, translate your prompts. You can generate datasets, train your prompt generator and generate prompts with it. You can access the repository [here](https://github.com/alpertunga-bile/prompt-markdown-parser).

## Table Of Contents

- [AIUpscaleGUI](#aiupscalegui)
  - [Table Of Contents](#table-of-contents)
  - [Updates (DD/MM/YY)](#updates-ddmmyy)
    - [Update Date : 03/08/2023](#update-date--03082023)
    - [Update Date : 24/05/2023](#update-date--24052023)
    - [Update Date : 27/04/2023](#update-date--27042023)
  - [Requirements](#requirements)
    - [Check Tkinter Module](#check-tkinter-module)
  - [Usage](#usage)
    - [Folder Selection Note](#folder-selection-note)
      - [Option 1](#option-1)
      - [Option 2](#option-2)
    - [Model Names And Attributes](#model-names-and-attributes)
  - [Examples](#examples)

## Updates (DD/MM/YY)

### Update Date : 03/08/2023

- VenvManager is added. Don't have to press **Startup** button after starting. It is handled by VenvManager. 
- Logging system is updated.
- Tiling is done by default.

### Update Date : 24/05/2023

- Not using GPU bug is fixed. Delete Real-ESRGAN folder and click **Startup** button.
- As a note, if you have encountered with black output, select FP32 option.

### Update Date : 27/04/2023

- Modern GUI style is added with customtkinter
- Virtual environment automation is added. No need to configure manually. Just run ```python start.py``` command.
- **Startup** and **Initialize** functions are done in threads so no more freezing.
- Selection for FP32 feature is added.
- [x] I did not hide the command outputs because some processes take minutes and it makes it difficult to understand what is going on. If there are no errors and application is not terminated, it is fine.

<p align="center">
  <img src=https://user-images.githubusercontent.com/76731692/234876288-9a368045-10a5-4455-997c-c0f8553ab9a4.gif alt="animated" />
</p>

## Requirements

- Tested in Windows OS environment.
- Venv, customtkinter and Tkinter packages are used.
- Git has to be in PATH variable.
- Tested with Python 3.10.6 and used Tkinter for GUI. As a note for Python 3.10.6 version Tkinter comes as default package. You can easily test it with these commands:

### Check Tkinter Module

- From command line enter ```python``` command and press Enter button.
- Write ```import tkinter``` command and press Enter button. If there are no errors. You are ready to go.
- Write ```exit()``` command and press Enter button to exit.

## Usage

- Open terminal or cmd and clone the repository and get into folder ```git clone https://github.com/alpertunga-bile/AIUpscaleGUI.git & cd AIUpscaleGUI```
- Start the application with ```python start.py``` command. This command is going to look for 'venv' file for virtual environment. It is going to setup the dependencies (customtkinter) and start the application. After the first setup, it is just going to start the GUI application.
- Press the **Startup** button. Check if [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) installed correctly. If not delete **paths.json** and **third-party** folder and start the application again.
- Choose your input and output directories.
- Then select which model and attributes you want to use.
- After selecting them, press **Initialize** button and wait for **DONE!!!** text to appear under the button or in terminal.
- [x] If you have encountered with black output, select FP32 option.

### Folder Selection Note

- You can choose one folder that includes images or you can choose one folder that includes folders that include images (Hmm?).

#### Option 1

<pre>
Folder1
  |----> image1
  |----> image2
</pre>

#### Option 2

<pre>
Folder1
  |----> Folder2
  |        |----> image1
  |        |----> image2
  |
  |----> Folder3
           |----> image3
           |----> image4
</pre>

- You can not choose multiple directories. You have to use the Option 2.

### Model Names And Attributes

- Currently RealESRGAN_x4plus, RealESRNet_x4plus, RealESRGAN_x4plus_anime_6B, RealESRGAN_x2plus, realesr-general-x4v3 models can be used. You dont have to download them, script will handle this.
- x2, x3 and x4 scales are supported.
- You can open and close face enhancement feature.
- You can select FP32 feature.

## Examples

- Prompts are parsed with [Prompt Markdown Parser](https://github.com/alpertunga-bile/prompt-markdown-parser) project.
- RealESRGAN_x4plus model, x4 scale and face enhancement are used.
- 512x512 images are created with NeverEndingDreamBakedVAE model, model hash is 64b14b6ca5. CodeFormer is used for face restoration.

|                                                          512x512                                                           |                                                           2048x2048                                                            |
| :------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------: |
| ![00024-3324991962](https://user-images.githubusercontent.com/76731692/233845862-bc77ede8-421b-4076-a31d-29b5ba4f109d.png) | ![00024-3324991962_out](https://user-images.githubusercontent.com/76731692/233845891-49a4df16-82b1-409e-bcea-2fdeac65044e.png) |

|                                                          512x512                                                           |                                                           2048x2048                                                            |
| :------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------: |
| ![00067-1531602356](https://user-images.githubusercontent.com/76731692/233845865-5379d7c0-d6b4-4396-86ff-3b2a82bcbb32.png) | ![00067-1531602356_out](https://user-images.githubusercontent.com/76731692/233845997-6fad9e31-ae50-430f-86cf-b98ddd7a0ad3.png) |
