import os
from tkinter import messagebox
from subprocess import call
from VenvManager import VenvManager

class RunManager:
    def GetImageFolder(self, imageFolder):
        if os.path.exists(imageFolder) is False:
            messagebox.showinfo(title="WARNING", message=f"There is no {imageFolder} file")
            exit(-1)

        isTherePNG = False
        filelist = os.listdir(imageFolder)
        for file in filelist:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                isTherePNG = True
                break
        
        if isTherePNG:
            self.imageFolders.append(imageFolder)
            return
        
        self.imageFolders = os.listdir(imageFolder)
        for i in range(0, len(self.imageFolders)):
            self.imageFolders[i] = os.path.join(imageFolder, self.imageFolders[i])

    def AddCommands(self):
        start = f'-n {self.modelName} -i '
        end = f"--ext png -s {self.scale} --tile 192"
        
        if self.faceEnhance == 1:
            end = end + " --face_enhance"

        if self.fp32 == 1:
            end = end + " --fp32"
        
        for folder in self.imageFolders:
            tempCommand = f'{start} "{folder}" -o "{self.outputFolder}" {end}'
            self.commands.append(tempCommand)

    def GetCommandString(self):
        finalCommand = ""
        for command in self.commands:
            finalCommand = finalCommand + command + " && "
        finalCommand = finalCommand[:-3]
        return finalCommand

    def Run(self):
        self.GetImageFolder(self.inputFolder)
        self.AddCommands()
        call('cls' if os.name=='nt' else 'clear', shell=True)
        for command in self.commands:
            self.venv_manager.RunScript("third-party/Real-ESRGAN/inference_realesrgan", command)
        call('cls' if os.name=='nt' else 'clear', shell=True)
        self.imageFolders.clear()

    imageFolders = []
    inputFolder = None
    outputFolder = os.path.join(os.getcwd(), "upscaled")
    modelName = None
    scale = "4"
    faceEnhance = 0
    fp32 = 1
    venv_manager : VenvManager = None
    commands = []