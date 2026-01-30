import customtkinter as ctk
import tkinter as tk
import utils

from .base_widget import BaseWidget


class OptionsWidget(BaseWidget):
    model_string: tk.StringVar
    model_combobox: ctk.CTkComboBox
    model_name_label: ctk.CTkLabel
    data_type_string: tk.StringVar
    data_type_combobox: ctk.CTkComboBox
    data_type_label: ctk.CTkLabel

    def __init__(self) -> None:
        super().__init__()

        self.model_string = tk.StringVar(value="2x-AnimeSharpV4_RCAN")
        self.data_type_string = tk.StringVar(value="bfloat16")

    def bind(self, main_frame: ctk.CTkFrame) -> None:
        self.model_combobox = ctk.CTkComboBox(
            main_frame,
            width=300,
            variable=self.model_string,
            state="readonly",
            values=utils.get_upscaler_names(),
        )
        self.model_name_label = ctk.CTkLabel(main_frame, text="Model Name")

        self.data_type_combobox = ctk.CTkComboBox(
            main_frame,
            width=300,
            variable=self.data_type_string,
            state="readonly",
            values=["bfloat16", "float16", "float32"],
        )
        self.data_type_label = ctk.CTkLabel(main_frame, text="Data Type")

    def place_on_grid(self) -> None:
        self.model_name_label.grid(column=0, row=2, padx=(0, 50), ipady=5)
        self.model_combobox.grid(column=1, row=2)
        self.data_type_label.grid(column=0, row=3, padx=(0, 50), ipady=5)
        self.data_type_combobox.grid(column=1, row=3)
