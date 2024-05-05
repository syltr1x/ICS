import logic
from PIL import Image
import customtkinter
import json
import time
import os

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
        self.data_frame = None
        self.works_scrollable_frame = None
        super().__init__(master, **kwargs)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")

        self.remove_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/trash.png")),
                dark_image=Image.open(os.path.join(image_path, "light/trash.png")), size=(20, 20))
        self.refresh_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/refresh.png")),
                dark_image=Image.open(os.path.join(image_path, "light/refresh.png")), size=(20, 20))
        self.back_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/back.png")),
                dark_image=Image.open(os.path.join(image_path, "light/back.png")), size=(20, 20))
        
        # create scrollable radiobutton frame
        with open("data/history.json", "r") as dF: data = dF.read(); dF.close(); datab = data[:-1][1:].replace("},","}},").split("},")
        if datab != [''] and type(datab) == list and datab != ['\n']:
            items = [f'{json.loads(i)["customer"]} -/- {json.loads(i)["lcplate"]} -/- {json.loads(i)["entrydt"]}' for i in datab]
        else: items = []
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=350, command=self.radiobutton_frame_event,
                item_list=items, label_text="Lista de Trabajos Archivados", corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")

        # create footer-menu
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=1, padx=15, pady=5)

        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Eliminar", image=self.remove_icon_image, compound="left", command=self.remove_work,
                text_color=("gray10", "gray90"), state='disabled')
        self.menu_frame_button_1.grid(row=0, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", command=self.refresh,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=0, column=1, padx=10, pady=10)

        self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound="left", command=self.back,
                text_color=("gray10", "gray90"), state='normal' if os.path.exists('data/temp/history.json') else 'disabled')
        self.menu_frame_button_3.grid(row=1, column=0, padx=10, pady=10, columnspan='2', sticky='nsew')

    def remove_work(self):
        self.data_frame.destroy()
        NpId = []
        LpId = []
        EpId = []
        Nid = logic.get_history("customer", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[0], "strict")
        Lid = logic.get_history("lcplate", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[1], "strict")
        Eid = logic.get_history("entrydt", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[2], "strict")

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

        open("data/temp/history.json", "w").write(open("data/history.json" ,"r").read())
        logic.remove_data("history.json", id, "id")
        self.refresh()

    def back(self):
        old_data = open('data/temp/history.json', 'r', encoding='utf-8').read()
        open('data/history.json', 'w', encoding='utf-8').write(old_data)
        os.remove(f'data/temp/history.json')
        self.refresh()

    def refresh(self):
        self.menu_frame_button_1.configure(state='disabled')
        if self.data_frame != None: self.data_frame.destroy()
        if self.works_scrollable_frame != None:
            self.works_scrollable_frame.grid_forget()
            self.works_scrollable_frame.destroy_frame()
        self.scrollable_radiobutton_frame.destroy()
        with open("data/history.json", "r") as dF: data = dF.read(); dF.close(); datab = data[:-1][1:].replace("},","}},").split("},")
        if datab != [''] and type(datab) == list and datab != ['\n']:
            items = [f'{json.loads(i)["customer"]} -/- {json.loads(i)["lcplate"]} -/- {json.loads(i)["entrydt"]}' for i in datab]
        else: items = []
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=350, command=self.radiobutton_frame_event,
                item_list=items, label_text="Lista de Trabajos Archivados", corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")

    def radiobutton_frame_event(self):
        if self.data_frame != None:
            self.data_frame.destroy()
        if self.works_scrollable_frame != None:
            self.works_scrollable_frame.grid_forget()
            self.works_scrollable_frame.destroy_frame()
        self.menu_frame_button_1.configure(state='normal')
        NpId = []
        LpId = []
        EpId = []
        Nid = logic.get_history("customer", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[0], "strict")
        Lid = logic.get_history("lcplate", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[1], "strict")
        Eid = logic.get_history("entrydt", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[2], "strict")

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
        customer = logic.get_history("id", id, "strict")
        dato = str(customer)[:-1][1:].replace("'",'"')
        self.data_frame = DataFrame(master=self, width=10, corner_radius=10)
        self.data_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
        dato = json.loads(dato)
        
        self.customer = customtkinter.CTkLabel(self.data_frame, text=f'Cliente : {dato["customer"]}')
        self.customer.grid(row=0, column=0, pady=15, padx=15)

        self.lcplate = customtkinter.CTkLabel(self.data_frame, text=f'Dominio : {dato["lcplate"]}')
        self.lcplate.grid(row=0, column=1, pady=15, padx=15)
        
        self.entrydt = customtkinter.CTkLabel(self.data_frame, text=f'Fecha de Entrada : {dato["entrydt"]}')
        self.entrydt.grid(row=1, column=0, pady=15, padx=15)
        
        self.exitdt = customtkinter.CTkLabel(self.data_frame, text=f'Fecha de Salida : {dato["exitdt"]}')
        self.exitdt.grid(row=1, column=1, pady=15, padx=15)
        
        self.price = customtkinter.CTkLabel(self.data_frame, text=f'Coste Total : ${dato["price"]}')
        self.price.grid(row=2, column=0, pady=15, padx=15)
        
        self.status = customtkinter.CTkLabel(self.data_frame, text=f'Estado de paga : {dato["status"]}', fg_color="red" if dato["status"] == 'adeuda' else "green", corner_radius=5)
        self.status.grid(row=2, column=1, pady=15, padx=15)
        
        self.works_scrollable_frame = ScrollableDataFrame(master=self, width=500, label_text=f'Diagnostico : {dato["diagnostic"]}', corner_radius=10,
                item_list=[f'Item : '+json.loads(str(i).replace("'", '"'))["item"]+'\nPrecio/u : $'+str(int(int(json.loads(str(i).replace("'", '"'))["price"])/int(json.loads(str(i).replace("'", '"'))["quantity"])))+
                '\nCantidad : '+json.loads(str(i).replace("'", '"'))["quantity"] for i in dato["work"]])
        self.works_scrollable_frame.grid(row=0, column=3, padx=(15, 5), pady=10, sticky="ns")
        self.works_scrollable_frame.configure(width=150)