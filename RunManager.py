import os
from tkinter import messagebox

class RunManager:
    def GetImageFolder(self, imageFolder):
        if os.path.exists(imageFolder) is False:
            messagebox.showinfo(title="WARNING", message=f"There is no {imageFolder} file")
            exit(-1)

        isTherePNG = False
        filelist = os.listdir(imageFolder)
        for file in filelist:
            if file.endswith(".png"):
                isTherePNG = True
                break
        
        if isTherePNG:
            self.imageFolders.append(imageFolder)
            return
        
        self.imageFolders = os.listdir(imageFolder)
        for i in range(0, len(self.imageFolders)):
            self.imageFolders[i] = os.path.join(imageFolder, self.imageFolders[i])

    def AddCommands(self):
        start = f'{self.python_exe} Real-ESRGAN\\inference_realesrgan.py -n {self.modelName} -i '
        end = f"--ext png --fp32 -s {self.scale}"
        if self.faceEnhance == "Yes":
            end = end + " --face_enhance"
        
        for folder in self.imageFolders:
            tempCommand = f'{start} "{folder}" -o "{self.outputFolder}" {end}'
            self.commands.append(tempCommand)

        self.commands.append(self.deactivate_env_command)

    def GetCommandString(self):
        finalCommand = ""
        for command in self.commands:
            finalCommand = finalCommand + command + " &\n"
        finalCommand = finalCommand[:-3]
        return finalCommand
    
    def WriteToBat(self):
        if os.exists("run.bat"):
            os.remove("run.bat")
        file = open("run.bat", "w")
        file.write(self.GetCommandString())
        file.close()

    def Run(self):
        self.AddCommands()
        self.WriteToBat()
        os.system("run.bat")

    python_exe = "call Real-ESRGAN\\env\\Scripts\\python.exe"
    activate_env_command = "call .\Real-ESRGAN\\env\\Scripts\\activate"
    deactivate_env_command = "call deactivate"
    imageFolders = []
    outputFolder = f"{os.getcwd}\\upscaled"
    modelName = None
    scale = "4"
    faceEnhance = "No"
    commands = [activate_env_command]