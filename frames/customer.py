import logic
from PIL import Image
import customtkinter
import json
import os

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

class App(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")

        self.remove_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/remove.png")),
                dark_image=Image.open(os.path.join(image_path, "light/remove.png")), size=(20, 20))
        self.add_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/add.png")),
                dark_image=Image.open(os.path.join(image_path, "light/add.png")), size=(20, 20))
        self.refresh_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/refresh.png")),
                dark_image=Image.open(os.path.join(image_path, "light/refresh.png")), size=(20, 20))
        self.back_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/back.png")),
                dark_image=Image.open(os.path.join(image_path, "light/back.png")), size=(20, 20))
        
        # create scrollable radiobutton frame
        with open("data/customer.json", "r") as dF: data = dF.read(); dF.close(); data = data[:-1][1:].replace("},","}},").split("},")
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                item_list=[f'{json.loads(i)["name"]} {json.loads(i)["lastname"]}' for i in data],
                label_text="Lista de Clientes", corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=292)

        # create footer-menu
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=1, padx=15, pady=5)

        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Eliminar", image=self.remove_icon_image, compound="left", command=self.remove_customer)
        self.menu_frame_button_1.grid(row=2, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_customer)
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", command=self.refresh)
        self.menu_frame_button_3.grid(row=3, column=1, padx=10, pady=10)

        self.menu_frame_button_4 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound="left", command=self.back)
        self.menu_frame_button_4.grid(row=3, column=0, padx=10, pady=10)

    def close_app(self):
        self.destroy()

    def remove_customer(self):
        self.scrollable_label_button_frame.destroy()
        NpId = []
        LpId = []
        Nid = str(logic.get_customer("name", self.scrollable_radiobutton_frame.get_checked_item().split(" ")[0], "strict"))
        Lid = str(logic.get_customer("lastname", self.scrollable_radiobutton_frame.get_checked_item().split(" ")[1], "strict"))
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
        logic.remove_data("customer.json", id, "id")
        self.refresh()

    def add_customer(self):
        self.add_customer_frame = AddCustomerFrame(master=self, width=420, corner_radius=10)
        self.add_customer_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")

    def refresh(self):
        self.scrollable_radiobutton_frame.destroy()
        with open("data/customer.json", "r") as dF: data = dF.read(); dF.close(); data = data[:-1][1:].replace("},","}},").split("},")
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                item_list=[f'{json.loads(i)["name"]} {json.loads(i)["lastname"]}' for i in data],
                label_text="Lista de Clientes", corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=292)
    
    def back():
        print("")

    def label_button_frame_event(self, item):
        print(item)
    def radiobutton_frame_event(self):
        NpId = []
        LpId = []
        Nid = str(logic.get_customer("name", self.scrollable_radiobutton_frame.get_checked_item().split(" ")[0], "strict"))
        Lid = str(logic.get_customer("lastname", self.scrollable_radiobutton_frame.get_checked_item().split(" ")[1], "strict"))
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
        
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=420, command=self.label_button_frame_event, corner_radius=10)
        self.scrollable_label_button_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
        for a in dato.split(","):
            if dato.split(",").index(a) < len(dato.split(","))-1:
                self.scrollable_label_button_frame.add_item(a.split(":")[0][:-1][1:].replace('"',"").capitalize()+" : "+str(datojs[a.split(":")[0][:-1][1:]
                        .replace('"',"")]).replace("', '","  ,  ").replace("['","").replace("']",""))
            elif ":" in a:
                self.scrollable_label_button_frame.add_item(a.split(":")[0][:-1][1:].replace('"',"").capitalize()+" : "+str(datojs[a.split(":")[0][:-1][1:]
                        .replace('"',"")]).replace("', '","  ,  ").replace("['","").replace("']",""))