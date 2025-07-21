import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
from tqdm import tqdm
import urllib3

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RAW_DIR = "raw-files"
OUT_DIR = "out-files"
CHECK_URL = "https://github.com"
TIMEOUT = 5
MAX_THREADS = 50
PROXY_TYPES = ["http", "socks4", "socks5"]

os.makedirs(OUT_DIR, exist_ok=True)

def check_proxy(proxy, proxy_type):
    proxies = {
        "http": f"{proxy_type}://{proxy}",
        "https": f"{proxy_type}://{proxy}"
    }
    try:
        response = requests.get(CHECK_URL, proxies=proxies, timeout=TIMEOUT, verify=False)
        return proxy if response.ok else None
    except:
        return None

def check_proxies(proxy_type, proxy_list):
    print(f"{Fore.WHITE}========== [ {Fore.RED}{proxy_type.upper()}{Fore.WHITE} ] ==========")
    print(f"{Fore.WHITE}Check Raw Files ::  {Fore.RED}{proxy_type.upper()} {Style.DIM}(raw-{proxy_type}.txt)")

    working = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(check_proxy, proxy, proxy_type) for proxy in proxy_list]

        for f in tqdm(as_completed(futures), total=len(futures),
                      desc=f"{Fore.WHITE}[{Fore.RED}{proxy_type.upper()}{Fore.WHITE}]: Checking Proxies",
                      colour="red"):
            result = f.result()
            if result:
                working.append(result)
                # tqdm.write(f"{Fore.WHITE}[{Fore.RED}OK{Fore.WHITE}] {Fore.LIGHTBLACK_EX}{result}")

    out_path = os.path.join(OUT_DIR, f"{proxy_type}.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(working))

    print(f"{Fore.WHITE}[{Fore.RED}SUCCESS{Fore.WHITE}] {len(working)} working proxies saved to {out_path}\n")

def main():
    for proxy_type in PROXY_TYPES:
        raw_file = os.path.join(RAW_DIR, f"raw-{proxy_type}.txt")
        if not os.path.exists(raw_file):
            print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] File not found: {raw_file}")
            continue

        with open(raw_file, "r") as f:
            proxy_list = [line.strip() for line in f if line.strip()]

        if proxy_list:
            check_proxies(proxy_type, proxy_list)
        else:
            print(f"{Fore.WHITE}[{Fore.RED}EMPTY{Fore.WHITE}] No proxies found in: {raw_file}")

    print(f"{Fore.WHITE}All proxies checked and saved.\n")

if __name__ == "__main__":
    main()
