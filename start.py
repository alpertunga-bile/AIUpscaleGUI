import os
from subprocess import call, DEVNULL

if __name__ == "__main__":
    if(os.path.exists("venv") == False):
        venvCommand = "python -m venv venv && "
        venvCommand += ".\\venv\Scripts\\activate && "
        venvCommand += ".\\venv\Scripts\pip.exe install customtkinter && "
        venvCommand += "deactivate"
        
        print("Preparing virtual environment ...")
        result = call(venvCommand, shell=True)
        _ = print("Virtual environment is created") if result == 0 else print("Error")

    print("Starting GUI ...")
    guiCommand = ".\\venv\\Scripts\\python.exe main.py"
    result = call(guiCommand, shell=True)