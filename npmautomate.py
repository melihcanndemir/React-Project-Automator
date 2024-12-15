import subprocess
import os

# Kullanıcıdan proje adı alma
project_name = input("Proje adı girin (varsayılan: my-vite-app): ") or "my-vite-app"

# Tam yol ile npx komutunu belirleme
npx_command = [r"C:\Program Files\nodejs\npx.cmd", "create-vite@latest", project_name, "--template", "react"]

try:
    # Projeyi oluştur
    subprocess.run(npx_command, check=True)
    print(f"Proje '{project_name}' başarıyla oluşturuldu!")
except subprocess.CalledProcessError as e:
    print(f"Hata: Proje oluşturulamadı.\n{e}")
    exit()
except FileNotFoundError:
    print("Hata: npx komutu bulunamadı. PATH ayarlarınızı kontrol edin.")
    exit()

# Proje dizinine geçme
try:
    os.chdir(project_name)
    print(f"{project_name} dizinine geçildi.")
except FileNotFoundError:
    print(f"Hata: {project_name} dizini bulunamadı.")
    exit()

# Bağımlılıkları yükleme
npm_command = r"C:\Program Files\nodejs\npm.cmd"

try:
    subprocess.run([npm_command, "install"], check=True)
    print("Bağımlılıklar başarıyla yüklendi.")
except subprocess.CalledProcessError as e:
    print(f"Hata: Bağımlılıklar yüklenirken bir sorun oluştu.\n{e}")
    exit()

# Projeyi başlatma
try:
    subprocess.run([npm_command, "run", "dev"], check=True)
    print("Proje başarıyla başlatıldı!")
except subprocess.CalledProcessError as e:
    print(f"Hata: Proje başlatılamadı.\n{e}")
