import tkinter
import customtkinter
import frames.customer as custom

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("600x400")
app.title("Home | Punto Diesel")

frame = custom.App(master=app)
frame.grid(row=0, column=1, padx=(15, 0), pady=10, sticky="ns")
# l1=customtkinter.CTkOptionMenu(app, values=["Clientes", "Trabajos", "Autos"])
# l1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# l2 = customtkinter.CTkFrame(master=app, width=110, height=320, corner_radius=20)

app.mainloop()