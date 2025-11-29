// Global variables for IP information
let ipInfo = {};
let isRefreshing = false;
let currentMap = null;
let isSearchMode = false;
let originalIpInfo = {};

// Initialize the application
function initializeApp(ipData) {
    ipInfo = ipData;
    originalIpInfo = { ...ipData }; // Save original IP data
    
    if (ipInfo && ipInfo.latitude && ipInfo.longitude && !ipInfo.error) {
        initializeMap();
    } else {
        showMapUnavailable();
    }
    
    setupEventListeners();
    addPageAnimations();
}

// Initialize map with IP location
function initializeMap() {
    const latitude = ipInfo.latitude;
    const longitude = ipInfo.longitude;
    const city = ipInfo.city || 'Unknown';
    const country = ipInfo.country || 'Unknown';
    const ipv4 = ipInfo.ipv4 || 'Unknown';
    const owner = ipInfo.owner || ipInfo.org || 'Unknown';
    const isp = ipInfo.isp || 'Unknown';

    // Clear existing map if any
    if (currentMap) {
        currentMap.remove();
        currentMap = null;
    }

    // Initialize the map
    currentMap = L.map('map').setView([latitude, longitude], 13);

    // Add OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }).addTo(currentMap);

    // Custom icon for the marker 
    const customIcon = L.divIcon({
        className: 'custom-marker',
        html: '<i class="fas fa-map-marker-alt" style="color: hsl(67 35% 57%); font-size: 24px;"></i>',
        iconSize: [30, 30],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30]
    });

    // Add marker with popup including owner info
    const marker = L.marker([latitude, longitude], { icon: customIcon }).addTo(currentMap);
    marker.bindPopup(`
        <div style="text-align: center; padding: 12px; background: hsl(67 41% 6%); color: hsl(69 68% 89%); border-radius: 8px; border: 1px solid hsl(66 49% 13%);">
            <h4 style="margin: 0 0 12px 0; color: hsl(67 35% 57%);"><i class="fas fa-location-dot"></i> Location</h4>
            <p style="margin: 6px 0; color: hsl(69 68% 89%);"><strong>IP:</strong> ${ipv4}</p>
            <p style="margin: 6px 0; color: hsl(69 68% 89%);"><strong>Owner:</strong> ${owner}</p>
            <p style="margin: 6px 0; color: hsl(69 68% 89%);"><strong>ISP:</strong> ${isp}</p>
            <p style="margin: 6px 0; color: hsl(69 68% 89%);"><strong>City:</strong> ${city}</p>
            <p style="margin: 6px 0; color: hsl(69 68% 89%);"><strong>Country:</strong> ${country}</p>
            <p style="margin: 6px 0; color: hsl(69 68% 89%);"><strong>Coordinates:</strong> ${latitude.toFixed(4)}, ${longitude.toFixed(4)}</p>
        </div>
    `).openPopup();

    // Add a circle to show approximate area 
    L.circle([latitude, longitude], {
        color: 'hsl(67 35% 57%)',
        fillColor: 'hsl(67 35% 57%)',
        fillOpacity: 0.1,
        radius: 1000
    }).addTo(currentMap);
}

// Show when map is not available
function showMapUnavailable() {
    const mapElement = document.getElementById('map');
    if (mapElement) {
        mapElement.innerHTML = `
            <div style="height: 400px; display: flex; align-items: center; justify-content: center; background: hsl(68 69% 3%); border-radius: 6px; border: 1px solid hsl(66 49% 13%);">
                <div style="text-align: center; color: hsl(68 20% 64%);">
                    <i class="fas fa-map-marked-alt" style="font-size: 3rem; margin-bottom: 16px; color: hsl(9 26% 64%);"></i>
                    <h3 style="margin: 0 0 8px 0; color: hsl(69 68% 89%);">Map Not Available</h3>
                    <p style="margin: 0;">Location coordinates could not be determined</p>
                </div>
            </div>
        `;
    }
}

// Update the UI with new IP data
function updateUIWithIPData(data) {
    if (data.error) {
        showError(data.error);
        return;
    }

    ipInfo = data;

    // Update all info items
    updateInfoValue('IPv4 Address', data.ipv4 || 'Not available');
    updateInfoValue('IPv6 Address', data.ipv6 || 'Not available');
    updateInfoValue('IP Owner', data.owner || data.org || 'Unknown');
    updateInfoValue('ISP Provider', data.isp || 'Unknown');
    updateInfoValue('ASN', data.asn || 'Unknown');
    updateInfoValue('Connection Type', data.connection_type || 'Unknown');
    updateInfoValue('Postal Code (Partial)', data.postal || 'Unknown');
    updateInfoValue('City', data.city || 'Unknown');
    updateInfoValue('Region', data.region || 'Unknown');
    updateInfoValue('Country', data.country || 'Unknown');
    
    if (data.latitude && data.longitude) {
        updateInfoValue('Coordinates', `${data.latitude.toFixed(4)}, ${data.longitude.toFixed(4)}`);
    } else {
        updateInfoValue('Coordinates', 'Unknown');
    }

    // Reinitialize map
    if (data.latitude && data.longitude) {
        initializeMap();
    } else {
        showMapUnavailable();
    }
}

// Helper function to update info values
function updateInfoValue(label, value) {
    const infoItems = document.querySelectorAll('.info-item');
    infoItems.forEach(item => {
        const labelElement = item.querySelector('.info-label');
        if (labelElement && labelElement.textContent.includes(label)) {
            const valueElement = item.querySelector('.info-value');
            if (valueElement) {
                valueElement.textContent = value;
            }
        }
    });
}

// Search for IP address
async function searchIPAddress() {
    const searchInput = document.getElementById('ip-search-input');
    const searchBtn = document.getElementById('search-btn');
    const ipAddress = searchInput.value.trim();

    if (!ipAddress) {
        alert('Please enter an IP address');
        return;
    }

    // Basic IP validation
    const ipv4Pattern = /^(\d{1,3}\.){3}\d{1,3}$/;
    const ipv6Pattern = /^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/;
    
    if (!ipv4Pattern.test(ipAddress) && !ipv6Pattern.test(ipAddress)) {
        alert('Please enter a valid IP address');
        return;
    }

    // Show loading state
    const originalBtnContent = searchBtn.innerHTML;
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
    searchBtn.disabled = true;

    try {
        const response = await fetch('/api/lookup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ip: ipAddress })
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // Update UI with search results
        isSearchMode = true;
        updateUIWithIPData(data);

        // Show search results header
        const searchResultsHeader = document.getElementById('search-results-header');
        const searchedIP = document.getElementById('searched-ip');
        searchResultsHeader.style.display = 'flex';
        searchedIP.textContent = ipAddress;

        // Update mode badge
        const modeToggle = document.getElementById('mode-toggle');
        modeToggle.innerHTML = '<span class="mode-badge"><i class="fas fa-search"></i> Viewing Search Results</span>';

        // Scroll to results
        document.getElementById('main-grid').scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Search error:', error);
        alert(`Failed to lookup IP address: ${error.message}`);
    } finally {
        searchBtn.innerHTML = originalBtnContent;
        searchBtn.disabled = false;
    }
}

// Return to original IP view
function backToMyIP() {
    isSearchMode = false;
    
    // Hide search results header
    const searchResultsHeader = document.getElementById('search-results-header');
    searchResultsHeader.style.display = 'none';

    // Update mode badge
    const modeToggle = document.getElementById('mode-toggle');
    modeToggle.innerHTML = '<span class="mode-badge"><i class="fas fa-user"></i> Viewing Your IP</span>';

    // Clear search input
    const searchInput = document.getElementById('ip-search-input');
    searchInput.value = '';

    // Restore original IP data
    updateUIWithIPData(originalIpInfo);

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show error message
function showError(message) {
    const mainGrid = document.getElementById('main-grid');
    mainGrid.innerHTML = `
        <div class="card" style="grid-column: 1 / -1;">
            <div class="card-content">
                <div class="error-state">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Error</h3>
                    <p>${message}</p>
                </div>
            </div>
        </div>
    `;
}

// Refresh functionality with safety measures
function refreshData() {
    if (isRefreshing) {
        console.log('Refresh already in progress, ignoring request');
        return;
    }

    const refreshBtn = document.getElementById('refresh-btn');
    const refreshText = document.getElementById('refresh-text');
    const refreshIcon = refreshBtn.querySelector('i');

    if (refreshBtn && refreshText && refreshIcon) {
        isRefreshing = true;
        refreshBtn.disabled = true;
        refreshIcon.className = 'loading';
        refreshText.textContent = 'Refreshing...';

        const minDelay = 1000;
        const maxTimeout = 10000;
        const startTime = Date.now();
        
        const performRefresh = () => {
            const elapsed = Date.now() - startTime;
            const remainingDelay = Math.max(0, minDelay - elapsed);
            
            setTimeout(() => {
                try {
                    location.reload();
                } catch (error) {
                    console.error('Refresh failed:', error);
                    isRefreshing = false;
                    refreshBtn.disabled = false;
                    refreshIcon.className = 'fas fa-sync-alt';
                    refreshText.textContent = 'Refresh Data';
                }
            }, remainingDelay);
        };

        setTimeout(() => {
            if (isRefreshing) {
                console.warn('Refresh timeout reached, forcing reload');
                performRefresh();
            }
        }, maxTimeout);

        performRefresh();
    }
}

// Copy IP to clipboard
function copyToClipboard() {
    if (ipInfo && ipInfo.ipv4 && !ipInfo.error) {
        const ip = ipInfo.ipv4;
        
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(ip).then(() => {
                showCopySuccess();
            }).catch(() => {
                fallbackCopyToClipboard(ip);
            });
        } else {
            fallbackCopyToClipboard(ip);
        }
    }
}

// Fallback copy method for older browsers
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess();
    } catch (err) {
        alert('Failed to copy IP address');
    } finally {
        document.body.removeChild(textArea);
    }
}

// Show copy success feedback
function showCopySuccess() {
    const btn = document.getElementById('copy-btn');
    if (btn) {
        const originalText = btn.innerHTML;
        const originalStyle = {
            background: btn.style.background,
            borderColor: btn.style.borderColor,
            color: btn.style.color
        };
        
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        btn.style.background = 'hsl(146 17% 59%)';
        btn.style.borderColor = 'hsl(146 17% 59%)';
        btn.style.color = 'hsl(67 100% 1%)';

        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = originalStyle.background || '';
            btn.style.borderColor = originalStyle.borderColor || '';
            btn.style.color = originalStyle.color || '';
        }, 2000);
    }
}

// Clear cached data functionality
function clearCachedData() {
    const clearBtn = document.getElementById('clear-cache-btn');
    if (clearBtn) {
        const originalText = clearBtn.innerHTML;
        clearBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Clearing...';
        clearBtn.disabled = true;
        
        fetch('/api/clear-cache', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                clearBtn.innerHTML = '<i class="fas fa-check"></i> Cleared!';
                setTimeout(() => {
                    clearBtn.innerHTML = originalText;
                    clearBtn.disabled = false;
                }, 2000);
            })
            .catch(error => {
                console.error('Failed to clear cache:', error);
                clearBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Failed';
                setTimeout(() => {
                    clearBtn.innerHTML = originalText;
                    clearBtn.disabled = false;
                }, 2000);
            });
    }
}

// Setup event listeners
function setupEventListeners() {
    // Refresh button with debouncing
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        let refreshTimeout;
        refreshBtn.addEventListener('click', function(e) {
            if (refreshTimeout) {
                clearTimeout(refreshTimeout);
            }
            refreshTimeout = setTimeout(() => {
                refreshData();
            }, 100);
        });
    }

    // Copy button
    const copyBtn = document.getElementById('copy-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', copyToClipboard);
    }

    // Clear cache button
    const clearCacheBtn = document.getElementById('clear-cache-btn');
    if (clearCacheBtn) {
        clearCacheBtn.addEventListener('click', clearCachedData);
    }

    // Search button
    const searchBtn = document.getElementById('search-btn');
    if (searchBtn) {
        searchBtn.addEventListener('click', searchIPAddress);
    }

    // Search input - Enter key
    const searchInput = document.getElementById('ip-search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchIPAddress();
            }
        });
    }

    // Back button
    const backBtn = document.getElementById('back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', backToMyIP);
    }
}

// Add page animations
function addPageAnimations() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animation = `fadeInUp 0.6s ease-out ${index * 0.1}s both`;
    });

    if (!document.querySelector('#animation-styles')) {
        const style = document.createElement('style');
        style.id = 'animation-styles';
        style.textContent = `
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Add error boundary for the entire app
window.addEventListener('error', function(event) {
    console.error('Global error caught:', event.error);
    
    if (isRefreshing) {
        isRefreshing = false;
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.disabled = false;
            const refreshIcon = refreshBtn.querySelector('i');
            const refreshText = document.getElementById('refresh-text');
            if (refreshIcon) refreshIcon.className = 'fas fa-sync-alt';
            if (refreshText) refreshText.textContent = 'Refresh Data';
        }
    }
});

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('App.js loaded - waiting for IP data...');
});