from PIL import Image
import customtkinter
import logic
import json
import time
import os

class SelectAccountTypeFrame(customtkinter.CTkFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        
        self.label_frame = customtkinter.CTkFrame(self, fg_color="gray30", width=70, height=30, corner_radius=5)
        self.label_frame.grid(row=0, column=0, pady=(15, 20), padx=20, sticky="ns")

        self.label = customtkinter.CTkLabel(self.label_frame, text="Tipos de cuentas")
        self.label.grid(row=0, column=0, pady=5, padx=10)
        
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list)+1, column=0, padx=10, pady=5, sticky="nw")
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()

class AccountsListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master,  filename, command, **kwargs):
        super().__init__(master, **kwargs)        
        file = open(f"data/{filename}", "r", encoding='utf-8').read()[:-1][1:].replace("'", '"').replace("},","}},").split("},")

        self.command = command
        self.button_variable = customtkinter.StringVar()
        self.button_list = []
        self.label_frame = customtkinter.CTkFrame(self, fg_color="gray30", width=70, height=30, corner_radius=5)
        self.label_frame.grid(row=0, column=0, pady=(15, 20), padx=30, sticky="nse")

        if filename == "customer.json":
                self.label = customtkinter.CTkLabel(self.label_frame, text="Lista de clientes")
        elif filename == "account.json":
                self.label = customtkinter.CTkLabel(self.label_frame, text="Lista de cuentas")
        if file != ['']:
            for i in file:
                if filename == "customer.json":
                    self.add_item(f'{json.loads(i)["name"]} {json.loads(i)["lastname"]}', filename)
                elif filename == "account.json":
                    self.add_item(json.loads(i)["name"], filename)
        self.label.grid(row=0, column=0, pady=5, padx=10)


    def add_item(self, item, filename):
        accountbutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.button_variable)
        if self.command is not None:
            accountbutton.configure(command=lambda:(self.command(item, filename)))
        accountbutton.grid(row=len(self.button_list)+2, column=0, pady=(5, 5), padx=10, sticky='nw')
        self.button_list.append(accountbutton)

    def remove_item(self, item):
        for button in self.button_list:
            if item == button.cget("text"):
                button.destroy()
                self.button_list.remove(button)
                return

    def get_checked_item(self):
        return self.button_variable.get()
    

class AccountDataFrame(customtkinter.CTkFrame):
    def __init__(self, master, data, filename, **kwargs):
        super().__init__(master, **kwargs)

        if filename == "customer.json":
            NpId = []
            LpId = []
            Nid = logic.get_customer("name", data.split(" ")[0], "strict")
            Lid = logic.get_customer("lastname", data.split(" ")[1], "strict")

            if type(Nid) == list: 
                for item in Nid: NpId.append(item["id"])
            if type(Lid) == list:
                for item in Lid:  LpId.append(item["id"])

            if type(NpId):
                for i in NpId:
                    if type(LpId):
                        for y in LpId:
                            if i == y: id = i
                    else:
                        if i == Lid: id = i
            else:
                if Nid == Lid: id = i

            item = json.loads(str(logic.get_customer("id", id, "strict"))[:-1][1:].replace("'", '"'))
            self.name_data_label = customtkinter.CTkLabel(self, text=f'{item["name"]} {item["lastname"]}').grid(row=0, column=0, padx=10, pady=10)
            self.birthday_label = customtkinter.CTkLabel(self, text=item["birthday"]).grid(row=0, column=1, padx=10, pady=10)
        
        elif filename == "account.json":
            item = json.loads(str(logic.get_account("name", data, "strict"))[:-1][1:].replace("'", '"'))
            self.name_data_label = customtkinter.CTkLabel(self, text=item["name"]).grid(row=0, column=0, padx=10, pady=10)
            self.balance_label = customtkinter.CTkLabel(self, text="Balance : ", fg_color="gray30", corner_radius=5).grid(row=1, column=0, padx=10, pady=10)
            self.balance_data_label = customtkinter.CTkLabel(self, text=item["balance"]+" (A favor del cliente)" if int(item["balance"]) < 0 
                    else item["balance"]+" (A favor del taller)" if int(item["balance"]) != 0 else item["balance"]).grid(row=1, column=1, padx=10, pady=10)

        self.media_frame = customtkinter.CTkFrame(self)
        self.media_frame.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.media_title = customtkinter.CTkLabel(self.media_frame, text="Contactos del cliente" if filename == "customer.json" else "Contactos de la cuenta", fg_color=('gray60', 'gray30'), text_color=("gray1", "gray90"), corner_radius=5).grid(row=0, column=0, padx=1, pady=5, sticky='new')
        for k in range(0, len(item["contact"])):
            self.media_label = customtkinter.CTkLabel(self.media_frame, text=f'{item["contact"][k]["media"]} : {item["contact"][k]["value"]}')
            self.media_label.grid(row=k+1, column=0, padx=5, pady=2)
        
        self.cars_frame = customtkinter.CTkFrame(self)
        self.cars_label = customtkinter.CTkLabel(self.cars_frame, text="Vehículos", compound="center", fg_color=('gray60', 'gray30'), text_color=("gray1", "gray90"), corner_radius=5).grid(row=0, column=0, padx=5, pady=1, sticky='new')
        self.cars_frame.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        for x in range(0, len(item["cars"])):
            self.car_label = customtkinter.CTkLabel(self.cars_frame, text=item["cars"][x])
            self.car_label.grid(row=x+1, column=0, padx=5, pady=2)

class AddCustomerFrame(customtkinter.CTkFrame):
        def __init__(self, master, acType, comm=None, **kwargs):
            super().__init__(master, **kwargs)

            self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Nombre de la cuenta" if acType == "Corrientes" else "Nombre y Apellido", width=160)
            self.name_entry.grid(row=0, column=0, padx=(0, 5), pady=(15, 5))
            
            self.bday_entry = customtkinter.CTkEntry(self, placeholder_text="Cumpleaños: --/--/----", width=160)
            self.bday_entry.grid(row=0, column=1, padx=(5, 5), pady=(5, 5)) if acType != "Corrientes" else None

            def add_account(name, birthday="--/--/----"):
                contact=[]
                car=[]
                for a in contactos: 
                    contact.append(json.loads("{"+a+"}"))
                for b in cars: 
                    car.append(b)
                self.destroy()

                contact = [i for i in contact if i != ""]
                car = [i for i in car if i != ""]

                if acType == "Corrientes":
                    open("data/temp/account.json", "w", encoding="utf-8").write(open("data/account.json", "r", encoding="utf-8").read()) # Temp Save
                    logic.write_account("", '{"id":"'+logic.get_id("account.json")+'", "name":"'+name+'", "balance":"0", "contact":'+str(contact).replace("'", '"')+', "cars":'+str(cars).replace("'", '"')+'}')
                    comm('account.json')
                elif acType == "Particulares":
                    open("data/temp/customer.json", "w", encoding="utf-8").write(open("data/customer.json", "r", encoding="utf-8").read()) # Temp Save
                    name = name.split(" ")
                    logic.write_customer("", '{"id":"'+logic.get_id("customer.json")+'", "name":"'+name[0].capitalize()+
                            '", "lastname":"'+name[1].capitalize()+'", "birthday":"'+birthday+'", "contact":'+str(contact).replace("'", '"')+', "cars":'+str(cars).replace("'", '"')+'}')
                    comm('customer.json')
                self.destroy()

            self.contact_items_frame = customtkinter.CTkFrame(self, width=200, height=80)
            self.contact_items_frame.grid(row=1, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))
            self.contact_items_title = customtkinter.CTkLabel(self.contact_items_frame, text="Medios de contacto").grid(row=0, column=0, padx=(15,0), sticky="w")
            self.contact_item_add = customtkinter.CTkButton(self.contact_items_frame, text="Añadir medio", command=lambda:(add_contact_item())).grid(row=0, column=0, padx=(180,0), sticky='w')

            self.cars_items_frame = customtkinter.CTkFrame(self, width=200, height=80)
            self.cars_items_frame.grid(row=2, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))
            self.cars_items_title = customtkinter.CTkLabel(self.cars_items_frame, text="Vehículos").grid(row=0, column=0, padx=(15,0), sticky="w")
            self.cars_item_add = customtkinter.CTkButton(self.cars_items_frame, text="Añadir Vehículo", command=lambda:(add_car_item())).grid(row=0, column=0, padx=(180,0), sticky='w')

            self.add_customer_button = customtkinter.CTkButton(self, text="Añadir Cuenta" if acType == "Corrientes" else "Añadir Cliente", command=lambda:(add_account(self.name_entry.get()
                    ,self.bday_entry.get() if acType != "Corrientes" else "-")))
            self.add_customer_button.grid(row=3, column=0, padx=(100, 100), pady=(20,20), sticky="nsew")

            global contactos, cars
            contactos, cars = [], []
            def add_contact_item():
                pre_contact_add = NewContact(self.contact_items_frame)
                pre_contact_add.grid(row=len(contactos)+1, column=0, sticky="nsew")

            def add_car_item():
                pre_car_add = NewCar(self.cars_items_frame)
                pre_car_add.grid(row=len(cars)+1, column=0, sticky="nsew")

class NewContact(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pre_add_contact()

    def pre_add_contact(self):
        global item_menu
        global item_user
        global confirm_work
    
        self.item_menu = customtkinter.CTkEntry(self, placeholder_text="Medio de contacto")
        self.item_menu.grid(row=0, column=0)
        self.item_user = customtkinter.CTkEntry(self, placeholder_text="Usuario / N° Tel", width=120)
        self.item_user.grid(row=0, column=1)
        self.confirm_work = customtkinter.CTkButton(self, text="+", width=28, command=lambda:(self.add_contact(self.item_menu.get(), self.item_user.get())))
        self.confirm_work.grid(row=0, column=2)

    def add_contact(self, item, value):
        if item != "" and value != "":
            self.item_menu.destroy()
            self.item_user.destroy()
            self.confirm_work.destroy()

            item_label = customtkinter.CTkLabel(self, text=f'Medio : {item.capitalize()}', fg_color="gray30", corner_radius=5)
            item_label.grid(row=0, column=0, padx=15, pady=5)
            user_label = customtkinter.CTkLabel(self, text=f'Valor : {value}', fg_color="gray30", corner_radius=5)
            user_label.grid(row=0, column=1, padx=15, pady=5)
            contactos.append('"media":"'+item.capitalize()+'", "value":"'+value+'"')

class NewCar(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pre_add_work()

    def pre_add_car(self):
        global item_menu
        global confirm_work
    
        self.item_menu = customtkinter.CTkEntry(self, placeholder_text="Dominio")
        self.item_menu.grid(row=0, column=0)
        self.confirm_work = customtkinter.CTkButton(self, text="+", width=28, command=lambda:(self.add_car(self.item_menu.get())))
        self.confirm_work.grid(row=0, column=1)

    def add_car(self, item):
        if item != "":
            self.item_menu.destroy()
            self.confirm_work.destroy()

            item_label = customtkinter.CTkLabel(self, text=f'Dominio : {item}', fg_color="gray30", corner_radius=5)
            item_label.grid(row=0, column=0, padx=15, pady=5)
            cars.append(item)

class ModFrame(customtkinter.CTkFrame):
    def __init__(self, master, dato, acType, btn, command=None, **kwargs):
        super().__init__(master, **kwargs)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")
        self.mod_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/pencil.png")),
                dark_image=Image.open(os.path.join(image_path, "light/pencil.png")), size=(20, 20))
        
        data = str(logic.get_account("id", dato, "strict") if acType == "Corrientes" else logic.get_customer("id", dato, "strict"))
        data = json.loads(data[:-1][1:].replace("'", '"'))
        if acType == "Corrientes": data["birthday"] = "--/--/----"
        if acType == "Particulares": data["balance"] = "0"

        self.name_label = customtkinter.CTkLabel(self, text="Nombre de cuenta" if acType == "Corrientes" else "Nombre y apellido")
        self.name_label.grid(row=0, column=0, padx=(10, 0), pady=(15, 5), sticky="nw")
        self.name_entry = customtkinter.CTkEntry(self, placeholder_text=data["name"] if acType == "Corrientes" else data["name"]+" "+data["lastname"], width=160)
        self.name_entry.grid(row=0, column=1, padx=(0, 10), pady=(15, 5), sticky="w")

        self.bday_label = customtkinter.CTkLabel(self, text="Fecha de Nacimiento")
        self.bday_label.grid(row=1, column=0, padx=(10, 0), pady=(15, 5), sticky="nw") if acType != "Corrientes" else None
        self.bday_entry = customtkinter.CTkEntry(self, placeholder_text=data["birthday"], width=160)
        self.bday_entry.grid(row=1, column=1, padx=(0, 10), pady=(15, 5), sticky="w") if acType != "Corrientes" else None

        self.balance_label = customtkinter.CTkLabel(self, text="Balance")
        self.balance_label.grid(row=1, column=0, padx=(10, 0), pady=(15, 5), sticky="nw") if acType == "Corrientes" else None
        self.balance_entry = customtkinter.CTkEntry(self, placeholder_text=data["balance"], width=160)
        self.balance_entry.grid(row=1, column=1, padx=(0, 10), pady=(15, 5), sticky="w") if acType == "Corrientes" else None

        self.car_label = customtkinter.CTkLabel(self, text="Vehiculos")
        self.car_label.grid(row=2, column=0, padx=(10, 0), pady=(15, 5), sticky="nw")
        self.car_entry = customtkinter.CTkTextbox(self, height=60, width=160)
        for i in data["cars"]:
            if data["cars"].index(i) % 2 != 0: self.car_entry.insert("end", i+"\n")
            else: self.car_entry.insert("end", i+" | ")
        self.car_entry.grid(row=2, column=1, padx=(0, 10), pady=(15, 5), sticky="w")

        self.contact_label = customtkinter.CTkLabel(self, text="Contactos")
        self.contact_label.grid(row=3, column=0, padx=(10, 0), pady=(15, 5), sticky="nw")
        self.contact_entry = customtkinter.CTkTextbox(self, width=180)
        for i in data["contact"]:
            self.contact_entry.insert("end", f'{i["media"]}:{i["value"]}\n')
        self.contact_entry.grid(row=3, column=1, padx=(0, 10), pady=(15, 5), sticky="w")

        self.car_button = customtkinter.CTkButton(self, text="Modificar Cuenta", command=lambda:(mod_account(acType, self.name_entry.get()
        ,bday=self.bday_entry.get(), balance=self.balance_entry.get(), contact=self.contact_entry.get("1.0", "end"), cars=self.car_entry.get("1.0", "end"))))
        self.car_button.grid(row=4, column=0, padx=30, pady=(20, 5), columnspan=2)

        def mod_account(acType, name, contact, cars, bday="", balance=""):
            cambios = []

            if name != "":
                if acType == "Corrientes":
                    cambios.append('{"field":"name", "value":"'+name+'"}')
                else: 
                    cambios.append('{"field":"name", "value":"'+name.split(" ")[0]+'"}')
                    cambios.append('{"field":"lastname", "value":"'+name.split(" ")[1]+'"}')
            
            if balance != "":
                cambios.append('{"field":"balance", "value":"'+balance+'"}')
            if bday != "":
                cambios.append('{"field":"birthday", "value":"'+bday+'"}')
            if contact != "":
                contact = [i.strip() for i in contact.split('\n') if i != '']
                contacts = [{"media":i.split(':')[0], "value":i.split(":")[1]} for i in contact]
                cambios.append('{"field":"contact", "value":'+str(contacts).replace("'", '"')+'}')
            if cars != "":
                cars = [i.strip() for i in cars.split("|") if i != ""]
                cambios.append('{"field":"cars", "value":'+str(cars).replace('\n','').replace('\\n','').replace("'", '"')+'}')

            for c in cambios:
                ic = json.loads(c)
                logic.mod_data(data["id"], "id", ic["field"], ic["value"], "account.json" if acType == "Corrientes" else "customer.json")
            btn.configure(text="Modificar")
            btn.configure(image=self.mod_icon_image)
            btn.configure(command=command)
            self.destroy()
                
class App(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.account_frame = None
        self.account_list_frame = None
        self.mod_customer_frame = None
        self.fileT = None
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")

        self.remove_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/trash.png")),
                dark_image=Image.open(os.path.join(image_path, "light/trash.png")), size=(20, 20))
        self.x_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/x.png")),
                dark_image=Image.open(os.path.join(image_path, "light/x.png")), size=(20, 20))
        self.add_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/add.png")),
                dark_image=Image.open(os.path.join(image_path, "light/add.png")), size=(20, 20))
        self.refresh_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/refresh.png")),
                dark_image=Image.open(os.path.join(image_path, "light/refresh.png")), size=(20, 20))
        self.back_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/back.png")),
                dark_image=Image.open(os.path.join(image_path, "light/back.png")), size=(20, 20))
        self.mod_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/pencil.png")),
                dark_image=Image.open(os.path.join(image_path, "light/pencil.png")), size=(20, 20))
        self.car_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/car.png")),
                dark_image=Image.open(os.path.join(image_path, "light/car.png")), size=(20, 20))
        
        # create scrollable radiobutton frame
        self.scrollable_radiobutton_frame = SelectAccountTypeFrame(master=self, width=300, command=self.select_account_type,
                item_list=["Particulares", "Corrientes"], corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="ns")

    # footer-menu functions
    def remove_customer(self):
        data = self.account_list_frame.get_checked_item()
        if self.fileT == "customer.json":
            NpId = []
            LpId = []
            Nid = logic.get_customer("name", data.split(" ")[0], "strict")
            Lid = logic.get_customer("lastname", data.split(" ")[1], "strict")

            if type(Nid) == list: 
                for item in Nid:  NpId.append(item["id"])
            if type(Lid) == list:
                for item in Lid:  LpId.append(item["id"])

            if type(NpId):
                for i in NpId:
                    if type(LpId):
                        for y in LpId:
                            if i == y: id = i
                    else:
                        if i == Lid: id = i
            else:
                if Nid == Lid: id = i

        else: id = logic.get_account("name", data, "strict")[0]["id"]
        open(f"data/temp/{self.fileT}", "w", encoding='utf-8').write(open(f"data/{self.fileT}", "r", encoding='utf-8').read()) # Temp Save
        logic.remove_data(self.fileT, id, "id")
        self.refresh(self.fileT)
        self.account_frame.destroy()

    def add_customer(self):
        self.refresh(self.fileT)
        def cancel():
            self.add_customer_frame.destroy()
            self.menu_frame_button_2.destroy()
            self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_customer,
                    text_color=("gray10", "gray90"))
            self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Cancelar", image=self.x_icon_image, compound="left", command=cancel, 
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.add_customer_frame = AddCustomerFrame(master=self, width=500, corner_radius=10, acType=self.scrollable_radiobutton_frame.get_checked_item(), comm=self.refresh)
        self.add_customer_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")

    def mod_customer(self):
        def cancel():
            self.mod_customer_frame.destroy()
            self.menu_frame_button_3.configure(text="Modificar")
            self.menu_frame_button_3.configure(state="disabled")
            self.menu_frame_button_3.configure(image=self.mod_icon_image)
            self.menu_frame_button_3.configure(command=self.mod_customer)

        data = self.account_list_frame.get_checked_item()
        self.refresh(self.fileT)
        if self.fileT == "customer.json":
            NpId = []
            LpId = []
            Nid = logic.get_customer("name", data.split(" ")[0], "strict")
            Lid = logic.get_customer("lastname", data.split(" ")[1], "strict")

            if type(Nid) == list: 
                for item in Nid: NpId.append(item["id"])
            if type(Lid) == list:
                for item in Lid:  LpId.append(item["id"])

            if type(NpId):
                for i in NpId:
                    if type(LpId):
                        for y in LpId:
                            if i == y: id = i
                    else:
                        if i == Lid: id = i
            else:
                if Nid == Lid: id = i
        else: id = logic.get_account("name", data, "strict")[0]["id"]
        self.mod_customer_frame = ModFrame(master=self, dato=id, width=500, corner_radius=10, acType=self.scrollable_radiobutton_frame.get_checked_item(), btn=self.menu_frame_button_3, command=self.mod_customer)
        self.mod_customer_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew", rowspan=3)
        # Button Refresh
        self.menu_frame_button_3.configure(text="Cancelar")
        self.menu_frame_button_3.configure(state="normal")
        self.menu_frame_button_3.configure(image=self.x_icon_image)
        self.menu_frame_button_3.configure(command=cancel)
        
    
    def add_car(self):
        self.menu_frame_button_1.configure(state='disabled')
        self.menu_frame_button_3.configure(state='disabled')
        dato = self.account_list_frame.get_checked_item()
        if self.fileT == "customer.json":
            NpId = []
            LpId = []
            Nid = logic.get_customer("name", dato.split(" ")[0], "strict")
            Lid = logic.get_customer("lastname", dato.split(" ")[1], "strict")

            if type(Nid) == list: 
                for item in Nid: NpId.append(item["id"])
            if type(Lid) == list:
                for item in Lid:  LpId.append(item["id"])

            if type(NpId):
                for i in NpId:
                    if type(LpId):
                        for y in LpId:
                            if i == y: id = i
                    else:
                        if i == Lid: id = i
            else:
                if Nid == Lid: id = i
        else: id = logic.get_account("name", dato, "strict")[0]["id"]
        def mod_car_data(dom):
            if dom != '':
                data = logic.get_account("id", id, "strict") if self.fileT == "account.json" else logic.get_customer("id", id, "strict")
                nCar = data[0]["cars"]
                nCar.append(dom)
                logic.mod_data(id, "id", "cars", nCar, self.fileT)

            # Restore Button
            self.menu_frame_button_1.configure(state='normal')
            self.menu_frame_button_3.configure(state='normal')
            self.menu_frame_button_5.destroy()
            self.menu_frame_entry_5.destroy()
            self.menu_frame_button_5 = customtkinter.CTkButton(self.menu_frame, text="Añadir Vehículo", image=self.car_icon_image, compound="left", command=self.add_car,
                text_color=("gray10", "gray90"))
            self.menu_frame_button_5.grid(row=4, column=0, padx=10, pady=10)
            self.refresh(self.fileT)
        # Input Car Domain 
        self.menu_frame_button_5.destroy()
        self.menu_frame_entry_5 = customtkinter.CTkEntry(self.menu_frame, placeholder_text="Dominio", width=110)
        self.menu_frame_button_5 = customtkinter.CTkButton(self.menu_frame, text="+", width=1, command=lambda:(mod_car_data(self.menu_frame_entry_5.get())), text_color=("gray10", "gray90"))
        self.menu_frame_button_5.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.menu_frame_entry_5.grid(row=4, column=0, padx=(10, 10), pady=10, sticky='e')

    def refresh(self, file):
        if self.mod_customer_frame != None: self.mod_customer_frame.destroy()
        if self.account_frame != None: self.account_frame.destroy()
        if self.account_list_frame != None: self.account_list_frame.destroy()
        self.menu_frame_button_4.configure(state='normal' if os.path.exists(f'data/temp/{file}') else 'disabled')
        self.menu_frame_button_1.configure(state='disabled')
        self.menu_frame_button_3.configure(state='disabled')
        self.menu_frame_button_5.configure(state='disabled')
        self.account_list_frame = AccountsListFrame(master=self, width=300, filename=file, command=self.select_account)
        self.account_list_frame.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="ns")
    
    def back(self, file):
        old_data = open(f'data/temp/{file}', 'r', encoding='utf-8').read()
        open(f'data/{file}', 'w', encoding='utf-8').write(old_data)
        os.remove(f'data/temp/{file}')
        self.refresh()

    # buttons frames actions
    def select_account_type(self):
        if self.account_list_frame != None:
            self.account_list_frame.destroy()
        if self.account_frame != None:
            self.account_frame.destroy()

        acType = self.scrollable_radiobutton_frame.get_checked_item()
        if acType == "Corrientes":
            self.fileT = "account.json"
            self.account_list_frame = AccountsListFrame(master=self, width=300, filename="account.json", command=self.select_account)
        elif acType == "Particulares":
            self.fileT = "customer.json"
            self.account_list_frame = AccountsListFrame(master=self, width=300, filename="customer.json", command=self.select_account)
        self.account_list_frame.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="nsew")
        
        # footer-menu buttons
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=1, padx=15, pady=5)

        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Eliminar", image=self.remove_icon_image, compound="left", command=self.remove_customer,
                text_color=("gray10", "gray90"), state="disabled")
        self.menu_frame_button_1.grid(row=2, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_customer,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Modificar", image=self.mod_icon_image, compound="left", command=self.mod_customer,
                text_color=("gray10", "gray90"), state="disabled")
        self.menu_frame_button_3.grid(row=3, column=1, padx=10, pady=10)

        self.menu_frame_button_4 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound="left", command=lambda:(self.back(self.fileT)),
                text_color=("gray10", "gray90"), state='normal' if os.path.exists(f'data/temp/{self.fileT}') else 'disabled')
        self.menu_frame_button_4.grid(row=3, column=0, padx=10, pady=10)

        self.menu_frame_button_5 = customtkinter.CTkButton(self.menu_frame, text="Añadir Vehículo", image=self.car_icon_image, compound="left", command=self.add_car,
                text_color=("gray10", "gray90"), state="disabled")
        self.menu_frame_button_5.grid(row=4, column=0, padx=10, pady=10)

        if self.scrollable_radiobutton_frame.get_checked_item() == "Corrientes": self.menu_frame_button_6 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", 
                image=self.refresh_icon_image, compound="left", command=lambda:(self.refresh("account.json")),
                text_color=("gray10", "gray90")) 
        else: self.menu_frame_button_6 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", 
                command=lambda:(self.refresh("customer.json")), text_color=("gray10", "gray90"))
        self.menu_frame_button_6.grid(row=4, column=1, padx=10, pady=10)

    def select_account(self, account, file):
        self.menu_frame_button_1.configure(state='normal')
        self.menu_frame_button_3.configure(state='normal')
        self.menu_frame_button_5.configure(state='normal')
        if self.account_frame != None:
            self.account_frame.destroy()
        
        self.account_frame = AccountDataFrame(master=self, width=500, data=account, filename=file)
        self.account_frame.grid(row=0, column=2, padx=(20, 20), pady=10, sticky="nsew")