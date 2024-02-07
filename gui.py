import tkinter as tk
from tkinter import filedialog as fdia
import customtkinter as ctk
from PIL import Image, ImageTk
import time


class GUI:
    def __init__(self):
        self.fluff_folder_path = r"D:\Programming\FoodReguCheck\fluff".replace("\\", "/")
        self.filepath = ""
        self.window = tk.Tk()
        self.window.geometry("600x400")
        self.window.title("FoodReguCheck")
        self.window.iconbitmap(f"{self.fluff_folder_path}/legal.ico")
        self.window.config(bg="linen", padx=50, pady=20)

        self.canvas = tk.Canvas(height=200, width=200, bg="linen", highlightthickness=0)
        resized_img = Image.open(f"{self.fluff_folder_path}/bowl.png").resize((200, 200))
        bowl_img = ImageTk.PhotoImage(image=resized_img)
        self.canvas.create_image(100, 100, image=bowl_img)
        self.canvas.pack()

        self.open_collection_button = ctk.CTkButton(master=self.window, text="Find your list", corner_radius=10,
                                                    border_width=2, text_color="black", fg_color="burlywood2",
                                                    hover_color="sandy brown", command=self.open_collection)
        self.open_collection_button.pack()
        self.loading_label = ctk.CTkLabel(master=self.window, text="Checking your documents...",
                                          corner_radius=10, text_color="black", fg_color="burlywood2")
        self.large_screen = ctk.CTkLabel(master=self.window, text="Done",
                                         corner_radius=10, text_color="black", fg_color="burlywood2")

        self.window.mainloop()

    def open_collection(self):
        self.open_collection_button.destroy()
        self.loading_label.pack()
        self.filepath = fdia.askopenfilename(title="Select your PDF file", filetypes=[("PDF files", "*.pdf")])
        self.loading_label.destroy()
        self.canvas.destroy()
        self.window.quit()

    def show_evaluation(self, repealed, old):
        self.large_screen.grid(row=0, column=0, sticky="nsew")
        time.sleep(3)
        self.large_screen.configure(text=f"No longer in force: {repealed}\n Was modified: {old}")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
    def run(self):
        self.window.mainloop()