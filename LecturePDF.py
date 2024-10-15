import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import fitz  # PyMuPDF

class PDFViewer(tk.Tk):
    def __init__(self, pdf_path):
        super().__init__()
        self.title("Visualisation PDF")
        self.geometry("800x600")

        # Charger le PDF
        self.doc = fitz.open(pdf_path)
        self.current_page = 0

        # Canvas pour afficher l'image
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack()

        # Boutons pour navigation
        prev_button = tk.Button(self, text="Page Précédente", command=self.prev_page)
        prev_button.pack(side=tk.LEFT, padx=10)

        next_button = tk.Button(self, text="Page Suivante", command=self.next_page)
        next_button.pack(side=tk.RIGHT, padx=10)

        # Afficher la première page
        self.show_page()

    def render_page(self, page_num):
        """Rend une page du PDF en image"""
        page = self.doc.load_page(page_num)
        pix = page.get_pixmap()  # Convertit la page en image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img

    def show_page(self):
        """Affiche la page actuelle dans le canvas Tkinter"""
        img = self.render_page(self.current_page)
        img = img.resize((800, 600), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def next_page(self):
        """Passe à la page suivante si disponible"""
        if self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.show_page()

    def prev_page(self):
        """Revient à la page précédente si disponible"""
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

def open_pdf():
    """Ouvre un fichier PDF et lance la visualisation"""
    filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if filepath:
        viewer = PDFViewer(filepath)
        viewer.mainloop()

if __name__ == "__main__":
    open_pdf()
