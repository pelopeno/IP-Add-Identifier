// Global variables for IP information
let ipInfo = {};
let isRefreshing = false; // Prevent multiple refresh attempts

// Initialize the application
function initializeApp(ipData) {
    ipInfo = ipData;
    
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

    // Initialize the map
    const map = L.map('map').setView([latitude, longitude], 13);

    // Add OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }).addTo(map);

    // Custom icon for the marker 
    const customIcon = L.divIcon({
        className: 'custom-marker',
        html: '<i class="fas fa-map-marker-alt" style="color: hsl(67 35% 57%); font-size: 24px;"></i>',
        iconSize: [30, 30],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30]
    });

    // Add marker w/ popup including owner info
    const marker = L.marker([latitude, longitude], { icon: customIcon }).addTo(map);
    marker.bindPopup(`
        <div style="text-align: center; padding: 12px; background: hsl(67 41% 6%); color: hsl(69 68% 89%); border-radius: 8px; border: 1px solid hsl(66 49% 13%);">
            <h4 style="margin: 0 0 12px 0; color: hsl(67 35% 57%);"><i class="fas fa-location-dot"></i> Your Location</h4>
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
    }).addTo(map);
}

// when map is not available
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

// Refresh functionality with safety measures
function refreshData() {
    // Prevent multiple simultaneous refresh attempts
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

        // Add minimum delay and maximum timeout
        const minDelay = 1000; // Minimum 1 second
        const maxTimeout = 10000; // Maximum 10 seconds
        
        const startTime = Date.now();
        
        const performRefresh = () => {
            const elapsed = Date.now() - startTime;
            const remainingDelay = Math.max(0, minDelay - elapsed);
            
            setTimeout(() => {
                try {
                    location.reload();
                } catch (error) {
                    console.error('Refresh failed:', error);
                    // Reset button state on error
                    isRefreshing = false;
                    refreshBtn.disabled = false;
                    refreshIcon.className = 'fas fa-sync-alt';
                    refreshText.textContent = 'Refresh Data';
                }
            }, remainingDelay);
        };

        // Set maximum timeout to prevent hanging
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
        
        // Make request to clear server cache
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
            // Prevent rapid clicking
            if (refreshTimeout) {
                clearTimeout(refreshTimeout);
            }
            refreshTimeout = setTimeout(() => {
                refreshData();
            }, 100); // 100ms debounce
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
}

// Add page animations
function addPageAnimations() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animation = `fadeInUp 0.6s ease-out ${index * 0.1}s both`;
    });

    // Add CSS for animations if not already present
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
    
    // Reset refresh state if there's an error
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
    // This will be called from the HTML template with the IP data
    console.log('App.js loaded - waiting for IP data...');
});
