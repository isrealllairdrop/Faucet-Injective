import requests
import bech32
import time
import os
import random
import logging

# ==============================================================================
# --- KONFIGURASI (Ubah sesuai kebutuhan Anda) ---
# ==============================================================================

# File & URL
API_URL = "https://jsbqfdd4yk.execute-api.us-east-1.amazonaws.com/v2/faucet"
ADDRESS_FILE = "address.txt"
PROCESSED_FILE = "processed.txt"
LOG_FILE = "faucet_claim.log"

# --- Pengaturan Jeda Manual (dalam detik) ---
# Jeda ini akan digunakan di antara setiap request klaim.
JEDA_ANTAR_KLAIM_DETIK = 5

# --- Pengaturan Proxy ---
# Isi detail proxy Anda di bawah ini. Script akan bertanya apakah akan menggunakannya.
PROXIES = {
   "http": "http://user:pass@123.45.67.89:8080",
   "https": "http://user:pass@123.45.67.89:8080",
}

# Header Request
HEADERS = {
    "authority": "jsbqfdd4yk.execute-api.us-east-1.amazonaws.com",
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
    "origin": "https://multivm.injective.com",
    "referer": "https://multivm.injective.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
}

# ==============================================================================
# --- FUNGSI-FUNGSI UTAMA (Dengan penyempurnaan log) ---
# ==============================================================================

class SimpleConsoleFormatter(logging.Formatter):
    """Formatter khusus untuk log di konsol yang lebih simpel."""
    def format(self, record):
        if record.levelno == logging.INFO:
            return record.getMessage()
        else:
            return f"[{record.levelname}] {record.getMessage()}"

def setup_logging():
    """Mengkonfigurasi logging: detail ke file, simpel ke konsol."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(SimpleConsoleFormatter())
    logger.addHandler(console_handler)

def convert_eth_to_inj(eth_address: str) -> str:
    """Mengonversi alamat EVM (0x...) menjadi alamat Injective (inj...)."""
    try:
        hex_data = bytes.fromhex(eth_address.lower().replace("0x", ""))
        five_bit_words = bech32.convertbits(hex_data, 8, 5)
        return bech32.bech32_encode("inj", five_bit_words)
    except Exception as e:
        logging.error(f"Gagal konversi alamat {eth_address}: {e}")
        return None

def claim_faucet(session: requests.Session, inj_address: str) -> bool:
    """Mengirim request klaim faucet dan mengembalikan status keberhasilan."""
    payload = {"address": inj_address}
    logging.info(f"[*] Mencoba klaim untuk: {inj_address}")
    
    try:
        response = session.post(API_URL, json=payload, timeout=45)
        
        # Jika status code 200, selalu anggap SUKSES
        if response.status_code == 200:
            try:
                # Coba baca pesan dari JSON jika ada
                message = response.json().get('message', '')
                if "successfully requested funds" in message.lower():
                    logging.info(f"  [+] SUKSES: {message}")
                else:
                    # Jika pesan tidak biasa, tetap catat sebagai SUKSES dengan detailnya
                    logging.info(f"  [+] SUKSES (Pesan server tidak biasa): {response.text}")
            except requests.exceptions.JSONDecodeError:
                # Jika respons bukan JSON, tetap catat sebagai SUKSES dengan detailnya
                logging.info(f"  [+] SUKSES (Respon server bukan JSON): {response.text}")
            return True
        else:
            # Jika status code bukan 200, anggap GAGAL
            logging.error(f"GAGAL: Status Code {response.status_code}, Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        # Jika ada error jaringan, anggap GAGAL
        logging.error(f"GAGAL: Terjadi error pada request: {e}")
        return False

# ==============================================================================
# --- FUNGSI UTAMA (ALUR KERJA SCRIPT) ---
# ==============================================================================

def main():
    """Fungsi utama untuk menjalankan seluruh proses."""
    setup_logging()
    logging.info("\n" + "="*50 + "\n--- Auto Claim Faucet Injective Dimulai ---\n" + "="*50)

    # --- Input Pilihan dari Pengguna ---
    while True:
        choice_mode = input("Pilih mode:\n[1] Ulangi dari Awal (hapus riwayat)\n[2] Lanjutkan Proses Sebelumnya\n>> ").strip()
        if choice_mode in ['1', '2']:
            break
        print("Pilihan tidak valid, silakan masukkan 1 atau 2.")

    while True:
        choice_proxy = input("Gunakan proxy untuk sesi ini? (y/n): ").strip().lower()
        if choice_proxy in ['y', 'n']:
            break
        print("Pilihan tidak valid, silakan masukkan 'y' atau 'n'.")

    # --- Memproses Pilihan Pengguna ---
    if choice_mode == '1':
        if os.path.exists(PROCESSED_FILE):
            os.remove(PROCESSED_FILE)
            logging.info(f"[*] File riwayat '{PROCESSED_FILE}' telah dihapus.")
    else:
        logging.info("[*] Mode 'Lanjutkan' dipilih.")
    
    use_proxy_this_run = (choice_proxy == 'y')

    # --- Memuat Alamat ---
    if not os.path.exists(ADDRESS_FILE):
        logging.error(f"File '{ADDRESS_FILE}' tidak ditemukan. Harap buat dan isi dengan alamat EVM.")
        return

    with open(ADDRESS_FILE, 'r') as f:
        all_addresses = {line.strip() for line in f if line.strip().startswith('0x')}

    processed_addresses = set()
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as f:
            processed_addresses = {line.strip() for line in f}

    addresses_to_process = list(all_addresses - processed_addresses)
    random.shuffle(addresses_to_process)

    if not addresses_to_process:
        logging.info("\nSemua alamat sudah pernah diproses. Tidak ada pekerjaan baru.")
        return

    logging.info(f"\nTotal Alamat: {len(all_addresses)} | Sudah Diproses: {len(processed_addresses)} | Akan Diproses: {len(addresses_to_process)}\n" + "-"*50)

    # --- Memulai Proses Klaim ---
    with requests.Session() as session:
        session.headers.update(HEADERS)
        if use_proxy_this_run:
            session.proxies.update(PROXIES)
            logging.info(f"[*] Menggunakan proxy: {PROXIES.get('https', 'Tidak ada')}")

        for i, eth_addr in enumerate(addresses_to_process):
            logging.info(f"Memproses Alamat #{i+1}/{len(addresses_to_process)}: {eth_addr}")
            
            inj_addr = convert_eth_to_inj(eth_addr)
            
            if inj_addr:
                success = claim_faucet(session, inj_addr)
                if success:
                    with open(PROCESSED_FILE, 'a') as f:
                        f.write(eth_addr + '\n')
            
            if i < len(addresses_to_process) - 1:
                delay = JEDA_ANTAR_KLAIM_DETIK
                logging.info(f"  [*] Jeda selama {delay} detik...\n" + "-"*50)
                time.sleep(delay)

    logging.info("\n" + "="*50 + "\n--- Semua Proses Selesai ---\n" + "="*50)

if __name__ == "__main__":
    main()
