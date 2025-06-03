import re
import time
import os
import requests
from colorama import init, Style
from itertools import cycle
from concurrent.futures import ThreadPoolExecutor
import json

# Initialize Colorama
init(autoreset=True)

# Function to create a smooth color gradient for text
def gradient_text(text, start_color, end_color):
    gradient = ""
    text_length = len(text)
    for i, char in enumerate(text):
        progress = i / (text_length - 1) if text_length > 1 else 0
        r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    return gradient + Style.RESET_ALL

# Banner with a smooth blue-purple gradient
def print_banner():
    banner = """
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██╗  ██╗███████╗██╗  ██╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝╚██╗██╔╝
██║  ███╗███████║██║   ██║███████╗   ██║   ███████║█████╗   ╚███╔╝ 
██║   ██║██╔══██║██║   ██║╚════██║   ██║   ██╔══██║██╔══╝   ██╔██╗ 
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██║  ██║███████╗██╔╝ ██╗
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """
    start_color = (0, 0, 255)  # Blue
    end_color = (128, 0, 128)  # Purple
    print(gradient_text(banner, start_color, end_color))

# Function to clear the screen and reprint the banner
def clear_screen_with_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

# Validate webhook URL
def is_valid_webhook_url(url):
    webhook_pattern = r'^https://(discord\.com|discordapp\.com)/api/webhooks/.*$'
    return bool(re.match(webhook_pattern, url))

def get_webhook_url():
    while True:
        url = input(gradient_text("Enter the webhook URL (HTTPS required): ", (0, 0, 255), (128, 0, 128)))
        if is_valid_webhook_url(url):
            return url.strip()
        print(gradient_text("[!] Invalid URL. Please enter a valid Discord webhook URL (HTTPS).", (255, 0, 0), (255, 69, 0)))

# Validate proxy format
def is_valid_proxy(proxy):
    proxy_pattern = r'^http://[a-zA-Z0-9\.\-_]+:[0-9]+$'
    return bool(re.match(proxy_pattern, proxy))

# Fetch public HTTPS proxies from multiple sources
def fetch_proxies():
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=yes&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=http&anon=elite"
    ]
    proxies = []
    for source in sources:
        print(gradient_text(f"[!] Fetching proxies from {source}...", (0, 255, 255), (0, 128, 128)))
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                proxy_list = response.text.strip().split('\n')
                proxies.extend([f"http://{proxy}" for proxy in proxy_list if proxy and is_valid_proxy(f"http://{proxy}")])
            else:
                print(gradient_text(f"[!] Error fetching proxies from {source}: {response.status_code}", (255, 0, 0), (255, 69, 0)))
        except Exception as e:
            print(gradient_text(f"[!] Error fetching from {source}: {e}", (255, 0, 0), (255, 69, 0)))
    return list(set(proxies))  # Remove duplicates

# Test a single proxy for HTTPS compatibility
def test_proxy(proxy, timeout=10):
    try:
        start_time = time.time()
        response = requests.get(
            "https://httpbin.org/ip",
            proxies={'http': proxy, 'https': proxy},
            timeout=timeout
        )
        if response.status_code == 200:
            latency = (time.time() - start_time) * 1000  # Latency in ms
            print(gradient_text(f"[✓] Proxy {proxy} is valid (latency: {latency:.2f} ms)", (0, 255, 0), (173, 255, 47)))
            return proxy, latency
        else:
            print(gradient_text(f"[!] Proxy {proxy} failed: HTTP {response.status_code}", (255, 0, 0), (255, 69, 0)))
            return None, None
    except Exception as e:
        print(gradient_text(f"[!] Proxy {proxy} failed: {str(e)}", (255, 0, 0), (255, 69, 0)))
        return None, None

# Get valid HTTPS proxies
def get_valid_proxies(max_proxies=5):
    proxies = fetch_proxies()
    if not proxies:
        print(gradient_text("[!] No proxies retrieved. Consider adding a custom proxy.", (255, 0, 0), (255, 69, 0)))
        return []
    
    print(gradient_text(f"[!] Testing {len(proxies)} proxies...", (0, 255, 255), (0, 128, 128)))
    valid_proxies = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(test_proxy, proxies)
        for proxy, latency in results:
            if proxy and latency:
                valid_proxies.append((proxy, latency))
    
    # Sort by latency and take the fastest
    valid_proxies.sort(key=lambda x: x[1])
    valid_proxies = [proxy for proxy, _ in valid_proxies[:max_proxies]]
    
    if valid_proxies:
        print(gradient_text(f"[✓] {len(valid_proxies)} valid HTTPS proxies found.", (0, 255, 0), (173, 255, 47)))
    else:
        print(gradient_text("[!] No valid HTTPS proxies found. Consider adding a custom proxy.", (255, 0, 0), (255, 69, 0)))
    return valid_proxies

# Add a custom proxy
def add_custom_proxy(proxies):
    while True:
        proxy = input(gradient_text("Enter a custom proxy (format: http://host:port) or 'cancel' to return: ", (0, 0, 255), (128, 0, 128)))
        if proxy.lower() == 'cancel':
            return proxies
        if is_valid_proxy(proxy):
            print(gradient_text(f"[!] Testing custom proxy {proxy}...", (0, 255, 255), (0, 128, 128)))
            proxy, latency = test_proxy(proxy)
            if proxy:
                proxies.append(proxy)
                print(gradient_text(f"[✓] Proxy {proxy} added (latency: {latency:.2f} ms).", (0, 255, 0), (173, 255, 47)))
                input(gradient_text("Press Enter to continue...", (0, 255, 0), (173, 255, 47)))
                return proxies
            else:
                print(gradient_text("[!] Proxy is not valid or does not support HTTPS.", (255, 0, 0), (255, 69, 0)))
        else:
            print(gradient_text("[!] Invalid proxy format. Use http://host:port.", (255, 0, 0), (255, 69, 0)))

# Validate frequency
def get_frequency_ms():
    while True:
        try:
            freq = int(input(gradient_text("Frequency (in ms, minimum 100): ", (0, 0, 255), (128, 0, 128))))
            if freq >= 100:
                return freq
            print(gradient_text("[!] Frequency must be at least 100 ms.", (255, 0, 0), (255, 69, 0)))
        except ValueError:
            print(gradient_text("[!] Please enter a valid integer.", (255, 0, 0), (255, 69, 0)))

# Send POST messages at high frequency (Nuke)
def send_nuke(webhook_url, proxies=None):
    session = requests.Session()
    proxy_pool = cycle(proxies) if proxies else None
    
    print(gradient_text("Enter details for sending:", (0, 0, 255), (128, 0, 128)))
    message = input(gradient_text("Message to send: ", (0, 0, 255), (128, 0, 128)))
    username = input(gradient_text("Bot username: ", (0, 0, 255), (128, 0, 128)))
    frequency_ms = get_frequency_ms()

    print(gradient_text("[!] Starting Nuke...", (255, 0, 0), (255, 165, 0)))
    try:
        payload = {"content": message, "username": username}
        while True:
            proxy = next(proxy_pool) if proxy_pool else None
            proxies_dict = {'http': proxy, 'https': proxy} if proxy else None
            try:
                response = session.post(webhook_url, json=payload, proxies=proxies_dict, timeout=10)
                if response.status_code in [200, 204]:
                    proxy_info = f" via proxy {proxy}" if proxy else ""
                    print(gradient_text(f"[✓] Message sent successfully{proxy_info}!", (0, 255, 0), (173, 255, 47)))
                elif response.status_code == 429:
                    retry_after = response.json().get('retry_after', 1000) / 1000  # In seconds
                    print(gradient_text(f"[!] Rate limit reached. Waiting {retry_after} seconds...", (255, 165, 0), (255, 69, 0)))
                    time.sleep(retry_after)
                else:
                    print(gradient_text(f"[✗] Error: {response.status_code}", (255, 0, 0), (255, 69, 0)))
            except requests.RequestException as e:
                print(gradient_text(f"[!] Network error with proxy {proxy or 'none'}: {e}", (255, 0, 0), (255, 69, 0)))
            time.sleep(frequency_ms / 1000)
    except KeyboardInterrupt:
        print(gradient_text("\n[!] Nuke interrupted by user.", (255, 0, 0), (255, 165, 0)))
    finally:
        session.close()

# Delete a webhook
def delete_webhook(webhook_url, proxies=None):
    session = requests.Session()
    proxy_pool = cycle(proxies) if proxies else None
    proxy = next(proxy_pool) if proxy_pool else None
    proxies_dict = {'http': proxy, 'https': proxy} if proxy else None
    
    print(gradient_text("[!] Deleting webhook...", (255, 0, 0), (255, 165, 0)))
    try:
        response = session.delete(webhook_url, proxies=proxies_dict, timeout=10)
        if response.status_code == 204:
            print(gradient_text("[✓] Webhook deleted successfully!", (0, 255, 0), (173, 255, 47)))
            input(gradient_text("Press Enter to continue...", (0, 255, 0), (173, 255, 47)))
        else:
            print(gradient_text(f"[✗] Error: {response.status_code}", (255, 0, 0), (255, 69, 0)))
            input(gradient_text("Press Enter to continue...", (255, 0, 0), (255, 69, 0)))
    except requests.RequestException as e:
        print(gradient_text(f"[!] Error: {e}", (255, 0, 0), (255, 69, 0)))
        input(gradient_text("Press Enter to continue...", (255, 0, 0), (255, 69, 0)))
    finally:
        session.close()

# Test a webhook
def test_webhook(webhook_url, proxies=None):
    session = requests.Session()
    proxy_pool = cycle(proxies) if proxies else None
    proxy = next(proxy_pool) if proxy_pool else None
    proxies_dict = {'http': proxy, 'https': proxy} if proxy else None
    
    print(gradient_text("[!] Testing webhook...", (0, 255, 255), (0, 128, 128)))
    try:
        response = session.get(webhook_url, proxies=proxies_dict, timeout=10)
        if response.status_code == 200:
            print(gradient_text("[✓] Webhook is active!", (0, 255, 0), (173, 255, 47)))
            input(gradient_text("Press Enter to continue...", (0, 255, 0), (173, 255, 47)))
        else:
            print(gradient_text(f"[✗] Webhook returned code: {response.status_code}", (255, 0, 0), (255, 69, 0)))
            input(gradient_text("Press Enter to continue...", (255, 0, 0), (255, 69, 0)))
    except requests.RequestException as e:
        print(gradient_text(f"[!] Error: {e}", (255, 0, 0), (255, 69, 0)))
        input(gradient_text("Press Enter to continue...", (255, 0, 0), (255, 69, 0)))
    finally:
        session.close()

# Display help
def show_help():
    help_text = """
Available commands:
1. Send POST messages (Nuke) with HTTPS proxy rotation.
2. Delete webhook.
3. Test webhook connection.
4. Add a custom HTTPS proxy.
5. Show this help.
6. Exit.
"""
    print(gradient_text(help_text, (0, 0, 255), (128, 0, 128)))
    input(gradient_text("Press Enter to continue...", (0, 0, 255), (128, 0, 128)))

# Main menu
def main():
    print_banner()
    webhook_url = get_webhook_url()
    proxies = get_valid_proxies(max_proxies=5)
    if not proxies:
        print(gradient_text("[!] No valid proxies found. Would you like to add a custom proxy?", (255, 165, 0), (255, 69, 0)))
        if input(gradient_text("(y/n): ", (0, 0, 255), (128, 0, 128))).lower() == 'y':
            proxies = add_custom_proxy(proxies)

    while True:
        clear_screen_with_banner()
        proxy_count = len(proxies) if proxies else 0
        print(gradient_text(f"HTTPS proxies in use: {proxy_count}", (0, 255, 255), (0, 128, 128)))
        print(gradient_text("""
1. Send messages (Nuke)
2. Delete webhook
3. Test webhook
4. Add custom proxy
5. Show help
6. Exit
""", (0, 0, 255), (128, 0, 128)))

        choice = input(gradient_text("Choose an option: ", (0, 0, 255), (128, 0, 128)))
        if choice == "1":
            send_nuke(webhook_url, proxies)
        elif choice == "2":
            delete_webhook(webhook_url, proxies)
        elif choice == "3":
            test_webhook(webhook_url, proxies)
        elif choice == "4":
            proxies = add_custom_proxy(proxies)
        elif choice == "5":
            show_help()
        elif choice == "6":
            clear_screen_with_banner()
            print(gradient_text("Goodbye!", (0, 0, 255), (128, 0, 128)))
            break
        else:
            print(gradient_text("[!] Invalid option, please try again.", (255, 0, 0), (255, 69, 0)))
            input(gradient_text("Press Enter to continue...", (255, 0, 0), (255, 69, 0)))

if __name__ == "__main__":
    main()
