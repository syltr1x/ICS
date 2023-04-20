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
        radiobutton.grid(row=len(self.radiobutton_list)+1, column=0, pady=(5, 5))
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
        file = open(f"data/{filename}", "r").read()[:-1][1:].replace("'", '"').replace("},","}},").split("},")

        self.command = command
        self.button_variable = customtkinter.StringVar()
        self.button_list = []
        self.label_frame = customtkinter.CTkFrame(self, fg_color="gray30", width=70, height=30, corner_radius=5)
        self.label_frame.grid(row=0, column=0, pady=(15, 20), padx=30, sticky="nse")

        self.label = customtkinter.CTkLabel(self.label_frame, text="Lista de cuentas")
        self.label.grid(row=0, column=0, pady=5, padx=10)

        for i in file:
            if filename == "customer.json":
                self.add_item(f'{json.loads(i)["name"]} {json.loads(i)["lastname"]}', filename)
            elif filename == "account.json":
                self.add_item(json.loads(i)["name"], filename)


    def add_item(self, item, filename):
        accountbutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.button_variable)
        if self.command is not None:
            accountbutton.configure(command=lambda:(self.command(item, filename)))
        accountbutton.grid(row=len(self.button_list)+2, column=0, pady=(5, 5), padx=10)
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

        self.name_label = customtkinter.CTkLabel(self, text="Nombre : ", fg_color="gray30", corner_radius=5).grid(row=0, column=0, padx=10, pady=10)
        self.tel_label = customtkinter.CTkLabel(self, text="Telefono : ", fg_color="gray30", corner_radius=5).grid(row=1, column=0, padx=10, pady=10)

        if filename == "customer.json":
            NpId = []
            LpId = []
            Nid = str(logic.get_customer("name", data.split(" ")[0], "strict"))
            Lid = str(logic.get_customer("lastname", data.split(" ")[1], "strict"))
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

            item = json.loads(str(logic.get_customer("id", id, "strict"))[:-1][1:].replace("'", '"'))
            self.name_data_label = customtkinter.CTkLabel(self, text=f'{item["name"]} {item["lastname"]}').grid(row=0, column=1, padx=10, pady=10)
        
        elif filename == "account.json":
            item = json.loads(str(logic.get_account("name", data, "strict"))[:-1][1:].replace("'", '"'))
            self.name_data_label = customtkinter.CTkLabel(self, text=item["name"]).grid(row=0, column=1, padx=10, pady=10)
            self.balance_label = customtkinter.CTkLabel(self, text="Balance : ", fg_color="gray30", corner_radius=5).grid(row=2, column=0, padx=10, pady=10)
            self.balance_data_label = customtkinter.CTkLabel(self, text=item["balance"]+" (A favor del cliente)" if int(item["balance"]) < 0 
                    else item["balance"]+" (A favor del taller)" if int(item["balance"]) != 0 else item["balance"]).grid(row=2, column=1, padx=10, pady=10)

        self.tel_data_label = customtkinter.CTkLabel(self, text=item["tel"]).grid(row=1, column=1, padx=10, pady=10)

class AddCustomerFrame(customtkinter.CTkFrame):
        def __init__(self, master, acType, command=None, **kwargs):
            super().__init__(master, **kwargs)
            
            self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Nombre de la cuenta" if acType == "Corrientes" else "Nombre completo", width=160)
            self.name_entry.grid(row=0, column=0, padx=(0, 5), pady=(15, 5))
            
            self.tel_entry = customtkinter.CTkEntry(self, placeholder_text="Telefono", width=100)
            self.tel_entry.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))

            self.add_customer_button = customtkinter.CTkButton(self, text="Añadir Cuenta", command=lambda:(add_account(self.name_entry.get()
                    ,self.tel_entry.get())))
            self.add_customer_button.grid(row=4, column=0, padx=(100, 100), pady=(20,20), sticky="nsew")

            def add_account(name, tel):
                if acType == "Corrientes":
                    logic.write_account("", '{"id":"'+logic.get_id("account.json")+'", "name":"'+name+'", "tel":"'+tel+'", "balance":"0"}')
                elif acType == "Particulares":
                    name = name.split(" ")
                    logic.write_customer("", '{"id":"'+logic.get_id("customer.json")+'", "name":"'+name[0].capitalize()+
                            '", "lastname":"'+name[1].capitalize()+'", "tel":"'+tel+'"}')
                self.add_customer_button.destroy()
                self.add_customer_button = customtkinter.CTkButton(self, text="Cuenta Añadida...")
                self.add_customer_button.grid(row=4, column=0, padx=(100, 100), pady=(20,20), sticky="nsew")
                time.sleep(5)
                self.destroy()

                
class App(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")

        self.remove_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/clock.png")),
                dark_image=Image.open(os.path.join(image_path, "light/clock.png")), size=(20, 20))
        self.add_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/add.png")),
                dark_image=Image.open(os.path.join(image_path, "light/add.png")), size=(20, 20))
        self.refresh_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/refresh.png")),
                dark_image=Image.open(os.path.join(image_path, "light/refresh.png")), size=(20, 20))
        self.back_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/back.png")),
                dark_image=Image.open(os.path.join(image_path, "light/back.png")), size=(20, 20))
        
        # create scrollable radiobutton frame
        with open("data/customer.json", "r") as dF: data = dF.read(); dF.close(); data = data[:-1][1:].replace("},","}},").split("},")
        self.scrollable_radiobutton_frame = SelectAccountTypeFrame(master=self, width=300, command=self.select_account_type,
                item_list=["Particulares", "Corrientes"], corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="ns")

    # footer-menu functions

    def remove_customer(self):
        if self.scrollable_radiobutton_frame.get_checked_item() == "Particulares":
            NpId = []
            LpId = []
            Nid = str(logic.get_customer("name", self.account_list_frame.get_checked_item().split(" ")[0], "strict"))
            Lid = str(logic.get_customer("lastname", self.account_list_frame.get_checked_item().split(" ")[1], "strict"))
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
            open("data/temp/customer.json", "w").write(open("data/customer.json", "r").read()) # Temp Save
            logic.remove_data("customer.json", id, "id")
            self.refresh("customer.json")
        elif self.scrollable_radiobutton_frame.get_checked_item() == "Corrientes":
            name = str(self.account_list_frame.get_checked_item())
            open("data/temp/account.json", "w").write(open("data/account.json", "r").read()) # Temp Save
            logic.remove_data("account.json", name, "name")
            self.refresh("account.json")

    def add_customer(self):
        self.add_customer_frame = AddCustomerFrame(master=self, width=500, corner_radius=10, acType=self.scrollable_radiobutton_frame.get_checked_item())
        self.add_customer_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")

    def refresh(self, file):
        self.account_list_frame.destroy()
        self.account_list_frame = AccountsListFrame(master=self, width=300, filename=file, command=self.select_account)
        self.account_list_frame.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="ns")
    
    def back(self):
        file = str(os.listdir('data/temp/'))[:-2][2:]
        open(f'data/{file}', "w").write(open(f'data/temp/{file}', "r").read())
        os.remove(f'data/temp/{file}')
        self.refresh(file)

    # buttons frames actions
    def select_account_type(self):
        acType = self.scrollable_radiobutton_frame.get_checked_item()
        if acType == "Corrientes":
            self.account_list_frame = AccountsListFrame(master=self, width=300, filename="account.json", command=self.select_account)
        elif acType == "Particulares":
            self.account_list_frame = AccountsListFrame(master=self, width=300, filename="customer.json", command=self.select_account)
        self.account_list_frame.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="nsew")
        
        # footer-menu buttons
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=1, padx=15, pady=5)

        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Historico", image=self.remove_icon_image, compound="left", command=self.remove_customer,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_1.grid(row=2, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_customer,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        if self.scrollable_radiobutton_frame.get_checked_item() == "Corrientes": self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", 
                image=self.refresh_icon_image, compound="left", command=lambda:(self.refresh("account.json")),
                text_color=("gray10", "gray90")) 
        else: self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", 
                command=lambda:(self.refresh("customer.json")), text_color=("gray10", "gray90"))
        self.menu_frame_button_3.grid(row=3, column=1, padx=10, pady=10)

        self.menu_frame_button_4 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound="left", command=self.back,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_4.grid(row=3, column=0, padx=10, pady=10)

    def select_account(self, account, file):
        self.account_frame = AccountDataFrame(master=self, width=500, data=account, filename=file)
        self.account_frame.grid(row=0, column=2, padx=(20, 20), pady=10, sticky="nsew")