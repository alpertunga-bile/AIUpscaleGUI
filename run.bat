call .\Real-ESRGAN\env\Scripts\activate &
call Real-ESRGAN\env\Scripts\python.exe Real-ESRGAN\inference_realesrgan.py -n RealESRGAN_x4plus -i  "D:/Projects/AIUpscale/input" -o "D:/Projects/AIUpscale/output" --ext png --fp32 -s 4 --face_enhance &
call deactivate