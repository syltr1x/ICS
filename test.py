from PIL import Image
import customtkinter
import logic
import json
import os


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Punto Diesel")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.customer_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "customer_dark.png")),
                dark_image=Image.open(os.path.join(image_path, "customer_light.png")), size=(20, 20))
        self.work_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "spanner_dark.png")),
                dark_image=Image.open(os.path.join(image_path, "spanner_light.png")), size=(20, 20))
        self.car_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "car_dark.png")),
                dark_image=Image.open(os.path.join(image_path, "car_light.png")), size=(20, 20))

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

        class AddCustomerFrame(customtkinter.CTkFrame):
            def __init__(self, master, command=None, **kwargs):
                super().__init__(master, **kwargs)

                self.command = command
                self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Nombre")
                self.name_entry.grid(row=1, column=0, columnspan=2, padx=(100, 10), pady=(20, 20), sticky="nsew")

                self.lastname_entry = customtkinter.CTkEntry(self, placeholder_text="Apellido")
                self.lastname_entry.grid(row=2, column=0, columnspan=2, padx=(100, 10), pady=(20, 20), sticky="nsew")

                self.lcplate_entry = customtkinter.CTkEntry(self, placeholder_text="Patente")
                self.lcplate_entry.grid(row=3, column=0, columnspan=2, padx=(100, 10), pady=(20, 20), sticky="nsew")

                self.add_customer_button = customtkinter.CTkButton(self, text="Añadir Cliente", command=lambda:(self.add_customer(self.name_entry.get().capitalize(), self.lastname_entry.get().capitalize(), self.lcplate_entry.get())))
                self.add_customer_button.grid(row=4, column=0, columnspan=2, padx=(100, 10), pady=(20,20), sticky="nsew")

            def add_customer(self, name, lastname, lcplate):
                logic.write_customer("none", name, lastname, lcplate)

        class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
            def __init__(self, master, command=None, **kwargs):
                super().__init__(master, **kwargs)
                self.grid_columnconfigure(0, weight=1)

                self.radiobutton_variable = customtkinter.StringVar()
                self.label_list = []

            def add_item(self, item):
                label = customtkinter.CTkLabel(self, text=item, width=280)
                label.grid(row=len(self.label_list), column=0, pady=(20, 5), sticky="nsew")
                self.label_list.append(label)

            def remove_item(self, item):
                for label, button in zip(self.label_list, self.button_list):
                    if item == label.cget("text"):
                        label.destroy()
                        button.destroy()
                        self.label_list.remove(label)
                        self.button_list.remove(button)
                        return

        class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
            def __init__(self, master, item_list, command=None, **kwargs):
                super().__init__(master, **kwargs)

                self.command = command
                self.radiobutton_variable = customtkinter.StringVar()
                self.radiobutton_list = []
                for i, item in enumerate(item_list):
                    self.add_item(item)

            def add_item(self, item):
                radiobutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
                if self.command is not None:
                    radiobutton.configure(command=self.command)
                radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(5, 5))
                self.radiobutton_list.append(radiobutton)

            def remove_item(self, item):
                for radiobutton in self.radiobutton_list:
                    if item == radiobutton.cget("text"):
                        radiobutton.destroy()
                        self.radiobutton_list.remove(radiobutton)
                        return

            def get_checked_item(self):
                return self.radiobutton_variable.get()
        
        remove_icon_image = customtkinter.CTkImage(Image.open(os.path.join("img/dark", "remove.png")), size=(20, 20))
        add_icon_image = customtkinter.CTkImage(Image.open(os.path.join("img/dark", "add.png")), size=(20, 20))
        refresh_icon_image = customtkinter.CTkImage(Image.open(os.path.join("img/dark", "refresh.png")), size=(20, 20))        
        
        def remove_customer():
            self.scrollable_label_button_frame.destroy()
            id = str(logic.get_customer("name", scrollable_radiobutton_frame.get_checked_item().split(" ")[0], "strict"))[:-1][1:].replace("'",'"')
            id = json.loads(id)
            id = id["id"]
            logic.remove_data("customer.json", id, "id")
            self.refresh()

        def add_customer():
            add_customer_frame = AddCustomerFrame(master=self, width=420, corner_radius=10)
            add_customer_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")

        def refresh():
            scrollable_radiobutton_frame.destroy()
            with open("data/customer.json", "r") as dF: data = dF.read(); dF.close(); data = data[:-1][1:].replace("},","}},").split("},")
            scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=radiobutton_frame_event,
                    item_list=[f'{json.loads(i)["name"]} {json.loads(i)["lastname"]}' for i in data],
                    label_text="Lista de Clientes", corner_radius=10)
            scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")
            scrollable_radiobutton_frame.configure(width=292)
            

        def label_button_frame_event(item):
            print(item)
        def radiobutton_frame_event():
            NpId = []
            LpId = []
            Nid = str(logic.get_customer("name", scrollable_radiobutton_frame.get_checked_item().split(" ")[0], "strict"))
            Lid = str(logic.get_customer("lastname", scrollable_radiobutton_frame.get_checked_item().split(" ")[1], "strict"))
            Nid = Nid[:-1][1:].replace("'", '"').replace('}, {', '}}, {{').split("}, {")
            Lid = Lid[:-1][1:].replace("'", '"').replace('}, {', '}}, {{').split("}, {")

            if type(Nid) == list: 
                for item in Nid:  NpId.append(json.loads(item)["id"])
            if type(Lid) == list:
                for item in Lid:  LpId.append(json.loads(item)["id"])

            if type(NpId):
                for i in NpId:
                    if type(LpId):
                        for y in LpId:
                            if i == y: id = i
                    else:
                        if i == Lid: id = i
            else:
                if Nid == Lid: id = i
                
            customer = logic.get_customer("id", id, "strict")
            dato = str(customer)[:-1][1:].replace("'",'"')
            datojs = json.loads(dato)
            
            self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.customer_frame, width=420, command=label_button_frame_event, corner_radius=10)
            self.scrollable_label_button_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
            for a in dato.split(","):
                if dato.split(",").index(a) < len(dato.split(","))-1:
                    self.scrollable_label_button_frame.add_item(a.split(":")[0][:-1][1:].replace('"',"").capitalize()+" : "+str(datojs[a.split(":")[0][:-1][1:]
                            .replace('"',"")]).replace("', '","  ,  ").replace("['","").replace("']",""))
                elif ":" in a:
                    self.scrollable_label_button_frame.add_item(a.split(":")[0][:-1][1:].replace('"',"").capitalize()+" : "+str(datojs[a.split(":")[0][:-1][1:]
                            .replace('"',"")]).replace("', '","  ,  ").replace("['","").replace("']",""))
        
        # create scrollable radiobutton frame
        with open("data/customer.json", "r") as dF: data = dF.read(); dF.close(); data = data[:-1][1:].replace("},","}},").split("},")
        scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self.customer_frame, width=500, command=radiobutton_frame_event,
                item_list=[f'{json.loads(i)["name"]} {json.loads(i)["lastname"]}' for i in data],
                label_text="Lista de Clientes", corner_radius=10)
        scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")
        scrollable_radiobutton_frame.configure(width=292)

        # create footer-menu
        menu_frame = customtkinter.CTkFrame(self.customer_frame, corner_radius=10)
        menu_frame.grid(row=1, column=1, padx=15, pady=5)

        menu_frame_button_1 = customtkinter.CTkButton(menu_frame, text="Eliminar", image=remove_icon_image, compound="left", command=remove_customer)
        menu_frame_button_1.grid(row=2, column=0, padx=10, pady=10)

        menu_frame_button_2 = customtkinter.CTkButton(menu_frame, text="Añadir", image=add_icon_image, compound="left", command=add_customer)
        menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        menu_frame_button_3 = customtkinter.CTkButton(menu_frame, text="Actualizar", image=refresh_icon_image, compound="left", command=refresh)
        menu_frame_button_3.grid(row=3, column=1, padx=10, pady=10)

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