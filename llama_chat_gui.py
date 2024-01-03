import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import llama_settings_gui as settings
import llama_script as llama
from tkinter import filedialog as fd
import os

class ChatApp:
    def __init__(self, root):

        global attachment_filename
        attachment_filename = "" # Initialize to nothing

        self.root = root
        self.root.title(f"{settings.model} chat")
        window_width = 600
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width/2) - window_width/2)
        y_coordinate = int((screen_height/2) - window_height/2)
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        # Set the background color
        root.configure(bg="#343540")

        # Create the chat history display
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, bg="#343540", fg="white", relief=tk.FLAT, highlightbackground="#343540", highlightcolor="#343540")
        self.chat_history.config(font="Arial, 15")
        self.chat_history.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)
        self.chat_history.config(state="disabled")

        # Create a frame for input box and submit button
        input_frame = tk.Frame(root, bg="#343540")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Create the input box
        self.input_box = tk.Entry(input_frame, width=40, relief=tk.FLAT, bg="#343540", fg="white", highlightbackground="#797979", highlightcolor="#797979")
        self.input_box.bind('<Return>', self.enter_submit_message)
        self.input_box.pack(side=tk.LEFT, padx=(0, 1))

        # Create the submit button
        self.submit_button = tk.Button(input_frame, text="Send", command=self.submit_message, relief=tk.FLAT, bg="#797979", fg="#343540", highlightbackground="#343540", highlightcolor="#343540", activeforeground="#343540", activebackground="#343540", background="#343540", foreground="#343540", disabledforeground="#343540")
        self.submit_button.pack(side=tk.RIGHT)

        # Create the settings button
        self.settings_button = tk.Button(text="Settings", command=self.go_to_settings, relief=tk.FLAT, bg="#797979", fg="#343540", highlightbackground="#343540", highlightcolor="#343540", activeforeground="#343540", activebackground="#343540", background="#343540", foreground="#343540", disabledforeground="#343540")
        self.settings_button.pack(side=tk.LEFT, padx=(0, 5))

        # Create attachments dropdown and label
        if (str(settings.model).strip().lower() == "llava"):
            # Create the attatchments button
            self.attatchment_button = tk.Button(input_frame, text="Attatchments", command=self.select_file, relief=tk.FLAT, bg="#797979", fg="#343540", highlightbackground="#343540", highlightcolor="#343540", activeforeground="#343540", activebackground="#343540", background="#343540", foreground="#343540", disabledforeground="#343540")
            self.attatchment_button.pack(side=tk.RIGHT)
            # Create the attachments label
            self.attatchment_label = tk.Label(bg="#343540", fg="#797979", text="No file selected")
            self.attatchment_label.pack(side=tk.RIGHT, padx=(0, 10))
            # Move label below

        # Protocal for closing
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def go_to_settings(self):
        settings.create_settings(self.root)

    def on_closing(self):
        self.root.destroy()
        exit()

    def select_file(self):
        global attachment_filename
        filename = fd.askopenfile(title='Open a file', initialdir='/', filetypes=(('Png Files', '*.png'),))
        if filename:
            attachment_filename = str(filename)
            start_ind = attachment_filename.find("'") + 1
            end_index = attachment_filename.find("'", start_ind)
            attachment_filename = attachment_filename[start_ind:end_index]
            display_filename = attachment_filename.rsplit('/', 1)[-1]
            display_filename = display_filename.split(".png")[0]
            self.attatchment_label.configure(text=display_filename)
        else:
            self.attatchment_label.configure(text="No file selected")

    def enter_submit_message(self, event):
        self.submit_message()

    def submit_message(self):
        global attachment_filename
        # Start animation
        message = self.input_box.get()
        if message:
            self.input_box.delete(0, tk.END)
            self.update_chat_history(f"You: {message}\n")

            time.sleep(0.1)

            # Gather response
            response = llama.choose_model_generate_response(message, settings.model, attachment_filename)
            self.update_chat_history(f"{settings.model}: {response}\n")

            if message.strip().lower() == "bye" or message.strip().lower() == "bye!":
                time.sleep(3)
                self.on_closing()

    def update_chat_history(self, message):
        # Stop animation
        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.configure(state=tk.DISABLED)
        self.chat_history.yview(tk.END)  # Scroll to the bottom

        # Scroll the entire window to show the latest message
        self.root.update_idletasks()
        self.root.geometry(self.root.geometry())

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

# Make less jolty and more efficient
def update_model(root, settings):
    root.destroy()
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
    # Spawn settings back in? But without it it's fine

## Add increase text size functionality