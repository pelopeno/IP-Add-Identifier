from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_ip_info():
    try:
        ipv4 = requests.get("https://api.ipify.org?format=json").json().get("ip")

        try:
            ipv6 = requests.get("https://api64.ipify.org?format=json").json().get("ip")
        except Exception:
            ipv6 = "Not available"

        geo_url = f"https://ipapi.co/{ipv4}/json/"
        geo_data = requests.get(geo_url).json()

        return {
            "ipv4": ipv4,
            "ipv6": ipv6,
            "city": geo_data.get("city", "Unknown"),
            "region": geo_data.get("region", "Unknown"),
            "country": geo_data.get("country_name", "Unknown"),
            "org": geo_data.get("org", "Unknown"),
            "latitude": geo_data.get("latitude", "Unknown"),
            "longitude": geo_data.get("longitude", "Unknown")
        }
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    ip_info = get_ip_info()
    return render_template("index.html", ip_info=ip_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
