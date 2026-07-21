import tkinter as tk
import subprocess
import os
import time

# [KUNCI FIX 1: Suntikkan Otorisasi Keamanan X11 untuk OS BARU]
# Ini memaksa Python mengetahui monitor mana yang dipakai dan di mana kuncinya
os.environ["DISPLAY"] = ":0"
os.environ["XAUTHORITY"] = "/root/.Xauthority"

class OtoskopKamera:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Otoskop Medis V3")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#121212') 
        # Matikan kursor agar terlihat pro
        self.root.config(cursor="none") 

        # =========================================
        # 1. LAYOUT: BELAH LAYAR KIRI DAN KANAN
        # =========================================
        # Frame Video di Kiri (Hitam pekat)
        self.video_frame = tk.Frame(root, bg='black')
        self.video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame Kontrol di Kanan (Abu-abu gelap mewah)
        self.control_frame = tk.Frame(root, bg='#1E1E1E', width=250)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.control_frame.pack_propagate(False)

        # =========================================
        # 2. INJEKSI VIDEO MPV DENGAN JEDA RENDER
        # =========================================
        # [KUNCI FIX 2: Jeda Render Mutlak]
        # Tanpa Window Manager, kita harus memberi jeda agar bingkai grafis
        # benar-benar siap secara fisik sebelum mpv menempel.
        self.root.update_idletasks()
        self.root.update()
        time.sleep(1.0) # Jeda 1 detik agar aman dari blank screen
        
        # Ambil Window ID setelah jeda
        self.wid = self.video_frame.winfo_id()
        self.mpv_process = None
        
        # Bantai mpv hantu yang mungkin masih nyangkut
        os.system("killall -9 mpv 2>/dev/null") 
        os.system("rm -f /tmp/mpvsocket")
        time.sleep(0.3) 
        
        # Nyalakan mata kamera
        self.jalankan_kamera()

        # =========================================
        # 3. BANGUN TOMBOL VISUAL MEDIS
        # =========================================
        self.label_buttons = []
        self.selected_index = 0 
        self.buat_panel_kontrol()

        # Binding Kontrol Keyboard
        self.root.bind_all("<Up>", self.navigasi_atas)
        self.root.bind_all("<Down>", self.navigasi_bawah)
        self.root.bind_all("<Return>", self.eksekusi_pilihan)
        
        # Loop pengunci fokus mutlak
        self.paku_fokus_loop()
        # Perbarui tampilan selektor
        self.update_visual_selektor()

    def paku_fokus_loop(self):
        self.root.focus_force()
        self.root.after(200, self.paku_fokus_loop)

    def jalankan_kamera(self):
        # Konfigurasi MPV performa tinggi untuk RPi Zero 2 W
        cmd = [
            "mpv",
            "av://v4l2:/dev/video0",
            "--profile=low-latency",
            "--untimed",
            "--vo=gpu",
	    #"--geometry=774x600+0+0",
	    #"--border=no",
	    #"--ontop", # Gunakan Vo=gpu untuk performa mjpeg terbaik
            f"--wid={self.wid}", # Tempelkan video ke Window ID Tkinter
            "--input-ipc-server=/tmp/mpvsocket",
            "--demuxer-lavf-o=video_size=640x480,input_format=mjpeg",
            "--vd-lavc-threads=3",
            "--cache=no",
            "--screenshot-dir=/home/home",
            "--screenshot-format=jpg",
            "--screenshot-template=foto_medis_%M%S",
            "--msg-level=all=status,demux=error",
            "--input-default-bindings=no", 
            "--input-vo-keyboard=no",      
            "--osd-level=0",
            "--no-osc",      
            "--no-osd-bar",  
            "--config=no"    
        ]
        # Jalankan mpv di latar belakang tanpa memblokir Python
        self.mpv_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def buat_panel_kontrol(self):
        tk.Label(self.control_frame, text="PANEL MEDIS", fg="#00FF00", bg="#1E1E1E", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Bergaya ATM/Mesin ATM (Raised Relief)
        lbl_capture = tk.Label(self.control_frame, text="📸 AMBIL FOTO", font=("Helvetica", 12, "bold"), height=2, bd=2, relief="raised")
        lbl_capture.pack(fill=tk.X, padx=10, pady=10)
        self.label_buttons.append(lbl_capture)

        lbl_zoom_in = tk.Label(self.control_frame, text="🔍 ZOOM IN (+)", font=("Helvetica", 12), height=2, bd=2, relief="raised")
        lbl_zoom_in.pack(fill=tk.X, padx=10, pady=5)
        self.label_buttons.append(lbl_zoom_in)

        lbl_zoom_out = tk.Label(self.control_frame, text="🔎 ZOOM OUT (-)", font=("Helvetica", 12), height=2, bd=2, relief="raised")
        lbl_zoom_out.pack(fill=tk.X, padx=10, pady=5)
        self.label_buttons.append(lbl_zoom_out)

        # Tombol tutup ditaruh di paling bawah frame kontrol
        lbl_quit = tk.Label(self.control_frame, text="TUTUP KAMERA", font=("Helvetica", 12), height=2, bd=2, relief="raised")
        lbl_quit.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=20)
        self.label_buttons.append(lbl_quit)

    def update_visual_selektor(self):
        # Skema hover warna: Putih salju saat dipilih
        for index, label in enumerate(self.label_buttons):
            if index == self.selected_index:
                label.configure(bg='#FFFFFF', fg='#000000')
            else:
                # Abu-abu gelap saat dilepas
                label.configure(bg='#333333', fg='#FFFFFF')

    def navigasi_atas(self, event=None):
        self.selected_index = (self.selected_index - 1) % len(self.label_buttons)
        self.update_visual_selektor()

    def navigasi_bawah(self, event=None):
        self.selected_index = (self.selected_index + 1) % len(self.label_buttons)
        self.update_visual_selektor()

    def eksekusi_pilihan(self, event=None):
        # State mesin untuk eksekusi tombol
        if self.selected_index == 0:
            # Perintah Ambil Foto (Screenshot mpv)
            waktu_sekarang = time.strftime("%H%M%S")
            nama_file = f"/home/home/foto_medis_{waktu_sekarang}.jpg"
            cmd = f"echo '{{ \"command\": [\"screenshot-to-file\", \"{nama_file}\", \"video\"] }}' | socat - /tmp/mpvsocket"
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif self.selected_index == 1:
            # Perintah Zoom In
            cmd = "echo '{ \"command\": [\"add\", \"video-zoom\", 0.2] }' | socat - /tmp/mpvsocket"
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif self.selected_index == 2:
            # Perintah Zoom Out
            cmd = "echo '{ \"command\": [\"add\", \"video-zoom\", -0.2] }' | socat - /tmp/mpvsocket"
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif self.selected_index == 3:
            # Perintah Tutup dan Hancurkan antarmuka
            self.tutup_aplikasi()

    def tutup_aplikasi(self):
        # Bersihkan mpv sebelum menutup jendela Python
        if self.mpv_process:
            self.mpv_process.terminate()
            subprocess.Popen("killall -9 mpv 2>/dev/null", shell=True)
        # Hancurkan jendela Tkinter (membuat subprocess.run di menu utama selesai)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = OtoskopKamera(root)
    root.mainloop()
