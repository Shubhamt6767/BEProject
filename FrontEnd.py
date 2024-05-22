import customtkinter
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from Connector import mainMethod

customtkinter.set_appearance_mode("dark")

customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk()
app.geometry("1800x1000")
app.title("Pedestrian Road Crossing Intention Prediction")


# print(filename)

def select_file():
    global file
    app.filename = filedialog.askopenfilename(initialdir="BE_project", title="Select A File",
                                              filetypes=(("Video Files", "*.mp4"), ("all files", "*.*")))

    file = app.filename


select_folder_img = ImageTk.PhotoImage(Image.open("Select1.png").resize((30, 30), Image.ANTIALIAS))

but = customtkinter.CTkButton(master=app, image=select_folder_img, text="Select Folder",
                              text_color="white", width=300, height=100, compound="left", command=select_file)
but.pack(pady=160, padx=20)

but1 = customtkinter.CTkButton(master=app, text="Predict", text_color="white",
                               width=300, height=100, command=lambda: mainMethod(file))
but1.pack(pady=10, padx=20)

app.mainloop()
