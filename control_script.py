import os
import signal
import subprocess

PROCESS_FILE = "background_script.py"
PID_FILE = "background_pid.txt"

def start_background_process():
    if os.path.exists(PID_FILE):
        print("Arka plan süreci zaten çalışıyor.")
        return

    # Arka plan sürecini başlat
    process = subprocess.Popen(
        ["pythonw", PROCESS_FILE], creationflags=subprocess.CREATE_NO_WINDOW
    )
    # PID'yi dosyada sakla
    with open(PID_FILE, "w") as pid_file:
        pid_file.write(str(process.pid))
    print("Arka plan süreci başlatıldı.")

def is_pid_running(pid):
    """PID'nin geçerli bir sürece ait olup olmadığını kontrol eder."""
    try:
        os.kill(pid, 0)  # Sürecin var olup olmadığını kontrol eder
        return True
    except OSError:
        return False

def stop_background_process():
    if not os.path.exists(PID_FILE):
        print("Arka planda çalışan süreç bulunamadı.")
        return

    # PID dosyasını oku
    with open(PID_FILE, "r") as pid_file:
        try:
            pid = int(pid_file.read().strip())
        except ValueError:
            print("PID dosyası bozuk. Süreç bilgisi okunamadı.")
            os.remove(PID_FILE)
            return

    # PID'nin geçerliliğini kontrol et
    if not is_pid_running(pid):
        print("PID artık geçerli değil. Süreç zaten sonlanmış.")
        os.remove(PID_FILE)
        return

    # Süreci durdur
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"PID {pid} durduruldu.")
    except OSError as e:
        print(f"Süreç sonlandırılamadı: {e}")
    finally:
        # PID dosyasını sil
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

if __name__ == "__main__":
    while True:
        command = input("Komut girin (start/stop/exit): ").lower()
        if command == "start":
            start_background_process()
        elif command == "stop":
            stop_background_process()
        elif command == "exit":
            print("Kontrol uygulamasından çıkılıyor.")
            break
        else:
            print("Geçersiz komut.")
