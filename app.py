from flask import Flask, render_template
import requests
import logging
import time
from functools import wraps

app = Flask(__name__, static_folder='templates', static_url_path='/')
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

@cache_result(timeout=300)
def get_whois_info(ip):
    """
    Get WHOIS information for an IP address with rate limiting
    Returns organization/ISP information
    """
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
    """
    Get enhanced IP information including ISP details with rate limiting
    """
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
    """
    Sanitize sensitive information before displaying
    """
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
    """
    Check if IP address is in private range
    """
    try:
        import ipaddress
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except:
        if ip.startswith(('192.168.', '10.', '172.')):
            return True
        if ip.startswith('127.'):  # Localhost dito
            return True
        return False

def add_privacy_notice(result):
    """
    Add privacy information to the result
    """
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

def get_ip_info():
    """
    Fetch IP information with privacy controls
    """
    try:
        cache_key = "current_ipv4"
        current_time = time.time()
        
        if cache_key in _cache:
            cached_time, ipv4 = _cache[cache_key]
            if current_time - cached_time < 60:  
                logger.info("Using cached IPv4 address")
            else:
                logger.info("Fetching fresh IPv4 address...")
                ipv4_response = requests.get("https://api.ipify.org?format=json", timeout=10)
                ipv4_response.raise_for_status()
                ipv4 = ipv4_response.json().get("ip")
                _cache[cache_key] = (current_time, ipv4)
        else:
            logger.info("Fetching IPv4 address...")
            ipv4_response = requests.get("https://api.ipify.org?format=json", timeout=10)
            ipv4_response.raise_for_status()
            ipv4 = ipv4_response.json().get("ip")
            _cache[cache_key] = (current_time, ipv4)
        
        ipv6 = "Not available"
        try:
            logger.info("Fetching IPv6 address...")
            ipv6_response = requests.get("https://api64.ipify.org?format=json", timeout=5)
            if ipv6_response.status_code == 200:
                ipv6_data = ipv6_response.json()
                fetched_ipv6 = ipv6_data.get("ip", "")
                
                if fetched_ipv6 and fetched_ipv6 != ipv4:
                    if ':' in fetched_ipv6:
                        ipv6 = fetched_ipv6
                        logger.info(f"IPv6 address found: {ipv6}")
                    else:
                        logger.info("IPv6 service returned IPv4 address, no IPv6 available")
                        ipv6 = "Not available"
                else:
                    logger.info("No IPv6 address available or same as IPv4")
                    ipv6 = "Not available"
        except Exception as e:
            logger.warning(f"IPv6 fetch failed (non-critical): {e}")
            ipv6 = "Not available"

        if not ipv4:
            raise Exception("Unable to determine IP address")

        result = {
            "ipv4": ipv4,
            "ipv6": ipv6,
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
        
        if apis_tried < max_apis:
            try:
                apis_tried += 1
                logger.info(f"Trying primary API (attempt {apis_tried}/{max_apis})")
                geo_data = get_enhanced_ip_info(ipv4)
                if geo_data:
                    logger.info("Primary API successful")
                else:
                    raise Exception("Primary API returned no data")
                    
            except Exception as e:
                logger.warning(f"Primary API failed: {e}")
                geo_data = None
        
        if not geo_data and apis_tried < max_apis:
            try:
                apis_tried += 1
                logger.info(f"Trying fallback API ip-api.com (attempt {apis_tried}/{max_apis})")
                fallback_url = f"http://ip-api.com/json/{ipv4}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,query"
                fallback_response = requests.get(fallback_url, timeout=10)
                fallback_response.raise_for_status()
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
                    logger.info("Fallback API successful")
                else:
                    raise Exception(fallback_data.get("message", "Fallback API failed"))
                    
            except Exception as e:
                logger.warning(f"Fallback API failed: {e}")
                geo_data = None

        if not geo_data and apis_tried < max_apis:
            try:
                apis_tried += 1
                logger.info(f"Trying final fallback API ipinfo.io (attempt {apis_tried}/{max_apis})")
                ipinfo_url = f"https://ipinfo.io/{ipv4}/json"
                ipinfo_response = requests.get(ipinfo_url, timeout=10)
                ipinfo_response.raise_for_status()
                ipinfo_data = ipinfo_response.json()
                
                loc_parts = ipinfo_data.get("loc", "").split(",")
                latitude = float(loc_parts[0]) if len(loc_parts) > 0 and loc_parts[0] else None
                longitude = float(loc_parts[1]) if len(loc_parts) > 1 and loc_parts[1] else None
                
                geo_data = {
                    "city": ipinfo_data.get("city"),
                    "region": ipinfo_data.get("region"),
                    "country_name": ipinfo_data.get("country"),
                    "org": ipinfo_data.get("org"),
                    "isp": ipinfo_data.get("org"),
                    "latitude": latitude,
                    "longitude": longitude,
                    "timezone": ipinfo_data.get("timezone"),
                    "postal": ipinfo_data.get("postal")
                }
                logger.info("Final fallback API successful")
                
            except Exception as e:
                logger.warning(f"Final fallback API failed: {e}")
                logger.info("All geolocation APIs failed, returning basic IP info")

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
                whois_data = get_whois_info(ipv4)
                if whois_data:
                    result.update({
                        "owner": whois_data.get("owner", result.get("org", "Unknown")),
                        "asn_org": whois_data.get("asn_org", "Unknown"),
                        "ip_type": whois_data.get("type", "Unknown")
                    })
                    logger.info("WHOIS data added successfully")
            except Exception as e:
                logger.warning(f"WHOIS lookup failed (non-critical): {e}")

        result = sanitize_sensitive_data(result)
        result = add_privacy_notice(result)
        
        if result.get('postal') and result['postal'] != 'Unknown':
            result['postal'] = result['postal'][:3] + 'XXX'  
        
        logger.info(f"IP info gathering completed. APIs tried: {apis_tried}")
        return result
            
    except requests.exceptions.Timeout:
        logger.error("Request timeout while fetching IP information")
        return {"error": "Request timeout - please try again"}
    except requests.exceptions.ConnectionError:
        logger.error("Connection error while fetching IP information")
        return {"error": "Connection error - please check your internet connection"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": f"An error occurred: {str(e)}"}

@app.route("/")
def index():
    """
    Main route that renders the IP information page 
    """
    ip_info = get_ip_info()
    return render_template("index.html", ip_info=ip_info)

@app.route("/api/ip-info")
def api_ip_info():
    """
    API endpoint that returns IP information as JSON
    """
    return get_ip_info()

@app.route("/api/clear-cache", methods=['POST'])
def clear_cache():
    """
    Clear the application cache
    """
    global _cache
    _cache.clear()
    logger.info("Cache cleared by user request")
    return {"status": "success", "message": "Cache cleared successfully"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
