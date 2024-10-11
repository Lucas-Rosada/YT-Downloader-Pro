import customtkinter as ctk
import yt_dlp as youtube_dl
import threading

# variavel cancelamento
cancelar_download = False

# função baixar video ou adio
def baixar_midia(url, formato):
    global cancelar_download
    cancelar_download = False  # Reseta o cancelamento a cada nova tentativa

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if formato == 'mp4' else 'bestaudio',  # Garante o download com vídeo e áudio
        'outtmpl': '%(title)s.' + formato,  # Salva o arquivo + nome do video
        'merge_output_format': formato  # garante que seja m4 ou m3 o formato final
    }

    # Função interna para controlar o cancelamento e atualizar o log com progresso
    def hook(d):
        if d['status'] == 'downloading':
            percent = d['_percent_str']
            velocidade = d['_speed_str']
            tamanho_total = d['_total_bytes_str']
            tempo_restante = d['_eta_str']
            
            # Atualizando a caixa de logs com a porcentagem
            log_text.insert(ctk.END, f"Progresso: {percent} - Velocidade: {velocidade} - Tamanho: {tamanho_total} - Tempo restante: {tempo_restante}\n")
            log_text.see(ctk.END) 
        elif d['status'] == 'finished':
            log_text.insert(ctk.END, "Download concluído!\n")
            log_text.see(ctk.END)
            status_label.configure(text="Download finalizado com sucesso!")
        if cancelar_download:
            raise youtube_dl.DownloadError('Download Cancelado!')

    ydl_opts['progress_hooks'] = [hook]  # Adiciona o hook para monitorar o progresso e cancelamento

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except youtube_dl.DownloadError:
        status_label.configure(text="Download cancelado...")

# Função acionada ao clicar no botão de download (em thread)
def iniciar_download():
    url = url_entry.get()
    formato = formato_var.get()

    # Limpar log antes de iniciar novo dowload
    log_text.delete(1.0, ctk.END)
    status_label.configure(text="Iniciando download...")

    # Executa o download em uma thread separada para não dar bug na interface
    download_thread = threading.Thread(target=baixar_midia, args=(url, formato))
    download_thread.start()

# Função acionada ao clicar no botão de cancelar
def cancelar_download_func():
    global cancelar_download
    cancelar_download = True 
    status_label.configure(text="Cancelando download...")

app = ctk.CTk()
app.geometry("500x450")
app.title("Baixar Vídeo/Áudio do YouTube")

titulo_label = ctk.CTkLabel(app, text="Baixar Vídeo/Áudio do YouTube", font=("Arial", 16))
titulo_label.pack(pady=10)

url_label = ctk.CTkLabel(app, text="URL do Vídeo:")
url_label.pack(pady=5)
url_entry = ctk.CTkEntry(app, width=300)
url_entry.pack(pady=5)

formato_var = ctk.StringVar(value="mp4")
formato_label = ctk.CTkLabel(app, text="Formato:")
formato_label.pack(pady=5)
formato_frame = ctk.CTkFrame(app)
formato_frame.pack(pady=5)

mp4_radio = ctk.CTkRadioButton(formato_frame, text="MP4 (vídeo completo)", variable=formato_var, value="mp4")
mp4_radio.pack(side="left", padx=10)
mp3_radio = ctk.CTkRadioButton(formato_frame, text="MP3 (somente áudio)", variable=formato_var, value="mp3")
mp3_radio.pack(side="left", padx=10)

download_button = ctk.CTkButton(app, text="Iniciar Download", command=iniciar_download)
download_button.pack(pady=10)

cancelar_button = ctk.CTkButton(app, text="Cancelar Download", command=cancelar_download_func)
cancelar_button.pack(pady=10)

log_text = ctk.CTkTextbox(app, width=400, height=150)
log_text.pack(pady=10)

status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=10)

app.mainloop()
