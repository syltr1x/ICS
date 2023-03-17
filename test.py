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
        self.customer_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/customer_dark.png")),
                dark_image=Image.open(os.path.join(image_path, "light/customer_light.png")), size=(20, 20))
        self.work_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/spanner_dark.png")),
                dark_image=Image.open(os.path.join(image_path, "light/spanner_light.png")), size=(20, 20))
        self.car_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/car_dark.png")),
                dark_image=Image.open(os.path.join(image_path, "light/car_light.png")), size=(20, 20))

        # create navigation frame  /  Lateral Menu
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Punto Diesel", image=self.logo_image,
                compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.customer_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Clientes",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.customer_image, anchor="w", command=self.customer_button_event)
        self.customer_button.grid(row=1, column=0, sticky="ew")

        self.work_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Trabajos",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.work_image, anchor="w", command=self.work_button_event)
        self.work_button.grid(row=2, column=0, sticky="ew")

        self.car_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Autos",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                image=self.car_image, anchor="w", command=self.car_button_event)
        self.car_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["System", "Dark", "Light"],
                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create customer frame

        self.customer_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # l1 = customtkinter.CTkLabel(self.customer_frame, text="Clientes").grid(row=1, column=1, padx=20, pady=10)

        # create works frame

        self.work_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # l2 = customtkinter.CTkLabel(self.work_frame, text="Trabajos").grid(row=2, column=2, padx=40, pady=40)

        # create cars frame

        self.car_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # l3 = customtkinter.CTkLabel(self.car_frame, text="Autos").grid(row=3, column=3, padx=60, pady=60)
        
        # select default frame
        self.select_frame_by_name("customer")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.customer_button.configure(fg_color=("gray75", "gray25") if name == "customer" else "transparent")
        self.work_button.configure(fg_color=("gray75", "gray25") if name == "work" else "transparent")
        self.car_button.configure(fg_color=("gray75", "gray25") if name == "car" else "transparent")

        # show selected frame
        if name == "customer":
            self.customer_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.customer_frame.grid_forget()
        if name == "work":
            self.work_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.work_frame.grid_forget()
        if name == "car":
            self.car_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.car_frame.grid_forget()

    def customer_button_event(self):
        self.select_frame_by_name("customer")

    def work_button_event(self):
        self.select_frame_by_name("work")

    def car_button_event(self):
        self.select_frame_by_name("car")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()