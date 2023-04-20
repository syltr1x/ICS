import customtkinter
import frames.car as custom

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("red")

app = customtkinter.CTk()
app.geometry("1100x400")
app.title("Home | Punto Diesel")

# frame = custom.App(master=app)
# frame.grid(row=0, column=1, padx=(15, 0), pady=10, sticky="ns")

def pepe(marco):
    print(marco)

list1 = ["manzana", "banana", "uva"]
list2 = ["merca", "marihuana", "jeringas"]

carlos = customtkinter.CTkComboBox(app, values=list1, command=pepe)
carlos.grid(row=1, column=1)



app.mainloop()