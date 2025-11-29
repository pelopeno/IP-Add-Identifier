import app

def test_validate_ip_address_valid():
    assert app.validate_ip_address("8.8.8.8") == True

def test_validate_ip_address_invalid():
    assert app.validate_ip_address("999.999.999.999") == False

def test_is_private_ip():
    assert app.is_private_ip("192.168.1.1") == True
    assert app.is_private_ip("8.8.8.8") == False

def test_sanitize_sensitive_data():
    data = {"org": "Internal internal Network"}
    result = app.sanitize_sensitive_data(data)
    assert result["org"] == "Private Network"

def test_lookup_ip_invalid():
    result = app.lookup_ip_info("abc123")
    assert "error" in result
