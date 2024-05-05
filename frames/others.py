from PIL import Image
import customtkinter
import logic
import json
import os

class DayBalanceFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, title, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        
        self.label_frame = customtkinter.CTkFrame(self, fg_color="gray30", width=70, height=30, corner_radius=5)
        self.label_frame.grid(row=0, column=0, pady=(15, 20), padx=20, sticky="ns")

        self.label = customtkinter.CTkLabel(self.label_frame, text=title)
        self.label.grid(row=0, column=0, pady=5, padx=10)
        
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = customtkinter.CTkRadioButton(self, text=f'[{item["id"]}] {item["client"]}', value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list)+1, column=0, pady=(5, 5), sticky="nw")
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()
    
class CustomerBalanceFrame(customtkinter.CTkFrame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, **kwargs)

        self.customer_label = customtkinter.CTkLabel(self, text="Cliente: "+data["client"])
        self.technician_label = customtkinter.CTkLabel(self, text="Mecanico: "+data["mecanico"])
        self.description_label = customtkinter.CTkLabel(self, text="Descripcion: "+data["desc"])
        self.price_label = customtkinter.CTkLabel(self, text="Precio: "+data["price"])

        self.customer_label.grid(row=0, column=0, padx=5, pady=5)
        self.technician_label.grid(row=0, column=1, padx=5, pady=5)
        self.description_label.grid(row=1, column=0, padx=5, pady=5)
        self.price_label.grid(row=1, column=1, padx=5, pady=5)

class AddSaleFrame(customtkinter.CTkFrame):
        def __init__(self, master, comm=None, **kwargs):
            super().__init__(master, **kwargs)

            def add_pay(name, tech, price, desc):
                logic.add_balance(logic.get_date(), name, tech, price, desc)
                comm()

            file = open("data/config.json", 'r', encoding='utf-8')
            self.config_data = json.loads(file.read())
            file.close()

            # Obtain Clients and Accounts Data
            self.acc_type_values = []
            self.customers = open('data/customer.json', 'r', encoding='utf-8').read()[:-1][1:].replace("\n", "").replace('},','}},').split('},')
            self.accounts = open('data/account.json', 'r', encoding='utf-8').read()[:-1][1:].replace("\n", "").replace('},','}},').split('},')
            if self.customers != [''] and type(self.customers) == list:
                self.acc_type_values.append("Clientes")
            if self.accounts != [''] and type(self.accounts) == list:
                self.acc_type_values.append("Cuentas")

            self.acc_type_menu = customtkinter.CTkOptionMenu(self, values=[i for i in self.acc_type_values], command=self.select_acc, width=160,
                    state="disabled" if self.acc_type_values == [] else "normal")
            clis = "Clientes" if len(self.customers) > 1 else "Cliente"
            accs = "Cuentas" if len(self.accounts) > 1 else "Cuenta"
            self.acc_type_menu.set(f"{len(self.customers)} {clis}. {len(self.accounts)} {accs}.")
            self.acc_type_menu.grid(row=0, column=0, padx=5, pady=5)

            self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Nombre del cliente", width=160)
            self.name_entry.grid(row=0, column=1, padx=5, pady=5)

            if self.config_data["mechanics"].split('|') != [''] and type(self.config_data["mechanics"].split('|')) == list:
                self.tech_entry = customtkinter.CTkOptionMenu(self, values=self.config_data["mechanics"].split('|'), width=160)
                self.tech_entry.set("Mecanicos")
            else: 
                self.tech_entry = customtkinter.CTkEntry(self, placeholder_text="Mecanico", width=160)
            self.tech_entry.grid(row=1, column=0, padx=5, pady=5)

            self.price_entry = customtkinter.CTkEntry(self, placeholder_text="Precio del Trabajo", width=160)
            self.price_entry.grid(row=1, column=1, padx=5, pady=5)

            self.description_entry = customtkinter.CTkEntry(self, placeholder_text="Concepto", width=160)
            self.description_entry.grid(row=2, column=0, padx=5, pady=5)

            self.add_customer_button = customtkinter.CTkButton(self, text="Añadir Pago", command=lambda:(add_pay(self.name_entry.get()
                    ,self.tech_entry.get(), self.price_entry.get(), self.description_entry.get())), width=160)
            self.add_customer_button.grid(row=2, column=1, padx=5, pady=5)
        
        def select_acc(self, acc):
            self.name_entry.destroy()
            if acc == "Clientes":
                    self.name_entry = customtkinter.CTkOptionMenu(self, values=[json.loads(i)["name"]+" "+json.loads(i)["lastname"] for i in self.customers])
            elif acc == "Cuentas":
                    self.name_entry = customtkinter.CTkOptionMenu(self, values=[json.loads(i)["name"] for i in self.accounts])
            self.name_entry.grid(row=0, column=1, padx=5, pady=5)

class App(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.scrollable_radiobutton_frame = None
        self.customer_balance_frame = None
        self.add_customer_frame = None
        self.account_list_frame = None
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
        
        # create scrollable radiobutton frame
        with open("data/balance.json", "r", encoding='utf-8') as dF: data = dF.read()
        dF.close()
        data = data[:-1][1:].replace(',{', ',{{').split(',{')if len(data) > 5 else []
        ilist = []
        bExist = False
        title = "No hay movimientos todavia"
        for i in data:
            i = json.loads(i)
            if i["date"] == logic.get_date():
                bExist = True
                title = f'Movimientos de {i["date"]}'
                ilist = i["movements"]
        if not bExist: logic.write_balance('','{"date":"'+logic.get_date()+'", "balance":"0", "movements":[]}')
        self.scrollable_radiobutton_frame = DayBalanceFrame(master=self, width=300, title=title, command=self.select_balance,
                item_list=ilist, corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="ns")

        # footer-menu buttons
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=0, padx=15, pady=5)

        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Eliminar", image=self.remove_icon_image, compound="left", command=self.remove_customer,
                text_color=("gray10", "gray90"), state='disabled')
        self.menu_frame_button_1.grid(row=2, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_customer,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", command=self.refresh,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_3.grid(row=3, column=1, padx=10, pady=10)

        self.menu_frame_button_4 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound="left", command=self.back,
                text_color=("gray10", "gray90"), state='normal' if os.path.exists('data/temp/balance.json') else 'disabled')
        self.menu_frame_button_4.grid(row=3, column=0, padx=10, pady=10)

    # footer-menu functions
    def remove_customer(self):
        id = json.loads(self.scrollable_radiobutton_frame.get_checked_item().replace("'", '"'))["id"]
        open("data/temp/balance.json", "w").write(open("data/balance.json", "r").read()) # Temp Save
        logic.del_balance(logic.get_date(), id)
        self.customer_balance_frame.destroy()
        logic.order_id('balance.json')
        self.refresh()

    def add_customer(self):
        self.refresh()
        def cancel():
            self.add_customer_frame.destroy()
            self.add_customer_frame = None
            self.menu_frame_button_2.destroy()
            self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_customer,
                    text_color=("gray10", "gray90"))
            self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Cancelar", image=self.x_icon_image, compound="left", command=cancel, 
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.add_customer_frame = AddSaleFrame(master=self, width=500, corner_radius=10, comm=self.refresh)
        self.add_customer_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")

    def refresh(self):
        if self.scrollable_radiobutton_frame != None : self.scrollable_radiobutton_frame.destroy()
        if self.account_list_frame != None: self.account_list_frame.destroy()
        if self.add_customer_frame != None: self.add_account_frame.destroy()
        self.menu_frame_button_1.configure(state='disabled')
        with open("data/balance.json", "r", encoding='utf-8') as dF: data = dF.read()
        dF.close()
        data = data[:-1][1:].replace(',{', ',{{').split(',{')if len(data) > 5 else []
        ilist = []
        bExist = False
        title = "No hay movimientos todavia"
        for i in data:
            i = json.loads(i)
            if i["date"] == logic.get_date():
                bExist = True
                title = f'Movimientos de {i["date"]}'
                ilist = i["movements"]
        if not bExist: logic.write_balance('','{"date":"'+logic.get_date()+'", "balance":"0", "movements":[]}')
        self.scrollable_radiobutton_frame = DayBalanceFrame(master=self, width=300, title=title, command=self.select_balance,
                item_list=ilist, corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="ns")
    
    def back(self):
        old_data = open('data/temp/balance.json', 'r', encoding='utf-8').read()
        open('data/balance.json', 'w', encoding='utf-8').write(old_data)
        os.remove(f'data/temp/balance.json')
        self.refresh()

    # buttons frames actions
    def select_balance(self):
        self.menu_frame_button_1.configure(state='normal')
        if self.customer_balance_frame != None:
            self.customer_balance_frame.destroy()
        self.customer_balance = json.loads(self.scrollable_radiobutton_frame.get_checked_item().replace("'", '"'))
        self.customer_balance_frame = CustomerBalanceFrame(master=self, width=500, data=self.customer_balance)
        self.customer_balance_frame.grid(row=0, column=2, padx=5, pady=5)