import customtkinter as ctk


class BaseWidget:
    def __init__(self) -> None:
        pass

    def bind(self, main_frame: ctk.CTkFrame) -> None:
        NotImplementedError()

    def place_on_grid(self) -> None:
        NotImplementedError()
