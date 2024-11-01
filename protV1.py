import os
import sys
import winshell
import win32com.client
import tkinter as tk
import time
from threading import Timer

def add_desktop_script_to_startup():
                                                                                    # Masaüstü klasörünün yolunu alın
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    script_path = os.path.abspath(sys.argv[0])                                      # Dosya adı "protV1.py" olarak varsayıldı

                                                                                    # Başlangıç klasörünün yolunu al
    startup_folder = winshell.startup()
    shortcut_name = os.path.splitext(os.path.basename(script_path))[0] + ".lnk"
    shortcut_path = os.path.join(startup_folder, shortcut_name)

                                                                                    # Kısayol zaten mevcut mu kontrol et
    if not os.path.exists(shortcut_path):
                                                                                    # Windows Shell'i kullanarak kısayolu oluştur
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = sys.executable                                        # Python çalıştırıcısının yolu
        shortcut.Arguments = f'"{script_path}"'
        shortcut.WorkingDirectory = desktop_path
        shortcut.save()

                                                                                    # Fonksiyonu çağırarak masaüstündeki dosyayı başlangıç klasörüne ekleyin
add_desktop_script_to_startup()

def show_welcome_message():
                                                                                    # Yeni bir pencere oluştur
    root = tk.Tk()
    root.title("Welcome Message")
    root.geometry("600x400")                                                        # Pencere boyutları
    root.configure(bg="black")

                                                                                    # Mesajı yazdırmak için etiket oluştur
    label = tk.Label(root, text="Welcome Sir", font=("Old English Text MT", 36, "bold"), fg="#FFD700", bg="black")
    label.pack(expand=True)

                                                                                    # 30 saniye sonra pencereyi otomatik kapat
    def close_window():
        root.destroy()
    
                                                                                    # 30 saniye sonra kapanma
    Timer(30, close_window).start()

                                                                                    # Pencereyi göster
    root.mainloop()

                                                                                    # Karşılama mesajı penceresini göster
show_welcome_message()
