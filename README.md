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
ip-address-identifier/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── requirements.txt
└── README.md
```

---
## Acknowledgments

* [Leaflet.js](https://leafletjs.com) – for map visualization
* [Font Awesome](https://fontawesome.com) – for icons
* [Google Fonts](https://fonts.google.com) – for typography


