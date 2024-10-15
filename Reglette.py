import tkinter as tk
from tkinter import ttk

class SliderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slider Example")

        # Slider horizontal
        self.h_slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=self.on_slider_change)
        self.h_slider.pack(fill='x', padx=10, pady=10)

        # Label to display the value of the horizontal slider
        self.h_value_label = ttk.Label(root, text="Horizontal Slider Value: 0")
        self.h_value_label.pack()

        # Slider vertical
        self.v_slider = ttk.Scale(root, from_=0, to=100, orient='vertical', command=self.on_slider_change)
        self.v_slider.pack(side='left', fill='y', padx=10, pady=10)

        # Label to display the value of the vertical slider
        self.v_value_label = ttk.Label(root, text="Vertical Slider Value: 0")
        self.v_value_label.pack(side='left')

    def on_slider_change(self, value):
        self.h_value_label.config(text=f"Horizontal Slider Value: {int(self.h_slider.get())}")
        self.v_value_label.config(text=f"Vertical Slider Value: {int(self.v_slider.get())}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SliderApp(root)
    root.mainloop()
