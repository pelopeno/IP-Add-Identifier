# IP Address Identifier

A modern Flask web application that displays comprehensive IP address information including geolocation, ISP details, network information, and interactive maps with privacy controls.

![IP Address Identifier](templates/logo.png)

## Features

- 🌐 **IP Detection**: Automatic IPv4 and IPv6 address detection
- 📍 **Geolocation**: City, region, country, and coordinate information
- 🏢 **Network Details**: ISP, organization, ASN, and connection type
- 🗺️ **Interactive Map**: Leaflet-powered map with location markers
- 🔒 **Privacy Controls**: Data sanitization and privacy notices
- 📱 **Responsive Design**: Modern, mobile-friendly interface
- ⚡ **Performance**: Intelligent caching and API fallbacks
- 🎨 **Dark Theme**: Custom styled interface with yellow accents

## Screenshots

![Main Interface](screenshots/main-interface.png)
*Clean, modern interface showing network and location information*

## Prerequisites

Before installing, ensure you have the following installed on your system:

- **Python 3.7 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager) - Usually comes with Python
- **Git** (optional, for cloning) - [Download Git](https://git-scm.com/downloads/)
- **Internet connection** - Required for IP geolocation APIs

## Installation Guide

### Method 1: Download ZIP (Recommended for beginners)

1. **Download the application**
   - Click the "Download ZIP" button on the repository page
   - Extract the ZIP file to your desired location
   - Navigate to the extracted folder

2. **Open Command Prompt/Terminal**
   ```bash
   # Windows: Press Win + R, type 'cmd', press Enter
   # macOS: Press Cmd + Space, type 'terminal', press Enter
   # Linux: Press Ctrl + Alt + T
   ```

3. **Navigate to the project directory**
   ```bash
   cd "C:\Users\Letson\OneDrive\Desktop\4ITE\SomethingIPAdd\IP-Add-Identifier"
   ```

### Method 2: Git Clone (For developers)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ip-address-identifier.git
   cd ip-address-identifier
   ```

## Setup Instructions

### 1. Create Virtual Environment (Recommended)

Creating a virtual environment keeps your project dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your command prompt, indicating the virtual environment is active.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file, install dependencies manually:

```bash
pip install Flask requests
```

### 3. Add Required Files

Ensure these files are in your `templates` folder:

- **logo.png** - Your application logo (500px width recommended)
- **bg.png** - Background image (optional)

### 4. Run the Application

```bash
python app.py
```

You should see output similar to:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[your-ip]:5000
```

### 5. Open in Browser

Navigate to: **http://localhost:5000**

## Project Structure

```
IP-Add-Identifier/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/
│   ├── index.html        # Main HTML template
│   ├── logo.png          # Application logo
│   ├── bg.png            # Background image
│   │
│   ├── css/
│   │   └── app.css       # Main stylesheet
│   │
│   └── js/
│       └── app.js        # Client-side JavaScript
│
└── screenshots/          # Application screenshots
    └── main-interface.png
```

## Configuration

### Environment Variables (Optional)

Create a `.env` file for custom configuration:

```bash
# .env file
FLASK_ENV=development
FLASK_DEBUG=True
CACHE_TIMEOUT=300
API_TIMEOUT=10
```

### API Rate Limits

The application uses multiple fallback APIs to ensure reliability:

1. **Primary**: ipapi.co (1000 requests/month free)
2. **Fallback 1**: ip-api.com (unlimited for non-commercial)
3. **Fallback 2**: ipinfo.io (50,000 requests/month free)
4. **WHOIS**: ipwhois.app (10,000 requests/month free)

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'flask'**
```bash
# Solution: Install Flask
pip install flask
```

**2. Port 5000 already in use**
```bash
# Solution: Use a different port
python app.py --port 8080
```

**3. CSS/JS files not loading**
- Check that files are in the correct `templates/` subdirectories
- Verify Flask static folder configuration in `app.py`

**4. API rate limits exceeded**
- Use the "Clear Cached Data" button to reset cache
- Wait for rate limit reset (usually 1 hour)

**5. Map not displaying**
- Check browser console for JavaScript errors
- Ensure internet connection for Leaflet CDN
- Verify coordinates are valid numbers

### Debug Mode

For detailed error information, run with debug enabled:

```bash
# In app.py, ensure debug=True
app.run(host="0.0.0.0", port=5000, debug=True)
```

### Logs

Check the console output for detailed logging:
- API requests and responses
- Cache usage
- Error messages
- Performance metrics

## Customization

### Styling

Edit `templates/css/app.css` to customize:
- Colors and themes
- Layout and spacing
- Responsive breakpoints
- Animations

### Features

Modify `app.py` to:
- Add new API providers
- Change cache timeouts
- Customize privacy settings
- Add new data fields

### UI Components

Update `templates/index.html` to:
- Rearrange information cards
- Add new sections
- Modify button layouts
- Change branding

## Performance Optimization

### Caching

The application includes intelligent caching:
- **IP addresses**: Cached for 1 minute
- **Geolocation data**: Cached for 5 minutes
- **WHOIS data**: Cached for 5 minutes

### API Optimization

- Multiple fallback APIs prevent failures
- Request timeouts prevent hanging
- Rate limiting prevents API abuse
- Error handling ensures graceful degradation

## Security Features

### Privacy Protection

- Partial postal code masking
- Sensitive network name sanitization
- Coordinate precision reduction for sensitive locations
- Privacy notices for users

### Data Handling

- No persistent data storage
- Temporary caching only
- No user tracking
- Local processing only

## Browser Compatibility

- **Chrome** 80+
- **Firefox** 75+
- **Safari** 13+
- **Edge** 80+

## Mobile Support

Fully responsive design supporting:
- Smartphones (320px+)
- Tablets (768px+)
- Desktops (1024px+)

## API Documentation

### Endpoints

**GET /** - Main application interface
**GET /api/ip-info** - JSON API endpoint
**POST /api/clear-cache** - Clear server cache

### Response Format

```json
{
  "ipv4": "203.0.113.1",
  "ipv6": "2001:db8::1",
  "city": "Example City",
  "region": "Example Region",
  "country": "Example Country",
  "org": "Example ISP",
  "isp": "Example ISP",
  "asn": "AS12345",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timezone": "America/New_York",
  "postal": "100XXX",
  "connection_type": "corporate"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues and questions:
- Check this README first
- Look for similar issues in the repository
- Create a new issue with detailed information
- Include error messages and system information

## Changelog

### Version 1.0.0
- Initial release
- IPv4/IPv6 detection
- Geolocation mapping
- Privacy controls
- Responsive design
- API fallbacks
- Caching system

---

**Happy IP tracking! 🌐**


