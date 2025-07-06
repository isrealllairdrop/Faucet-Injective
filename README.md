# 🤖 Auto Claim Faucet Injective

![image](https://github.com/user-attachments/assets/e3540da4-2efd-4cc1-be11-a5543af95ef8)


## ✨ Fitur Unggulan

- **🚀 Automasi Penuh**: Cukup siapkan daftar alamat EVM Anda, dan biarkan skrip bekerja.
- **🔄 Manajemen Sesi**: Pernah mati lampu atau koneksi terputus? Skrip ini bisa melanjutkan proses dari alamat terakhir yang belum diklaim, jadi tidak ada pekerjaan yang sia-sia.
- **🌐 Dukungan Proxy**: Tingkatkan anonimitas atau lewati batasan rate-limit dengan dukungan proxy bawaan.
- **✨ Konversi Alamat Otomatis**: Secara otomatis mengubah alamat `0x...` (EVM) Anda menjadi format `inj...` (Injective) yang diperlukan oleh faucet.
- **📝 Logging Detail**: Setiap aksi, baik sukses maupun gagal, dicatat ke dalam file `faucet_claim.log` untuk kemudahan audit dan *troubleshooting*. Output di konsol tetap bersih dan mudah dibaca.
- **🔧 Konfigurasi Mudah**: Semua pengaturan penting seperti jeda waktu dan detail proxy ditempatkan di bagian atas skrip agar mudah diubah.

## ⚙️ Cara Penggunaan

Ikuti langkah-langkah sederhana ini untuk memulai.

### 1. Prasyarat

Pastikan Anda telah menginstal **Python 3** di sistem Anda.

### 2. Clone repositori
```bash
git clone https://github.com/isrealllairdrop/Faucet-Injective.git
cd Faucet-Injective
```
### 3. Instalasi
```bash
pip install requests bech32
```

### 3. Konfigurasi

1.  **Buat `address.txt`**
    Buat sebuah file bernama `address.txt` di direktori yang sama dengan `bot.py`. Isi file ini dengan semua alamat dompet EVM (`0x...`) Anda, di mana setiap alamat berada di baris baru.

    **Contoh `address.txt`:**
    ```
    0x1234567890abcdef1234567890abcdef12345678
    0xabcdef1234567890abcdef1234567890abcdef12
    0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
    ```

2.  **(Opsional) Atur Konfigurasi Lanjutan**
    Buka file `bot.py` dan sesuaikan pengaturan di bagian `KONFIGURASI` jika perlu:
    - `JEDA_ANTAR_KLAIM_DETIK`: Ubah nilai `5` untuk mengatur jeda (dalam detik) antar setiap klaim.
    - `PROXIES`: Jika Anda ingin menggunakan proxy, isi detailnya di sini.

### 4. Menjalankan Skrip

1.  Buka terminal atau Command Prompt di direktori tempat Anda menyimpan file.
2.  Jalankan skrip dengan perintah:
    ```bash
    python bot.py
    ```
3.  Skrip akan menanyakan dua hal:
    - **Pilih mode**: Apakah Anda ingin memulai dari awal (menghapus riwayat) atau melanjutkan sesi sebelumnya.
    - **Gunakan proxy**: Apakah Anda ingin mengaktifkan proxy untuk sesi ini.
4.  Duduk santai dan biarkan skrip menyelesaikan tugasnya!

## 📂 Struktur File

Setelah menjalankan skrip, Anda akan melihat beberapa file baru dibuat:

- `bot.py`: Skrip utama Anda.
- `address.txt`: **(Anda yang membuat)** Daftar alamat EVM yang akan diproses.
- `processed.txt`: Daftar alamat yang telah berhasil diklaim. Skrip menggunakan file ini untuk fitur "Lanjutkan Proses".
- `faucet_claim.log`: Catatan detail dari semua aktivitas skrip, termasuk timestamp, error, dan respons dari server.

## 📞 Kontak & Dukungan

Punya pertanyaan, kritik, atau saran? Jangan ragu untuk menghubungi saya.

- **Telegram**: [https://t.me/Isrealll1](https://t.me/Isrealll1)
- **Website**: [https://isrealllairdrop.tech/](https://isrealllairdrop.tech/)

## ⚠️ Peringatan

- Skrip ini dibuat untuk tujuan edukasi dan otomatisasi tugas pribadi.
- Jangan menyalahgunakan faucet. Jeda antar klaim yang wajar telah diatur secara default untuk menghormati layanan yang disediakan.
- Pengguna bertanggung jawab penuh atas penggunaan skrip ini.

---

