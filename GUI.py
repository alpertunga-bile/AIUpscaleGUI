import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import subprocess
import os
from RunManager import RunManager

class GUI:
    def __init__(self):
        self.inputDirectory = os.getcwd()
        self.window = tk.Tk(baseName="Upscale with Real ESRGAN")
        self.window.geometry("500x500")

        """
        StartUp Frame Widgets
        """
        self.startUpFrame = tk.Frame()
        self.startUpInformationlabel = tk.Label(master=self.startUpFrame, text='')
        startupButton = tk.Button(
            master=self.startUpFrame,
            text="Startup",
            command=self.StartUp
        )

        self.startUpInformationlabel.pack(side="top")
        startupButton.pack(pady=20)
        self.startUpFrame.pack(pady=50)

        """
        Initialize Frame Widgets
        """
        self.initializeFrame = tk.Frame()
        self.inputDirectoryLabel = tk.Label(master=self.initializeFrame, text=f'{os.getcwd()}\input')
        self.outputDirectoryLabel = tk.Label(master=self.initializeFrame, text=f'{os.getcwd()}\output')
        
        inputSelectButton = tk.Button(
            master = self.initializeFrame,
            text="Choose Directory",
            command=self.ChangeInputDirectory
        )

        outputSelectButton = tk.Button(
            master = self.initializeFrame,
            text="Choose Directory",
            command=self.ChangeOutputDirectory
        )

        modelString = tk.StringVar()
        self.modelCombobox = ttk.Combobox(
            self.initializeFrame,
            width=30,
            textvariable= modelString
        )

        modelNameLabel = tk.Label(self.initializeFrame, text="Model Name")

        self.modelCombobox['values'] = (
            'RealESRGAN_x4plus',
            'RealESRNet_x4plus',
            'RealESRGAN_x4plus_anime_6B',
            'RealESRGAN_x2plus',
            'realesr-general-x4v3'
        )

        self.modelCombobox.state(["readonly"])

        scaleLabel = tk.Label(self.initializeFrame, text="Scale")

        scaleString = tk.StringVar()
        self.scaleCombobox = ttk.Combobox(
            self.initializeFrame,
            width=7,
            textvariable=scaleString
        )

        self.scaleCombobox['values'] = (
            '2', '3', '4'
        )

        self.scaleCombobox.state(["readonly"])

        faceLabel = tk.Label(self.initializeFrame, text="Face Enhancement")

        faceString = tk.StringVar()
        self.faceCombobox = ttk.Combobox(
            self.initializeFrame,
            width=5,
            textvariable=faceString
        )

        self.faceCombobox['values'] = ("Yes", "No")
        self.faceCombobox.state(["readonly"])

        self.inputDirectoryLabel.grid(column=0, row=0, padx=(0, 50), ipady=5)
        inputSelectButton.grid(column=1, row=0)
        self.outputDirectoryLabel.grid(column=0, row=1, padx=(0, 50), ipady=5)
        outputSelectButton.grid(column=1, row=1)
        modelNameLabel.grid(column=0, row=2, padx=(0, 50), ipady=5)
        self.modelCombobox.grid(column=1, row=2)
        scaleLabel.grid(column=0, row=3, padx=(0, 50), ipady=5)
        self.scaleCombobox.grid(column=1, row=3)
        faceLabel.grid(column=0, row=4, padx=(0, 50), ipady=5)
        self.faceCombobox.grid(column=1, row=4)

        self.initializeFrame.pack()

        initializeButton = tk.Button(
            text="Initialize",
            command=self.Initialize
        )

        initializeButton.pack(pady=30)

        self.initializeInfoLabel = tk.Label(text="")
        self.initializeInfoLabel.pack()

    def ChangeInputDirectory(self):
        self.initializeInfoLabel.config(text="")
        self.inputDirectory = filedialog.askdirectory(initialdir=self.inputDirectory)
        self.inputDirectoryLabel.config(text=f"{self.inputDirectory}")
        self.runManager.GetImageFolder(self.inputDirectory)

    def ChangeOutputDirectory(self):
        self.outputDirectory = filedialog.askdirectory(mustexist=True, initialdir=os.getcwd())
        self.outputDirectoryLabel.config(text=self.outputDirectory)
        self.runManager.outputFolder = self.outputDirectory

    def Initialize(self):
        self.runManager.modelName = self.modelCombobox.get()
        self.runManager.scale = self.scaleCombobox.get()
        self.runManager.faceEnhance = self.faceCombobox.get()
        self.runManager.Run()
        self.initializeInfoLabel.config(text="DONE!!!")
        print("DONE!!!")

    def StartUp(self):
        if os.path.exists("Real-ESRGAN"):
            self.startUpInformationlabel.config(text="Real-ESRGAN repo is already installed")
            return

        process = subprocess.Popen("git --version", stdout=subprocess.PIPE)
        streamdata = process.communicate()[0]

        if process.returncode != 0:
            messagebox.showerror(message="There is no Git on your computer or not included in PATH variable, please install it or add to PATH variable and try again")
            exit(-1)

        self.startUpInformationlabel.config(text="Cloning repository ...")
        print("Cloning repository ...")
        process = subprocess.Popen("git clone https://github.com/xinntao/Real-ESRGAN.git", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        self.WaitUntilFinishSubprocess(process)

        self.startUpInformationlabel.config(text="Installing required packages ...")
        print("Installing required packages ...")
        command = ""
        command += "py -m venv Real-ESRGAN\env & "
        command += ".\Real-ESRGAN\env\Scripts\\activate & "
        command += ".\Real-ESRGAN\env\Scripts\pip.exe install basicsr facexlib gfpgan & "
        command += ".\Real-ESRGAN\env\Scripts\pip.exe install -r Real-ESRGAN\\requirements.txt & "
        command += "cd Real-ESRGAN & call .\env\Scripts\python.exe setup.py develop & cd .. & deactivate"
        os.system(command)
        self.startUpInformationlabel.config(text="Installation is complete!!! You can continue")
        os.system('cls' if os.name=='nt' else 'clear')
        print("Installation is complete!!! You can continue")

    def WaitUntilFinishSubprocess(self, process):
        poll = process.poll()
        while poll is None:
            poll = process.poll()
        print("Finished process")

    def Loop(self):
        self.window.mainloop()

    startUpInformationlabel = None
    startUpFrame = None
    
    initializeFrame = None
    inputDirectoryLabel = None
    outputDirectoryLabel = None
    initializeInfoLabel = None
    inputDirectory = None
    outputDirectory = None
    modelCombobox = None
    scaleCombobox = None
    faceCombobox = None

    window = None
    runManager = RunManager()