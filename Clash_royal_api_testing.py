import tkinter as tk
from tkinter import ttk
import requests
import json
from PIL import Image, ImageTk
import io

# Read the API token from a file
with open("clash_api_token.txt", "r") as file:
    API_TOKEN = file.read().strip()

def fetch_json_response(api_token, player_tag):
    """Fetch player data using the provided tag"""
    url = f"https://api.clashroyale.com/v1/players/%23{player_tag}"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def create_gui():
    root = tk.Tk()
    root.title("Clash Royale API Tester")

    # Create widgets
    tag_entry = tk.Entry(root)
    tag_entry.pack(pady=5)

    selected_option = tk.StringVar()
    dropdown = ttk.Combobox(root, textvariable=selected_option, state="readonly")
    dropdown.pack(pady=5)

    result_text = tk.Text(root, height=10, width=40)
    result_text.pack(pady=5)

    def refresh_data():
        """Handle button click: fetch data and update UI"""
        result_text.delete("1.0", tk.END)
        
        # Get player tag from entry
        player_tag = tag_entry.get().strip()
        if not player_tag:
            result_text.insert(tk.END, "Please enter a player tag")
            return

        try:
            # Fetch new data
            data = fetch_json_response(API_TOKEN, player_tag)
            keys = list(data.keys())
            
            # Update dropdown
            dropdown['values'] = keys
            if keys:
                selected_option.set(keys[0])
            
            # Store data for display
            result_text.data = data

        except Exception as e:
            result_text.insert(tk.END, f"Error: {str(e)}")

    def show_selected():
        """Display selected information from dropdown"""
        if not hasattr(result_text, 'data'):
            return
            
        result_text.delete("1.0", tk.END)
        key = selected_option.get()
        info = result_text.data.get(key, "No data available")

        if isinstance(info, bytes):
            image = Image.open(io.BytesIO(info))
            photo = ImageTk.PhotoImage(image)
            img_label = tk.Label(root, image=photo)
            img_label.image = photo
            img_label.pack()
        else:
            result_text.insert(tk.END, json.dumps(info, indent=2))

    # Button to fetch data
    fetch_btn = tk.Button(root, text="Fetch Data", command=refresh_data)
    fetch_btn.pack(side=tk.LEFT, padx=5)

    # Button to show selected info
    show_btn = tk.Button(root, text="Show Info", command=show_selected)
    show_btn.pack(side=tk.RIGHT, padx=5)

    root.mainloop()

create_gui()