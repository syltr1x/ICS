import logic
from PIL import Image
import customtkinter
import json
import time
import os

class AddProductFrame(customtkinter.CTkFrame):
    def __init__(self, master, comm=None, **kwargs):
        super().__init__(master, **kwargs)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")
        self.loupe_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/loupe.png")),
                dark_image=Image.open(os.path.join(image_path, "light/loupe.png")), size=(20, 20))
        def get_data(request):
            if request == "customer":
                clientes = []
                with open("data/customer.json", "r", encoding='utf-8') as dF: dataC = dF.read(); dF.close()
                dataC = dataC[:-1][1:].replace("},","}},").split("},")
                if dataC != [] and dataC != [""] and len(dataC) >= 1:
                    for i in dataC:
                        item = json.loads(i)
                        clientes.append(str(item["lastname"]+" "+item["name"]))
                return clientes
            elif request == "account":
                cuentas = []
                with open("data/account.json", "r", encoding='utf-8') as dF: dataC = dF.read(); dF.close()
                dataC = dataC[:-1][1:].replace("},","}},").split("},")
                if dataC != [] and dataC != [""] and len(dataC) >= 1:
                    for i in dataC:
                        item = json.loads(i)
                        cuentas.append(str(item["name"]))
                return cuentas
            elif request == "makers":
                makers = []
                with open("data/vehicles.json", "r", encoding='utf-8') as dF: dataC = dF.read(); dF.close()
                if len(dataC) > 5:
                    dataC = dataC[:-1][1:].replace("\n","").split("]")
                    for i in dataC:
                        if len(i) >= 2:
                            makers.append(i.split('"')[1].capitalize())
                return makers
            
        def searcher(data):
            clientes = get_data("customer")
            cuentas = get_data("account")
            dato = []
            for i in clientes:
                if data.lower() in i.split(" ")[0].lower() or data.lower() in i.split(" ")[1].lower(): dato.append(i)
            for y in cuentas:
                if data.lower() in y.lower(): dato.append(i)
            self.customer_entry.destroy()
            self.customer_entry = customtkinter.CTkComboBox(self, values=[i for i in dato], button_hover_color="gray10", corner_radius=5, fg_color="gray50", width=120)
            self.customer_entry.grid(row=0, column=0, padx=(0, 5), pady=(15, 5))
            self.customer_entry.set(f'Resultados : {len(dato)}')

        self.customer_filter_btn = customtkinter.CTkButton(self, image=self.loupe_icon_image, text="", width=1, command=lambda:(searcher(self.customer_entry.get())))
        self.customer_filter_btn.grid(row=0, column=0, padx=(165, 10), pady=(15, 5))
        
        clientes = get_data("customer")
        cuentas = get_data("account")
        makers = get_data("makers")
        
        dato = ["--Clientes--"]+[i for i in clientes]
        dato = dato+["--Cuentas--"]+[i for i in cuentas]
        
        self.customer_entry = customtkinter.CTkComboBox(self, values=[i for i in dato], width=120)
        self.customer_entry.grid(row=0, column=0, padx=(0, 5), pady=(15, 5))
        self.customer_entry.set('Clientes')

        self.lcplate_entry = customtkinter.CTkEntry(self, placeholder_text="Dominio", width=120)
        self.lcplate_entry.grid(row=0, column=1, padx=(5, 15), pady=(15, 5))

        self.maker_entry = customtkinter.CTkComboBox(self, values=makers, width=120, command=self.set_maker)
        self.maker_entry.set("Fabricante")
        self.maker_entry.grid(row=1, column=0, padx=(0, 5), pady=(5, 5))

        self.model_entry = customtkinter.CTkComboBox(self, values=[], width=120, state='disabled')
        self.model_entry.set("Modelo")
        self.model_entry.grid(row=1, column=1, padx=(5, 15), pady=(5, 5))
    
        self.color_entry = customtkinter.CTkEntry(self, placeholder_text="Color", width=120)
        self.color_entry.grid(row=2, column=0, padx=(0, 5), pady=(5, 5))

        self.type_entry = customtkinter.CTkEntry(self, placeholder_text="Tipo", width=120)
        self.type_entry.grid(row=2, column=1, padx=(5, 15), pady=(5, 5))

        self.year_entry = customtkinter.CTkEntry(self, placeholder_text="Año", width=120)
        self.year_entry.grid(row=3, column=0, padx=(0, 5), pady=(5, 5))

        self.add_customer_button = customtkinter.CTkButton(self, text="Añadir Vehiculo", command=lambda:(add_car(self.customer_entry.get(), self.lcplate_entry.get()
                ,self.color_entry.get(), self.maker_entry.get(), self.model_entry.get(), self.type_entry.get(), self.year_entry.get())), width=110)
        self.add_customer_button.grid(row=3, column=1, padx=(5, 15), pady=(5, 5), sticky="nsew")

        def add_car(customer, lcplate, color, maker, model, tipo, year):
            self.destroy()
            logic.write_cars("", '{"customer":"'+customer+'", "lcplate":"'+lcplate+'", "color":"'+color+'", "make":"'+maker+'", "model":"'+model+'", "type":"'+tipo+'", "year":"'+year+'"}')
            comm()
    def set_maker(self, maker):
        with open("data/vehicles.json", "r", encoding='utf-8') as dF: dataC = dF.read(); dF.close()
        data = json.loads(dataC)
        models = data[maker.lower()]
        self.model_entry.configure(values=models)
        self.model_entry.configure(state='normal')

class DataFrame(customtkinter.CTkFrame):
    def __init__(self, master, dato, command=None, **kwargs):
        super().__init__(master, **kwargs)
        data = str(logic.get_cars("lcplate", dato.split(' - ')[0], "strict"))
        data = json.loads(data[:-1][1:].replace("'", '"'))

        self.lclpate_title = customtkinter.CTkLabel(self, text="Dominio", fg_color='gray30', corner_radius=5, width=70)
        self.lclpate_title.grid(row=0, column=0, padx=(30, 10), pady=(15, 5))

        self.lcplate_label = customtkinter.CTkLabel(self, text=data["lcplate"])
        self.lcplate_label.grid(row=0, column=1, padx=(10, 30), pady=(15, 5))

        self.color_title = customtkinter.CTkLabel(self, text="Color", fg_color='gray30', corner_radius=5, width=70)
        self.color_title.grid(row=1, column=0, padx=(30, 10), pady=(15, 5))

        self.color_label = customtkinter.CTkLabel(self, text=data["color"])
        self.color_label.grid(row=1, column=1, padx=(10, 30), pady=(15, 5))
                
        self.make_title = customtkinter.CTkLabel(self, text="Fabricante", fg_color='gray30', corner_radius=5, width=70)
        self.make_title.grid(row=2, column=0, padx=(30, 10), pady=(15, 5))
        
        self.make_label = customtkinter.CTkLabel(self, text=data["make"])
        self.make_label.grid(row=2, column=1, padx=(10, 30), pady=(15, 5))

        self.model_title = customtkinter.CTkLabel(self, text="Modelo", fg_color='gray30', corner_radius=5, width=70)
        self.model_title.grid(row=3, column=0, padx=(30, 10), pady=(15, 5))

        self.model_label = customtkinter.CTkLabel(self, text=data["model"])
        self.model_label.grid(row=3, column=1, padx=(10, 30), pady=(15, 5))

        self.type_title = customtkinter.CTkLabel(self, text="Tipo", fg_color='gray30', corner_radius=5, width=70)
        self.type_title.grid(row=4, column=0, padx=(30, 10), pady=(15, 5))        
        
        self.type_label = customtkinter.CTkLabel(self, text=data["type"])
        self.type_label.grid(row=4, column=1, padx=(10, 30), pady=(15, 5))
        
        self.year_title = customtkinter.CTkLabel(self, text="Año", fg_color='gray30', corner_radius=5, width=70)
        self.year_title.grid(row=5, column=0, padx=(30, 10), pady=(15, 5))
        
        self.year_label = customtkinter.CTkLabel(self, text=data["year"])
        self.year_label.grid(row=5, column=1, padx=(10, 30), pady=(15, 5))

class ModFrame(customtkinter.CTkFrame):
    def __init__(self, master, dato, command=None, **kwargs):
        super().__init__(master, **kwargs)
        data = str(logic.get_cars("lcplate", dato.split(' - ')[0], "strict"))
        data = json.loads(data[:-1][1:].replace("'", '"'))        

        self.lcplate_entry = customtkinter.CTkEntry(self, placeholder_text=data["lcplate"])
        self.lcplate_entry.grid(row=0, column=0, padx=30, pady=(15, 5))
        
        self.color_entry = customtkinter.CTkEntry(self, placeholder_text=data["color"])
        self.color_entry.grid(row=1, column=0, padx=30, pady=(15, 5))
                
        self.make_entry = customtkinter.CTkEntry(self, placeholder_text=data["make"])
        self.make_entry.grid(row=2, column=0, padx=30, pady=(15, 5))

        self.model_entry = customtkinter.CTkEntry(self, placeholder_text=data["model"])
        self.model_entry.grid(row=3, column=0, padx=30, pady=(15, 5))

        self.type_entry = customtkinter.CTkEntry(self, placeholder_text=data["type"])
        self.type_entry.grid(row=4, column=0, padx=30, pady=(15, 5))

        self.year_entry = customtkinter.CTkEntry(self, placeholder_text=data["year"])
        self.year_entry.grid(row=5, column=0, padx=30, pady=(15, 5))

        self.car_button = customtkinter.CTkButton(self, text="Modificar Vehiculo", command=lambda:(mod_car(self.lcplate_entry.get()
        ,self.color_entry.get(), self.make_entry.get(), self.model_entry.get(), self.type_entry.get(), self.year_entry.get())))

        self.car_button.grid(row=6, column=0, padx=30, pady=(20, 5))
        def mod_car(lcplate, color, make, model, tipo, year):
            cambios = []

            if lcplate != "":
                cambios.append('{"field":"lcplate", "value":"'+lcplate+'"}')
            if color != "":
                cambios.append('{"field":"color", "value":"'+color+'"}')
            if make != "":
                cambios.append('{"field":"make", "value":"'+make+'"}')
            if model != "":
                cambios.append('{"field":"model", "value":"'+model+'"}')
            if tipo != "":
                cambios.append('{"field":"type", "value":"'+tipo+'"}')
            if year != "":
                cambios.append('{"field":"year", "value":"'+year+'"}')

            for c in cambios:
                ic = json.loads(c)
                logic.mod_data(data["lcplate"], "lcplate", ic["field"], ic["value"], "car.json")
            self.destroy()

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
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(5, 5), sticky="nw")
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
        self.scrollable_radiobutton_frame = None
        self.mod_item_frame = None
        self.mod_frame = None
        super().__init__(master, **kwargs)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")

        self.clock_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/trash.png")),
                dark_image=Image.open(os.path.join(image_path, "light/trash.png")), size=(20, 20))
        self.x_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/x.png")),
                dark_image=Image.open(os.path.join(image_path, "light/x.png")), size=(20, 20))
        self.add_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/add.png")),
                dark_image=Image.open(os.path.join(image_path, "light/add.png")), size=(20, 20))
        self.mod_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/pencil.png")),
                dark_image=Image.open(os.path.join(image_path, "light/pencil.png")), size=(20, 20))
        self.refresh_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/refresh.png")),
                dark_image=Image.open(os.path.join(image_path, "light/refresh.png")), size=(20, 20))
        self.back_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/back.png")),
                dark_image=Image.open(os.path.join(image_path, "light/back.png")), size=(20, 20))
        
        # create scrollable radiobutton frame
        with open("data/car.json", "r") as dF: data = dF.read(); dF.close(); data = data[:-1][1:].replace("},","}},").split("},")
        if data != ['']:
            self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                    item_list=[f'{json.loads(i)["lcplate"]} - {json.loads(i)["model"]}' for i in data],                                                                       
                    label_text="Lista de Autos", corner_radius=10)
        else:
            self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                item_list=[], label_text="Lista de Autos", corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=292)

        # create footer-menu
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=1, padx=15, pady=5)

        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Eliminar", image=self.clock_icon_image, compound="left", command=self.remove_car,
                text_color=("gray10", "gray90"), state='disabled')
        self.menu_frame_button_1.grid(row=2, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_car,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", command=self.refresh,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_3.grid(row=3, column=1, padx=10, pady=10)

        self.menu_frame_button_4 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound="left", command=self.back,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_4.grid(row=3, column=0, padx=10, pady=10)

    def remove_car(self):
        open("data/temp/car.json", "w").write(open("data/car.json", "r").read()) # Temp Save
        lcplate = str(self.scrollable_radiobutton_frame.get_checked_item()).split(' - ')[0]
        logic.remove_data("car.json", lcplate, "lcpate")
        self.refresh()

    def add_car(self):
        self.refresh()
        def cancel():
            self.add_item_frame.destroy()
            self.menu_frame_button_2.destroy()
            self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_car,
                    text_color=("gray10", "gray90"))
            self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
            
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Cancelar", image=self.x_icon_image, compound="left", command=cancel, 
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.add_item_frame = AddProductFrame(master=self, width=420, corner_radius=10, comm=self.refresh)
        self.add_item_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")
    
    def mod_car(self):
        dato = self.scrollable_radiobutton_frame.get_checked_item()
        self.refresh()
        def cancel():
            self.mod_item_frame.destroy()
            self.menu_frame_button_2.destroy()
            self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_car,
                    text_color=("gray10", "gray90"))
            self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
        
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Cancelar", image=self.x_icon_image, compound="left", command=cancel, 
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.mod_item_frame = ModFrame(master=self, width=420, corner_radius=10, dato=dato)
        self.mod_frame.destroy()
        self.mod_item_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")

    def refresh(self):
        self.menu_frame_button_1.configure(state='disabled')
        if self.scrollable_radiobutton_frame != None : self.scrollable_radiobutton_frame.destroy()
        if self.mod_item_frame != None: self.mod_item_frame.destroy()
        if self.mod_frame != None: self.mod_frame.destroy()
        with open("data/car.json", "r") as dF: data = dF.read(); dF.close(); data = data[:-1][1:].replace("},","}},").split("},")
        if data != ['']:
            self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                    item_list=[f'{json.loads(i)["lcplate"]} - {json.loads(i)["model"]}' for i in data],                                                                       
                    label_text="Lista de Autos", corner_radius=10)
        else:
            self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                item_list=[], label_text="Lista de Autos", corner_radius=10)
        self.scrollable_radiobutton_frame.configure(width=292)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_car,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
    
    def back(self):
        file = str(os.listdir('data/temp/'))[:-2][2:]
        open(f'data/{file}', "w").write(open(f'data/temp/{file}', "r").read())
        os.remove(f'data/temp/{file}')
        self.refresh()

    def radiobutton_frame_event(self):
        self.menu_frame_button_1.configure(state='normal')
        if self.mod_item_frame != None: self.mod_item_frame.destroy()
        if self.mod_frame != None: self.mod_frame.destroy()
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Modificar", image=self.mod_icon_image, compound="left", command=self.mod_car,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
        self.mod_frame = DataFrame(self, width=420, dato=self.scrollable_radiobutton_frame.get_checked_item())
        self.mod_frame.grid(row=0, column=2, padx=30, pady=10, sticky="nsew")