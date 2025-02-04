import tkinter as tk
from tkinter import messagebox, filedialog
import json

# Main window setup
root = tk.Tk()
root.title("JSON Editor")
root.configure(bg='black')

# Global variable to store the JSON file path
json_file_path = None

# Create button frame for Load JSON, Save, and Save As
button_frame = tk.Frame(root, bg='black')
button_frame.pack(fill=tk.X, padx=10, pady=5)

load_button = tk.Button(button_frame, text="Load JSON", command=lambda: load_json_file(), bg='black', fg='white')
load_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Save", command=lambda: save_changes(), bg='black', fg='white')
save_button.pack(side=tk.LEFT, padx=5)

save_as_button = tk.Button(button_frame, text="Save As", command=lambda: save_as(), bg='black', fg='white')
save_as_button.pack(side=tk.LEFT, padx=5)

# Frame for the left side (Allowed Stores) and right side (Loadouts)
left_frame = tk.Frame(root, bg='black')
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5)

right_frame = tk.Frame(root, bg='black')
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5)

# Create store widget frame with entry fields and buttons
def create_store_widget(store=None):
    frame = tk.Frame(left_frame, pady=3, bg='black')
    
    tk.Label(frame, text="WPN: ", bg='black', fg='white', font=("Arial", 10)).pack(side=tk.LEFT)
    store_name = tk.Entry(frame, font=("Arial", 10))
    store_name.insert(0, store["Store"] if store else "")
    store_name.pack(side=tk.LEFT)

    tk.Label(frame, text="Config: ", bg='black', fg='white', font=("Arial", 10)).pack(side=tk.LEFT)
    max_count = tk.Spinbox(frame, from_=0, to=1000, font=("Arial", 10))
    max_count.insert(0, store["MaxCountPerStation"] if store else 0)
    max_count.pack(side=tk.LEFT)

    tk.Label(frame, text="WPN rack: ", bg='black', fg='white', font=("Arial", 10)).pack(side=tk.LEFT)
    launcher_paths = tk.Entry(frame, font=("Arial", 10))
    launcher_paths.insert(0, json.dumps(store["LauncherModelPaths"]) if store else "")
    launcher_paths.pack(side=tk.LEFT)

    remove_btn = tk.Button(frame, text="Remove", command=lambda: remove_store(frame), bg='black', fg='white', font=("Arial", 10))
    remove_btn.pack(side=tk.RIGHT)

    return frame

# Create loadout widget frame with entry fields and buttons
def create_loadout_widget(loadout=None):
    frame = tk.Frame(right_frame, pady=2, bg='black')  # Reduced pady for less spacing between loadouts

    # Create editable Entry for the loadout name
    loadout_name = tk.Entry(frame, font=("Arial", 10, "bold"))
    loadout_name.insert(0, loadout["Name"] if loadout else "New Loadout")
    loadout_name.pack(fill=tk.X, pady=2)  # Reduced pady for less spacing

    stores_frame = tk.Frame(frame, bg='black')
    stores_frame.pack(fill=tk.X)

    tk.Label(stores_frame, text="Config: ", bg='black', fg='white', font=("Arial", 10)).pack(side=tk.LEFT)
    fuel_slider = tk.Scale(stores_frame, from_=0, to=100, orient=tk.HORIZONTAL, bg='black', fg='white', font=("Arial", 10))
    fuel_slider.set(loadout["NormalizedFuel"] * 100 if loadout else 0)
    fuel_slider.pack(side=tk.LEFT)

    # Config Section: Editable for each station with weapon and amount
    config_frame = tk.Frame(frame, bg='black')
    config_frame.pack(fill=tk.X, pady=5)

    tk.Label(config_frame, text="Weapon (WPN):", bg='black', fg='white', font=("Arial", 10)).pack(side=tk.LEFT)
    weapon_name = tk.Entry(config_frame, font=("Arial", 10))
    weapon_name.insert(0, loadout["Stores"][0]["Weapon"] if loadout and loadout["Stores"] else "")
    weapon_name.pack(side=tk.LEFT)

    tk.Label(config_frame, text="Amount:", bg='black', fg='white', font=("Arial", 10)).pack(side=tk.LEFT)
    amount = tk.Spinbox(config_frame, from_=0, to=1000, font=("Arial", 10))
    amount.insert(0, loadout["Stores"][0]["Amount"] if loadout and loadout["Stores"] else 0)
    amount.pack(side=tk.LEFT)

    tk.Label(config_frame, text="Config:", bg='black', fg='white', font=("Arial", 10)).pack(side=tk.LEFT)
    config = tk.Entry(config_frame, font=("Arial", 10))
    config.insert(0, loadout["Stores"][0]["Config"] if loadout and loadout["Stores"] else "")
    config.pack(side=tk.LEFT)

    remove_btn = tk.Button(frame, text="Remove", command=lambda: remove_loadout(frame), bg='black', fg='white', font=("Arial", 10))
    remove_btn.pack(side=tk.RIGHT)

    return frame

# Function to add a store
def add_store():
    frame = create_store_widget()
    frame.pack(fill=tk.X)

# Function to add a loadout
def add_loadout():
    frame = create_loadout_widget()
    frame.pack(fill=tk.X, pady=5)

# Function to remove store
def remove_store(frame):
    frame.destroy()

# Function to remove loadout
def remove_loadout(frame):
    frame.destroy()

# Function to load JSON file
def load_json_file():
    global json_file_path
    json_file_path = filedialog.askopenfilename(initialdir=".", filetypes=[("JSON Files", "*.json")])
    if json_file_path:
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                # Validate the JSON data
                if not validate_aircraft_data(data):
                    messagebox.showerror("Error", "Wrong JSON formatting for use with loadout editor.\nUse a valid loadout JSON.")
                    return
                update_gui(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the JSON file: {e}")

# Function to save changes (example)
def save_changes():
    if json_file_path:
        try:
            data = get_data_from_gui()
            with open(json_file_path, 'w') as file:
                json.dump(data, file, indent=4)
                messagebox.showinfo("Saved", "Changes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the JSON file: {e}")
    else:
        messagebox.showwarning("No File", "No file loaded to save!")

def save_as():
    global json_file_path
    save_as_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if save_as_path:
        try:
            data = get_data_from_gui()
            with open(save_as_path, 'w') as file:
                json.dump(data, file, indent=4)
                json_file_path = save_as_path  # Update the global file path
                messagebox.showinfo("Saved", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the JSON file: {e}")

# Helper function to get data from the GUI (stores, loadouts, etc.)
def get_data_from_gui():
    data = {
        "AllowedStores": [],
        "Loadouts": []
    }

    # Extracting data from the GUI widgets
    for widget in left_frame.winfo_children():
        if isinstance(widget, tk.Frame):
            store_data = {}
            # Logic to extract store data from widgets (store name, config, and racks)
            pass  # Add logic to extract store data

    return data

def update_gui(data):
    # This function will update the GUI after the JSON data is loaded
    for widget in left_frame.winfo_children():
        widget.destroy()
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Allowed Stores Section
    tk.Label(left_frame, text="Allowed Stores", bg='black', fg='white', font=("Arial", 12, "bold")).pack()
    allowed_stores = data.get("AllowedStores", [])
    if allowed_stores:
        for store in allowed_stores:
            create_store_widget(store).pack(fill=tk.X)
    else:
        messagebox.showwarning("No Data", "No stores found in the JSON data.")

    # Loadouts Section
    tk.Label(right_frame, text="Loadouts", bg='black', fg='white', font=("Arial", 12, "bold")).pack()
    loadouts = data.get("Loadouts", [])
    if loadouts:
        for loadout in loadouts:
            create_loadout_widget(loadout).pack(fill=tk.X, pady=5)
    else:
        messagebox.showwarning("No Data", "No loadouts found in the JSON data.")

def validate_aircraft_data(data):
    """
    Validate that the aircraft data has the necessary keys and structure:
    - 'Name' should be a string.
    - 'AllowedStores' should be a list of objects, each containing a 'Store' key.
    - 'Loadouts' should be a list of objects, each containing 'Name' and 'Stores' keys.
    """
    # Check if 'Name' is a string
    if not isinstance(data.get("Name"), str):
        return False

    # Check for required 'AllowedStores' section
    allowed_stores = data.get("AllowedStores")
    if allowed_stores is None or not isinstance(allowed_stores, list) or not allowed_stores:
        return False  # Fail if 'AllowedStores' is missing, not a list, or empty
    
    for store in allowed_stores:
        if not isinstance(store, dict) or "Store" not in store:
            return False

    # Check for required 'Loadouts' section
    loadouts = data.get("Loadouts")
    if loadouts is None or not isinstance(loadouts, list) or not loadouts:
        return False  # Fail if 'Loadouts' is missing, not a list, or empty
    
    for loadout in loadouts:
        if not isinstance(loadout, dict) or "Name" not in loadout or "Stores" not in loadout:
            return False

    return True

root.mainloop()
