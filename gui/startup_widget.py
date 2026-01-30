import customtkinter as ctk
import threading

from .base_widget import BaseWidget


class StartupWidget(BaseWidget):
    info_label: ctk.CTkLabel
    start_button: ctk.CTkButton

    def __init__(self) -> None:
        pass

    def bind(self, main_frame: ctk.CTkFrame) -> None:
        self.info_label = ctk.CTkLabel(master=main_frame, text="")
        self.start_button = ctk.CTkButton(
            master=main_frame, text="Startup", command=self.start_startup
        )

    def place_on_grid(self) -> None:
        self.info_label.pack(side="top")
        self.start_button.pack()

    def startup(self):
        self.info_label.configure(text="Startup is completed!!!")

    def start_startup(self):
        threading.Thread(target=self.startup).start()
