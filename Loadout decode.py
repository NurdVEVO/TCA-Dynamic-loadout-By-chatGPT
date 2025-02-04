import tkinter as tk
from tkinter import messagebox, filedialog
import json
import ctypes

# Hide the console window (only works on Windows)
try:
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
except Exception as e:
    print(f"Could not hide console window: {e}")

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    messagebox.showinfo("Save", "Data saved successfully!")

def load_json_file():
    global json_file_path
    json_file_path = filedialog.askopenfilename(initialdir="C:/Program Files (x86)/Steam/steamapps/common/TinyCombatArena", filetypes=[("JSON Files", "*.json")])
    if json_file_path:
        data = load_json(json_file_path)
        update_gui(data)

def save_as():
    global json_file_path
    save_as_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if save_as_path:
        save_changes()
        save_json(data, save_as_path)
        json_file_path = save_as_path

def update_gui(data):
    for widget in allowed_stores_frame.winfo_children():
        widget.destroy()
    for widget in loadouts_frame.winfo_children():
        widget.destroy()

    # Allowed Stores Section
    tk.Label(allowed_stores_frame, text="Allowed Stores", bg='black', fg='white').pack()
    for idx, store in enumerate(data["AllowedStores"]):
        frame = tk.Frame(allowed_stores_frame, pady=5, bg='black')
        frame.pack(fill=tk.X)
        frame.store_data = store

        tk.Label(frame, text="Store: ", bg='black', fg='white').pack(side=tk.LEFT)
        store_name = tk.Entry(frame)
        store_name.insert(0, store["Store"])
        store_name.pack(side=tk.LEFT)

        tk.Label(frame, text="Max Count Per Station: ", bg='black', fg='white').pack(side=tk.LEFT)
        max_count = tk.Entry(frame)
        max_count.insert(0, json.dumps(store["MaxCountPerStation"]))
        max_count.pack(side=tk.LEFT)

        tk.Label(frame, text="Launcher Model Paths: ", bg='black', fg='white').pack(side=tk.LEFT)
        launcher_paths = tk.Entry(frame)
        launcher_paths.insert(0, json.dumps(store["LauncherModelPaths"]))
        launcher_paths.pack(side=tk.LEFT)

        remove_btn = tk.Button(frame, text="Remove", command=lambda f=frame: remove_store(f), bg='black', fg='white')
        remove_btn.pack(side=tk.RIGHT)

        if idx > 0:
            up_btn = tk.Button(frame, text="Up", command=lambda f=frame: move_store_up(f), bg='black', fg='white')
            up_btn.pack(side=tk.RIGHT)

        if idx < len(data["AllowedStores"]) - 1:
            down_btn = tk.Button(frame, text="Down", command=lambda f=frame: move_store_down(f), bg='black', fg='white')
            down_btn.pack(side=tk.RIGHT)

    add_store_button = tk.Button(allowed_stores_frame, text="Add Store", command=add_store, bg='black', fg='white')
    add_store_button.pack(pady=5)

    # Loadouts Section
    tk.Label(loadouts_frame, text="Loadouts", bg='black', fg='white').pack()
    for idx, loadout in enumerate(data["Loadouts"]):
        loadout_frame = tk.Frame(loadouts_frame, pady=10, bg='black')
        loadout_frame.pack(fill=tk.X, pady=10)
        loadout_frame.loadout_data = loadout

        tk.Label(loadout_frame, text=loadout["Name"], bg='black', fg='white', font=("Arial", 12, "bold")).pack()

        stores_frame = tk.Frame(loadout_frame, bg='black')
        stores_frame.pack(fill=tk.X)

        tk.Label(stores_frame, text="Fuel %: ", bg='black', fg='white').pack(side=tk.LEFT)
        fuel_slider = tk.Scale(stores_frame, from_=0, to=100, orient=tk.HORIZONTAL, bg='black', fg='white')
        fuel_slider.set(loadout["NormalizedFuel"] * 100)
        fuel_slider.pack(side=tk.LEFT)

        tk.Label(stores_frame, text="Stores: ", bg='black', fg='white').pack(side=tk.LEFT)
        stores = tk.Entry(stores_frame)
        stores.insert(0, json.dumps(loadout["Stores"]))
        stores.pack(side=tk.LEFT)

        remove_btn = tk.Button(loadout_frame, text="Remove", command=lambda f=loadout_frame: remove_loadout(f), bg='black', fg='white')
        remove_btn.pack(side=tk.RIGHT)

        if idx > 0:
            up_btn = tk.Button(loadout_frame, text="Up", command=lambda f=loadout_frame: move_loadout_up(f), bg='black', fg='white')
            up_btn.pack(side=tk.RIGHT)

        if idx < len(data["Loadouts"]) - 1:
            down_btn = tk.Button(loadout_frame, text="Down", command=lambda f=loadout_frame: move_loadout_down(f), bg='black', fg='white')
            down_btn.pack(side=tk.RIGHT)

    add_loadout_button = tk.Button(loadouts_frame, text="Add Loadout", command=add_loadout, bg='black', fg='white')
    add_loadout_button.pack(pady=5)

def add_store():
    frame = tk.Frame(allowed_stores_frame, pady=5, bg='black')
    frame.pack(fill=tk.X)
    tk.Label(frame, text="Store: ", bg='black', fg='white').pack(side=tk.LEFT)
    store_name = tk.Entry(frame)
    store_name.pack(side=tk.LEFT)

    tk.Label(frame, text="Max Count Per Station: ", bg='black', fg='white').pack(side=tk.LEFT)
    max_count = tk.Entry(frame)
    max_count.pack(side=tk.LEFT)

    tk.Label(frame, text="Launcher Model Paths: ", bg='black', fg='white').pack(side=tk.LEFT)
    launcher_paths = tk.Entry(frame)
    launcher_paths.pack(side=tk.LEFT)

    remove_btn = tk.Button(frame, text="Remove", command=lambda f=frame: remove_store(f), bg='black', fg='white')
    remove_btn.pack(side=tk.RIGHT)

def add_loadout():
    loadout_frame = tk.Frame(loadouts_frame, pady=10, bg='black')
    loadout_frame.pack(fill=tk.X, pady=10)

    tk.Label(loadout_frame, text="New Loadout", bg='black', fg='white', font=("Arial", 12, "bold")).pack()

    stores_frame = tk.Frame(loadout_frame, bg='black')
    stores_frame.pack(fill=tk.X)

    tk.Label(stores_frame, text="Fuel %: ", bg='black', fg='white').pack(side=tk.LEFT)
    fuel_slider = tk.Scale(stores_frame, from_=0, to=100, orient=tk.HORIZONTAL, bg='black', fg='white')
    fuel_slider.pack(side=tk.LEFT)

    tk.Label(stores_frame, text="Stores: ", bg='black', fg='white').pack(side=tk.LEFT)
    stores = tk.Entry(stores_frame)
    stores.pack(side=tk.LEFT)

    remove_btn = tk.Button(loadout_frame, text="Remove", command=lambda f=loadout_frame: remove_loadout(f), bg='black', fg='white')
    remove_btn.pack(side=tk.RIGHT)

def remove_store(frame):
    frame.destroy()

def remove_loadout(frame):
    frame.destroy()

def move_store_up(frame):
    frame_idx = allowed_stores_frame.winfo_children().index(frame)
    if frame_idx > 0:
        allowed_stores_frame.winfo_children()[frame_idx - 1].pack_forget()
        frame.pack_forget()
        frame.pack(before=allowed_stores_frame.winfo_children()[frame_idx - 1])
        allowed_stores_frame.winfo_children()[frame_idx].pack(before=frame)

def move_store_down(frame):
    frame_idx = allowed_stores_frame.winfo_children().index(frame)
    if frame_idx < len(allowed_stores_frame.winfo_children()) - 1:
        allowed_stores_frame.winfo_children()[frame_idx + 1].pack_forget()
        frame.pack_forget()
        frame.pack(after=allowed_stores_frame.winfo_children()[frame_idx + 1])
        allowed_stores_frame.winfo_children()[frame_idx + 1].pack(after=frame)

def move_loadout_up(frame):
    frame_idx = loadouts_frame.winfo_children().index(frame)
    if frame_idx > 0:
        loadouts_frame.winfo_children()[frame_idx - 1].pack_forget()
        frame.pack_forget()
        frame.pack(before=loadouts_frame.winfo_children()[frame_idx - 1])
        loadouts_frame.winfo_children()[frame_idx].pack(before=frame)

def move_loadout_down(frame):
    frame_idx = loadouts_frame.winfo_children().index(frame)
    if frame_idx < len(loadouts_frame.winfo_children()) - 1:
        loadouts_frame.winfo_children()[frame_idx + 1].pack_forget()
        frame.pack_forget()
        frame.pack(after=loadouts_frame.winfo_children()[frame_idx + 1])
        loadouts_frame.winfo_children()[frame_idx + 1].pack(after=frame)

def save_changes():
    global data
    data["AllowedStores"] = []
    data["Loadouts"] = []

    # Get store data
    for frame in allowed_stores_frame.winfo_children():
        if isinstance(frame, tk.Frame) and hasattr(frame, "store_data"):
            entries = [w for w in frame.winfo_children() if isinstance(w, tk.Entry)]
            if len(entries) == 3:
                store = {
                    "Store": entries[0].get(),
                    "MaxCountPerStation": json.loads(entries[1].get()),
                    "LauncherModelPaths": json.loads(entries[2].get())
                }
                data["AllowedStores"].append(store)

    # Get loadout data
    for frame in loadouts_frame.winfo_children():
        if isinstance(frame, tk.Frame) and hasattr(frame, "loadout_data"):
            stores_frame = [f for f in frame.winfo_children() if isinstance(f, tk.Frame)][0]
            fuel_slider = [w for w in stores_frame.winfo_children() if isinstance(w, tk.Scale)][0]
            stores_entry = [w for w in stores_frame.winfo_children() if isinstance(w, tk.Entry)][0]

            loadout = {
                "Name": frame.loadout_data["Name"],
                "NormalizedFuel": fuel_slider.get() / 100,
                "Stores": json.loads(stores_entry.get())
            }
            data["Loadouts"].append(loadout)

    save_json(data, json_file_path)

# Main window setup
root = tk.Tk()
root.title("JSON Editor")
root.configure(bg='black')

# Create main frames
allowed_stores_frame = tk.Frame(root, bg='black')
allowed_stores_frame.pack(fill=tk.X, padx=10, pady=5)

loadouts_frame = tk.Frame(root, bg='black')
loadouts_frame.pack(fill=tk.X, padx=10, pady=5)

# Create button frame for Load JSON, Save, and Save As
button_frame = tk.Frame(root, bg='black')
button_frame.pack(fill=tk.X, padx=10, pady=5)

load_button = tk.Button(button_frame, text="Load JSON", command=load_json_file, bg='black', fg='white')
load_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Save", command=save_changes, bg='black', fg='white')
save_button.pack(side=tk.LEFT, padx=5)

save_as_button = tk.Button(button_frame, text="Save As", command=save_as, bg='black', fg='white')
save_as_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
