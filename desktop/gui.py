import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import keyboard
import pyperclip
import math
from utils import resource_path
from summarizer import summarize_text

class FloatingPen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart Summarizer")
        self.geometry("400x300")
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Animation-related attributes
        self.hover_scale = 1.0
        self.opacity = 1.0
        self.fade_direction = -1

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

        # Start hover animation
        self.animate_hover()

    def setup_pen_icon(self):
        image_path = resource_path("assets/pen.png")
        self.pen_image = Image.open(image_path).convert("RGBA")
        self.original_pen_image = self.pen_image.copy()
        self.pen_image = self.pen_image.resize((100, 100), Image.Resampling.LANCZOS)
        self.pen_photo = ImageTk.PhotoImage(self.pen_image)

        self.pen_label = tk.Label(self.main_frame, image=self.pen_photo, bg='white')
        self.pen_label.pack(fill=tk.BOTH, expand=True)
        self.pen_label.bind('<Enter>', self.on_hover_enter)
        self.pen_label.bind('<Leave>', self.on_hover_leave)
        self.pen_label.bind("<Button-3>", self.on_right_click)
        self.pen_label.bind("<Button-1>", self.start_drag)
        self.pen_label.bind("<B1-Motion>", self.drag)

    def animate_hover(self):
        """Animate subtle hover effect for the pen icon."""
        # Subtle scaling and fading animation
        self.hover_scale += 0.02 * (1.1 - self.hover_scale)
        
        # Resize the image
        resized_width = int(100 * self.hover_scale)
        resized_height = int(100 * self.hover_scale)
        resized_image = self.original_pen_image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
        self.pen_photo = ImageTk.PhotoImage(resized_image)
        self.pen_label.config(image=self.pen_photo)

        # Subtle fading effect
        self.opacity += 0.05 * self.fade_direction
        if self.opacity <= 0.7:
            self.fade_direction = 1
        elif self.opacity >= 1.0:
            self.fade_direction = -1
        
        self.attributes('-alpha', self.opacity)

        # Schedule next animation frame
        self.after(50, self.animate_hover)

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
            borderwidth=0,
            insertbackground='#333333'  # Add a cursor color
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
        # Animate text area appearance
        keyboard.send('ctrl+c')
        self.after(200, self.process_clipboard_text)

    def process_clipboard_text(self):
        selected_text = pyperclip.paste()
        if selected_text.strip():
            summary = summarize_text(selected_text)
            
            # Animate text area appearance
            self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.text_area.delete(1.0, tk.END)
            
            # Animate text insertion
            self.animate_text_insertion(summary)
        else:
            self.show_error("No text selected!")

    def animate_text_insertion(self, text):
        """Animate text insertion character by character."""
        def insert_char(idx=0):
            if idx < len(text):
                self.text_area.insert(tk.END, text[idx])
                self.after(20, lambda: insert_char(idx + 1))
        
        insert_char()

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
        # Animate text area disappearance
        def fade_out(alpha=1.0):
            if alpha > 0:
                self.text_area.configure(bg=self.blend_colors('#f5f5f5', 'white', alpha))
                self.after(20, lambda: fade_out(alpha - 0.1))
            else:
                self.text_area.pack_forget()
        
        fade_out()

    def stop_application(self):
        # Animate application closure
        def fade_out(alpha=1.0):
            if alpha > 0:
                self.attributes('-alpha', alpha)
                self.after(20, lambda: fade_out(alpha - 0.1))
            else:
                self.destroy()
        
        fade_out()

    def blend_colors(self, color1, color2, ratio):
        """Helper method to blend two colors."""
        def parse_color(color):
            # Handle named colors and hex colors
            color_map = {
                'white': '#FFFFFF',
                'black': '#000000',
                'red': '#FF0000',
                # Add more named colors as needed
            }
            
            # Use the color map if it's a named color
            if color.lower() in color_map:
                color = color_map[color.lower()]
            
            # Remove hash if present
            color = color.lstrip('#')
            
            # Pad with zeros if needed
            color = color.zfill(6)
            
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

        r1, g1, b1 = parse_color(color1)
        r2, g2, b2 = parse_color(color2)
        
        r = int(r1 * ratio + r2 * (1 - ratio))
        g = int(g1 * ratio + g2 * (1 - ratio))
        b = int(b1 * ratio + b2 * (1 - ratio))
        
        return f'#{r:02x}{g:02x}{b:02x}'

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB."""
        # Deprecated - using parse_color in blend_colors instead
        return self.parse_color(hex_color)

    # def hex_to_rgb(self, hex_color):
    #     """Convert hex color to RGB."""
    #     hex_color = hex_color.lstrip('#')
    #     return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def on_hover_enter(self, event):
        """Handle hover enter event with scaling animation."""
        self.hover_scale = 1.1
        self.fade_direction = 1

    def on_hover_leave(self, event):
        """Handle hover leave event with scaling animation."""
        self.hover_scale = 1.0
        self.fade_direction = -1