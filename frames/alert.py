import customtkinter as ctk
import os
from PIL import Image
import json

# Images Definition
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")
warning_icon_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/warning.png"))
        , size=(50, 50))
alert_icon_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/alert.png"))
        , size=(50, 50))
cross_icon_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/x.png"))
        , size=(50, 50))

icons = {
    "x":cross_icon_image,
    "w":warning_icon_image,
    "a":alert_icon_image,
}

def create(title="Warning Window", icon="", msg="Warning Message", buttons=[{"text":"Aceptar", "action":"close"}, {"text":"Cancelar", "action":"close"}]):
    window = ctk.CTk()
    actions = {
        "close":lambda:(window.destroy()),
        "kill":lambda:(exit()),
    }
    window.title(title)
    window.geometry("280x280")
    label = ctk.CTkLabel(window, text=msg, compound="left")
    if icon != "": label.configure(image=icons[icon])
    label.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
    if buttons != []:
        cl = 0
        rw = 1
        for k in range(0, len(buttons)):
            data = buttons[k]
            btn = ctk.CTkButton(window, text=data["text"], command=actions[data["action"]], corner_radius=4)
            btn.grid(row=rw, column=cl, padx=(5*cl, 5), pady=5)
            if len(buttons) % 3 == 0 and len(buttons):
                if cl == 3:
                    cl = 0
                    rw += 1
            if len(buttons) % 2 == 0 and len(buttons):
                clc = len(buttons)/2 if len(buttons)/2 != 1 else 2
                if cl == clc:
                    cl = 0
                    rw += 1
            cl += 1
    window.mainloop()