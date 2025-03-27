import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import keyboard
import pyperclip
from utils import resource_path
from summarizer import summarize_text

class FloatingPen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart Summarizer")
        self.geometry("400x300")
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background='white')

        self.main_frame = ttk.Frame(self, style="Custom.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_pen_icon()
        self.create_text_area()
        self.create_menu()

        self.configure(bg='white')
        self.attributes('-alpha', 1.0)
        self.attributes('-transparentcolor', 'white')

    def setup_pen_icon(self):
        image_path = resource_path("assets/pen.png")
        self.pen_image = Image.open(image_path).convert("RGBA")
        self.pen_image = self.pen_image.resize((100, 100), Image.Resampling.LANCZOS)
        self.pen_photo = ImageTk.PhotoImage(self.pen_image)

        self.pen_label = tk.Label(self.main_frame, image=self.pen_photo, bg='white')
        self.pen_label.pack(fill=tk.BOTH, expand=True)
        self.pen_label.bind('<Enter>', self.on_hover_enter)
        self.pen_label.bind('<Leave>', self.on_hover_leave)
        self.pen_label.bind("<Button-3>", self.on_right_click)
        self.pen_label.bind("<Button-1>", self.start_drag)
        self.pen_label.bind("<B1-Motion>", self.drag)

    def create_text_area(self):
        self.text_area = tk.Text(
            self.main_frame,
            height=15,
            width=50,
            wrap=tk.WORD,
            font=('Helvetica', 12),
            bg='#f5f5f5',
            fg='#333333',
            padx=10,
            pady=10,
            relief="flat",
            borderwidth=0
        )
        self.text_area.pack_forget()

    def create_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.configure(font=('Helvetica', 10), bg='#ffffff', fg='#333333', relief="flat")
        self.menu.add_command(label="✨ Summarize", command=self.show_message)
        self.menu.add_command(label="🎯 Hide Summary", command=self.hide_text_area)
        self.menu.add_command(label="❌ Cancel", command=self.cancel_action)
        self.menu.add_command(label="🚫 Stop", command=self.stop_application)

    def show_message(self):
        keyboard.send('ctrl+c')
        self.after(200, self.process_clipboard_text)

    def process_clipboard_text(self):
        selected_text = pyperclip.paste()
        if selected_text.strip():
            summary = summarize_text(selected_text)
            self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, summary)
        else:
            self.show_error("No text selected!")

    def show_error(self, message):
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Error: {message}")

    def on_right_click(self, event):
        self.menu.post(event.x_root, event.y_root)

    def start_drag(self, event):
        global offset_x, offset_y
        offset_x = event.x
        offset_y = event.y

    def drag(self, event):
        x = self.winfo_pointerx() - offset_x
        y = self.winfo_pointery() - offset_y
        self.geometry(f"+{x}+{y}")

    def cancel_action(self):
        self.menu.unpost()

    def hide_text_area(self):
        self.text_area.pack_forget()

    def stop_application(self):
        self.destroy()

    def on_hover_enter(self, event):
        """Handle hover enter event."""
        self.pen_label.config(bg='white')  # Change background color on hover

    def on_hover_leave(self, event):
        """Handle hover leave event."""
        self.pen_label.config(bg='white')  # Revert background color
