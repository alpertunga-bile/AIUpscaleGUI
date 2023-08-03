import os
from VenvManager import VenvManager

from os.path import exists, join
from os import mkdir, remove

def CheckFolder(foldername : str) -> None:
    if exists(foldername) is False:
        mkdir(foldername)

def RemoveIfExists(filename : str) -> None:
    if exists(filename):
        remove(filename)

if __name__ == "__main__":
    venv_manager = VenvManager()
    realesrgan_repokey = "realesrgan"

    CheckFolder("third-party")

    if exists(join("third-party", "Real-ESRGAN")) is False:
        venv_manager.CloneRepository("https://github.com/xinntao/Real-ESRGAN.git", realesrgan_repokey, "third-party")
        venv_manager.InstallRequirementsFromRepository(realesrgan_repokey)
        venv_manager.RunScriptInsideRepository(realesrgan_repokey, "setup.py develop")

    RemoveIfExists("0.2.5")
    RemoveIfExists("1.3.5")
    RemoveIfExists("1.4.2")
    RemoveIfExists("1.7")

    venv_manager.InstallWRequirements()

    venv_manager.RunScript("main")