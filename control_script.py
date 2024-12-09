import os
import subprocess
import psutil  # PID kontrolü için kullanıyoruz

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
    return psutil.pid_exists(pid)

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
        process = psutil.Process(pid)
        process.terminate()  # Süreci düzgün bir şekilde sonlandır
        process.wait(timeout=5)  # Sürecin kapanmasını bekle
        print(f"PID {pid} durduruldu.")
    except psutil.NoSuchProcess:
        print("Süreç bulunamadı. Zaten sonlanmış.")
    except psutil.AccessDenied:
        print("Süreç sonlandırılamadı: Yetki reddedildi.")
    except psutil.TimeoutExpired:
        print("Süreç zamanında sonlandırılamadı.")
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
            print("Kontrol uygulamasından çıkılıyor. Arka plan süreci etkilenmedi.")
            break
        else:
            print("Geçersiz komut.")
