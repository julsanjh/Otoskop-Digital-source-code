import tkinter as tk
import os

os.environ["DISPLAY"] = ":0"
os.environ["XAUTHORITY"] = "/root/.Xauthority"

class LayarLoading:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#050B14') 
        self.root.config(cursor="none")

        # Jarak dari atas
        tk.Frame(root, bg='#050B14', height=120).pack(fill=tk.X)

        # Elemen Teks
        tk.Label(root, text="SISTEM OTOSKOP MEDIS", fg="#38BDF8", bg="#050B14", font=("Helvetica", 32, "bold")).pack(pady=15)
        self.lbl_status = tk.Label(root, text="Inisialisasi Kernel Linux...", fg="#94A3B8", bg="#050B14", font=("Helvetica", 14))
        self.lbl_status.pack(pady=10)

        # Bingkai Progress Bar (Lebar 500px)
        self.canvas = tk.Canvas(root, width=500, height=6, bg="#1E293B", highlightthickness=0)
        self.canvas.pack(pady=40)

        # Batang Progress (Awalnya lebar 0)
        self.rect = self.canvas.create_rectangle(0, 0, 0, 6, fill="#38BDF8")
        
        self.progress = 0
        self.update_progress()

    def update_progress(self):
        self.progress += 1
        
        if self.progress == 30:
            self.lbl_status.config(text="Memuat Modul Sensor Kamera...")
        elif self.progress == 60:
            self.lbl_status.config(text="Menghubungkan Mesin Grafis X11...")
        elif self.progress == 90:
            self.lbl_status.config(text="Memulai Antarmuka Medis...", fg="#00FF00")

        self.canvas.coords(self.rect, 0, 0, self.progress * 5, 6)
        
        if self.progress < 100:
            self.root.after(30, self.update_progress) 
        else:
            self.root.after(500, self.root.destroy) 

if __name__ == "__main__":
    root = tk.Tk()
    app = LayarLoading(root)
    root.mainloop()
