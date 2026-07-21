import tkinter as tk
import subprocess
import os
import time
import glob

os.environ["DISPLAY"] = ":0"
os.environ["XAUTHORITY"] = "/root/.Xauthority"

class OtoskopMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Otoskop Medis V3 - Menu")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#0F172A') 
        self.root.config(cursor="arrow")

        self.root.bind_all("<Up>", self.on_up)
        self.root.bind_all("<Down>", self.on_down)
        self.root.bind_all("<Return>", self.on_enter)

        self.menu_options = [
            "📸   Live Kamera Otoskop", 
            "🖼️   Buka Galeri Observasi", 
            "🗑️   Hapus Semua Foto", 
            "🔄   Restart Perangkat", 
            "⏻   Matikan Perangkat"
        ]
        self.menu_labels = []
        self.menu_index = 0

        self.build_ui()
        self.update_clock()
        self.paku_fokus()

    def paku_fokus(self):
        self.root.focus_force()
        self.root.after(500, self.paku_fokus)

    def build_ui(self):
        header_frame = tk.Frame(self.root, bg='#0F172A')
        header_frame.pack(fill=tk.X, pady=(40, 20))
        
        tk.Label(header_frame, text="SISTEM OTOSKOP MEDIS", fg="#38BDF8", bg="#0F172A", font=("Helvetica", 28, "bold")).pack()
        tk.Label(header_frame, text="Teknologi Kedokteran ITS", fg="#94A3B8", bg="#0F172A", font=("Helvetica", 14)).pack(pady=(5, 0))

        main_container = tk.Frame(self.root, bg='#0F172A')
        main_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        menu_frame = tk.Frame(main_container, bg='#0F172A')
        menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        tk.Label(menu_frame, text="PILIHAN MENU", fg="#F8FAFC", bg="#0F172A", font=("Helvetica", 12, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 10))

        for opt in self.menu_options:
            btn_lbl = tk.Label(menu_frame, text=opt, fg="#F8FAFC", bg="#1E293B", font=("Helvetica", 16, "bold"), anchor="w", padx=20, pady=15, bd=0, relief="flat")
            btn_lbl.pack(fill=tk.X, pady=8)
            self.menu_labels.append(btn_lbl)

        # FIX 1: ipadx dan ipady disesuaikan agar memberikan ruang vertikal yang cukup
        info_frame = tk.Frame(main_container, bg='#1E293B', bd=0, relief="flat")
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, ipadx=40, ipady=10) 

        tk.Label(info_frame, text="STATUS SISTEM", fg="#38BDF8", bg="#1E293B", font=("Helvetica", 14, "bold")).pack(pady=(20, 30))

        self.lbl_time = tk.Label(info_frame, text="00:00", fg="#F8FAFC", bg="#1E293B", font=("Helvetica", 42, "bold"))
        self.lbl_time.pack()
        self.lbl_date = tk.Label(info_frame, text="Senin, 01 Jan 2026", fg="#94A3B8", bg="#1E293B", font=("Helvetica", 14))
        self.lbl_date.pack(pady=(0, 30))

        stat_box = tk.Frame(info_frame, bg='#0F172A', padx=20, pady=20)
        stat_box.pack(fill=tk.X, padx=20)
        tk.Label(stat_box, text="Total Observasi", fg="#94A3B8", bg="#0F172A", font=("Helvetica", 12)).pack()
        self.lbl_total_obs = tk.Label(stat_box, text="0", fg="#32CD32", bg="#0F172A", font=("Helvetica", 36, "bold"))
        self.lbl_total_obs.pack()

        # FIX 2: Teks panduan kontrol dipadatkan dan pady dikurangi agar tidak terpotong layar
        tk.Label(info_frame, text="Panduan Kontrol:\nNavigasi :  [↑] [↓]\nPilih Menu :  [ENTER]\nKeluar Galeri :  [Q]", fg="#64748B", bg="#1E293B", font=("Helvetica", 11), justify=tk.LEFT).pack(side=tk.BOTTOM, pady=15)

        self.update_menu_visual()

    def update_clock(self):
        self.lbl_time.config(text=time.strftime("%H:%M:%S"))
        self.lbl_date.config(text=time.strftime("%d-%m-%Y"))
        self.lbl_total_obs.config(text=f"{len(glob.glob('/home/home/*.jpg'))}")
        self.root.after(1000, self.update_clock)

    def update_menu_visual(self):
        for i, lbl in enumerate(self.menu_labels):
            if i == self.menu_index:
                lbl.config(bg="#38BDF8", fg="#0F172A") 
            else:
                lbl.config(bg="#1E293B", fg="#F8FAFC")

    def on_up(self, event=None):
        self.menu_index = (self.menu_index - 1) % len(self.menu_options)
        self.update_menu_visual()

    def on_down(self, event=None):
        self.menu_index = (self.menu_index + 1) % len(self.menu_options)
        self.update_menu_visual()

    def on_enter(self, event=None):
        if self.menu_index == 0: 
            self.root.withdraw() 
            self.root.update()
            subprocess.run(["/usr/bin/python3", "/home/home/kamera_medis.py"])
            self.root.deiconify() 
            self.root.focus_force() 
            
        elif self.menu_index == 1: 
            if not glob.glob("/home/home/*.jpg"):
                return
            self.root.withdraw()
            self.root.update()
            subprocess.run(["/usr/bin/feh", "-F", "-Z", "-Y", "--sort", "filename", "/home/home/"])
            self.root.deiconify()
            self.root.focus_force()
            
        elif self.menu_index == 2: 
            os.system("rm -f /home/home/*.jpg")
            self.lbl_total_obs.config(text="0")
            
        elif self.menu_index == 3: 
            os.system("sudo reboot")
            
        elif self.menu_index == 4: 
            os.system("sudo poweroff")

if __name__ == "__main__":
    root = tk.Tk()
    app = OtoskopMenu(root)
    root.mainloop()
