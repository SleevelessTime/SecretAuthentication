import os
import subprocess
import psutil
import ctypes

PROCESS_FILE = "background_script.py"
PID_FILE = "background_pid.txt"
MAX_ATTEMPTS = 3

def sleep_computer():
    """Bilgisayarı uyku moduna alır."""
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # Sleep mode

def secure_stop_process():
    """Şifre ile süreci durdurma işlemi."""
    password = "your_secret_password"  # Güvenli şifrenizi buraya girin
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        user_input = input("Enter password to stop process: ")
        
        if user_input == password:
            print("Password correct! Stopping process.")
            stop_background_process()
            return  # Süreç durdurulacak
        else:
            attempts += 1
            print(f"Incorrect password! {MAX_ATTEMPTS - attempts} attempts left.")
    
    print("Too many incorrect attempts! Putting the computer to sleep.")
    sleep_computer()

def start_background_process():
    """Arka plan sürecini başlatır."""
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
    """Arka plan sürecini durdurur."""
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
            secure_stop_process()  # Şifreli durdurma
        elif command == "exit":
            print("Kontrol uygulamasından çıkılıyor. Arka plan süreci etkilenmedi.")
            break
        else:
            print("Geçersiz komut.")
