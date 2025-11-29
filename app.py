from flask import Flask, render_template, request, jsonify
import requests
import logging
import time
from functools import wraps
from dotenv import load_dotenv
import os
import ipaddress

load_dotenv(dotenv_path=".env")
print("DEBUG ENV KEY:", os.getenv("OPENWEATHER_API_KEY"))


app = Flask(__name__, static_folder='static', static_url_path='/static')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_cache = {}
_cache_timeout = 300  

def cache_result(timeout=300):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            current_time = time.time()
            
            if cache_key in _cache:
                cached_time, cached_result = _cache[cache_key]
                if current_time - cached_time < timeout:
                    logger.info(f"Returning cached result for {func.__name__}")
                    return cached_result
            
            result = func(*args, **kwargs)
            _cache[cache_key] = (current_time, result)
            
            keys_to_remove = []
            for key, (cache_time, _) in _cache.items():
                if current_time - cache_time > timeout:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del _cache[key]
            
            return result
        return wrapper
    return decorator


def validate_ip_address(ip):
    """Validate if the provided string is a valid IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


@cache_result(timeout=300)
def get_whois_info(ip):
    """Get WHOIS information for an IP address with rate limiting"""
    try:
        logger.info(f"Fetching WHOIS data for {ip}")
        whois_url = f"https://ipwhois.app/json/{ip}"
        response = requests.get(whois_url, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success", True):
                return {
                    "owner": data.get("org", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "asn": data.get("asn", "Unknown"),
                    "asn_org": data.get("asn_org", "Unknown"),
                    "type": data.get("type", "Unknown")
                }
        elif response.status_code == 429:
            logger.warning("WHOIS API rate limit exceeded")
            return None
        
    except requests.exceptions.Timeout:
        logger.warning("WHOIS lookup timed out")
    except Exception as e:
        logger.warning(f"WHOIS lookup failed: {e}")
    
    return None


@cache_result(timeout=300)
def get_enhanced_ip_info(ip):
    """Get enhanced IP information including ISP details with rate limiting"""
    try:
        logger.info(f"Fetching enhanced IP data for {ip}")
        url = f"https://ipapi.co/{ip}/json/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                return {
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country_name": data.get("country_name"),
                    "org": data.get("org"),
                    "isp": data.get("org"),
                    "asn": data.get("asn"),
                    "latitude": data.get("latitude"),
                    "longitude": data.get("longitude"),
                    "timezone": data.get("timezone"),
                    "postal": data.get("postal"),
                    "connection_type": data.get("connection_type"),
                    "threat_level": data.get("threat_level")
                }
        elif response.status_code == 429:
            logger.warning("Primary API rate limit exceeded")
            raise Exception("Rate limit exceeded")
            
    except requests.exceptions.Timeout:
        logger.warning("Primary API timed out")
        raise Exception("Primary API timeout")
    except Exception as e:
        logger.warning(f"Primary API failed: {e}")
        raise e
    
    return None


def sanitize_sensitive_data(data):
    """Sanitize sensitive information before displaying"""
    private_indicators = [
        'internal', 'private', 'corp', 'intranet', 'lan', 'vpn',
        'employee', 'staff', 'admin', 'secure'
    ]
    
    if data.get('org'):
        org_lower = data['org'].lower()
        for indicator in private_indicators:
            if indicator in org_lower:
                data['org'] = "Private Network"
                break
    
    if data.get('owner'):
        owner_lower = data['owner'].lower()
        for indicator in private_indicators:
            if indicator in owner_lower:
                data['owner'] = "Private Network"
                break
    
    if data.get('org') and any(word in data['org'].lower() for word in ['government', 'military', 'defense']):
        if data.get('latitude') and data.get('longitude'):
            data['latitude'] = round(float(data['latitude']), 1)
            data['longitude'] = round(float(data['longitude']), 1)
    
    return data


def is_private_ip(ip):
    """Check if IP address is in private range"""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except:
        if ip.startswith(('192.168.', '10.', '172.')):
            return True
        if ip.startswith('127.'):
            return True
        return False


def add_privacy_notice(result):
    """Add privacy information to the result"""
    privacy_info = {
        'privacy_notice': 'This information is publicly available through your internet connection.',
        'data_retention': 'Location data is approximate and cached temporarily for performance.',
        'is_private_ip': False
    }
    
    if result.get('ipv4'):
        privacy_info['is_private_ip'] = is_private_ip(result['ipv4'])
        if privacy_info['is_private_ip']:
            privacy_info['privacy_notice'] = 'Private IP detected. Limited information available.'
    
    result.update(privacy_info)
    return result


def get_weather_and_time(lat, lon, timezone):
    """Fetch local weather and local time for the given coordinates."""
    try:
        local_time = "Unknown"
        try:
            from datetime import datetime
            import pytz
            tz = pytz.timezone(timezone)
            local_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass

        WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
        if not WEATHER_API_KEY:
            raise Exception("Missing OpenWeather API key")

        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        )

        weather = requests.get(weather_url, timeout=5).json()

        if "main" in weather:
            weather_info = {
                "temperature": weather["main"]["temp"],
                "feels_like": weather["main"]["feels_like"],
                "humidity": weather["main"]["humidity"],
                "condition": weather["weather"][0]["description"],
            }
        else:
            weather_info = {
                "temperature": None,
                "feels_like": None,
                "humidity": None,
                "condition": "Unknown"
            }

        return {
            "local_time": local_time,
            "weather": weather_info
        }

    except Exception as e:
        logger.warning(f"Weather/Time Lookup Failed: {e}")
        return {
            "local_time": "Unknown",
            "weather": {
                "temperature": None,
                "feels_like": None,
                "humidity": None,
                "condition": "Unknown"
            }
        }


def lookup_ip_info(ip_address):
    """Lookup information for a specific IP address"""
    try:
        if not validate_ip_address(ip_address):
            return {"error": "Invalid IP address format"}
        
        result = {
            "ipv4": ip_address,
            "ipv6": "N/A",
            "city": "Unknown",
            "region": "Unknown",
            "country": "Unknown",
            "org": "Unknown",
            "isp": "Unknown",
            "asn": "Unknown",
            "latitude": None,
            "longitude": None,
            "timezone": "Unknown",
            "postal": "Unknown",
            "connection_type": "Unknown",
            "owner": "Unknown",
            "asn_org": "Unknown",
            "ip_type": "Unknown"
        }

        geo_data = None
        apis_tried = 0
        max_apis = 3  
        
        # Primary API
        if apis_tried < max_apis:
            try:
                apis_tried += 1
                geo_data = get_enhanced_ip_info(ip_address)
                if not geo_data:
                    raise Exception("Primary API returned no data")
            except:
                geo_data = None

        # Fallback API
        if not geo_data and apis_tried < max_apis:
            try:
                apis_tried += 1
                fallback_url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,query"
                fallback_response = requests.get(fallback_url, timeout=10)
                fallback_data = fallback_response.json()
                
                if fallback_data.get("status") == "success":
                    geo_data = {
                        "city": fallback_data.get("city"),
                        "region": fallback_data.get("regionName"),
                        "country_name": fallback_data.get("country"),
                        "org": fallback_data.get("org"),
                        "isp": fallback_data.get("isp"),
                        "asn": fallback_data.get("as"),
                        "asn_org": fallback_data.get("asname"),
                        "latitude": fallback_data.get("lat"),
                        "longitude": fallback_data.get("lon"),
                        "timezone": fallback_data.get("timezone"),
                        "postal": fallback_data.get("zip")
                    }
            except:
                geo_data = None

        # Final Fallback API
        if not geo_data and apis_tried < max_apis:
            try:
                apis_tried += 1
                ipinfo_url = f"https://ipinfo.io/{ip_address}/json"
                ipinfo_data = requests.get(ipinfo_url, timeout=10).json()
                
                loc_parts = ipinfo_data.get("loc", "").split(",")
                lat = float(loc_parts[0]) if len(loc_parts) > 0 else None
                lon = float(loc_parts[1]) if len(loc_parts) > 1 else None

                geo_data = {
                    "city": ipinfo_data.get("city"),
                    "region": ipinfo_data.get("region"),
                    "country_name": ipinfo_data.get("country"),
                    "org": ipinfo_data.get("org"),
                    "isp": ipinfo_data.get("org"),
                    "latitude": lat,
                    "longitude": lon,
                    "timezone": ipinfo_data.get("timezone"),
                    "postal": ipinfo_data.get("postal")
                }
            except:
                geo_data = None

        # Geo merge
        if geo_data:
            result.update({
                "city": geo_data.get("city", "Unknown"),
                "region": geo_data.get("region", "Unknown"),
                "country": geo_data.get("country_name", "Unknown"),
                "org": geo_data.get("org", "Unknown"),
                "isp": geo_data.get("isp", geo_data.get("org", "Unknown")),
                "asn": geo_data.get("asn", "Unknown"),
                "latitude": float(geo_data.get("latitude", 0)) if geo_data.get("latitude") else None,
                "longitude": float(geo_data.get("longitude", 0)) if geo_data.get("longitude") else None,
                "timezone": geo_data.get("timezone", "Unknown"),
                "postal": geo_data.get("postal", "Unknown"),
                "connection_type": geo_data.get("connection_type", "Unknown")
            })
            
            try:
                whois_data = get_whois_info(ip_address)
                if whois_data:
                    result.update({
                        "owner": whois_data.get("owner", result.get("org", "Unknown")),
                        "asn_org": whois_data.get("asn_org", "Unknown"),
                        "ip_type": whois_data.get("type", "Unknown")
                    })
            except:
                pass

        result = sanitize_sensitive_data(result)
        result = add_privacy_notice(result)
        print("DEBUG GEO:", result["latitude"], result["longitude"], result["timezone"])
        print("DEBUG KEY:", os.getenv("OPENWEATHER_API_KEY"))

        # ---- Add Local Time + Weather ----
        if result.get("latitude") and result.get("longitude") and result.get("timezone"):
            extra = get_weather_and_time(
                result["latitude"],
                result["longitude"],
                result["timezone"]
            )
            result.update(extra)
        else:
            result["local_time"] = "Unknown"
            result["weather"] = {
                "temperature": None,
                "feels_like": None,
                "humidity": None,
                "condition": "Unknown"
            }

        # Postal masking
        if result.get('postal') and result['postal'] != 'Unknown':
            result['postal'] = result['postal'][:3] + 'XXX'

        return result

    except Exception as e:
        logger.error(f"Error looking up IP {ip_address}: {e}")
        return {"error": f"An error occurred: {str(e)}"}


def get_ip_info():
    try:
        cache_key = "current_ipv4"
        current_time = time.time()
        
        if cache_key in _cache:
            cached_time, ipv4 = _cache[cache_key]
            if current_time - cached_time < 60:
                logger.info("Using cached IPv4 address")
            else:
                ipv4 = requests.get("https://api.ipify.org?format=json", timeout=10).json().get("ip")
                _cache[cache_key] = (current_time, ipv4)
        else:
            ipv4 = requests.get("https://api.ipify.org?format=json", timeout=10).json().get("ip")
            _cache[cache_key] = (current_time, ipv4)
        
        ipv6 = "Not available"
        try:
            data = requests.get("https://api64.ipify.org?format=json", timeout=5).json()
            fetched_ipv6 = data.get("ip", "")
            if fetched_ipv6 and fetched_ipv6 != ipv4 and ":" in fetched_ipv6:
                ipv6 = fetched_ipv6
        except:
            pass

        result = lookup_ip_info(ipv4)
        result['ipv6'] = ipv6
        
        return result

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": f"An error occurred: {str(e)}"}


@app.route("/")
def index():
    ip_info = get_ip_info()
    return render_template("index.html", ip_info=ip_info)


@app.route("/api/ip-info")
def api_ip_info():
    return jsonify(get_ip_info())


@app.route("/api/lookup", methods=['POST'])
def api_lookup():
    data = request.get_json()
    ip_address = data.get('ip', '').strip()
    
    if not ip_address:
        return jsonify({"error": "IP address is required"}), 400

    # Step 1: Lookup basic IP info
    result = lookup_ip_info(ip_address)

    # If lookup error happen → return early
    if "error" in result:
        return jsonify(result)

    # Step 2: Weather + Time (only if lat + lon)
    lat = result.get("latitude")
    lon = result.get("longitude")
    tz  = result.get("timezone")

    if lat and lon and tz:
        weather_time = get_weather_and_time(lat, lon, tz)

        result["local_time"] = weather_time.get("local_time", "Unknown")
        result["timezone"] = weather_time.get("timezone", tz)
        result["weather"] = weather_time.get("weather", None)
    else:
        result["local_time"] = "Unknown"
        result["weather"] = None

    return jsonify(result)

@app.route("/api/clear-cache", methods=['POST'])
def clear_cache():
    global _cache
    _cache.clear()
    return jsonify({"status": "success", "message": "Cache cleared successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

THIS IS A SYNTAX ERROR

