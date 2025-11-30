import app
import time

# ------------------------------
# 1. validate_ip_address tests
# ------------------------------
def test_validate_ip_address_valid():
    assert app.validate_ip_address("8.8.8.8") is True

def test_validate_ip_address_invalid_too_large():
    assert app.validate_ip_address("999.999.999.999") is False

def test_validate_ip_address_invalid_format():
    assert app.validate_ip_address("abc.def.ghi.jkl") is False

def test_validate_ip_address_empty():
    assert app.validate_ip_address("") is False


# ------------------------------
# 2. is_private_ip tests
# ------------------------------
def test_is_private_ip_true():
    assert app.is_private_ip("192.168.0.1") is True
    assert app.is_private_ip("10.0.0.5") is True
    assert app.is_private_ip("172.16.0.10") is True

def test_is_private_ip_false():
    assert app.is_private_ip("8.8.8.8") is False


# ------------------------------
# 3. sanitize_sensitive_data tests
# ------------------------------
def test_sanitize_sensitive_data_internal_org():
    data = {"org": "Internal Corporate LAN"}
    sanitized = app.sanitize_sensitive_data(data)
    assert sanitized["org"] == "Private Network"

def test_sanitize_sensitive_data_owner_private():
    data = {"owner": "Admin Staff VPN Services"}
    sanitized = app.sanitize_sensitive_data(data)
    assert sanitized["owner"] == "Private Network"

def test_sanitize_sensitive_data_no_change():
    data = {"org": "Google LLC"}
    sanitized = app.sanitize_sensitive_data(data)
    assert sanitized["org"] == "Google LLC"


# ------------------------------
# 4. add_privacy_notice tests
# ------------------------------
def test_add_privacy_notice_private_ip():
    result = {"ipv4": "192.168.1.1"}
    updated = app.add_privacy_notice(result)
    assert updated["is_private_ip"] is True
    assert "Private IP detected" in updated["privacy_notice"]

def test_add_privacy_notice_public_ip():
    result = {"ipv4": "8.8.8.8"}
    updated = app.add_privacy_notice(result)
    assert updated["is_private_ip"] is False
    assert "publicly available" in updated["privacy_notice"]


# ------------------------------
# 5. lookup_ip_info tests (safe cases)
# ------------------------------
def test_lookup_invalid_ip():
    result = app.lookup_ip_info("abc123")
    assert "error" in result

def test_lookup_valid_ip_but_no_api_call():
    # Use a private IP to avoid triggering external API calls
    result = app.lookup_ip_info("192.168.0.1")
    assert result["ipv4"] == "192.168.0.1"

    # City should either be Unknown (fallback) or None (if not filled)
    assert result["city"] in (None, "Unknown")



# ------------------------------
# 6. cache_result decorator tests
# ------------------------------
def test_cache_result_works():
    @app.cache_result(timeout=2)
    def sample(x):
        return time.time()

    t1 = sample(1)
    t2 = sample(1)
    assert t1 == t2  # cached result should match

    time.sleep(2)
    t3 = sample(1)
    assert t1 != t3  # cache expired, new result generated

def test_get_weather_and_time_missing_key():
    """
    If API key exists → temperature will be a float.
    If API key is missing → temperature will be None and condition will be 'Unknown'.
    Both behaviors are valid.
    """
    result = app.get_weather_and_time(14.6, 120.9, "Asia/Manila")

    # Local time should always be returned
    assert result["local_time"] != ""

    temp = result["weather"]["temperature"]

    # Accept either real weather or Unknown fallback
    assert (temp is None) or (isinstance(temp, (int, float)))

def test_lookup_structure():
    result = app.lookup_ip_info("8.8.8.8")

    expected_keys = [
        "ipv4", "ipv6", "city", "region", "country",
        "org", "isp", "asn", "latitude", "longitude",
        "timezone", "postal", "connection_type",
        "owner", "asn_org", "ip_type",
        "privacy_notice", "is_private_ip", "data_retention"
    ]

    for key in expected_keys:
        assert key in result

def test_get_ip_info_structure():
    result = app.get_ip_info()

    assert "ipv4" in result
    assert "ipv6" in result
    assert "privacy_notice" in result

def test_force_fail_for_cicd():
    assert False, "Intentional failure to test CI/CD pipeline"