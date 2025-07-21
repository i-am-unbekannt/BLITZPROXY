import os
import json
import requests
import subprocess
import time
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

RAW_DIR = "raw-files"
os.makedirs(RAW_DIR, exist_ok=True)

PROXY_TYPES = ["http", "socks4", "socks5"]

FILTER_START = "---------- [ ProxyList.to"
FILTER_END = "For the full list go to:"

def clean_proxy_list(lines):
    cleaned = []
    skip_rest = False
    for line in lines:
        if line.startswith(FILTER_START):
            continue
        if FILTER_END in line:
            skip_rest = True
            continue
        if skip_rest:
            continue
        if line.strip():
            cleaned.append(line.strip())
    return cleaned

def fetch_proxies_from_urls(urls, proxy_type):
    proxies = set()
    print(f"{Fore.WHITE}Get Raw Files ::  {Fore.RED}{proxy_type.upper()} {Style.DIM}(via ProxyURL.json)")
    for url in tqdm(urls, desc=f"{Fore.WHITE}[{Fore.RED}{proxy_type.upper()}{Fore.WHITE}]: Fetching {proxy_type.upper()} URLs", colour='red'):
        try:
            response = requests.get(url, timeout=10)
            if response.ok:
                lines = response.text.splitlines()
                cleaned = clean_proxy_list(lines)
                proxies.update(cleaned)
            else:
                tqdm.write(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RED} Failed to fetch {url} - Status code: {response.status_code}")
        except Exception as e:
            tqdm.write(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RED} Error fetching {url}: {e}")
    return proxies

def run_proxy_scraper(proxy_type):
    output_file = f"raw-{proxy_type}.txt"
    print(f"{Fore.WHITE}Get Raw Files ::  {Fore.RED}{proxy_type.upper()} {Style.DIM}(via proxy_scraper)")
    try:
        result = subprocess.run(
            ["proxy_scraper", "-p", proxy_type, "-o", output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            os.remove(output_file)
            return set(clean_proxy_list(lines))
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[{Fore.WHITE}ERROR{Fore.RED}]{Fore.WHITE} proxy_scraper failed: {e}")
    return set()

def save_proxies_to_file(proxy_type, proxies):
    filename = os.path.join(RAW_DIR, f"raw-{proxy_type}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        for proxy in sorted(proxies):
            f.write(proxy + "\n")
    print(f"{Fore.WHITE}[{Fore.RED}SUCCESS{Fore.WHITE}] Saved {len(proxies)} proxies to {filename}")

def main():
    with open("ProxyURL.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for proxy_type in PROXY_TYPES:
        print(f"\n{Fore.WHITE}========== [ {Fore.RED}{proxy_type.upper()}{Fore.WHITE} ] ==========")
        urls = data.get(proxy_type, {}).get("urls", [])
        proxies = fetch_proxies_from_urls(urls, proxy_type)
        scraped = run_proxy_scraper(proxy_type)
        proxies.update(scraped)
        save_proxies_to_file(proxy_type, proxies)
        time.sleep(1)

    print(f"\n{Fore.WHITE}All proxy types processed successfully.")

if __name__ == "__main__":
    main()
