import customtkinter as ctk
import os.path
from tkinter import filedialog

from .base_widget import BaseWidget


class SelectDirectoryWidget(BaseWidget):
    input_dir_label: ctk.CTkLabel
    output_dir_label: ctk.CTkLabel
    input_select_button: ctk.CTkButton
    output_select_button: ctk.CTkButton
    input_dir: str = ""
    output_dir: str = ""

    def __init__(self) -> None:
        self.input_dir = os.path.join(os.getcwd(), "input")
        self.output_dir = os.path.join(os.getcwd(), "output")

    def bind(self, main_frame: ctk.CTkFrame) -> None:
        self.input_dir_label = ctk.CTkLabel(master=main_frame, text=self.input_dir)
        self.output_dir_label = ctk.CTkLabel(master=main_frame, text=self.output_dir)

        self.input_select_button = ctk.CTkButton(
            master=main_frame,
            text="Choosing Directory",
            command=self.change_input_directory,
        )
        self.output_select_button = ctk.CTkButton(
            master=main_frame,
            text="Choosing Directory",
            command=self.change_output_directory,
        )

    def place_on_grid(self) -> None:
        self.input_dir_label.grid(column=0, row=0, padx=(0, 50), ipady=5)
        self.input_select_button.grid(column=1, row=0)
        self.output_dir_label.grid(column=0, row=1, padx=(0, 50), ipady=5)
        self.output_select_button.grid(column=1, row=1)

    def change_input_directory(self):
        self.input_dir = filedialog.askdirectory(mustexist=True, initialdir=os.getcwd())
        self.input_dir = self.input_dir if len(self.input_dir) > 0 else os.getcwd()
        self.input_dir_label.configure(text=self.input_dir)

    def change_output_directory(self):
        self.output_dir = filedialog.askdirectory(
            mustexist=True, initialdir=os.getcwd()
        )
        self.output_dir = self.output_dir if len(self.output_dir) > 0 else os.getcwd()
        self.output_dir_label.configure(text=self.output_dir)
