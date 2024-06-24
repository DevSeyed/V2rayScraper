import requests
from bs4 import BeautifulSoup
import os
import shutil
import logging
from datetime import datetime
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_v2ray_links(url):
    """Fetches V2Ray links from the given URL."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    all_tags = soup.find_all(['div', 'span', 'code'], class_=['tgme_widget_message_text', 'tgme_widget_message_text js-message_text before_footer'])

    v2ray_configs = []
    for tag in all_tags:
        text = tag.get_text()
        if any(text.startswith(proto) for proto in ['vless://', 'ss://', 'trojan://', 'tuic://']):
            v2ray_configs.append(text)

    return v2ray_configs

def get_region_from_ip(ip):
    """Fetches the region based on the given IP."""
    api_endpoints = [
        f'https://ipapi.co/{ip}/json/',
        f'https://ipwhois.app/json/{ip}',
        f'http://www.geoplugin.net/json.gp?ip={ip}',
        f'https://api.ipbase.com/v1/json/{ip}'
    ]

    for endpoint in api_endpoints:
        try:
            response = requests.get(endpoint, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            if 'country' in data:
                return data['country']
        except requests.RequestException as e:
            logging.error(f"Error retrieving region from {endpoint}: {e}")
    return None

def save_configs_by_region(configs):
    """Saves the configurations grouped by region."""
    config_folder = "sub"
    if os.path.exists(config_folder):
        shutil.rmtree(config_folder)
    os.makedirs(config_folder, exist_ok=True)

    for config in configs:
        try:
            ip = config.split('//')[1].split('/')[0]
            region = get_region_from_ip(ip)
            if region:
                region_folder = os.path.join(config_folder, region)
                os.makedirs(region_folder, exist_ok=True)
                with open(os.path.join(region_folder, 'config.txt'), 'a', encoding='utf-8') as file:
                    file.write(config + '\n')
        except Exception as e:
            logging.error(f"Error saving config {config}: {e}")

def fetch_v2ray_configs(urls, max_workers=10):
    """Fetches V2Ray configurations from multiple URLs concurrently."""
    all_v2ray_configs = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(get_v2ray_links, url): url for url in urls}
        for future in tqdm(as_completed(future_to_url), total=len(urls), desc="Fetching V2Ray links"):
            try:
                v2ray_configs = future.result()
                if v2ray_configs:
                    all_v2ray_configs.extend(v2ray_configs)
            except Exception as e:
                url = future_to_url[future]
                logging.error(f"Error fetching data from {url}: {e}")
    return all_v2ray_configs

def main():
    telegram_urls = [
        "https://t.me/s/v2line", "https://t.me/s/forwardv2ray", "https://t.me/s/inikotesla", "https://t.me/s/PrivateVPNs",
        "https://t.me/s/VlessConfig", "https://t.me/s/V2pedia", "https://t.me/s/v2rayNG_Matsuri", "https://t.me/s/PrivateVPNs",
        "https://t.me/s/proxystore11", "https://t.me/s/DirectVPN", "https://t.me/s/VmessProtocol", "https://t.me/s/OutlineVpnOfficial",
        "https://t.me/s/networknim", "https://t.me/s/beiten", "https://t.me/s/MsV2ray", "https://t.me/s/foxrayiran",
        "https://t.me/s/DailyV2RY", "https://t.me/s/yaney_01", "https://t.me/s/FreakConfig", "https://t.me/s/EliV2ray",
        "https://t.me/s/ServerNett", "https://t.me/s/proxystore11", "https://t.me/s/v2rayng_fa2", "https://t.me/s/v2rayng_org",
        "https://t.me/s/V2rayNGvpni", "https://t.me/s/custom_14", "https://t.me/s/v2rayNG_VPNN", "https://t.me/s/v2ray_outlineir",
        "https://t.me/s/v2_vmess", "https://t.me/s/FreeVlessVpn", "https://t.me/s/vmess_vless_v2rayng", "https://t.me/s/PrivateVPNs",
        "https://t.me/s/freeland8", "https://t.me/s/vmessiran", "https://t.me/s/Outline_Vpn", "https://t.me/s/vmessq",
        "https://t.me/s/WeePeeN", "https://t.me/s/V2rayNG3", "https://t.me/s/ShadowsocksM", "https://t.me/s/shadowsocksshop",
        "https://t.me/s/v2rayan", "https://t.me/s/ShadowSocks_s", "https://t.me/s/VmessProtocol", "https://t.me/s/napsternetv_config",
        "https://t.me/s/Easy_Free_VPN", "https://t.me/s/V2Ray_FreedomIran", "https://t.me/s/V2RAY_VMESS_free", "https://t.me/s/v2ray_for_free",
        "https://t.me/s/V2rayN_Free", "https://t.me/s/free4allVPN", "https://t.me/s/vpn_ocean", "https://t.me/s/configV2rayForFree",
        "https://t.me/s/FreeV2rays", "https://t.me/s/DigiV2ray", "https://t.me/s/v2rayNG_VPN", "https://t.me/s/freev2rayssr",
        "https://t.me/s/v2rayn_server", "https://t.me/s/Shadowlinkserverr", "https://t.me/s/iranvpnet", "https://t.me/s/vmess_iran",
        "https://t.me/s/mahsaamoon1", "https://t.me/s/V2RAY_NEW", "https://t.me/s/v2RayChannel", "https://t.me/s/configV2rayNG",
        "https://t.me/s/config_v2ray", "https://t.me/s/vpn_proxy_custom", "https://t.me/s/vpnmasi", "https://t.me/s/v2ray_custom",
        "https://t.me/s/VPNCUSTOMIZE", "https://t.me/s/HTTPCustomLand", "https://t.me/s/vpn_proxy_custom", "https://t.me/s/ViPVpn_v2ray",
        "https://t.me/s/FreeNet1500", "https://t.me/s/v2ray_ar", "https://t.me/s/beta_v2ray", "https://t.me/s/vip_vpn_2022",
        "https://t.me/s/FOX_VPN66", "https://t.me/s/VorTexIRN", "https://t.me/s/YtTe3la", "https://t.me/s/V2RayOxygen",
        "https://t.me/s/Network_442", "https://t.me/s/VPN_443", "https://t.me/s/v2rayng_v", "https://t.me/s/ultrasurf_12",
        "https://t.me/s/iSeqaro", "https://t.me/s/frev2rayng", "https://t.me/s/frev2ray", "https://t.me/s/FreakConfig",
        "https://t.me/s/Awlix_ir", "https://t.me/s/v2rayngvpn", "https://t.me/s/God_CONFIG", "https://t.me/s/Configforvpn01"
    ]

    all_v2ray_configs = fetch_v2ray_configs(telegram_urls, max_workers=20)

    if all_v2ray_configs:
        save_configs_by_region(all_v2ray_configs)
        logging.info("Configs saved successfully.")
    else:
        logging.info("No V2Ray configs found.")

if __name__ == "__main__":
    main()
