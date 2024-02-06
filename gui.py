import tkinter as tk
from tkinter import filedialog as fdia
import customtkinter as ctk
from PIL import Image, ImageTk



class GUI:
    def __init__(self):
        fluff_folder_path = r"D:\Projects\FoodReguCheck\FoodReguCheck\fluff".replace("\\", "/")
        self.window = tk.Tk()
        self.window.geometry("600x400")
        self.window.title("FoodReguCheck")
        self.window.iconbitmap(f"{fluff_folder_path}/legal.ico")
        self.window.config(bg="linen", padx=50, pady=20)

        self.canvas = tk.Canvas(height=200, width=200, bg="linen", highlightthickness=0)
        resized_img = Image.open(f"{fluff_folder_path}/bowl.png").resize((200, 200))
        bowl_img = ImageTk.PhotoImage(image=resized_img)
        self.canvas.create_image(100, 100, image=bowl_img)
        self.canvas.pack()

        self.open_collection_button = ctk.CTkButton(master=self.window, text="Find your list", corner_radius=10,
                                                    border_width=2, text_color="black", fg_color="burlywood2",
                                                    hover_color="sandy brown", command=self.open_collection)
        self.open_collection_button.pack()

    def run(self):
        self.window.mainloop()

    def open_collection(self):
        file_path = fdia.askopenfilename(title="Select your PDF file", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.open_collection_button.pack_forget()
            return file_path