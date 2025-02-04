import tkinter as tk
from tkinter import ttk
import json
import os
from pathlib import Path
import ctypes

# Hide the console window
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

min_amount = 1
max_amount = 9

# Function to validate the amount entry
def validate_amount(value_if_allowed, selected_store):
    if value_if_allowed.isdigit():
        amount = int(value_if_allowed)
        if selected_store == "AIM-9 Sidewinder":
            return min_amount <= amount <= 2
        return min_amount <= amount <= max_amount
    elif value_if_allowed == "":
        return True
    return False

# Function to save the current selection of stores for each station
def save_selection():
    # Create a dictionary of station numbers and their selected stores and amounts
    selection = {
        f"Station {i+1}": {"Store": var.get(), "Amount": amt_var.get()}
        for i, (var, amt_var) in enumerate(zip(pylon_vars, amount_vars))
        if i != 9
    }
    print("Store Selection:", selection)
    save_to_json(selection)  # Save the selection to a JSON file

# Function to save the selection dictionary to a JSON file
def save_to_json(selection):
    formatted_selection = [
        {"Pylon": pylon, "Store": info["Store"], "Amount": info["Amount"]}
        for pylon, info in selection.items()
    ]
    # Get the path to the user's Documents folder
    documents_path = os.path.join(str(Path.home()), "Documents")
    # Specify the filename and combine it with the Documents path
    file_path = os.path.join(documents_path, 'store_selection.json')
    
    # Save the selection to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(formatted_selection, json_file, indent=4)
    print(f"Selection saved to {file_path}")

# Function to update the amount entry based on selected store
def update_amount_entry(event, amt_entry, store_var):
    selected_store = store_var.get()
    if selected_store == "None":
        amt_entry['state'] = 'disabled'
        amt_entry.delete(0, tk.END)  # Clear the entry when "None" is selected
    else:
        amt_entry['state'] = 'normal'
        validate_cmd = (amt_entry.register(validate_amount), '%P', store_var.get())
        amt_entry.config(validate="key", validatecommand=validate_cmd)

# Initialize the main Tkinter window
root = tk.Tk()
root.title("F-4E Phantom II Store Selector")

# Invert colors: background black, text white
root.configure(bg='black')

# List of pylon (station) numbers (excluding the 10th pylon)
pylons = [f"{i+1}" for i in range(12) if i != 9]

# List of possible stores to be selected
stores = [
    "None",
    "AIM-9 Sidewinder",
    "AIM-7 Sparrow",
    "Mk 82 Bomb",
    "Mk 84 Bomb",
    "GBU-12 Paveway II",
    "AGM-65 Maverick",
    "CBU-87 Cluster Bomb"
]

pylon_vars = []  # List to hold StringVar for each pylon
amount_vars = []  # List to hold StringVar for each amount
frame = tk.Frame(root, bg='black')
frame.pack(padx=10, pady=10)

# Create labels and combo boxes vertically
for pylon in pylons:
    pylon_frame = tk.Frame(frame, bg='black')
    pylon_frame.pack(pady=5)

    # Label for pylon number
    label = tk.Label(pylon_frame, text=f"Pylon {pylon}", fg='white', bg='black')
    label.pack(side=tk.LEFT, padx=5)

    # Default selected store is "None"
    var = tk.StringVar(value="None")
    pylon_vars.append(var)
    
    # Combo box for selecting a store
    combo = ttk.Combobox(pylon_frame, textvariable=var, values=stores, state="readonly")
    combo.pack(side=tk.LEFT, padx=5)

    # Amount entry (disabled by default)
    amt_var = tk.StringVar(value="1")
    amount_vars.append(amt_var)

    validate_amount_cmd = (root.register(validate_amount), '%P', var.get())
    amt_entry = tk.Entry(pylon_frame, textvariable=amt_var, validate="key", validatecommand=validate_amount_cmd)
    amt_entry['state'] = 'disabled'
    amt_entry.pack(side=tk.LEFT, padx=5)

    # Bind the store combobox to the update function
    combo.bind("<<ComboboxSelected>>", lambda event, amt_entry=amt_entry, store_var=var: update_amount_entry(event, amt_entry, store_var))

# Button to save the current selection of stores
save_button = tk.Button(root, text="Save Selection", command=save_selection, fg='white', bg='black')
save_button.pack(pady=10)

# Start the main event loop
root.mainloop()
