import tkinter as tk
from tkinter import filedialog as fdia
import customtkinter as ctk
from PIL import Image, ImageTk
import webbrowser


class GUI:
    def __init__(self):

        # Basic starting stuff
        self.fluff_folder_path = r"D:\Projects\FoodReguCheck\fluff".replace("\\", "/")
        self.filepath = ""
        self.window = tk.Tk()
        self.window.geometry("600x400")
        self.window.title("FoodReguCheck")
        self.window.iconbitmap(f"{self.fluff_folder_path}/legal.ico")
        self.window.config(bg="linen", padx=50, pady=20)

        # Add a food photo
        self.canvas = tk.Canvas(height=200, width=200, bg="linen", highlightthickness=0)
        resized_img = Image.open(f"{self.fluff_folder_path}/bowl.png").resize((200, 200))
        bowl_img = ImageTk.PhotoImage(image=resized_img)
        self.canvas.create_image(100, 100, image=bowl_img)
        self.canvas.pack()

        # A button to start the File Explorer
        self.open_collection_button = ctk.CTkButton(master=self.window, text="Find your list", corner_radius=10,
                                                    border_width=2, text_color="black", fg_color="burlywood2",
                                                    hover_color="sandy brown", command=self.open_collection)
        self.open_collection_button.pack()

        # A label to show the user that the docs are being checked
        self.loading_label = ctk.CTkLabel(master=self.window, text="Checking your documents...",
                                          corner_radius=10, text_color="black", fg_color="burlywood2")

        # Create two tabs for the repealed and modified documents
        self.tabs = ctk.CTkTabview(master=self.window, width=580,
                                   bg_color="snow", fg_color="snow", text_color="black",
                                   segmented_button_fg_color="burlywood2",
                                   segmented_button_selected_color="sandy brown",
                                   segmented_button_selected_hover_color="navajo white",
                                   segmented_button_unselected_color="linen",
                                   segmented_button_unselected_hover_color="navajo white")
        self.tabs.add("No longer in force")
        self.tabs.add("Was modified")
        self.repealed_frame = ctk.CTkFrame(master=self.tabs.tab("No longer in force"),
                                           width=580, bg_color="snow", fg_color="transparent")
        self.modified_frame = ctk.CTkFrame(master=self.tabs.tab("Was modified"),
                                           width=580, bg_color="snow", fg_color="transparent")

        self.window.mainloop()

    # Start the File Explorer and clear out the GUI
    def open_collection(self):
        self.open_collection_button.destroy()
        self.loading_label.pack()
        self.filepath = fdia.askopenfilename(title="Select your PDF file", filetypes=[("PDF files", "*.pdf")])
        self.loading_label.destroy()
        self.canvas.destroy()
        self.window.quit()

    # Show the repealed and modified documents' data
    def show_evaluation(self, repealed_list, modified_list):

        # Create the new window after the file was found
        self.tabs.pack()
        self.repealed_frame.pack()
        self.modified_frame.pack()

        # For having intermittent coloring
        color_num = 1

        # Loop through the repealed list's documents as show them in separate blocks
        for i in range(len(repealed_list)):
            name = repealed_list[i]["name"]
            link = repealed_list[i]["repealed_by"]
            end = repealed_list[i]["end_date"]

            if color_num % 2 == 0:
                color = "snow"
            else:
                color = "navajo white"

            document_block = ctk.CTkFrame(master=self.repealed_frame, width=560, bg_color=color, fg_color=color,
                                          corner_radius=10)
            document_block.grid(row=i, column=0, sticky="NW")

            # Fill the blocks with the name, end_date and link widgets
            name_label = tk.Label(master=document_block, text=name, wraplength=460, relief="solid", borderwidth=0,
                                  highlightthickness=10, highlightbackground=color, background=color)
            end_date_label = ctk.CTkLabel(master=document_block, text=end, corner_radius=10,
                                          text_color="black", fg_color=color, bg_color=color)
            link_button = ctk.CTkButton(master=document_block, text="Open document", corner_radius=10,
                                        border_width=0, text_color="black", fg_color="burlywood2",
                                        hover_color="sandy brown", bg_color=color,
                                        command=lambda arg=link: self.open_link(arg))

            # Put every widget to the grid
            name_label.grid(row=0, column=0, columnspan=2)
            end_date_label.grid(row=1, column=0, sticky="N")
            link_button.grid(row=1, column=1, sticky="N")

            # Changing to the other color
            color_num += 1

        # Loop through the modified list's documents as show them in separate blocks
        color_num = 1  # Starting with the same color as in the 1st tab
        for j in range(len(modified_list)):
            name = modified_list[j]["name"]
            link = modified_list[j]["new_version"]
            change = modified_list[j]["date_of_change"]

            if color_num % 2 == 0:
                color = "snow"
            else:
                color = "navajo white"

            document_block = ctk.CTkFrame(master=self.modified_frame, width=560, bg_color=color, fg_color=color,
                                          corner_radius=10)
            document_block.grid(row=j, column=0, sticky="NW")

            # Fill the blocks with the name, change_date and link widgets
            name_label = tk.Label(master=document_block, text=name, wraplength=460, relief="solid", borderwidth=0,
                                  highlightthickness=10, highlightbackground=color, background=color)
            change_date_label = ctk.CTkLabel(master=document_block, text=change, corner_radius=10,
                                             text_color="black", fg_color=color, bg_color=color)
            link_button = ctk.CTkButton(master=document_block, text="Open document", corner_radius=10,
                                        border_width=0, text_color="black", fg_color="burlywood2",
                                        hover_color="sandy brown", bg_color=color,
                                        command=lambda arg=link: webbrowser.open_new(arg))

            # Put every widget to the grid
            name_label.grid(row=0, column=0, columnspan=2, sticky="nesw")
            change_date_label.grid(row=1, column=0, sticky="N")
            link_button.grid(row=1, column=1, sticky="N")

            color_num += 1

    # Opening the repealed or modified document if its button is clicked
    def open_link(self, link):
        webbrowser.open_new(link)

    def run(self):
        self.window.mainloop()