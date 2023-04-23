@ECHO OFF

call git clone https://github.com/xinntao/Real-ESRGAN.git &
call py -m venv Real-ESRGAN\env &
call .\Real-ESRGAN\env\Scripts\activate &
call .\Real-ESRGAN\env\Scripts\pip.exe install basicsr facexlib gfpgan &
call .\Real-ESRGAN\env\Scripts\pip.exe install -r Real-ESRGAN\requirements.txt &
cd Real-ESRGAN &
call .\env\Scripts\python.exe setup.py develop &
cd .. &
call deactivate

