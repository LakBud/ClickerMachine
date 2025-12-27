import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import tkinter as tk
from tkinter import font, messagebox


# ---------------------------------------LOGIC-----------------------------------------

clicking = False
mouse = Controller()
toggle_key = KeyCode(char="t") # Default is "t"


def click_loop(cps):
    global clicking
    interval = 1 / cps if cps > 0 else 0.1
    
    while clicking:
        mouse.click(Button.left, 1)
        time.sleep(interval)


def start_clicking(cps):
    global clicking
    
    if clicking:
        return
    
    clicking = True
    threading.Thread(target=click_loop, args=(cps,), daemon=True).start()

def stop_clicking():
    global clicking
    clicking = False
    run_button.config(state=tk.NORMAL)

def on_start():
    try:
        cps = float(interval_input.get())
        
        if cps <= 0 or cps > 100:
            raise ValueError
        
        start_clicking(cps)
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a positive number within 1-99 CPS")

# Toggle clicking using hotkey
def toggle_clicking(key):
    
    if key == toggle_key:
        
        if clicking:
            stop_clicking()
        else:
            try:
                on_start()
                
            except ValueError:
                pass  # ignore invalid input

# Start keyboard listener in background thread
def start_hotkey_listener():
    listener = Listener(on_press=toggle_clicking)
    listener.daemon = True
    listener.start()

def update_toggle_key():
    global toggle_key
    char = toggle_entry.get().strip()
    
    if len(char) != 1:
        messagebox.showerror("Invalid Input", "Enter a single character for toggle key.")
        return
    
    toggle_key = KeyCode(char=char.lower())
    messagebox.showinfo("Success", f"Toggle key updated to '{char}'")

# ---------------------------------------GUI-----------------------------------------

def main():
    global run_button, interval_input, toggle_entry

    root = tk.Tk()
    root.geometry("300x350")
    root.title("ClickerMachine")
    root.resizable(False, False)
    root.configure(bg="#2c3e50")

    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Arial")

    # Header
    main_header = tk.Label(root, text="ClickerMachine", font=("Arial", 20))
    main_header.pack(padx=10, pady=10)

    main_frame = tk.Frame(root, bg="#273440")
    main_frame.pack(padx=10, pady=10)

    # CPS input
    interval_frame = tk.Frame(main_frame)
    interval_frame.pack(padx=10, pady=10)

    interval_label = tk.Label(interval_frame, text="Clicks per Second (CPS):")
    interval_label.pack()

    interval_input = tk.Entry(interval_frame)
    interval_input.pack()
    interval_input.insert(0, "10")

    # Toggle key input
    key_frame = tk.Frame(main_frame, bg="#273440")
    key_frame.pack(pady=5)

    key_label = tk.Label(key_frame, text="Toggle Key (press a single character):")
    key_label.pack()
    toggle_entry = tk.Entry(key_frame)
    toggle_entry.pack()
    toggle_entry.insert(0, "t")  # default

    update_key_button = tk.Button(key_frame, text="Set Toggle Key", command=update_toggle_key)
    update_key_button.pack(pady=5)

    # Control Buttons
    control_frame = tk.Frame(main_frame, bg="#273440")
    control_frame.pack(pady=20)

    run_button = tk.Button(control_frame, text="Start", command=on_start)
    run_button.pack(side=tk.LEFT, padx=10)

    disable_button = tk.Button(control_frame, text="Stop", command=stop_clicking)
    disable_button.pack(side=tk.LEFT, padx=10)

    start_hotkey_listener()
    root.mainloop()


if __name__ == "__main__":
    main()