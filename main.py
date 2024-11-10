import requests
from concurrent.futures import ThreadPoolExecutor
import json
from colorama import Fore, Style

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

session = requests.Session()
retries = requests.adapters.Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
session.mount('http://', requests.adapters.HTTPAdapter(max_retries=retries))
session.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))

def fetch_page(base_url, path):
    url = base_url + path
    try:
        response = session.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        print(f"{Fore.GREEN}{Style.BRIGHT}{path}{Style.RESET_ALL}")
        return path
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}{Style.BRIGHT}{path}{Style.RESET_ALL}")
        return None

def main():
    base_url = input(f"\n{Fore.CYAN}{Style.BRIGHT}請輸入要爬取的網站：{Style.RESET_ALL} ").strip()

    try:
        with open('paths.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            common_paths = data.get("paths", [])
    except FileNotFoundError:
        print(f"{Fore.RED}{Style.BRIGHT}未找到 paths.json 文件{Style.RESET_ALL}")
        input(f"\n請按 Enter 鍵退出...{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}{Style.BRIGHT}開始爬取網站：{base_url}{Style.RESET_ALL}")
    with ThreadPoolExecutor(max_workers=20) as executor:
        pages_data = list(executor.map(lambda path: fetch_page(base_url, path), common_paths))

    valid_pages = [base_url + path for path in pages_data if path]
    with open('page.json', 'w', encoding='utf-8') as f:
        json.dump(valid_pages, f, ensure_ascii=False, indent=4)

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}共找到 {len(valid_pages)} 個頁面，並儲存到 page.json。{Style.RESET_ALL}")
    input(f"\n請按 Enter 鍵退出...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()