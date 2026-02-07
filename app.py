from flask import Flask
import requests
import re
import os

app = Flask(__name__)

# لیست کانال‌های پابلیک
CHANNELS = ["Tweety_Proxy", "vpnsal", "VPNConectd"]

# فایل ذخیره کانفیگ‌های قبلی
OLD_FILE = "old_configs.txt"

def get_old_configs():
    if os.path.exists(OLD_FILE):
        with open(OLD_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_configs(configs):
    with open(OLD_FILE, "w") as f:
        for c in configs:
            f.write(c + "\n")

def fetch_configs():
    all_configs = set()
    for channel in CHANNELS:
        try:
            url = f"https://t.me/s/{channel}"
            html = requests.get(url, timeout=10).text
            configs = re.findall(
                r'(vmess://\S+|vless://\S+|trojan://\S+|tg://proxy\S+)', html
            )
            all_configs.update(configs)
        except:
            continue
    return all_configs

@app.route("/sub")  # لینک subscription
def subscription():
    old_configs = get_old_configs()
    all_configs = fetch_configs()

    # کانفیگ تازه
    new_configs = all_configs - old_configs

    # ذخیره همه کانفیگ‌ها برای دفعه بعد
    save_configs(all_configs)

    if not new_configs:
        return "چیزی تازه پیدا نشد"
    
    # خروجی برای subscription (متن ساده)
    return "\n".join(new_configs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
