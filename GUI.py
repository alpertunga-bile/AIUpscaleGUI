import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from subprocess import call, DEVNULL
import customtkinter as ctk
import threading
import subprocess
import os
from RunManager import RunManager
from VenvManager import VenvManager

class GUI:
    startUpInformationlabel = None
    startUpFrame = None
    
    initializeFrame = None
    inputDirectoryLabel = None
    outputDirectoryLabel = None
    initializeInfoLabel = None
    inputDirectory = None
    outputDirectory = None
    modelCombobox = None

    scaleSlider = None
    scaleLabel = None
    faceCheckbox = None
    fp32Checkbox = None

    window = None
    runManager = RunManager()
    venv_manager = VenvManager()

    def __init__(self):
        self.inputDirectory = os.getcwd()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.window = ctk.CTk()
        self.window.title("Upscale with Real ESRGAN")
        self.window.geometry("700x500")

        """
        StartUp Frame Widgets
        """

        self.startUpFrame = ctk.CTkFrame(master=self.window)
        self.startUpInformationlabel = ctk.CTkLabel(master=self.startUpFrame, text='')
        startupButton = ctk.CTkButton(
            master=self.startUpFrame,
            text="Startup",
            command=self.StartTheStartup
        )

        self.startUpInformationlabel.pack(side="top")
        startupButton.pack()
        self.startUpFrame.pack(pady=25)
        

        """
        Initialize Frame Widgets
        """
        self.initializeFrame = ctk.CTkFrame(master=self.window)
        self.inputDirectoryLabel = ctk.CTkLabel(master=self.initializeFrame, text=f'{os.getcwd()}\input')
        self.outputDirectoryLabel = ctk.CTkLabel(master=self.initializeFrame, text=f'{os.getcwd()}\output')
        
        inputSelectButton = ctk.CTkButton(
            master = self.initializeFrame,
            text="Choose Directory",
            command=self.ChangeInputDirectory
        )

        outputSelectButton = ctk.CTkButton(
            master = self.initializeFrame,
            text="Choose Directory",
            command=self.ChangeOutputDirectory
        )

        modelString = tk.StringVar()
        self.modelCombobox = ctk.CTkComboBox(
            self.initializeFrame,
            width=300,
            variable= modelString,
            state='readonly',
            values=['RealESRGAN_x4plus',
            'RealESRNet_x4plus',
            'RealESRGAN_x4plus_anime_6B',
            'RealESRGAN_x2plus',
            'realesr-general-x4v3']
        )

        modelNameLabel = ctk.CTkLabel(self.initializeFrame, text="Model Name")

        self.scaleLabel = ctk.CTkLabel(self.initializeFrame, text="Scale : 3")
        
        self.scaleSlider = ctk.CTkSlider(
            master=self.initializeFrame,
            width=200,
            from_=2,
            to=4,
            number_of_steps=2,
            command=self.SliderEvent
        )

        faceLabel = ctk.CTkLabel(self.initializeFrame, text="Face Enhancement")

        self.faceCheckbox = ctk.CTkCheckBox(
            master=self.initializeFrame,
            text="",
            onvalue=1,
            offvalue=0
        )

        fp32Label = ctk.CTkLabel(self.initializeFrame, text="FP32")
        self.fp32Checkbox = ctk.CTkCheckBox(
            master=self.initializeFrame,
            text="",
            onvalue=1,
            offvalue=0
        )

        self.inputDirectoryLabel.grid(column=0, row=0, padx=(0, 50), ipady=5)
        inputSelectButton.grid(column=1, row=0)
        self.outputDirectoryLabel.grid(column=0, row=1, padx=(0, 50), ipady=5)
        outputSelectButton.grid(column=1, row=1)
        modelNameLabel.grid(column=0, row=2, padx=(0, 50), ipady=5)
        self.modelCombobox.grid(column=1, row=2)
        self.scaleLabel.grid(column=0, row=3, padx=(0, 50), ipady=5)
        self.scaleSlider.grid(column=1, row=3)
        faceLabel.grid(column=0, row=4, padx=(0, 50), ipady=5)
        self.faceCheckbox.grid(column=1, row=4)
        fp32Label.grid(column=0, row=5, padx=(0, 50), ipady=5)
        self.fp32Checkbox.grid(column=1, row=5)

        self.initializeFrame.pack()

        initializeButton = ctk.CTkButton(
            master=self.window,
            text="Initialize",
            command=self.StartInitialize
        )

        initializeButton.pack(pady=30)

        self.initializeInfoLabel = ctk.CTkLabel(master=self.window, text="")
        self.initializeInfoLabel.pack()

    def SliderEvent(self, value):
        self.scaleLabel.configure(text=f"Scale : {int(self.scaleSlider.get())}")

    def ChangeInputDirectory(self):
        self.initializeInfoLabel.configure(text="")
        self.inputDirectory = filedialog.askdirectory(initialdir=self.inputDirectory)
        self.inputDirectoryLabel.configure(text=f"{self.inputDirectory}")
        self.runManager.inputFolder = self.inputDirectory

    def ChangeOutputDirectory(self):
        self.outputDirectory = filedialog.askdirectory(mustexist=True, initialdir=os.getcwd())
        self.outputDirectoryLabel.configure(text=self.outputDirectory)
        self.runManager.outputFolder = self.outputDirectory

    def Initialize(self):
        self.runManager.venv_manager = self.venv_manager
        self.runManager.modelName = self.modelCombobox.get()
        self.runManager.scale = f"{int(self.scaleSlider.get())}"
        self.runManager.faceEnhance = self.faceCheckbox.get()
        self.runManager.fp32 = self.fp32Checkbox.get()
        self.initializeInfoLabel.configure(text="Upscaling ...")
        self.runManager.Run()
        self.initializeInfoLabel.configure(text="DONE!!!")
        print("DONE!!!")

    def StartUp(self):
        if os.path.exists(os.path.join("third-party", "Real-ESRGAN")):
            self.startUpInformationlabel.configure(text="Real-ESRGAN repo is already installed")
            return

        realesrgan_repokey = "realesrgan"

        if os.path.exists(os.path.join("third-party", "Real-ESRGAN")) is False:
            self.venv_manager.CloneRepository("https://github.com/xinntao/Real-ESRGAN.git", realesrgan_repokey, "third-party")
            self.venv_manager.InstallRequirementsFromRepository(realesrgan_repokey)
            self.venv_manager.RunScriptInsideRepository(realesrgan_repokey, "setup.py develop")

        self.startUpInformationlabel.configure(text="Installation is completed!!! You can continue")
        print("Installation is completed!!! You can continue")

    def Loop(self):
        self.window.mainloop()

    def Refresh(self):
        self.window.update()
        self.window.after(1000, self.Refresh)

    def StartTheStartup(self):
        self.Refresh()
        threading.Thread(target=self.StartUp).start()

    def StartInitialize(self):
        self.Refresh()
        threading.Thread(target=self.Initialize).start()