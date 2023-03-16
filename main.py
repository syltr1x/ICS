import tkinter
import customtkinter

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("600x400")
app.title("Home | Punto Diesel")

frame = customtkinter.CTkFrame(master=app, width=320, height=320, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

def test(jorge):
    l2 = customtkinter.CTkFrame(master=app, width=900, height=120, corner_radius=20)

l1=customtkinter.CTkOptionMenu(frame, values=["Clientes", "Trabajos", "Autos"], command=test)
l1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2 = customtkinter.CTkFrame(master=app, width=110, height=320, corner_radius=20)

app.mainloop()