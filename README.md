# AIUpscaleGUI

<p align="center">
  <img src=https://user-images.githubusercontent.com/76731692/234883310-86fceaa3-45b3-4870-83ca-3642b98ccf20.gif alt="animated" />
</p>

- Using upscaling models for upscaling images.

## Table Of Contents

- [AIUpscaleGUI](#aiupscalegui)
  - [Table Of Contents](#table-of-contents)
  - [Changelogs](#changelogs)
  - [Requirements](#requirements)
    - [Check Tkinter Module](#check-tkinter-module)
  - [Usage](#usage)
    - [Folder Selection Note](#folder-selection-note)
    - [Model Names And Attributes](#model-names-and-attributes)
  - [Examples](#examples)

## Changelogs

- See the changelogs.md file

## Requirements

- Tested in Windows OS environment.
- Git has to be in PATH variable.
- Tested with Python 3.12 and used Tkinter for GUI. As a note for Python 3.10.6
  version Tkinter comes as default package. You can easily test it with these
  commands:

### Check Tkinter Module

- From command line enter `python` command and press Enter button.
- Write `import tkinter` command and press Enter button. If there are no errors.
  You are ready to go.
- Write `exit()` command and press Enter button to exit.

## Usage

- Open terminal or cmd and clone the repository and get into folder
  `git clone https://github.com/alpertunga-bile/AIUpscaleGUI.git & cd AIUpscaleGUI`
- Start the application with `python start.py` command. This command is going to
  look for 'venv' file for virtual environment. It is going to setup the
  dependencies (customtkinter) and start the application. After the first setup,
  it is just going to start the GUI application.
- Choose your input and output directories.
- Then select which model and attributes you want to use.
- After selecting them, press **Initialize** button and wait for **Done !!!**
  text under the button.

### Folder Selection Note

- Recursive image file location support is added.

### Model Names And Attributes

- Supported models and their supported scale values are listed below. Select one
  model from the table:

|           Model Name           | Supported Scale |
| :----------------------------: | :-------------: |
|       RealESRGAN_x4plus        |       4x        |
|       RealESRNET_x4plus        |       4x        |
|   RealESRGAN_x4plus_anime_6B   |       4x        |
|       RealESRGAN_x2plus        |       2x        |
|      2x-AnimeSharpV4_RCAN      |       2x        |
|  2x-AnimeSharpV4_Fast_RCAN_PU  |       2x        |
|        4x-UltraSharpV2         |       4x        |
|     2x-ModernSpanimationV1     |       2x        |
| 2x_Ani4Kv2_G6i2_Compact_107500 |       2x        |
|    4xmssim_drct-l_pretrain     |       4x        |
|     4xmssim_drct_pretrain      |       4x        |
|     4xmssim_span_pretrain      |       4x        |

- You can select `bfloat16` `float16` and `float32` PyTorch data types.

## Examples

- Prompts are parsed with
  [Prompt Markdown Parser](https://github.com/alpertunga-bile/prompt-markdown-parser)
  project.
- RealESRGAN_x4plus model, x4 scale and face enhancement are used.
- 512x512 images are created with NeverEndingDreamBakedVAE model, model hash is
  64b14b6ca5. CodeFormer is used for face restoration.

|                                                          512x512                                                           |                                                           2048x2048                                                            |
| :------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------: |
| ![00024-3324991962](https://user-images.githubusercontent.com/76731692/233845862-bc77ede8-421b-4076-a31d-29b5ba4f109d.png) | ![00024-3324991962_out](https://user-images.githubusercontent.com/76731692/233845891-49a4df16-82b1-409e-bcea-2fdeac65044e.png) |

|                                                          512x512                                                           |                                                           2048x2048                                                            |
| :------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------: |
| ![00067-1531602356](https://user-images.githubusercontent.com/76731692/233845865-5379d7c0-d6b4-4396-86ff-3b2a82bcbb32.png) | ![00067-1531602356_out](https://user-images.githubusercontent.com/76731692/233845997-6fad9e31-ae50-430f-86cf-b98ddd7a0ad3.png) |
