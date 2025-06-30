# Telegram Bot Reminder - Minimal Resource

Bot Telegram untuk mengirim reminder otomatis dengan penggunaan resource yang minimal. Bot akan berjalan sesuai jadwal crontab dan berhenti setelah mengirim pesan.

## 🚀 **Keunggulan:**

- ✅ **Minimal Resource**: Tidak ada server yang terus berjalan
- ✅ **Efisien**: Hanya berjalan saat diperlukan sesuai jadwal
- ✅ **Sederhana**: Setup yang mudah dan straightforward
- ✅ **Reliable**: Logging yang jelas untuk monitoring

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Konfigurasi

Pastikan file `auth.py` sudah berisi TOKEN dan CHAT_ID yang valid:

```python
TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
```

## Penggunaan

### 1. Testing Manual

```bash
# Test reminder tertentu
python test_bot.py tidur
python test_bot.py siang
python test_bot.py olahraga
python test_bot.py ekonomi
python test_bot.py ai
```

### 2. Setup Crontab (Otomatis)

#### Langkah 1: Buat script executable

```bash
chmod +x scheduler.py
chmod +x test_bot.py
```

#### Langkah 2: Edit crontab

```bash
crontab -e
```

#### Langkah 3: Tambahkan jadwal

```bash
# Contoh jadwal (sesuaikan dengan kebutuhan):

# Olahraga pagi - setiap hari jam 6 pagi
0 6 * * * cd /Users/mwlanaz/Desktop/github/bot && /usr/bin/python3 scheduler.py olahraga

# Belajar AI siang - setiap hari jam 12 siang
0 12 * * * cd /Users/mwlanaz/Desktop/github/bot && /usr/bin/python3 scheduler.py siang

# Belajar AI malam - setiap hari jam 8 malam
0 20 * * * cd /Users/mwlanaz/Desktop/github/bot && /usr/bin/python3 scheduler.py ai

# Belajar Ekonomi - setiap hari jam 9 malam
0 21 * * * cd /Users/mwlanaz/Desktop/github/bot && /usr/bin/python3 scheduler.py ekonomi

# Persiapan tidur - setiap hari jam 10 malam
0 22 * * * cd /Users/mwlanaz/Desktop/github/bot && /usr/bin/python3 scheduler.py tidur
```

#### Format Crontab:

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * * command
```

### 3. Monitoring

Bot akan membuat file log `bot.log` yang berisi:

- ✅ Status pengiriman pesan
- ❌ Error yang terjadi
- 🕐 Waktu eksekusi reminder
- 📊 Statistik keberhasilan

## 📋 **Reminder yang Tersedia:**

| Nama       | Waktu | Pesan                                                                          |
| ---------- | ----- | ------------------------------------------------------------------------------ |
| `olahraga` | Pagi  | 💪 Selamat pagi, Lana! Saatnya olahraga biar segar seharian! 🏃‍♀️✨              |
| `siang`    | Siang | 📚 Hai Lana! Sudah siang 🌞 Yuk belajar AI! 💻🧠                               |
| `ai`       | Malam | 🤖 Malam ini waktunya belajar AI! Jangan lupa catatan dan semangatnya ya! 🔍🧠 |
| `ekonomi`  | Malam | 📈 Terakhir sebelum tidur, ayo belajar Ekonomi bareng grafik dan logika! 💡💸  |
| `tidur`    | Malam | 🌙 Sudah jam 10 malam, Lana. Yuk persiapan tidur 😴🛏️ Biar besok lebih segar!  |

## 🔧 **Troubleshooting**

### 1. Crontab tidak berjalan

```bash
# Cek log crontab
tail -f /var/log/cron

# Test manual
python scheduler.py tidur

# Cek path Python
which python3
```

### 2. Bot tidak mengirim pesan

```bash
# Cek TOKEN dan CHAT_ID
cat auth.py

# Cek log bot
tail -f bot.log

# Test koneksi
python test_bot.py tidur
```

### 3. Permission error

```bash
# Buat executable
chmod +x scheduler.py
chmod +x test_bot.py
```

## 📁 **File Structure**

```
bot/
├── auth.py              # Konfigurasi TOKEN dan CHAT_ID
├── scheduler.py         # Main bot logic (minimal resource)
├── test_bot.py          # Script testing manual
├── requirements.txt     # Dependencies (hanya requests)
├── bot.log             # Log file (auto-generated)
└── reminder/           # File reminder (tidak digunakan lagi)
    ├── pengingat_tidur.py
    ├── pengingat_siang.py
    ├── pengingat_olahraga.py
    ├── pengingat_ekonomi.py
    └── pengingat_ai.py
```

## 💡 **Tips Penggunaan:**

1. **Test dulu sebelum setup crontab**:

   ```bash
   python test_bot.py tidur
   ```

2. **Monitor log secara berkala**:

   ```bash
   tail -f bot.log
   ```

3. **Cek crontab yang aktif**:

   ```bash
   crontab -l
   ```

4. **Restart crontab jika perlu**:
   ```bash
   sudo service cron restart
   ```
## Reminder Bot with Telegram Authorize
