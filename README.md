# 📞 Telegram Phone Processing Bot

Bot Telegram berbasis Python yang digunakan untuk memproses nomor telepon melalui API eksternal, mendukung multi-bahasa (Indonesia & English), sistem cooldown, deteksi negara nomor telepon, serta notifikasi otomatis ke grup Telegram.

## ✨ Fitur

- 🌍 Multi Bahasa (Indonesia & English)
- 📱 Validasi & Normalisasi Nomor Telepon
- 🗺️ Deteksi Negara Berdasarkan Nomor
- ⏳ Cooldown Anti Spam
- 🔔 Notifikasi Otomatis ke Grup
- 👑 Akses Khusus Owner
- 🔄 Toggle Notifikasi Grup
- 📊 Sensor Nomor Saat Ditampilkan
- 🚀 Dibangun menggunakan Python Telegram Bot v20+

---

## 📦 Requirements

Python 3.10+

Install dependencies:

```bash
pip install python-telegram-bot requests phonenumbers
```

Atau gunakan:

```bash
pip install -r requirements.txt
```

### requirements.txt

```txt
python-telegram-bot>=20.0
requests
phonenumbers
```

---

## ⚙️ Konfigurasi

Edit bagian konfigurasi pada file utama:

```python
TOKEN = "BOT_TOKEN"
GROUP_ID = "-100xxxxxxxxxx"
OWNER_ID = 123456789
API_URL = "https://wilz-api.web.id/api/banding"
API_KEY = "wilzfree"
EMAIL = "your@email.com"
APP_PW = "your_app_password"
```

### Penjelasan

| Variable | Keterangan |
|-----------|------------|
| TOKEN | Token Bot Telegram |
| GROUP_ID | ID Grup Notifikasi |
| OWNER_ID | User ID Owner Bot |
| API_URL | Endpoint API |
| API_KEY | API Key |
| EMAIL | Email API |
| APP_PW | Password API |

---

## 🚀 Menjalankan Bot

**Install (Wajib)**
```bash
pkg update && pkg upgrade -y
pkg install git -y
```
**Clone Repo**
```bash
git clone https://github.com/WILLzzz-Termux/Fix-Merah-Free.git
```
**Run**
```bash
python fixfree.py
```

**Jika berhasil:**

```text
BOT FIX MERAH FREE BY @Teamwilz Online...
```

---

## 📋 Command

### /start

Menampilkan pesan selamat datang dan pilihan bahasa.

```text
/start
```

### /f

Memproses nomor telepon.

Format:

```text
/f +628123456789
```

Contoh:

```text
/f 628123456789
```

### /toggle_notif

Mengaktifkan atau menonaktifkan notifikasi grup.

```text
/toggle_notif
```

Hanya dapat digunakan oleh Owner.

---

## 🔒 Keamanan

Bot memiliki beberapa lapisan keamanan:

- Hanya OWNER_ID yang dapat menjalankan command utama.
- Cooldown 60 detik untuk mencegah spam.
- Nomor telepon disensor saat ditampilkan.
- Error handling pada request API.

Contoh nomor yang ditampilkan:

```text
+62812******789
```

---

## 🌎 Bahasa yang Didukung

### Indonesia

```text
Halo! Bot siap. Gunakan /f <nomor> untuk mulai.
```

### English

```text
Hello! Bot is ready. Use /f <number> to start.
```

---

## 📢 Notifikasi Grup

Saat proses selesai, bot akan mengirim informasi ke grup:

```text
🔔 Status: Berhasil
Nomor: ${number}
Negara: ${country}
Respon: Success
```

---

## 🛠️ Teknologi

- Python
- python-telegram-bot
- Requests
- Phonenumbers
- Telegram Bot API

---

## 👨‍💻 Author

**WILLzzz-Termux**

GitHub: https://github.com/WILLzzz-Termux

---

## 📜 License

Project ini dibuat untuk kebutuhan pribadi dan edukasi. Gunakan dengan bijak dan sesuai kebijakan Telegram serta hukum yang berlaku.
