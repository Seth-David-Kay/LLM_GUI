import tkinter as tk
import llama_chat_gui as chat

global model
# For now just use llama2 as model always
model = "llama2"

global model_options

def save_state():
	# Read from file what saved models were, model settings, and more
	return

def create_settings(root):
	global model_options
	global model

	# Using grid layout to pack all below

	window = tk.Tk()
	# Center the window
	window_width = 300
	window_height = 300
	screen_width = window.winfo_screenwidth()
	screen_height = window.winfo_screenheight()
	# x_coordinate = int((screen_width/2) - window_width/2)
	# y_coordinate = int((screen_height/2) - window_height/2)
	x_coordinate = root.winfo_x()
	y_coordinate = root.winfo_y()
	window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
	window.title("Ollama Settings")

	# Frame & Grid Layout Init
	settings = tk.Frame(window)
	settings.grid(row=0, column=0, sticky="NESW")
	settings.grid_columnconfigure(0, weight=2)
	window.grid_rowconfigure(0, weight = 1)
	window.grid_columnconfigure(0, weight=1)

	model_options = ["llama2", "llava"]

	greetings = tk.Label(settings, text="Chat with " + model)
	greetings.grid(row=0, column=0, columnspan=2)

	# Choose model, put this in menu bar/settings page
	model_choice = tk.Label(settings, text="Choose your model or input your own")
	model_var = tk.StringVar(settings)
	if (str(model).lower().strip() == "llama2"):
		model_var.set(model_options[0])
	elif (str(model).lower().strip() == "llava"):
		model_var.set(model_options[1])
	else:
		model_var.set(model_options[0]) # Default value
	global model_dropdown
	model_dropdown = tk.OptionMenu(settings, model_var, *model_options)

	# Button press for drop down change
	def model_change():
		global model
		new_model_button = model_var.get()
		greetings.configure(text="Chat with " + new_model_button)
		model = new_model_button
		window.destroy() # Destroy this settings window
		chat.update_model(root, window)

	model_change_button = tk.Button(settings, text="OK", command=model_change)

	# More instructions
	model_addition_text = tk.Label(settings, text="Add additional llm's below")

	# Model change text input
	model_text_var = tk.StringVar(settings)
	global model_change_text_input
	model_change_text_input = tk.Entry(settings, textvariable=model_text_var)

	# Button press for adding an llm
	def model_adding():
		global model, model_options, model_dropdown
		new_model = model_text_var.get()
		# TODO Check if model is in database, if it is and undownloaded, download, if it is and
		# it is downloaded, add it to the dropdown, but if it's not, don't add it and display
		# some error message
		model_options.append(new_model)
		model_dropdown.destroy()
		model_dropdown = tk.OptionMenu(settings, model_var, *model_options)
		model_dropdown.grid(column=0, row=2)
		
		model_change_text_input.delete(0, len(new_model))

	model_addition = tk.Button(settings, text="Add", command=model_adding)

	# Packing in
	model_choice.grid(column=0, row=1, columnspan=2)
	model_dropdown.grid(column=0, row=2)
	model_change_button.grid(column=0, row=3, columnspan=2)
	model_addition_text.grid(column=0, row=4, columnspan=2)
	model_change_text_input.grid(column=0, row=5, columnspan=2)
	model_addition.grid(column=0, row=6, columnspan=2)

	# If new model is not already downloaded but it is supported, have option to download

	# Click to go to chat page

	# Option for adding files to messgae and no limit on number of files

	settings.mainloop()