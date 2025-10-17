# IP Address Identifier

A modern web application that provides detailed insights about IP addresses — including **geolocation data**, **network details**, and an **interactive map visualization**. Designed with privacy and clarity in mind.

---

## Features

### IP Address Detection

* Automatically detects both **IPv4** and **IPv6** addresses.

### Network Information

* IP Address (IPv4 & IPv6)
* IP Owner / Organization
* ISP Provider
* ASN Details
* Connection Type
* Partial Postal Code *(for privacy)*

### Location Details

* City
* Region / State
* Country
* Precise Coordinates

### Interactive Map

* Visualize IP location using **Leaflet.js**
* Zoom and pan controls for detailed exploration

### Privacy-Focused

* Displays only **partial postal codes**
* Clear privacy notices for sensitive data
* Special handling for **private network IPs**
* No permanent data storage

---
## Project Backlog (Future Enhancements)

### High Priority Items

**Custom IP Lookup (3 days)**  
Allow users to manually enter or paste any IP address or domain for lookup instead of only detecting their own.

**UI/UX Improvements (3 days)**  
Implement a dark/light theme toggle, add icons, and improve responsiveness for both desktop and mobile users.

---

### Medium Priority Items

**VPN/Proxy Detection (3 days)**  
Add functionality to detect and flag IPs associated with VPNs, proxies, or anonymizers for transparency.

**Time Zone & Weather Information (2 days)**  
Display the local time and weather conditions based on the detected IP’s location.

**Data Export Feature (3 days)**  
Enable exporting of IP details to formats like PDF, JSON, or TXT for documentation or sharing.

---

### Low Priority Items

**Speed Test Integration (4 days)**  
Add network speed and latency testing features to complement the IP and location details.

**Search History / Recent Lookups (4 days)**  
Store recent searches locally so users can quickly revisit previous IP results.

**Multi-Language Support (5 days)**  
Offer translation options for key UI text and location labels (e.g., English, Filipino, Spanish)..

---

## Technologies Used

### Frontend

* **HTML5**, **CSS3**, **JavaScript**
* **Leaflet.js** for map rendering
* **Font Awesome** for icons
* **Google Fonts** (*Inter*) for typography

### Backend

* **Python**
* **Flask** web framework

---

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/ip-address-identifier.git
   cd ip-address-identifier
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python app.py
   ```

4. **Open in your browser:**

   ```
   http://localhost:5000
   ```

---

## Feature Usage

* **Refresh Data:** Click the refresh button to get the latest IP information
* **Copy IP:** Quickly copy your detected IP address to clipboard
* **Clear Cache:** Remove saved IP data from browser storage
* **Interactive Map:** Explore your IP’s approximate location

---

##  Privacy Considerations

* Displays only **approximate location**
* Shows **partial postal codes**
* Detects and flags **private networks**
* Includes clear **privacy notices**
* **No permanent storage** of user data

---

## Project Structure

```
IP-ADD-IDENTIFIER/
├── templates/
│   ├── css/
│   │   └── app.css
│   └── js/
│       └── app.js
├── bg.png
├── index.html
├── logo.png
├── app.py
└── README.md
```

---
## Acknowledgments

* [Leaflet.js](https://leafletjs.com) – for map visualization
* [Font Awesome](https://fontawesome.com) – for icons
* [Google Fonts](https://fonts.google.com) – for typography


