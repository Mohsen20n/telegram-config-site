from flask import Flask
import requests
import re

app = Flask(__name__)

# لیست کانال‌های پابلیک (بدون @)
CHANNELS = [
    "vpnsal",
    "VPNConectd",
    "Tweety_Proxy"
]

@app.route("/")
def home():
    all_configs = []

    for channel in CHANNELS:
        try:
            url = f"https://t.me/s/{channel}"
            html = requests.get(url, timeout=10).text

            configs = re.findall(
                r'(vmess://\S+|vless://\S+|trojan://\S+|tg://proxy\S+)',
                html
            )

            all_configs.extend(configs)

        except:
            continue

    # حذف تکراری‌ها
    all_configs = list(set(all_configs))

    if not all_configs:
        return "چیزی پیدا نشد"

    # نمایش ساده در سایت
    return "<br>".join(all_configs)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
