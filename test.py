from PIL import Image
import customtkinter
import os


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Punto Diesel")
        self.geometry("978x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
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

        # create navigation frame  /  Lateral Menu
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Punto Diesel", image=self.logo_image,
                compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.work_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Trabajos",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.work_image, anchor="w", command=self.work_button_event)
        self.work_button.grid(row=1, column=0, sticky="ew")

        self.car_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Vehiculo",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.car_image, anchor="w", command=self.car_button_event)
        self.car_button.grid(row=2, column=0, sticky="ew")

        self.balance_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Balance",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.balance_image, anchor="w", command=self.balance_button_event)
        self.balance_button.grid(row=3, column=0, sticky="ew")

        self.account_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Cuentas",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.account_image, anchor="w", command=self.account_button_event)
        self.account_button.grid(row=4, column=0, sticky="ew")

        self.inventory_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Inventario",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.inventory_image, anchor="w", command=self.inventory_button_event)
        self.inventory_button.grid(row=5, column=0, sticky="ew")

        self.contacts_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Contactos",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.contacts_image, anchor="w", command=self.contacts_button_event)
        self.contacts_button.grid(row=6, column=0, sticky="ew")

        self.rell = customtkinter.CTkLabel(self.navigation_frame, corner_radius=0, height=50, text="")
        self.rell.grid(row=7, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["System", "Dark", "Light"],
                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=8, column=0, padx=20, pady=20, sticky="s")

        # create customer frame

        self.customer_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # l1 = customtkinter.CTkLabel(self.customer_frame, text="Clientes").grid(row=1, column=1, padx=20, pady=10)

        # create works frame
        self.work_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create cars frame
        self.car_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create balance frame
        self.balance_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create account frame
        self.account_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create inventory frame
        self.inventory_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create contacts frame
        self.contacts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        # select default frame
        self.select_frame_by_name("work")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.work_button.configure(fg_color=("gray75", "gray25") if name == "work" else "transparent")
        self.car_button.configure(fg_color=("gray75", "gray25") if name == "car" else "transparent")
        self.balance_button.configure(fg_color=("gray75", "gray25") if name == "balance" else "transparent")
        self.account_button.configure(fg_color=("gray75", "gray25") if name == "account" else "transparent")
        self.inventory_button.configure(fg_color=("gray75", "gray25") if name == "inventory" else "transparent")
        self.contacts_button.configure(fg_color=("gray75", "gray25") if name == "contacts" else "transparent")

        # show selected frame
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
        if name == "contacts":
            self.contacts_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.contacts_frame.grid_forget()

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

    def contacts_button_event(self):
        self.select_frame_by_name("contacts")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()