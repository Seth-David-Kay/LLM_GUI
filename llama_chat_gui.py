import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import llama_settings_gui as settings
import llama_script as llama

class ChatApp:
    def __init__(self, root):
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
        self.chat_history.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)
        self.chat_history.config(state="disabled")

        # Create a frame for input box and submit button
        input_frame = tk.Frame(root, bg="#343540")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Create the input box
        self.input_box = tk.Entry(input_frame, width=40, relief=tk.FLAT, bg="#343540", fg="white", highlightbackground="#797979", highlightcolor="#797979")
        self.input_box.pack(side=tk.LEFT, padx=(0, 5))

        # Create the submit button
        self.submit_button = tk.Button(input_frame, text="Send", command=self.submit_message, relief=tk.FLAT, bg="#797979", fg="#343540", highlightbackground="#343540", highlightcolor="#343540", activeforeground="#343540", activebackground="#343540", background="#343540", foreground="#343540", disabledforeground="#343540")
        self.submit_button.pack(side=tk.RIGHT)

        # Protocal for closing
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        self.root.destroy()
        exit()

    def submit_message(self):
        # Start animation
        message = self.input_box.get()
        if message:
            self.input_box.delete(0, tk.END)
            self.update_chat_history(f"You: {message}\n")

            time.sleep(0.1)

            # Simulate a response (you can replace this with actual logic)
            response = llama.generate_full_reponse(message)
            self.update_chat_history(f"{settings.model}: {response}\n")

            if message.strip().lower() == "bye" or message.strip().lower() == "bye!":
                time.sleep(2)
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

## Add increase text size functionality