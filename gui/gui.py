import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import threading
import os
import os.path
import utils

from .startup_widget import StartupWidget
from .seldir_widget import SelectDirectoryWidget
from .options_widget import OptionsWidget


class MainWindow:
    window: ctk.CTk

    startup_frame: ctk.CTkFrame
    initialize_frame: ctk.CTkFrame

    start_widget: StartupWidget
    seldir_widget: SelectDirectoryWidget
    options_widget: OptionsWidget

    initialize_button: ctk.CTkButton

    def __init__(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.window = ctk.CTk()
        self.window.title("Upscale your image")
        self.window.geometry("700x500")

        self.start_widget = StartupWidget()
        self.seldir_widget = SelectDirectoryWidget()
        self.options_widget = OptionsWidget()

        self.startup_frame = ctk.CTkFrame(master=self.window)
        self.initialize_frame = ctk.CTkFrame(master=self.window)

        self.start_widget.bind(self.startup_frame)
        self.seldir_widget.bind(self.initialize_frame)
        self.options_widget.bind(self.initialize_frame)

        self.start_widget.place_on_grid()
        self.startup_frame.pack(pady=25)

        self.seldir_widget.place_on_grid()
        self.options_widget.place_on_grid()
        self.initialize_frame.pack()

        self.initialize_button = ctk.CTkButton(
            master=self.window, text="Upscale", command=self.start_upscale
        )
        self.initialize_button.pack(pady=30)

        self.initializeInfoLabel = ctk.CTkLabel(master=self.window, text="")
        self.initializeInfoLabel.pack()

    def start_upscale(self):
        model_name = self.options_widget.model_combobox.get()
        input_folder = self.seldir_widget.input_dir
        output_folder = self.seldir_widget.output_dir
        data_type = self.options_widget.data_type_combobox.get()

        info = utils.UpscaleInfo(
            model_path=model_name,
            input_path=input_folder,
            output_path=output_folder,
            data_type=data_type,
        )

        utils.check_and_install_model(model_name)
        utils.upscale_images(input_folder, info)

    def Loop(self):
        self.window.mainloop()

    def Refresh(self):
        self.window.update()
        self.window.after(1000, self.Refresh)
