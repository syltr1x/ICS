from PIL import Image
import customtkinter
import requests as r
import ctypes
import logic
import sys
import os

# Frames
import frames.account
import frames.balance
import frames.car
import frames.history
import frames.inventory
import frames.work
import frames.budgets
import frames.others
import frames.config

# Version Managment
config = logic.get_config()
def update(obj, c):
    if c == 1 : obj.destroy()
    global lvi
    key = config["vkey"]
    customtkinter.set_default_color_theme(config["theme"])
    customtkinter.set_appearance_mode(config["mode"])
    try:
        vkey = r.get('https://raw.githubusercontent.com/syltr1x/ICS/main/vkey')
        if vkey.status_code == 200:
            if key != vkey.text[:-1]: lvi = False
            else: lvi = True
        else: lvi = True
    except:
        warn = customtkinter.CTk()
        warn.title("Error detected")
        warn.geometry("300x200")
        wlabel = customtkinter.CTkLabel(warn, text="""Fallo al obtener clave de version. Esto puede \ndeberse a que no se ha establecido una conexion \nde internet, esto no afecta el funcionamiento\n de la aplicacion.""")
        wlabel.grid(column=0, row=0, pady=(20, 48), padx=9)
        wbtn1 = customtkinter.CTkButton(warn, text="Reintentar", command=lambda:(update(warn, 1)))
        wbtn1.grid(column=0, row=1, pady=(0, 8))
        wbtn2 = customtkinter.CTkButton(warn, text="Cerrar", command=lambda:(warn.destroy()))
        wbtn2.grid(column=0, row=2)
        warn.mainloop()
        lvi = True

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Punto Diesel | WorkShop Solution")
        self.geometry("1260x550")
        self.icon_app = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img\\icon.ico")
        self.after(201, lambda :self.iconbitmap(self.icon_app))

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon.png")), size=(26, 26))
        self.budget_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/bill.png")),
                dark_image=Image.open(os.path.join(image_path, "light/bill.png")), size=(20, 20))
        self.work_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/spanner.png")),
                dark_image=Image.open(os.path.join(image_path, "light/spanner.png")), size=(20, 20))
        self.car_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/car.png")),
                dark_image=Image.open(os.path.join(image_path, "light/car.png")), size=(20, 20))
        self.balance_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/balance.png")),
                dark_image=Image.open(os.path.join(image_path, "light/balance.png")), size=(20, 20))
        self.account_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/account.png")),
                dark_image=Image.open(os.path.join(image_path, "light/account.png")), size=(20, 20))
        self.inventory_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/list.png")),
                dark_image=Image.open(os.path.join(image_path, "light/list.png")), size=(20, 20))
        self.contacts_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/phone_book.png")),
                dark_image=Image.open(os.path.join(image_path, "light/phone_book.png")), size=(20, 20))
        self.history_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/clock.png")),
                dark_image=Image.open(os.path.join(image_path, "light/clock.png")), size=(20, 20))
        self.cash_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/cash.png")),
                dark_image=Image.open(os.path.join(image_path, "light/cash.png")))
        self.config_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/config.png")),
                dark_image=Image.open(os.path.join(image_path, "light/config.png")))

        # create navigation frame  /  Lateral Menu
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(100, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Punto Diesel", image=self.logo_image,
                compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=1, column=0, padx=20, pady=20)
        
        self.budget_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Presupuestos",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.budget_image, anchor="w", command=self.budget_button_event)
        self.budget_button.grid(row=2, column=0, sticky="ew")

        self.work_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Ordenes",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.work_image, anchor="w", command=self.work_button_event)
        self.work_button.grid(row=3, column=0, sticky="ew")

        self.car_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Vehiculo",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.car_image, anchor="w", command=self.car_button_event)
        self.car_button.grid(row=4, column=0, sticky="ew")

        self.balance_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Balance",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.balance_image, anchor="w", command=self.balance_button_event)
        self.balance_button.grid(row=5, column=0, sticky="ew")

        self.account_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Cuentas",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.account_image, anchor="w", command=self.account_button_event)
        self.account_button.grid(row=6, column=0, sticky="new")

        self.inventory_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Inventario",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.inventory_image, anchor="w", command=self.inventory_button_event)
        self.inventory_button.grid(row=7, column=0, sticky="new")

        self.history_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Historial",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.history_image, anchor="w", command=self.history_button_event)
        self.history_button.grid(row=8, column=0, sticky="ew")

        self.others_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Cobros/Ventas",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.cash_image, anchor="w", command=self.others_button_event)
        self.others_button.grid(row=9, column=0, sticky="ew")

        self.config_btn = customtkinter.CTkButton(self.navigation_frame, image=self.config_image, text="", command=self.change_config, width=1)
        self.config_btn.grid(row=10, column=0, padx=(110, 0), pady=20, sticky="s")

        self.update_btn = customtkinter.CTkButton(self.navigation_frame, corner_radius=5, text="Actualizar", command=self.update, width=1)
        self.update_btn.grid(row=11, column=0, padx=(0, 5), pady=20, sticky="n") if lvi != True else None

        # create budget frame
        self.budget_frame = frames.budgets.App(self)

        # create works frame
        self.work_frame = frames.work.App(self)

        # create cars frame
        self.car_frame = frames.car.App(self)

        # create balance frame
        self.balance_frame = frames.balance.App(self)

        # create account frame
        self.account_frame = frames.account.App(self)

        # create inventory frame
        self.inventory_frame = frames.inventory.App(self)
        
        # create history frame
        self.history_frame = frames.history.App(self)

        # create cash frame
        self.others_frame = frames.others.App(self)

        # create config frame
        self.config_frame = frames.config.App(self)

        # select default frame
        self.select_frame_by_name("budget")

    def select_frame_by_name(self, name):
        if name != "account":
            logic.order_id(name+'.json') 
        else:
            logic.order_id("account.json")
            logic.order_id("customer.json")
        # set button color for selected button
        self.budget_button.configure(fg_color=("gray75", "gray25") if name == "budget" else "transparent")
        self.work_button.configure(fg_color=("gray75", "gray25") if name == "work" else "transparent")
        self.car_button.configure(fg_color=("gray75", "gray25") if name == "car" else "transparent")
        self.balance_button.configure(fg_color=("gray75", "gray25") if name == "balance" else "transparent")
        self.account_button.configure(fg_color=("gray75", "gray25") if name == "account" else "transparent")
        self.inventory_button.configure(fg_color=("gray75", "gray25") if name == "inventory" else "transparent")
        self.history_button.configure(fg_color=("gray75", "gray25") if name == "history" else "transparent")
        self.others_button.configure(fg_color=("gray75", "gray25") if name == "other" else "transparent")

        # show selected frame
        if name == "budget":
            self.budget_frame.grid(row=0, column=1, sticky='nsew')
        else:
            self.budget_frame.grid_forget()
        if name == "work":
            self.work_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.work_frame.grid_forget()
        if name == "car":
            self.car_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.car_frame.grid_forget()
        if name == "balance":
            self.balance_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.balance_frame.grid_forget()
        if name == "account":
            self.account_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.account_frame.grid_forget()
        if name == "inventory":
            self.inventory_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.inventory_frame.grid_forget()
        if name == "history":
            self.history_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.history_frame.grid_forget()
        if name == "other":
            self.others_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.others_frame.grid_forget()
        if name == "config":
            self.config_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.config_frame.grid_forget()

    def budget_button_event(self):
        self.select_frame_by_name("budget")

    def work_button_event(self):
        self.select_frame_by_name("work")

    def car_button_event(self):
        self.select_frame_by_name("car")

    def balance_button_event(self):
        self.select_frame_by_name("balance")

    def account_button_event(self):
        self.select_frame_by_name("account")
    
    def inventory_button_event(self):
        self.select_frame_by_name("inventory")
    
    def history_button_event(self):
        self.select_frame_by_name("history")

    def others_button_event(self):
        self.select_frame_by_name("other")

    def change_config(self):
        self.select_frame_by_name("config")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def update(self): 
        self.destroy()
        logic.update_app()

if __name__ == "__main__":
    try:
        def is_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        def run_as_admin():
            if is_admin():
                print("El programa ya se está ejecutando como administrador.")
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit()  # Salir del script si no se proporcionaron permisos de administrador
        # run_as_admin()
        if config["path"] == "":
            logic.mod_config([{"field":"path", "value":os.path.dirname(os.path.realpath(__name__))}])
        update("", 0)
        app = App()
        app.mainloop()
        [os.remove(f'data/temp/{i}') for i in os.listdir('data/temp/')] # Delete all temporal files
    except:
        [os.remove(f'data/temp/{i}') for i in os.listdir('data/temp/')] # Delete all temporal files