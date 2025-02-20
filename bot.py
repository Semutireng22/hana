import requests
import time
import json
from colorama import Fore, Style, init
from fake_useragent import UserAgent
import signal
import sys

# Inisialisasi Colorama
init(autoreset=True)

# Header Banner
def print_banner():
    print(Fore.CYAN + Style.BRIGHT + """
 █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗      █████╗ ███████╗ ██████╗ 
██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╔══██╗██╔════╝██╔════╝ 
███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝    ███████║███████╗██║      
██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝     ██╔══██║╚════██║██║      
██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║         ██║  ██║███████║╚██████╗ 
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚═╝  ╚═╝╚══════╝ ╚═════╝ 
                                                                                
====================================================
     BOT                : HanaFuda Auto Grow
     Telegram Channel   : @airdropasc
     Telegram Group     : @autosultan_group
====================================================
""" + Style.RESET_ALL)

# Membuat header dengan User-Agent acak
def get_headers(auth_code):
    ua = UserAgent()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_code}",
        "Origin": "https://hanafuda.hana.network",
        "Priority": "u=1, i",
        "Referer": "https://hanafuda.hana.network/",
        "Sec-CH-UA": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": ua.random
    }
    return headers

# Fungsi untuk membaca kode auth dari file
def read_auth_codes(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Fungsi untuk mendapatkan informasi pengguna
def get_user_info(auth_code):
    url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
    headers = get_headers(auth_code)
    
    payload = {
        "query": """query GetGardenForCurrentUser {
            getGardenForCurrentUser {
                gardenStatus {
                    growActionCount
                }
            }
        }""",
        "operationName": "GetGardenForCurrentUser"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Fungsi untuk melakukan spin
def spin(auth_code):
    url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
    headers = get_headers(auth_code)
    
    spin_payload = {
        "query": """mutation issueGrowAction {
            issueGrowAction
        }""",
        "operationName": "issueGrowAction"
    }
    
    response = requests.post(url, headers=headers, json=spin_payload)
    return response.json()

# Fungsi untuk mendapatkan hadiah spin
def get_spin_reward(auth_code):
    url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
    headers = get_headers(auth_code)
    
    reward_payload = {
        "query": """mutation commitGrowAction {
            commitGrowAction
        }""",
        "operationName": "commitGrowAction"
    }
    
    response = requests.post(url, headers=headers, json=reward_payload)
    return response.json()

# Fungsi untuk menampilkan informasi penting
def print_summary(spin_count, spin_value, reward_status):
    print(Fore.YELLOW + f"\n=== Spin {spin_count} ===")
    print(Fore.GREEN + f"[ASC] Nilai Spin: {spin_value}")
    print(Fore.MAGENTA + f"[ASC] Hadiah Berhasil: {reward_status}")

# Fungsi untuk keluar dengan aman
def safe_exit(signal, frame):
    print(Fore.CYAN + "\n\nTerima kasih telah menggunakan HanaFuda Auto Grow!")
    print(Fore.YELLOW + "Dari: Airdrop ASC | Telegram Channel: @airdropasc")
    sys.exit(0)

# Fungsi untuk membaca konfigurasi dari file JSON
def read_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Fungsi untuk menunggu hingga jumlah minimal grow actions tercapai
def wait_for_minimum_actions(auth_code, min_actions):
    while True:
        user_info = get_user_info(auth_code)
        grow_action_count = user_info['data']['getGardenForCurrentUser']['gardenStatus']['growActionCount']
        if grow_action_count >= min_actions:
            print(Fore.GREEN + f"[ASC] Jumlah Grow Action mencukupi: {grow_action_count}")
            break
        else:
            print(Fore.YELLOW + f"[ASC] Menunggu hingga jumlah Grow Action mencapai {min_actions}...")
            time.sleep(10)  # Tunggu 10 detik sebelum memeriksa lagi

# Main program
def main():
    print_banner()
    auth_codes = read_auth_codes('token.txt')  # Ganti dengan path file yang sesuai
    config = read_config('config.json')
    min_grow_actions = config.get('min_grow_actions', 5)

    # Menghubungkan sinyal CTRL+C ke fungsi safe_exit
    signal.signal(signal.SIGINT, safe_exit)

    for index, auth_code in enumerate(auth_codes, start=1):
        print(Fore.YELLOW + f"Memproses Akun Ke-{index}")
        
        # Mendapatkan informasi pengguna
        user_info = get_user_info(auth_code)
        
        # Mendapatkan jumlah growActionCount
        try:
            grow_action_count = user_info['data']['getGardenForCurrentUser']['gardenStatus']['growActionCount']
            print(Fore.CYAN + f"[ASC] Jumlah Grow Action Tersedia: {grow_action_count}")
        except KeyError:
            print(Fore.RED + "Gagal mendapatkan informasi jumlah Grow Action.")
            continue  # Lanjut ke akun berikutnya jika terjadi kesalahan
        
        # Jika jumlah Grow Action tersedia adalah nol, tunggu hingga mencapai jumlah minimal
        if grow_action_count == 0:
            wait_for_minimum_actions(auth_code, min_grow_actions)
            user_info = get_user_info(auth_code)  # Dapatkan info pengguna lagi setelah menunggu
            grow_action_count = user_info['data']['getGardenForCurrentUser']['gardenStatus']['growActionCount']

        # Melakukan spin sesuai jumlah growActionCount
        for i in range(grow_action_count):
            print(Fore.BLUE + f"\n=== Melakukan Spin {i + 1} dari {grow_action_count} ===")
            
            # Melakukan spin dan mendapatkan hasilnya
            spin_response = spin(auth_code)
            spin_value = spin_response['data']['issueGrowAction']
            reward_response = get_spin_reward(auth_code)
            reward_status = reward_response['data']['commitGrowAction']
            
            # Menampilkan ringkasan informasi spin
            print_summary(i + 1, spin_value, reward_status)
            
            # Delay setelah setiap spin
            time.sleep(2)

if __name__ == "__main__":
    main()
