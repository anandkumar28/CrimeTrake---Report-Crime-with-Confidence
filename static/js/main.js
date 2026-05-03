// CrimeTrake - Main JavaScript File

// Auto-hide messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#F56565';
        } else {
            field.style.borderColor = '#E2E8F0';
        }
    });
    
    return isValid;
}

// Mobile menu toggle
const mobileMenuBtn = document.createElement('button');
mobileMenuBtn.className = 'mobile-menu-btn';
mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
mobileMenuBtn.style.display = 'none';

if (window.innerWidth <= 768) {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.parentNode.insertBefore(mobileMenuBtn, navMenu);
        mobileMenuBtn.style.display = 'block';
        
        mobileMenuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
}

// Add slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .nav-menu.active {
        display: flex !important;
        flex-direction: column;
        position: absolute;
        top: 100%;
        right: 0;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 1rem;
        border-radius: 12px;
    }
    
    .mobile-menu-btn {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: var(--text);
    }
`;
document.head.appendChild(style);

// Google Maps initialization (if map element exists)
function initMap() {
    const mapElement = document.getElementById('crime-map');
    if (!mapElement) return;
    
    const map = new google.maps.Map(mapElement, {
        zoom: 12,
        center: { lat: 28.6139, lng: 77.2090 }, // Default: New Delhi
        styles: [
            {
                featureType: 'poi',
                elementType: 'labels',
                stylers: [{ visibility: 'off' }]
            }
        ]
    });
    
    // Add markers from crime data
    if (window.crimeData) {
        window.crimeData.forEach(crime => {
            const marker = new google.maps.Marker({
                position: { lat: crime.latitude, lng: crime.longitude },
                map: map,
                title: crime.title,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 8,
                    fillColor: '#FF6B35',
                    fillOpacity: 0.8,
                    strokeColor: '#fff',
                    strokeWeight: 2
                }
            });
            
            const infoWindow = new google.maps.InfoWindow({
                content: `
                    <div style="padding: 10px;">
                        <h4>${crime.case_id}</h4>
                        <p><strong>${crime.title}</strong></p>
                        <p>${crime.crime_type}</p>
                        <p><small>${crime.date}</small></p>
                    </div>
                `
            });
            
            marker.addListener('click', () => {
                infoWindow.open(map, marker);
            });
        });
    }
}

// Geolocation helper
function getCurrentLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                callback({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
            },
            error => {
                console.error('Error getting location:', error);
                alert('Unable to get your location. Please enter manually.');
            }
        );
    } else {
        alert('Geolocation is not supported by your browser.');
    }
}

// Export functions for use in templates
window.crimetrake = {
    validateForm,
    initMap,
    getCurrentLocation
};

console.log('CrimeTrake initialized successfully');
