import logic
from PIL import Image
import customtkinter
import json
import time
import os
import ast

class AddCustomerFrame(customtkinter.CTkFrame):
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
                if dataC != [] and dataC != ['']:
                    for i in dataC:
                        item = json.loads(i)
                        clientes.append(str(item["lastname"]+" "+item["name"]))
                return clientes
            elif request == "technician":
                mecanicos = []
                with open("data/config.json", "r", encoding='utf-8') as dF: dataM = json.loads(dF.read()); dF.close()
                mecanicos = [i for i in dataM["mechanics"].split('|')]
                return mecanicos
            elif request == "concept":
                return ["Reparacion", "Service", "Mantenimiento", "Revision", "Garantia"]
            elif request == "placas":
                patentes = []
                with open("data/car.json", "r", encoding='utf-8') as dF: dataP = dF.read(); dF.close()
                dataP = dataP[:-1][1:].replace("},","}},").split("},")
                if dataP != [] and dataP != ['']:
                    for i in dataP:
                        item = json.loads(i)
                        patentes.append(item["lcplate"])
                return patentes
            
        def auto_date():
            self.in_entry.delete(0, len(self.in_entry.get()))
            if self.in_entry_check.get() == 1:
                data = str(time.localtime()).split(',')
                year = data[0][-4:].replace("=","")
                month = data[1][-2:].replace("=","")
                day = data[2][-2:].replace("=","")
                hour = data[3][-2:].replace("=","")+":"+data[4][-2:].replace("=","")+":"+data[5][-2:].replace("=","")

                datetime = day+"/"+month+"/"+year+" , "+hour
                self.in_entry.insert(0, datetime)
            else:
                self.in_entry.configure(placeholder_text="dd/mm/aaaa,hh:mm:ss")
                
        def searcher(field, data):
            clientes = get_data("customer")
            if field == "customer":
                for i in clientes:
                    if data.lower() not in i.split(" ")[0].lower() and data.lower() not in i.split(" ")[1].lower(): clientes.remove(i)
                self.customer_entry.destroy()
                self.customer_entry = customtkinter.CTkComboBox(self, values=[i for i in clientes], button_hover_color="gray10", corner_radius=5, fg_color="gray50")
                self.customer_entry.grid(row=0, column=0, padx=(170, 10), pady=(20, 20))
                self.customer_entry.set(f'Resultados : {len(clientes)}')
                
        clientes = get_data("customer")
        mecanicos = get_data("technician")
        concepts = get_data("concept")
        patentes = get_data("placas")
        
        self.customer_filter_btn = customtkinter.CTkButton(self, image=self.loupe_icon_image, text="", width=1, command=lambda:(searcher("customer", self.customer_entry.get())))
        self.customer_filter_btn.grid(row=0, column=0, padx=(10, 0), pady=(5, 5), sticky='w')

        self.customer_entry = customtkinter.CTkComboBox(self, values=[i for i in clientes], button_hover_color="gray10",
                button_color="gray30", corner_radius=5, fg_color="gray50")
        self.customer_entry.set("Clientes")
        self.customer_entry.grid(row=0, column=0, padx=(50, 10), pady=(20, 20))

        self.lcplate_entry = customtkinter.CTkComboBox(self, values=[i for i in patentes], button_hover_color="gray10",
                button_color="gray30", corner_radius=5, fg_color="gray50")
        self.lcplate_entry.set("Dominio")
        self.lcplate_entry.grid(row=1, column=0, padx=(50, 10), pady=(20, 20))

        self.technician_entry = customtkinter.CTkComboBox(self, values=[i for i in mecanicos], button_hover_color="gray10",
                button_color="gray30", corner_radius=5, fg_color="gray50")
        self.technician_entry.set("Mecanicos")
        self.technician_entry.grid(row=0, column=1, padx=(10, 20), pady=(20, 20))

        self.concepto_entry = customtkinter.CTkOptionMenu(self, values=[i for i in concepts], button_hover_color="gray10",
                button_color="gray30", corner_radius=5, fg_color="gray50")
        self.concepto_entry.set("Concepto")
        self.concepto_entry.grid(row=1, column=1, padx=(10, 20), pady=(20, 20))

        self.in_entry_check = customtkinter.CTkCheckBox(self, command=lambda:(auto_date()), text="", width=220)
        self.in_entry_check.grid(row=3, column=0, padx=(15, 5), pady=(5, 5))

        self.in_entry = customtkinter.CTkEntry(self, placeholder_text="dd/mm/aaaa,hh:mm:ss", width=150)
        self.in_entry.grid(row=3, column=0, padx=(20, 20), pady=(20, 20))
        
        self.columnconfigure(1, weight=1)

        self.work_items_frame = customtkinter.CTkFrame(self, width=200, height=80)
        self.work_items_frame.grid(row=2, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))
        self.work_items_title = customtkinter.CTkLabel(self.work_items_frame, text="Lista de productos").grid(row=0, column=0, padx=(15,0), sticky="w")
        self.work_item_add = customtkinter.CTkButton(self.work_items_frame, text="Añadir Item", command=lambda:(add_work_item())).grid(row=0, column=-0, padx=(180,0), sticky='w')

        self.add_customer_button = customtkinter.CTkButton(self, text="Crear Presupuesto", command=lambda:(add_work(self.customer_entry.get().capitalize(), self.lcplate_entry.get().upper(),
                self.technician_entry.get(), self.in_entry.get(), self.concepto_entry.get())))
        self.add_customer_button.grid(row=3, column=1, padx=(0, 10), pady=(20,20), sticky="nsew")

        global works
        works= []
        def add_work_item():
            pre_work_add = NewWork(self.work_items_frame)
            pre_work_add.grid(row=len(works)+1, column=0, sticky="nsew")

        def add_work(name, lcplate, technician, entry, diagnostic):
            work=[]
            price = 0
            for p in works: price = price+int(json.loads("{"+p+"}")["price"]); work.append(json.loads("{"+p+"}"))
            logic.write_budget("", '{"id":"'+logic.get_id("budget.json")+'", "customer":"'+name+'", "lcplate":"'+lcplate+'", "technician":"'+technician+'","entrydt":"'+entry+'", "diagnostic":"'+diagnostic+'", "work":'+str(work).replace("'", '"')+', "price":"'+str(price)+'", "pd":"'+entry.split(' , ')[0]+'"}')
            self.destroy()
            comm()

class NewWork(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pre_add_work()

    def suggest_price(self, item):
        data = open("data/inventory.json", "r", encoding='utf-8').read()[:-1][1:].replace("},", "}},").split("},")
        for d in data:
            if json.loads(d)["item"] == item:
                self.item_price.delete(0, "end")
                self.item_price.insert(0, json.loads(d)["price"])
                break
        
    def pre_add_work(self):
        data = open("data/inventory.json", "r", encoding='utf-8').read()[:-1][1:].replace("},", "}},").split("},")
        global item_menu
        global item_price
        global item_quantity
        global confirm_work
    
        self.item_menu = customtkinter.CTkComboBox(self, values=[json.loads(i)["item"] for i in data], command=self.suggest_price)
        self.item_menu.grid(row=0, column=0)
        self.item_price = customtkinter.CTkEntry(self, placeholder_text="Precio/u", width=120)
        self.item_price.grid(row=0, column=1)
        self.item_quantity = customtkinter.CTkEntry(self, placeholder_text="Cantidad", width=80)
        self.item_quantity.grid(row=0, column=2)
        self.confirm_work = customtkinter.CTkButton(self, text="+", width=28, command=lambda:(self.add_work(self.item_menu.get(), self.item_price.get(), self.item_quantity.get())))
        self.confirm_work.grid(row=0, column=3)

    def add_work(self, item, price, quantity):
        if item != "" and price != "":
            self.item_menu.destroy()
            self.item_price.destroy()
            self.item_quantity.destroy()
            self.confirm_work.destroy()

            item_label = customtkinter.CTkLabel(self, text=f'Item : {item.capitalize()}', fg_color="gray30", corner_radius=5)
            item_label.grid(row=0, column=0, padx=15, pady=5)
            price_label = customtkinter.CTkLabel(self, text=f'Precio/u : ${price}', fg_color="gray30", corner_radius=5)
            price_label.grid(row=0, column=1, padx=15, pady=5)
            quantity = quantity if quantity != "" else "1"
            quantity_label = customtkinter.CTkLabel(self, text=f'Cantidad : {quantity}', fg_color="gray30", corner_radius=5)
            quantity_label.grid(row=0, column=2, padx=15, pady=5)
        works.append('"item":"'+item.capitalize()+'", "price":"'+str(int(price)*int(quantity))+'", "quantity":"'+quantity+'"')


class DataFrame(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)

class ScrollableDataFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):

        super().__init__(master, **kwargs)
        self.label_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        label_frame = customtkinter.CTkFrame(self, corner_radius=10, fg_color="gray30")
        label_frame.grid(row=len(self.label_list), column=0, pady=(5, 5))
        label_item = customtkinter.CTkLabel(label_frame, text=item)
        label_item.grid(row=0, column=0, pady=10, padx=10)
        self.label_list.append(label_item)

    def destroy_frame(self):
        for label_frame in self.label_list:
            label_frame.destroy()
        self.label_list = []
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
        self.works_scrollable_frame = None
        self.data_frame = None
        self.add_customer_frame = None 
        super().__init__(master, **kwargs)
        
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")
        self.x_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/x.png")),
                dark_image=Image.open(os.path.join(image_path, "light/x.png")), size=(20, 20))
        self.add_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/add.png")),
                dark_image=Image.open(os.path.join(image_path, "light/add.png")), size=(20, 20))
        self.refresh_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/refresh.png")),
                dark_image=Image.open(os.path.join(image_path, "light/refresh.png")), size=(20, 20))
        self.check_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/check.png")),
                dark_image=Image.open(os.path.join(image_path, "light/check.png")), size=(20, 20))
        self.remove_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/trash.png")),
                dark_image=Image.open(os.path.join(image_path, "light/trash.png")), size=(20, 20))
        self.back_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/back.png")),
                dark_image=Image.open(os.path.join(image_path, 'light/back.png')), size=(20, 20))

        with open("data/budget.json", "r", encoding='utf-8') as dF: datab = dF.read(); dF.close(); datab = datab[:-1][1:].replace("},","}},").split("},")
        if datab != [''] and type(datab) == list and datab != ['\n']:
            items = [f'{json.loads(i)["customer"]} -/- {json.loads(i)["lcplate"]} -/- {json.loads(i)["entrydt"]}' for i in datab]
        else: items = []
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=350, command=self.radiobutton_frame_event,
            item_list=items, corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="ns")

        # create footer-menu
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=0, padx=15, pady=5)
        
        # Scrollables Frames Function
        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Aprobado", image=self.check_icon_image, compound="left", command=self.aprobe_budget,
                text_color=("gray10", "gray90"), state='disabled')
        self.menu_frame_button_1.grid(row=1, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_budget,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=1, column=1, padx=10, pady=10)

        self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Eliminar", image=self.remove_icon_image, compound="left", command=self.remove_budget,
                text_color=("gray10", "gray90"), state='disabled')
        self.menu_frame_button_3.grid(row=2, column=0, padx=10, pady=10)

        self.menu_frame_button_4 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", command=self.refresh,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_4.grid(row=2, column=1, padx=10, pady=10)

        self.menu_frame_button_5 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound='left', command=self.back,
                text_color=("gray10", "gray90"), state='normal' if os.path.exists('data/temp/budget.json') else 'disabled')
        self.menu_frame_button_5.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
    
    def aprobe_budget(self):
        self.data_frame.destroy()
        NpId = []
        LpId = []
        EpId = []
        Nid = logic.get_budget("customer", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[0], "strict")
        Lid = logic.get_budget("lcplate", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[1], "strict")
        Eid = logic.get_budget("entrydt", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[2], "strict")

        if type(Nid) == list:
            for item in Nid:  NpId.append(json.loads(str(item).replace("'", '"'))["id"])
        if type(Lid) == list:
            for item in Lid:  LpId.append(json.loads(str(item).replace("'", '"'))["id"])
        if type(Eid) == list:
            for item in Eid: EpId.append(json.loads(str(item).replace("'", '"'))["id"])
        if type(NpId):
            for n in NpId:
                if type(LpId):
                    for l in LpId:
                        if type(EpId):
                            for e in EpId:
                                if n == e and e == l: id = n
                        else:
                            if n == l and Eid == l: id = n
                else:
                    if n == Lid and Eid == Lid: id = n
        else:
            if Nid == Lid and Nid == Eid: id = n

        open("data/temp/budget.json", "w", encoding='utf-8').write(open("data/budget.json" ,"r", encoding='utf-8').read())
        datos = logic.get_budget("id", id, "strict")[0]
        datos["exitdt"] = "--/--/----"
        datos["payed"] = '0'
        datos["status"] = 'adeuda'
        logic.write_works('', str(datos).replace("'", '"'))
        logic.remove_data("budget.json", id, "id")
        for item in datos["work"]:
            stock = logic.get_product('item', item["item"].lower(), 'strict')[0]["stock"]
            logic.mod_data(item["item"].lower(), 'item', 'stock', str(int(stock)-int(item["quantity"])), "inventory.json")
        self.refresh()

    def remove_budget(self):
        self.data_frame.destroy()
        NpId = []
        LpId = []
        EpId = []
        Nid = logic.get_budget("customer", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[0], "strict")
        Lid = logic.get_budget("lcplate", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[1], "strict")
        Eid = logic.get_budget("entrydt", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[2], "strict")

        if type(Nid) == list:
            for item in Nid:  NpId.append(json.loads(str(item).replace("'", '"'))["id"])
        if type(Lid) == list:
            for item in Lid:  LpId.append(json.loads(str(item).replace("'", '"'))["id"])
        if type(Eid) == list:
            for item in Eid: EpId.append(json.loads(str(item).replace("'", '"'))["id"])
        if type(NpId):
            for n in NpId:
                if type(LpId):
                    for l in LpId:
                        if type(EpId):
                            for e in EpId:
                                if n == e and e == l: id = n
                        else:
                            if n == l and Eid == l: id = n
                else:
                    if n == Lid and Eid == Lid: id = n
        else:
            if Nid == Lid and Nid == Eid: id = n

        logic.remove_data("budget.json", id, "id")
        self.refresh()

    def add_budget(self):
        self.refresh()
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Cancelar", image=self.x_icon_image, compound="left", command=self.cancel, 
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.add_customer_frame = AddCustomerFrame(master=self, width=420, corner_radius=10, comm=self.refresh)
        self.add_customer_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")

    def refresh(self):
        self.menu_frame_button_1.configure(state='disabled')
        self.menu_frame_button_3.configure(state='disabled')
        self.menu_frame_button_5.configure(state='normal' if os.path.exists('data/temp/budget.json') else 'disabled')
        if self.add_customer_frame != None: self.cancel()
        if self.data_frame != None: self.data_frame.destroy()
        if self.works_scrollable_frame != None:
            self.works_scrollable_frame.grid_forget()
            self.works_scrollable_frame.destroy_frame()
        self.scrollable_radiobutton_frame.destroy()
        with open("data/budget.json", "r", encoding='utf-8') as dF: datab = dF.read(); dF.close(); datab = datab[:-1][1:].replace("},","}},").split("},")
        if datab != [''] and type(datab) == list and datab != ['\n']: 
            items = [f'{json.loads(i)["customer"]} -/- {json.loads(i)["lcplate"]} -/- {json.loads(i)["entrydt"]}' for i in datab]
        else: items = []
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=350, command=self.radiobutton_frame_event,
            item_list=items, corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="ns")
  
    def back(self):
        old_data = open('data/temp/budget.json', 'r', encoding='utf-8').read()
        open('data/budget.json', 'w', encoding='utf-8').write(old_data)
        os.remove(f'data/temp/budget.json')
        self.refresh()

    def cancel(self):
        self.add_customer_frame.destroy()
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_budget,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
        
        # create scrollable radiobutton frame | 
        with open("data/budget.json", "r", encoding='utf-8') as dF: datab = dF.read(); dF.close(); datab = datab[:-1][1:].replace("},","}},").split("},")
        if datab != [''] and datab != ['\n']: items = [f'{json.loads(i)["customer"]} -/- {json.loads(i)["lcplate"]} -/- {json.loads(i)["entrydt"]}' for i in datab]
        else: items = []
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=350, command=self.radiobutton_frame_event,
            item_list=items, corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="ns")

    def uprices(self, id, lista):
        logic.update_prices(id, lista)
        self.refresh()

    def radiobutton_frame_event(self):
        self.menu_frame_button_1.configure(state='normal')
        self.menu_frame_button_3.configure(state='normal')
        dato = self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")
        if self.data_frame != None:
            self.data_frame.destroy()
        if self.works_scrollable_frame != None:
            self.works_scrollable_frame.grid_forget()
            self.works_scrollable_frame.destroy_frame()
        NpId = []
        LpId = []
        EpId = []
        Nid = logic.get_budget("customer", dato[0], "strict")
        Lid = logic.get_budget("lcplate", dato[1], "strict")
        Eid = logic.get_budget("entrydt", dato[2], "strict")

        if type(Nid) == list:
            for item in Nid:  NpId.append(json.loads(str(item).replace("'", '"'))["id"])
        if type(Lid) == list:
            for item in Lid:  LpId.append(json.loads(str(item).replace("'", '"'))["id"])
        if type(Eid) == list:
            for item in Eid: EpId.append(json.loads(str(item).replace("'", '"'))["id"])
        if type(NpId):
            for n in NpId:
                if type(LpId):
                    for l in LpId:
                        if type(EpId):
                            for e in EpId:
                                if n == e and e == l: id = n
                        else:
                            if n == l and Eid == l: id = n
                else:
                    if n == Lid and Eid == Lid: id = n
        else:
            if Nid == Lid and Nid == Eid: id = n
        customer = logic.get_budget("id", id, "strict")
        dato = str(customer)[:-1][1:].replace("'",'"')
        self.data_frame = DataFrame(master=self, width=10, corner_radius=10)
        self.data_frame.grid(row=0, column=2, padx=0, pady=10, sticky="nsew")
        dato = json.loads(dato)
        
        self.customer = customtkinter.CTkLabel(self.data_frame, text=f'Cliente : {dato["customer"]}')
        self.customer.grid(row=0, column=0, pady=15, padx=15)

        self.lcplate = customtkinter.CTkLabel(self.data_frame, text=f'Dominio : {dato["lcplate"]}')
        self.lcplate.grid(row=0, column=1, pady=15, padx=15)
        
        self.entrydt = customtkinter.CTkLabel(self.data_frame, text=f'Mecanico : {dato["technician"]}')
        self.entrydt.grid(row=1, column=0, pady=15, padx=15)

        self.entrydt = customtkinter.CTkLabel(self.data_frame, text=f'Fecha de Entrada : {dato["entrydt"]}')
        self.entrydt.grid(row=2, column=0, pady=15, padx=15)
        
        self.refbtn = customtkinter.CTkButton(self.data_frame, text="Actualizar Precios", command=lambda:(self.uprices(dato["id"], "budget")))
        self.refbtn.grid(row=4, column=0, pady=15, padx=15)

        self.works_scrollable_frame = ScrollableDataFrame(master=self, width=500, label_text=f'Diagnostico : {dato["diagnostic"]}\n Total : {dato["price"]}', corner_radius=10,
                item_list=[f'Item : '+json.loads(str(i).replace("'", '"'))["item"]+'\nPrecio/u : $'+str(int(int(json.loads(str(i).replace("'", '"'))["price"])/int(json.loads(str(i).replace("'", '"'))["quantity"])))+
                '\nCantidad : '+json.loads(str(i).replace("'", '"'))["quantity"] for i in dato["work"]])
        self.works_scrollable_frame.grid(row=0, column=3, padx=(15, 5), pady=10, sticky="ns")
        self.works_scrollable_frame.configure(width=150)