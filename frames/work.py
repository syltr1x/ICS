import logic
from PIL import Image
import customtkinter
import json
import time
import os
import tkinter

class AddCustomerFrame(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)

        def get_data(request):
            if request == "customer":
                clientes = ["Clientes"]
                with open("data/customer.json", "r") as dF: dataC = dF.read(); dF.close()
                dataC = dataC[:-1][1:].replace("},","}},").split("},")
                for i in dataC:
                    item = json.loads(i)
                    clientes.append(str(item["lastname"]+" "+item["name"]))
                return clientes
            elif request == "technician":
                mecanicos = ["Tecnicos"]
                with open("data/mecanicos.txt", "r") as dF: dataM = dF.read(); dF.close()
                for i in dataM.split(','):  mecanicos.append(i)
                return mecanicos
            elif request == "concept":
                return ["Concepto", "Reparacion", "Service", "Mantenimiento", "Revision", "Garantia"]
            
        def auto_date(field):
            if field == "in":
                self.in_entry.delete(0, len(self.in_entry.get()))
                if self.in_entry_check.get() == 1:
                    data = str(time.localtime()).split(',')
                    year = data[0][-4:].replace("=","")
                    month = data[1][-2:].replace("=","")
                    day = data[2][-2:].replace("=","")
                    hour = data[3][-2:].replace("=","")+":"+data[4][-2:].replace("=","")+":"+data[5][-2:].replace("=","")

                    datetime = day+"/"+month+"/"+year+" , "+hour
                    self.in_entry.insert(0, datetime)
                    self.in_entry
                else:
                    self.in_entry.destroy()
                    self.in_entry = customtkinter.CTkEntry(self, placeholder_text="dd/mm/aaaa,hh:mm:ss", width=150)
                    self.in_entry.grid(row=2, column=1, padx=(10, 20), pady=(20, 20))
            elif field == "out":
                self.out_entry.delete(0, len(self.out_entry.get()))
                if self.out_entry_check.get() == 1:
                    data = str(time.localtime()).split(',')
                    year = data[0][-4:].replace("=","")
                    month = data[1][-2:].replace("=","")
                    day = data[2][-2:].replace("=","")
                    hour = data[3][-2:].replace("=","")+":"+data[4][-2:].replace("=","")+":"+data[5][-2:].replace("=","")

                    datetime = day+"/"+month+"/"+year+" , "+hour
                    self.out_entry.insert(0, datetime)
                    self.out_entry
                else:
                    self.out_entry.destroy()
                    self.out_entry = customtkinter.CTkEntry(self, placeholder_text="dd/mm/aaaa,hh:mm:ss", width=150)
                    self.out_entry.grid(row=3, column=1, padx=(10, 20), pady=(20, 20))
                
        def check_status(value):
            clientes = get_data("customer")
            mecanicos = get_data("technician")
            concepts = get_data("concept")

            if value != "Clientes" and value != "Tecnicos" and value != "Concepto":
                if value in clientes:
                    clientes = [value]
                    with open("data/customer.json", "r") as dF: dataC = dF.read()[:-1][1:].replace("},","}},").split("},"); dF.close()
                    for i in dataC:
                        item = json.loads(i)
                        if item["lastname"] != value.split(" ")[0] or item["name"] != value.split(" ")[1]: 
                            clientes.append(str(item["lastname"]+" "+item["name"]))
                    self.customer_entry = customtkinter.CTkOptionMenu(self, values=[i for i in clientes], button_hover_color="gray10", corner_radius=5, fg_color="gray50", command=check_status)
                    self.customer_entry.grid(row=1, column=0, padx=(10, 10), pady=(20, 20))

                elif value in mecanicos:
                    mecanicos = [value]
                    with open("data/mecanicos.txt", "r") as dF: dataM = dF.read().split(","); dF.close()
                    for i in dataM:
                        if i != value: mecanicos.append(i)
                    self.technician_entry = customtkinter.CTkOptionMenu(self, values=[i for i in mecanicos], button_hover_color="gray10", corner_radius=5, fg_color="gray50", command=check_status)
                    self.technician_entry.grid(row=1, column=1, padx=(10, 20), pady=(20, 20))

                elif value in concepts:
                    concepts.remove("Concepto")
                    concepts.remove(value)
                    concepts.insert(0, value)
                    self.concepto_entry = customtkinter.CTkOptionMenu(self, values=[i for i in concepts], button_hover_color="gray10", corner_radius=5, fg_color="gray50", command=check_status)
                    self.concepto_entry.grid(row=3, column=0, padx=(10, 10), pady=(20, 20))
            else:
                if value == "Clientes":
                    self.customer_entry = customtkinter.CTkOptionMenu(self, values=[i for i in clientes], button_hover_color="gray10", corner_radius=5, fg_color="indian red", command=check_status)
                    self.customer_entry.grid(row=1, column=0, padx=(10, 10), pady=(20, 20))
                
                elif value == "Tecnicos":
                    self.technician_entry = customtkinter.CTkOptionMenu(self, values=[i for i in mecanicos], button_hover_color="gray10", corner_radius=5, fg_color="indian red", command=check_status)
                    self.technician_entry.grid(row=1, column=1, padx=(10, 20), pady=(20, 20))
                
                elif value == "Concepto":
                    self.concepto_entry = customtkinter.CTkOptionMenu(self, values=[i for i in concepts], button_hover_color="gray10", corner_radius=5, fg_color="indian red", command=check_status)
                    self.concepto_entry.grid(row=3, column=0, padx=(10, 10), pady=(20, 20))

        def searcher(field, filter):
            if field == "customer":
                clientes = []
                customer = get_data("customer")
                customer.remove("Clientes")
                for i in customer:
                    if filter.lower() in i.split(" ")[0].lower() or filter.lower() in i.split(" ")[1].lower(): clientes.append(i)
                if len(clientes) >= 1:
                    self.customer_filter.delete(0, len(self.customer_filter.get())); self.customer_filter.insert(0, f"{len(clientes)} Resultados")
                    self.customer_entry.destroy()
                    self.customer_entry = customtkinter.CTkOptionMenu(self, values=[i for i in clientes], button_hover_color="gray10", corner_radius=5, fg_color="gray50", command=check_status)
                    self.customer_entry.grid(row=1, column=0, padx=(10, 10), pady=(20, 20))

                else: 
                    self.customer_entry.destroy()
                    self.customer_entry = customtkinter.CTkOptionMenu(self, values=["No Resultados"], button_hover_color="gray10", corner_radius=5, fg_color="gray50", command=check_status)
                    self.customer_entry.grid(row=1, column=0, padx=(10, 10), pady=(20, 20))

        clientes = get_data("customer")
        mecanicos = get_data("technician")
        concepts = get_data("concept")
        
        self.customer_filter = customtkinter.CTkEntry(self, placeholder_text="Buscar cliente")
        self.customer_filter.grid(row=0, column=0, padx=(0, 5), pady=(5, 5))

        self.customer_filter_btn = customtkinter.CTkButton(self, text="Filtrar", width=10, command=lambda:(searcher("customer", self.customer_filter.get())))
        self.customer_filter_btn.grid(row=0, column=0, padx=(90, 0), pady=(5, 5))

        self.customer_entry = customtkinter.CTkOptionMenu(self, values=[i for i in clientes], button_hover_color="gray10", corner_radius=5, fg_color="gray50", command=check_status)
        self.customer_entry.grid(row=1, column=0, padx=(10, 10), pady=(20, 20))

        self.lcplate_entry = customtkinter.CTkEntry(self, placeholder_text="Dominio")
        self.lcplate_entry.grid(row=2, column=0, padx=(10, 10), pady=(20, 20))

        self.concepto_entry = customtkinter.CTkOptionMenu(self, values=[i for i in concepts], button_hover_color="gray10", corner_radius=5, fg_color="gray50", command=check_status)
        self.concepto_entry.grid(row=3, column=0, padx=(10, 10), pady=(20, 20))

        self.technician_entry = customtkinter.CTkOptionMenu(self, values=[i for i in mecanicos], button_hover_color="gray10", corner_radius=5, fg_color="gray50", command=check_status)
        self.technician_entry.grid(row=1, column=1, padx=(10, 20), pady=(20, 20))

        self.in_entry = customtkinter.CTkEntry(self, placeholder_text="dd/mm/aaaa,hh:mm:ss", width=150)
        self.in_entry.grid(row=2, column=1, padx=(10, 20), pady=(20, 20))

        self.in_entry_check = customtkinter.CTkCheckBox(self, command=lambda:(auto_date("in")), text="Ingreso Automatico")
        self.in_entry_check.grid(row=2, column=2, padx=(5, 10), pady=(5, 5))

        self.out_entry = customtkinter.CTkEntry(self, placeholder_text="dd/mm/aaaa,hh:mm:ss", width=150)
        self.out_entry.grid(row=3, column=1, padx=(10, 20), pady=(20, 20))

        self.out_entry_check = customtkinter.CTkCheckBox(self, command=lambda:(auto_date("out")), text="Salida Automatico")
        self.out_entry_check.grid(row=3, column=2, padx=(5, 10), pady=(5, 5))

        self.add_customer_button = customtkinter.CTkButton(self, text="Crear orden", command=lambda:(add_customer(self.customer_entry.get().capitalize(), self.lcplate_entry.get().capitalize(), self.concepto_entry.get()
                )))
        self.add_customer_button.grid(row=4, column=0, padx=(100, 100), pady=(20,20), sticky="nsew")

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
                label_text="Lista de Trabajos", corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=292)

        # create footer-menu
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=1, padx=15, pady=5)

        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Eliminar", image=self.remove_icon_image, compound="left", command=self.remove_customer,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_1.grid(row=2, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_customer,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", command=self.refresh,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_3.grid(row=3, column=1, padx=10, pady=10)

        self.menu_frame_button_4 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound="left", command=self.back,
                text_color=("gray10", "gray90"))
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