import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Variables
currentDir = os.path.abspath(os.getcwd())  
assetsDir = os.path.join(currentDir, 'assets')  
binariesDirPath = os.path.join(assetsDir, 'bin')  

ffmpeg_updater_file = os.path.join(currentDir, 'ffmpeg_updater.exe')  
ytdlp_updater_file = os.path.join(currentDir, 'ytdlp_updater.exe')  
ytblp_exe_file = os.path.join(binariesDirPath, 'yt-dlp.exe')  

exe_updaters= [ffmpeg_updater_file, ytdlp_updater_file]

def actualizar_binarios(binArray):
    for run_exe_update in binArray:
        process = subprocess.Popen(run_exe_update, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process.wait()
    messagebox.showinfo("Éxito", "Binarios actualizados con éxito.")

def ejecutar_comando(ytdlp_path_input):
    urls = url_text.get("1.0", tk.END).strip().split("\n")
    
    if not urls or urls == ['']:
        messagebox.showwarning("Advertencia", "Por favor, introduce al menos una URL para continuar.")
        return

    for index, url in enumerate(urls):
        cmd = [
            ytdlp_path_input,
            "--ignore-errors",
            "--format", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", calidad_audio_var.get(),
            "--output", os.path.join(directorio_salida_var.get(), "%(title)s.%(ext)s"),
            "--yes-playlist",
            url
        ]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", f"Hubo un error al procesar la URL: {url}. El proceso continuará con las siguientes URLs.")
        
        # Actualizar la Progressbar
        progress_percentage = (index + 1) * 100 / len(urls)
        progress_var.set(progress_percentage)
        app.update_idletasks()

    messagebox.showinfo("Éxito", "Todos los comandos han sido ejecutados.")

app = tk.Tk()
app.title("Interfaz para yt-dlp")
app.geometry("800x600")
app.minsize(640, 480)
app.maxsize(800, 600)

directorio_salida_var = tk.StringVar()
calidad_audio_var = tk.StringVar(value="128K")

tk.Label(app, text="URLs de los videos o playlists (una por línea):").pack(pady=10)
text_frame = tk.Frame(app)
text_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

url_text = tk.Text(text_frame, height=10, width=50, wrap=tk.NONE)
url_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(text_frame, command=url_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
url_text.config(yscrollcommand=scrollbar.set)

tk.Label(app, text="Directorio de salida:").pack(pady=10)
directorio_frame = tk.Frame(app)
directorio_frame.pack(pady=5, padx=10, fill=tk.X)
tk.Entry(directorio_frame, textvariable=directorio_salida_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
tk.Button(directorio_frame, text="Buscar", command=lambda: directorio_salida_var.set(filedialog.askdirectory())).pack(side=tk.RIGHT)

tk.Label(app, text="Calidad de audio:").pack(pady=10)
ttk.Combobox(app, values=["128K", "192K", "256K", "320K"], textvariable=calidad_audio_var, state='readonly').pack(pady=5, padx=10)

# Crear un frame para contener los botones
button_frame = tk.Frame(app)
button_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)

# Añadir la Progressbar al button_frame
progress_var = tk.DoubleVar()  
progress_bar = ttk.Progressbar(button_frame, variable=progress_var, maximum=100, mode='determinate', length=300)
progress_bar.grid(row=0, column=1, pady=10, padx=10)  

# Botón "Actualizar Binarios"
update_btn = tk.Button(button_frame, 
                       text="Actualizar Binarios", 
                       command=lambda: actualizar_binarios(exe_updaters),
                       height=2, 
                       width=20, 
                       bg="#FF5733", 
                       fg="white", 
                       font=("Arial", 12, "bold"), 
                       borderwidth=5, 
                       relief="raised")
update_btn.grid(row=0, column=0, padx=10, pady=10)

# Botón "Ejecutar"
execute_btn = tk.Button(button_frame, 
                        text="Ejecutar", 
                        command=lambda: ejecutar_comando(ytblp_exe_file),
                        height=2, 
                        width=15, 
                        bg="#007ACC", 
                        fg="white", 
                        font=("Arial", 12, "bold"), 
                        borderwidth=5, 
                        relief="raised")
execute_btn.grid(row=0, column=2, padx=10, pady=10)

app.mainloop()
