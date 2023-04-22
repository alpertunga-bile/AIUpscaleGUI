@ECHO OFF

call py -m venv env &
call .\env\Scripts\activate &
call .\env\Scripts\pip.exe install basicsr facexlib gfpgan &
call .\env\Scripts\pip.exe install -r requirements.txt &
call .\env\Scripts\python.exe setup.py develop
call deactivate