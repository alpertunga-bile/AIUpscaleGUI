@ECHO OFF

call py -m venv Real-ESRGAN\env &
call .\Real-ESRGAN\env\Scripts\activate &
call .\Real-ESRGAN\env\Scripts\pip.exe install basicsr facexlib gfpgan &
call .\Real-ESRGAN\env\Scripts\pip.exe install -r requirements.txt &
call .\Real-ESRGAN\env\Scripts\python.exe setup.py develop &
call deactivate
