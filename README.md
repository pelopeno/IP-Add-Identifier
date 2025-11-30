# IP Address Identifier

A modern web application that provides detailed insights about IP addresses — including **geolocation data**, **network details**, **local time**, **weather conditions**, and an **interactive map visualization**. Designed with privacy and clarity in mind.

---

## Features

### IP Address Detection & Lookup

* Automatically detects both **IPv4** and **IPv6** addresses
* **Search any IP address** - Look up information for any public IP
* Real-time IP address validation
* Seamless switching between your IP and searched IPs

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
* **Local Time** - Shows current time at IP location
* **Timezone Information** - Displays timezone of the location

### Weather Information

* **Current Weather Conditions** - Live weather at IP location
* **Temperature** - Current temperature in Celsius
* **Feels Like** - Apparent temperature
* **Humidity** - Current humidity percentage
* Powered by **OpenWeather API**

### Interactive Map

* Visualize IP location using **Leaflet.js**
* Zoom and pan controls for detailed exploration
* Custom markers with detailed popup information
* Approximate location indicator

### Privacy-Focused

* Displays only **partial postal codes**
* Clear privacy notices for sensitive data
* Special handling for **private network IPs**
* No permanent data storage
* Coordinates rounded for sensitive locations

---

## Technologies Used

### Frontend

* **HTML5**, **CSS3**, **JavaScript**
* **Leaflet.js** for map rendering
* **Font Awesome** for icons
* **Google Fonts** (*Inter*, *Montserrat*) for typography

### Backend

* **Python 3.7+**
* **Flask** web framework
* **python-dotenv** for environment variables
* **pytz** for timezone handling
* **requests** for API calls

### External APIs

* **ipapi.co** - Primary geolocation service
* **ip-api.com** - Fallback geolocation
* **ipinfo.io** - Secondary fallback
* **ipwhois.app** - WHOIS data
* **OpenWeather API** - Weather data

---

## Setup

### Prerequisites

* Python 3.7 or higher
* pip (Python package manager)
* Internet connection
* OpenWeather API key (free tier available)

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/ip-address-identifier.git
   cd ip-address-identifier
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   Create a `.env` file in the project root:

   ```env
   # OpenWeather API Key (Get from: https://openweathermap.org/api)
   OPENWEATHER_API_KEY=your_api_key_here
   
   # Flask Configuration (optional)
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

   > **Note:** To get a free OpenWeather API key:
   > 1. Visit https://openweathermap.org/api
   > 2. Sign up for a free account
   > 3. Generate an API key from your dashboard
   > 4. Replace `your_api_key_here` with your actual key

4. **Run the application:**

   ```bash
   python app.py
   ```

5. **Open in your browser:**

   ```
   http://localhost:5000
   ```

---

## Feature Usage

### Your IP Information

* **Auto-Detection:** Automatically shows your current IP information on page load
* **Refresh Data:** Click the refresh button to get the latest IP information
* **Copy IP:** Quickly copy your detected IP address to clipboard
* **Clear Cache:** Remove saved IP data from browser storage

### IP Address Lookup

* **Search Any IP:** Enter any public IP address in the search box
* **Instant Results:** Get comprehensive information about the searched IP
* **Validation:** Automatic validation of IPv4 and IPv6 formats
* **Back to My IP:** Easily return to viewing your own IP information

### Local Time & Weather

* **Real-Time Updates:** Shows current local time at IP location
* **Weather Conditions:** Displays live weather data including:
  - Temperature
  - Feels like temperature
  - Humidity
  - Weather description
* **Timezone Aware:** All times shown in the IP's local timezone

### Interactive Map

* Explore your IP's or searched IP's approximate location
* Click markers for detailed information popup
* Pan and zoom for better view

---

## API Configuration

### OpenWeather API Setup

The application uses OpenWeather API for weather data. Without an API key, weather information will show as "Unknown" but all other features will work normally.

**Free Tier Limits:**
* 60 calls/minute
* 1,000,000 calls/month
* Current weather data
* No credit card required

**Setup Instructions:**
1. Sign up at https://openweathermap.org/api
2. Get your free API key
3. Add to `.env` file
4. Restart the application

See `SETUP_WEATHER.md` for detailed instructions.

---

##  Privacy Considerations

* Displays only **approximate location** (based on IP geolocation)
* Shows **partial postal codes** (first 3 digits only)
* Detects and flags **private networks**
* Includes clear **privacy notices**
* **No permanent storage** of user data
* Coordinates rounded for government/military networks
* All data cached temporarily (5 minutes max)

---

## Project Structure

```
ip-address-identifier/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── SETUP_WEATHER.md           # Weather API setup guide
├── .env                        # Environment variables (create this)
├── .gitignore                 # Git ignore file
├── templates/
│   ├── index.html             # Main HTML template
│   ├── logo.png               # Application logo
│   ├── bg.png                 # Background image
│   ├── css/
│   │   └── app.css            # Main stylesheet
│   └── js/
│       └── app.js             # Client-side JavaScript
└── static/
    ├── css/
    │   └── app.css            # Main stylesheet
    └── js/
        └── app.js             # Client-side JavaScript
```

---

## Troubleshooting

### Weather Not Showing

* **Check API Key:** Ensure `.env` file has valid `OPENWEATHER_API_KEY`
* **Wait for Activation:** New API keys may take 10-15 minutes to activate
* **Restart App:** Always restart Flask after changing `.env`

### IP Lookup Not Working

* **Check IP Format:** Ensure valid IPv4 (e.g., 8.8.8.8) or IPv6 format
* **API Rate Limits:** Multiple APIs used as fallbacks
* **Clear Cache:** Use "Clear Cached Data" button if stale data appears

### Map Not Displaying

* **Check Coordinates:** Ensure latitude and longitude are valid
* **Internet Connection:** Leaflet.js requires CDN access
* **Browser Console:** Check for JavaScript errors

---

## Browser Compatibility

* **Chrome** 80+
* **Firefox** 75+
* **Safari** 13+
* **Edge** 80+
* Mobile browsers (iOS Safari, Chrome Mobile)

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

## Changelog

### Version 2.0.0
* ✨ **IP Address Lookup** - Search and analyze any public IP
* 🕐 **Local Time Display** - Shows current time at IP location
* 🌤️ **Weather Integration** - Live weather data from OpenWeather API
* 🔄 **Improved UI** - Search box with validation
* 🎨 **Enhanced Design** - Modern dark theme with yellow accents
* 🐛 **Bug Fixes** - Various stability improvements

### Version 1.0.0
* Initial release
* IPv4/IPv6 detection
* Geolocation mapping
* Privacy controls
* Responsive design
* API fallbacks
* Caching system

---

## Acknowledgments

* [Leaflet.js](https://leafletjs.com) – for map visualization
* [Font Awesome](https://fontawesome.com) – for icons
* [Google Fonts](https://fonts.google.com) – for typography
* [OpenWeather](https://openweathermap.org) – for weather data
* [ipapi.co](https://ipapi.co) – for geolocation services
* [ip-api.com](https://ip-api.com) – for fallback geolocation
* [ipinfo.io](https://ipinfo.io) – for additional IP data
* [ipwhois.app](https://ipwhois.app) – for WHOIS information

---

**Happy IP tracking! 🌐🔍🌤️**
