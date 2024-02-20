import logic
from PIL import Image
import customtkinter

class App(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        default_value = customtkinter.StringVar()
        default_value.set(logic.get_config()["mechanics"])

        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Modo de la Aplicacion")
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self, values=["Sistema","Oscuro", "Claro"])
        self.theme_mode_label = customtkinter.CTkLabel(self, text="Tema de la Aplicacion")
        self.theme_mode_menu = customtkinter.CTkOptionMenu(self, values=["Rojo", "Azul", "Verde", "Morado", "Amarillo"])
        self.technicians_label = customtkinter.CTkLabel(self, text="Mecanicos (separados por '|')")
        self.technicians_entry = customtkinter.CTkEntry(self, textvariable=default_value, width=170)
        self.confirm_btn = customtkinter.CTkButton(self, text="Confirmar", command=lambda:(logic.mod_config([
            {"field":"mode", "value":self.appearance_mode_menu.get()}, 
            {"field":"theme", "value":self.theme_mode_menu.get()}, 
            {"field":"mechanics", "value":self.technicians_entry.get()}, 
        ])))
        self.cancel_btn = customtkinter.CTkButton(self, text="Cancelar", command=lambda:(self.grid_forget()))

        self.appearance_mode_label.grid(row=0, column=0, padx=5, pady=5)
        self.appearance_mode_menu.grid(row=0, column=1, padx=5, pady=5)
        self.theme_mode_label.grid(row=1, column=0, padx=5, pady=5)
        self.theme_mode_menu.grid(row=1, column=1, padx=5, pady=5)
        self.technicians_label.grid(row=2, column=0, padx=5, pady=5)
        self.technicians_entry.grid(row=2, column=1, padx=5, pady=5)
        self.confirm_btn.grid(row=3, column=0, padx=5, pady=5)
        self.cancel_btn.grid(row=3, column=1, padx=5, pady=5)