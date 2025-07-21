# Telegram Reminder Bot

Bot Telegram sederhana untuk mengingatkan Anda dengan simulasi panggilan telepon setiap hari pada waktu yang dijadwalkan.

## Fitur

- Menjadwalkan pengingat harian dengan deskripsi.
- Simulasi panggilan masuk dengan stiker dan pesan berulang.
- Daftar dan hapus jadwal pengingat.
- Penyimpanan jadwal secara otomatis ke file JSON.

## Instalasi

1. **Clone repo & masuk ke folder**
   ```bash
   git clone <repo-url>
   cd bot
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Konfigurasi Token & User ID**

   - Salin file `config_example.py` menjadi `config.py`.
   - Masukkan token bot Telegram dan user ID Anda ke dalam `config.py`.

4. **Jalankan bot**
   ```bash
   python new.py
   ```

## Penggunaan

- `/start` — Menampilkan pesan bantuan.
- `/set HH:MM Deskripsi` — Menjadwalkan pengingat harian.
- `/list` — Melihat semua jadwal aktif.
- `/delete ID_Jadwal` — Menghapus jadwal tertentu.

## Catatan

- Hanya user dengan USER_ID yang dapat menggunakan bot ini.
- Jadwal disimpan di file `jadwal.json`.

---

**Dibuat dengan Python & [python-telegram-bot](https://python-telegram-bot.org/)**
