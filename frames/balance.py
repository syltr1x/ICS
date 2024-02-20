import logic
from PIL import Image
import customtkinter
import calendar
import json
import os

class MonthFrame(customtkinter.CTkFrame):
    def __init__(self, master, m, command=None,  **kwargs):
        super().__init__(master, **kwargs)
        month = int(m)
        year = 2024
        mxdays = calendar.monthrange(year, month)[1]
        aum = 0
        cont = 1
        cl = calendar.monthcalendar(year, month)[0].index(1)+1
        days = ["L", "M", "X", "J", "V", "S", "D"]
        for i in range(1):
            for j in range(mxdays):
                l = customtkinter.CTkButton(
                    self,
                    text=days[cl-1]+" "+str(cont),
                    width=40,
                    command=lambda cont=cont: self.create_frame(f'{cont}|{month}|{year}')
                )
                if cl == 7:
                    aum = aum+1
                    cl = 0
                l.grid(row=i+aum, column=cl, padx=5, pady=5)
                data = open('data/balance.json', 'r', encoding='utf8').read()
                data = data[:-1][1:].replace(',{', ',{{').split(',{') if len(data) > 5 else []; ck=False
                for a in data:
                    a = json.loads(a)
                    if a["date"] == f"{cont}/{month}/{year}":
                        ck = True
                        break
                    else: ck = False
                if ck == False: l.configure(state="disabled")
                cont = cont+1
                cl = cl+1

    def create_frame(self, data):
        frame = dayFrame(data)
        frame.mainloop()

class dayFrame(customtkinter.CTk):
    def __init__(self, dato):
        super().__init__()

        main = customtkinter.CTkScrollableFrame(self, fg_color='gray20', width=250)
        main.grid(row=0, column=0, padx=20)
        # Variables
        day = dato.split('|')[0]
        month = dato.split('|')[1]
        year = dato.split('|')[2]
        itera = 1
        self.title(f"Resumen de: {day}/{month}/{year}")
        self.geometry('380x220')
        self.resizable(False, False)
        
        # Leer Datos
        data = open('data/balance.json', 'r', encoding='utf8').read()[:-1][1:].replace(',{', ',{{').split(',{')
        for i in data:
            i = json.loads(i)
            if i["date"] == f"{day}/{month}/{year}":
                x = i
                break

        title = customtkinter.CTkLabel(main, text=f'Cierre del día: {x["balance"]}', fg_color='gray70', corner_radius=5, text_color='black')
        title.grid(row=0, column=0, padx=30)
        for y in x["movements"]:
            p = json.loads(str(y).replace("'",'"'))
            card = customtkinter.CTkFrame(master=main, fg_color='gray10')
            card.grid(row=itera, column=0, padx=10, pady=8)

            cl = customtkinter.CTkLabel(card, text=f'Cliente: {p["client"]}', fg_color='gray30', corner_radius=5)
            cl.grid(row=0, column=0, padx=5, pady=(6, 6))
            mc = customtkinter.CTkLabel(card, text=f'Mecanico: {p["mecanico"]}', fg_color='gray30', corner_radius=5)
            mc.grid(row=1, column=0, padx=5, pady=(0, 6))
            pr = customtkinter.CTkLabel(card, text=f'Valor: {p["price"]}', fg_color='gray30', corner_radius=5)
            pr.grid(row=2, column=0, padx=5, pady=(0, 6))
            dc = customtkinter.CTkLabel(card, text=f'Descripcion: {p["desc"]}', fg_color='gray30', corner_radius=5)
            dc.grid(row=3, column=0, padx=5, pady=(0, 6))
            
            itera = itera+1

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
        super().__init__(master, **kwargs)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../img")
        self.month_frame = None
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]        

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
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                item_list=[f'{i+1} {months[i]}' for i in range(0, 12)],                                                                       
                label_text="Meses del 2024", corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=292, height=400)
       
    def radiobutton_frame_event(self):
        if self.month_frame != None: self.month_frame.destroy()
        self.month_frame = MonthFrame(self, m=self.scrollable_radiobutton_frame.get_checked_item().split(' ')[0])
        self.month_frame.grid(row=0, column=2)