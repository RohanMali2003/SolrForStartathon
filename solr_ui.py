import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import subprocess
import json

def run_solr_connector():
    hostname = hostname_entry.get().strip() or "localhost"
    port = port_entry.get().strip() or "8983"
    core = core_entry.get().strip() or "mycore"

    try:
        result = subprocess.run(
            ["python", "solr_connector.py"],
            input=f"{hostname}\n{port}\n{core}\n",
            text=True,
            capture_output=True,
            check=True
        )
        messagebox.showinfo("Success", "Solr Connector executed successfully! Click 'View JSON' to see the generated data.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Execution failed: {e.stderr}")

def view_json():
    try:
        with open("solr_metadata.json", "r") as file:
            json_data = json.load(file)
        
        json_window = tk.Toplevel(root)
        json_window.title("Generated JSON Data")
        json_window.geometry("500x400")
        
        text_area = scrolledtext.ScrolledText(json_window, wrap=tk.WORD, width=150, height=40)
        text_area.insert(tk.END, json.dumps(json_data, indent=4))
        text_area.config(state=tk.DISABLED)
        text_area.pack(padx=10, pady=10)
    except FileNotFoundError:
        messagebox.showerror("Error", "solr_metadata.json not found! Run the connector first (or again).")

# Creating the Tkinter window
root = tk.Tk()
root.title("Solr Configuration UI")
root.geometry("400x400")

# Labels and Entry Fields
tk.Label(root, text="Solr Hostname:").pack(pady=5)
hostname_entry = tk.Entry(root, width=30)
hostname_entry.pack()
hostname_entry.insert(0, "localhost")

tk.Label(root, text="Solr Port:").pack(pady=5)
port_entry = tk.Entry(root, width=30)
port_entry.pack()
port_entry.insert(0, "8983")

tk.Label(root, text="Solr Core Name:").pack(pady=5)
core_entry = tk.Entry(root, width=30)
core_entry.pack()
core_entry.insert(0, "my_core")

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

tk.Button(button_frame, text="Run Solr Connector", command=run_solr_connector).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="View JSON", command=view_json).pack(side=tk.RIGHT, padx=10)

# Run the Tkinter loop
root.mainloop()