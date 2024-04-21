import logic
from PIL import Image
import customtkinter
import json
import time
import os

class AddProductFrame(customtkinter.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Nombre del Producto", width=160)
        self.name_entry.grid(row=0, column=0, padx=(0, 5), pady=(15, 5))
        
        self.price_entry = customtkinter.CTkEntry(self, placeholder_text="Precio", width=100)
        self.price_entry.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))

        self.stock_entry = customtkinter.CTkEntry(self, placeholder_text="Stock", width=100)
        self.stock_entry.grid(row=2, column=0, padx=(5, 5), pady=(5, 5))

        self.add_customer_button = customtkinter.CTkButton(self, text="Añadir Producto", command=lambda:(add_product(self.name_entry.get()
                ,self.price_entry.get(), self.stock_entry.get())))
        self.add_customer_button.grid(row=4, column=0, padx=(100, 100), pady=(20,20), sticky="nsew")

        def add_product(name, price, stock):
            logic.write_product("", '{"item":"'+name+'", "price":"'+price+'", "stock":"'+stock+'"}')

class DataFrame(customtkinter.CTkFrame):
    def __init__(self, master, dato, command=None, **kwargs):
        super().__init__(master, **kwargs)
        data = str(logic.get_product("item", dato, "strict"))
        data = json.loads(data[:-1][1:].replace("'", '"'))

        self.item_label = customtkinter.CTkLabel(self, text='Nombre de Producto :', fg_color="gray30", corner_radius=5).grid(row=0, column=0, padx=(30, 5), pady=(15, 5))
        self.item_data_label = customtkinter.CTkLabel(self, text=data["item"]).grid(row=0, column=1, padx=(5, 30), pady=(15, 5))

        self.price_label = customtkinter.CTkLabel(self, text='Precio/u :', fg_color="gray30", corner_radius=5).grid(row=1, column=0, padx=(30, 5), pady=(15, 5))
        self.price_data_label = customtkinter.CTkLabel(self, text=f'${data["price"]}').grid(row=1, column=1, padx=(5, 30), pady=(15, 5))
                
        self.stock_label = customtkinter.CTkLabel(self, text='Stock :', fg_color="gray30", corner_radius=5).grid(row=2, column=0, padx=(30, 5), pady=(15, 5))
        self.stock_data_label = customtkinter.CTkLabel(self, text=data["stock"]).grid(row=2, column=1, padx=(5, 30), pady=(15, 5))

class ModFrame(customtkinter.CTkFrame):
    def __init__(self, master, dato, command=None, **kwargs):
        super().__init__(master, **kwargs)
        data = str(logic.get_product("item", dato, "strict"))
        data = json.loads(data[:-1][1:].replace("'", '"'))        

        self.item_entry = customtkinter.CTkEntry(self, placeholder_text=data["item"])
        self.item_entry.grid(row=0, column=0, padx=30, pady=(15, 5))
        
        self.price_entry = customtkinter.CTkEntry(self, placeholder_text="$"+data["price"]+" c/u")
        self.price_entry.grid(row=1, column=0, padx=30, pady=(15, 5))
                
        self.stock_entry = customtkinter.CTkEntry(self, placeholder_text=data["stock"])
        self.stock_entry.grid(row=2, column=0, padx=30, pady=(15, 5))

        self.product_button = customtkinter.CTkButton(self, text="Modificar Producto", command=lambda:(mod_product(self.item_entry.get()
        ,self.price_entry.get(), self.stock_entry.get())))

        self.product_button.grid(row=3, column=0, padx=30, pady=(20, 5))
        def mod_product(name, price, stock):
            cambios = []

            if stock != "":
                cambios.append('{"field":"stock", "value":"'+stock+'"}')
            if price != "":
                cambios.append('{"field":"price", "value":"'+price+'"}')
            if name != "":
                cambios.append('{"field":"item", "value":"'+name+'"}')

            for c in cambios:
                ic = json.loads(c)
                logic.mod_data(data["item"], "item", ic["field"], ic["value"], "inventory.json")

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
        self.add_item_frame = None
        self.mod_item_frame = None
        self.mod_frame = None

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
        with open("data/inventory.json", "r", encoding="utf-8") as dF: data = dF.read(); dF.close(); data = data[:-1][1:].replace("},","}},").split("},")
        if data != ['']:
            self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                    item_list=[f'{json.loads(i)["item"]}' for i in data],                                                                       
                    label_text="Lista de Productos", corner_radius=10)
        else:
            self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                    item_list=[], label_text="Lista de Productos", corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=292)

        # create footer-menu
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=1, column=1, padx=15, pady=5)

        self.menu_frame_button_1 = customtkinter.CTkButton(self.menu_frame, text="Eliminar", image=self.clock_icon_image, compound="left", command=self.remove_item,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_1.grid(row=2, column=0, padx=10, pady=10)

        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_product,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.menu_frame_button_3 = customtkinter.CTkButton(self.menu_frame, text="Actualizar", image=self.refresh_icon_image, compound="left", command=self.refresh,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_3.grid(row=3, column=1, padx=10, pady=10)

        self.menu_frame_button_4 = customtkinter.CTkButton(self.menu_frame, text="Revertir", image=self.back_icon_image, compound="left", command=self.back,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_4.grid(row=3, column=0, padx=10, pady=10)

    def remove_item(self):
        open("data/temp/inventory.json", "w", encoding='utf8').write(open("data/inventory.json", "r", encoding='utf8').read()) # Temp Save
        item = str(self.scrollable_radiobutton_frame.get_checked_item())
        logic.remove_data("inventory.json", item, "item")
        self.refresh()

    def add_product(self):
        self.refresh()
        def cancel():
            self.add_item_frame.destroy()
            self.menu_frame_button_2.destroy()
            self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_product,
                    text_color=("gray10", "gray90"))
            self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
            
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Cancelar", image=self.x_icon_image, compound="left", command=cancel, 
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)

        self.add_item_frame = AddProductFrame(master=self, width=420, corner_radius=10)
        self.add_item_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")
    
    def mod_product(self):
        dato = self.scrollable_radiobutton_frame.get_checked_item()
        self.refresh()
        def cancel():
            self.mod_item_frame.destroy()
            self.menu_frame_button_2.destroy()
            self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_product,
                    text_color=("gray10", "gray90"))
            self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
            
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Cancelar", image=self.x_icon_image, compound="left", command=cancel, 
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
        self.mod_item_frame = ModFrame(master=self, width=420, corner_radius=10, dato=dato)
        self.mod_item_frame.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="nsew")

    def refresh(self):
        if self.scrollable_radiobutton_frame != None : self.scrollable_radiobutton_frame.destroy()
        if self.mod_item_frame != None: self.mod_item_frame.destroy()
        if self.mod_frame != None: self.mod_frame.destroy()
        with open("data/inventory.json", "r", encoding="utf-8") as dF: data = dF.read(); dF.close(); data = data[:-1][1:].replace("},","}},").split("},")
        if data != ['']:
            self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                    item_list=[f'{json.loads(i)["item"]}' for i in data],                                                                       
                    label_text="Lista de Productos", corner_radius=10)
        else:
            self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                    item_list=[], label_text="Lista de Productos", corner_radius=10)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=(15, 5), pady=10, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=292)
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Añadir", image=self.add_icon_image, compound="left", command=self.add_product,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
    
    def back(self):
        file = str(os.listdir('data/temp/'))[:-2][2:]
        open(f'data/{file}', "w").write(open(f'data/temp/{file}', "r").read())
        os.remove(f'data/temp/{file}')
        self.refresh()

    def radiobutton_frame_event(self):
        if self.mod_frame != None: self.mod_frame.destroy()
        self.menu_frame_button_2.destroy()
        self.menu_frame_button_2 = customtkinter.CTkButton(self.menu_frame, text="Modificar", image=self.mod_icon_image, compound="left", command=self.mod_product,
                text_color=("gray10", "gray90"))
        self.menu_frame_button_2.grid(row=2, column=1, padx=10, pady=10)
        self.mod_frame = DataFrame(self, width=420, dato=self.scrollable_radiobutton_frame.get_checked_item())
        self.mod_frame.grid(row=0, column=2, padx=30, pady=10, sticky="nsew")