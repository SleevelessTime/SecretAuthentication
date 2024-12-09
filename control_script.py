import os
import subprocess
import psutil

PROCESS_FILE = "background_script.py"
PID_FILE = "background_pid.txt"

def start_background_process():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as pid_file:
            try:
                pid = int(pid_file.read().strip())
                if is_pid_running(pid):
                    print("Arka plan süreci zaten çalışıyor.")
                    return
                else:
                    print("PID geçerli değil, eski sürecin kalıntıları temizleniyor.")
                    os.remove(PID_FILE)
            except ValueError:
                print("PID dosyası bozuk, eski dosya temizleniyor.")
                os.remove(PID_FILE)

    # Arka plan sürecini başlat
    process = subprocess.Popen(
        ["pythonw", PROCESS_FILE], creationflags=subprocess.CREATE_NO_WINDOW
    )
    with open(PID_FILE, "w") as pid_file:
        pid_file.write(str(process.pid))
    print(f"Arka plan süreci başlatıldı. PID: {process.pid}")

def is_pid_running(pid):
    """PID'nin geçerli bir sürece ait olup olmadığını kontrol eder."""
    try:
        process = psutil.Process(pid)
        return process.is_running() and process.name().startswith("python")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False

def stop_background_process():
    if not os.path.exists(PID_FILE):
        print("Arka planda çalışan süreç bulunamadı.")
        return

    with open(PID_FILE, "r") as pid_file:
        try:
            pid = int(pid_file.read().strip())
        except ValueError:
            print("PID dosyası bozuk, temizleniyor.")
            os.remove(PID_FILE)
            return

    if is_pid_running(pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5)
            print(f"Arka plan süreci durduruldu. PID: {pid}")
        except psutil.TimeoutExpired:
            print("Süreç zamanında sonlandırılamadı, zorla kapatılıyor.")
            process.kill()
        except psutil.NoSuchProcess:
            print("Süreç bulunamadı, zaten sonlanmış.")
    else:
        print("PID geçerli değil, arka plan süreci zaten çalışmıyor.")

    # PID dosyasını temizle
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
            print("Kontrol uygulamasından çıkılıyor. Arka plan süreci etkilenmedi.")
            break
        else:
            print("Geçersiz komut.")
