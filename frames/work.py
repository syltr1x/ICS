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
        self.works_scrollable_frame = None
        self.data_frame = None
        self.add_customer_frame = None 
        super().__init__(master, **kwargs)
        
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")
        self.clock_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/clock.png")),
                dark_image=Image.open(os.path.join(image_path, "light/clock.png")), size=(20, 20))
        self.x_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/x.png")),
                dark_image=Image.open(os.path.join(image_path, "light/x.png")), size=(20, 20))
        self.add_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/add.png")),
                dark_image=Image.open(os.path.join(image_path, "light/add.png")), size=(20, 20))
        self.refresh_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/refresh.png")),
                dark_image=Image.open(os.path.join(image_path, "light/refresh.png")), size=(20, 20))
        self.back_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/back.png")),
                dark_image=Image.open(os.path.join(image_path, "light/back.png")), size=(20, 20))
        self.check_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/check.png")),
                dark_image=Image.open(os.path.join(image_path, "light/check.png")), size=(20, 20))
        self.remove_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark/trash.png")),
                dark_image=Image.open(os.path.join(image_path, "light/trash.png")), size=(20, 20))

        with open("data/work.json", "r", encoding='utf-8') as dF: datab = dF.read(); dF.close(); datab = datab[:-1][1:].replace("},","}},").split("},")
        if datab != [''] and type(datab) == list and datab != ['\n']:
            items = [f'{json.loads(i)["customer"]} -/- {json.loads(i)["lcplate"]} -/- {json.loads(i)["entrydt"]}' for i in datab]
        else: items = []
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=350, command=self.radiobutton_frame_event,
            item_list=items, corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="ns")


        # create footer-menu
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=0, padx=15, pady=5)

        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Historico", image=self.clock_icon_image, compound="left", command=self.store_work,
                text_color=("gray10", "gray90"), state='disabled')
        self.menu_frame_button_1.grid(row=2, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Eliminar", image=self.remove_icon_image, compound="left", command=self.remove_work,
                text_color=("gray10", "gray90"), state='disabled')
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", command=self.refresh,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_3.grid(row=3, column=1, padx=10, pady=10)

        self.menu_frame_button_4 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound="left", command=self.back,
                text_color=("gray10", "gray90"), state='normal' if os.path.exists('data/temp/work.json') else 'disabled')
        self.menu_frame_button_4.grid(row=3, column=0, padx=10, pady=10)

    # Scrollables Frames Function
    def refresh(self):
        self.menu_frame_button_1.configure(state='disabled')
        self.menu_frame_button_2.configure(state='disabled')
        self.menu_frame_button_4.configure(state='normal' if os.path.exists('data/temp/work.json') else 'disabled')
        if self.add_customer_frame != None: self.cancel()
        if self.data_frame != None: self.data_frame.destroy()
        if self.works_scrollable_frame != None:
            self.works_scrollable_frame.grid_forget()
            self.works_scrollable_frame.destroy_frame()
        self.scrollable_radiobutton_frame.destroy()
        with open("data/work.json", "r", encoding='utf-8') as dF: datab = dF.read(); dF.close(); datab = datab[:-1][1:].replace("},","}},").split("},")
        if datab != [''] and type(datab) == list and datab != ['\n']:
            items = [f'{json.loads(i)["customer"]} -/- {json.loads(i)["lcplate"]} -/- {json.loads(i)["entrydt"]}' for i in datab]
        else: items = []
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=350, command=self.radiobutton_frame_event,
            item_list=items, corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="ns")
  
    def back(self, file):
        old_data = open('data/temp/work.json', 'r', encoding='utf-8').read()
        open('data/work.json', 'w', encoding='utf-8').write(old_data)
        os.remove(f'data/temp/work.json')
        self.refresh()

    def store_work(self):
        self.data_frame.destroy()
        NpId = []
        LpId = []
        EpId = []
        Nid = logic.get_works("customer", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[0], "strict")
        Lid = logic.get_works("lcplate", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[1], "strict")
        Eid = logic.get_works("entrydt", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[2], "strict")

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

        open("data/temp/work.json", "w").write(open("data/work.json" ,"r").read())
        logic.write_history('', str(logic.get_works("id", id, "strict")).replace("'", '"')[:-1][1:])
        logic.remove_data("work.json", id, "id")
        self.refresh()

    def remove_work(self):
        self.data_frame.destroy()
        NpId = []
        LpId = []
        EpId = []
        Nid = logic.get_works("customer", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[0], "strict")
        Lid = logic.get_works("lcplate", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[1], "strict")
        Eid = logic.get_works("entrydt", self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")[2], "strict")

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

        datos = logic.get_works("id", id, "strict")[0]
        logic.remove_data("work.json", id, "id")
        for item in datos["work"]:
            stock = logic.get_product('item', item["item"].lower(), 'strict')[0]["stock"]
            logic.mod_data(item["item"].lower(), 'item', 'stock', str(int(stock)+int(item["quantity"])), "inventory.json")
        self.refresh()

    def cancel(self):
        self.add_customer_frame.destroy()
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_customer,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
        
        self.refresh()

    def uprices(self, id, lista):
        logic.update_prices(id, lista)
        self.refresh()

    def upd_exit(self, id):
        logic.get_works("id", id, "strict")
        data = str(time.localtime()).split(',')
        year = data[0][-4:].replace("=","")
        month = data[1][-2:].replace("=","")
        day = data[2][-2:].replace("=","")
        hour = data[3][-2:].replace("=","")+":"+data[4][-2:].replace("=","")+":"+data[5][-2:].replace("=","")

        datetime = day+"/"+month+"/"+year+" , "+hour
        logic.mod_data(id, "id", "exitdt", datetime, "work.json")

    def pay_frame(self, price, id, dato, tech):
        def valPay():
            payed = int(payInp.get())
            payW.destroy()
            if payed >= price: payed = "total"
            logic.pay_work(logic.get_date(), id, payed, dato, tech)

        payW = customtkinter.CTk()
        payW.title("Pago de Trabajo")
        payW.geometry("180x180")
        payInp = customtkinter.CTkEntry(payW, placeholder_text=f"Precio: {price}")
        payInp.grid(column=0, row=0, pady=10)
        payBtn = customtkinter.CTkButton(payW, text="Pagar", command=valPay)
        payBtn.grid(column=0, row=1, pady=10)
        payW.mainloop()

    def radiobutton_frame_event(self):
        self.menu_frame_button_1.configure(state='normal')
        self.menu_frame_button_2.configure(state='normal')
        dato = self.scrollable_radiobutton_frame.get_checked_item().split(" -/- ")
        if self.data_frame != None:
            self.data_frame.destroy()
        if self.works_scrollable_frame != None:
            self.works_scrollable_frame.grid_forget()
            self.works_scrollable_frame.destroy_frame()
        NpId = []
        LpId = []
        EpId = []
        Nid = logic.get_works("customer", dato[0], "strict")
        Lid = logic.get_works("lcplate", dato[1], "strict")
        Eid = logic.get_works("entrydt", dato[2], "strict")

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
        customer = logic.get_works("id", id, "strict")
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
        
        self.exitdt = customtkinter.CTkLabel(self.data_frame, text=f'Fecha de Salida : {dato["exitdt"]}')
        self.exitdt.grid(row=1, column=1, pady=15, padx=15)

        self.price = customtkinter.CTkLabel(self.data_frame, text=f'Pago : ${dato["payed"]}')
        self.price.grid(row=2, column=1, pady=15, padx=15)
        
        self.price = customtkinter.CTkLabel(self.data_frame, text=f'Debe : ${str(int(dato["price"])-int(dato["payed"]))} ('+dato["pd"]+')')
        self.price.grid(row=3, column=0, pady=15, padx=15)
        
        self.status = customtkinter.CTkLabel(self.data_frame, text=f'Estado de paga : {dato["status"]}', fg_color="red" if dato["status"] == 'adeuda' else "green", corner_radius=5)
        self.status.grid(row=3, column=1, pady=15, padx=15)

        self.paybtn = customtkinter.CTkButton(self.data_frame, text="Ingresar Pago", command=lambda:(self.pay_frame(int(dato["price"])-int(dato["payed"]), dato["id"], dato["diagnostic"], dato["technician"])))
        self.paybtn.grid(row=4, column=1, pady=15, padx=15) if dato["status"] == 'adeuda' else None
        
        self.refbtn = customtkinter.CTkButton(self.data_frame, text="Actualizar Precios", command=lambda:(self.uprices(dato["id"], "works")))
        self.refbtn.grid(row=4, column=0, pady=15, padx=15 if dato["status"] != "pagado" else None)

        self.exitbtn = customtkinter.CTkButton(self.data_frame, command=lambda:(self.upd_exit(dato["id"])))
        self.exitbtn.grid(row=5, column=0, pady=15, padx=15)
        self.exitbtn.configure(state="disabled" if dato["exitdt"] != "--/--/---- , --:--:--" and dato["exitdt"] != "--/--/----" else "normal")
        self.exitbtn.configure(text="Vehiculo Entregado" if dato["exitdt"] != "--/--/---- , --:--:--" and dato["exitdt"] != "--/--/----" else "Entregar Vehiculo")

        self.works_scrollable_frame = ScrollableDataFrame(master=self, width=500, label_text=f'Diagnostico : {dato["diagnostic"]}\n Total : {dato["price"]}', corner_radius=10,
                item_list=[f'Item : '+json.loads(str(i).replace("'", '"'))["item"]+'\nPrecio/u : $'+str(int(int(json.loads(str(i).replace("'", '"'))["price"])/int(json.loads(str(i).replace("'", '"'))["quantity"])))+
                '\nCantidad : '+json.loads(str(i).replace("'", '"'))["quantity"] for i in dato["work"]])
        self.works_scrollable_frame.grid(row=0, column=3, padx=(15, 5), pady=10, sticky="ns")
        self.works_scrollable_frame.configure(width=150)
    