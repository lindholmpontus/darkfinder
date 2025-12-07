const map = L.map('map').setView([59.3, 18.1], 6);

// Use a dark map tile layer for better aesthetics
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

const loadingOverlay = document.getElementById('loading-overlay');
const controls = document.getElementById('controls');
const radiusSlider = document.getElementById('radius-slider');
const radiusValue = document.getElementById('radius-value');

let currentSpots = [];
let currentIndex = 0;
let currentMarker = null;
let currentLine = null;
let userLocation = null;


radiusSlider.addEventListener('input', (e) => {
    radiusValue.textContent = e.target.value;
});

function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

function showControls() {
    controls.classList.remove('hidden');
}

async function fetchSpots() {
    if (!userLocation) return;

    const [userLat, userLon] = userLocation;
    const radius = parseInt(radiusSlider.value);

    showLoading();

    try {
        const response = await fetch("http://localhost:8000/nearest-dark-spot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                lat: userLat,
                lon: userLon,
                radius: radius
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("BACKEND RESPONSE:", data);

        if (!data || data.length === 0) {
            alert("Could not find any dark spots nearby with this radius.");
            return;
        }

        currentSpots = data;
        currentIndex = 0;

        displaySpot(currentIndex);
        showControls();

    } catch (error) {
        console.error("Error fetching dark spots:", error);
        alert("Failed to find dark spots. Please try again later.");
    } finally {
        hideLoading();
    }
}

radiusSlider.addEventListener('change', fetchSpots);

function displaySpot(index) {
    if (!currentSpots || currentSpots.length === 0) return;

    const spot = currentSpots[index];
    const { lat, lon, value } = spot;


    if (currentMarker) map.removeLayer(currentMarker);
    if (currentLine) map.removeLayer(currentLine);

    const darkIcon = L.divIcon({
        className: 'dark-marker',
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });

    currentMarker = L.marker([lat, lon], { icon: darkIcon, title: "Darkest Spot" }).addTo(map);
    currentMarker.bindPopup(`
        <div style="text-align: center;">
            <h3 style="margin: 0 0 5px 0;">🌌 Darkest Spot Found</h3>
            <p style="margin: 0;">Option ${index + 1} of ${currentSpots.length}</p>
            <p style="margin: 0;">Lat: ${lat.toFixed(4)}, Lon: ${lon.toFixed(4)}</p>
            <p style="margin: 0; font-weight: bold; color: #38bdf8;">Radiance: ${value.toFixed(3)}</p>
        </div>
    `).openPopup();


    if (userLocation) {
        currentLine = L.polyline([userLocation, [lat, lon]], {
            color: '#facc15', 
            weight: 3,
            dashArray: '10, 10',
            opacity: 0.8
        }).addTo(map);


        map.fitBounds(currentLine.getBounds(), { padding: [100, 100] });
    }
}


window.nextSpot = function () {
    if (currentSpots.length === 0) return;
    currentIndex = (currentIndex + 1) % currentSpots.length;
    displaySpot(currentIndex);
}

navigator.geolocation.getCurrentPosition(async pos => {
    const userLat = pos.coords.latitude;
    const userLon = pos.coords.longitude;
    userLocation = [userLat, userLon];

    const userIcon = L.divIcon({
        className: 'user-marker',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });

    const userMarker = L.marker([userLat, userLon], { icon: userIcon }).addTo(map);
    userMarker.bindPopup("📍 You are here").openPopup();


    map.setView([userLat, userLon], 8);


    fetchSpots();

}, (error) => {
    console.error("Geolocation error:", error);
    alert("Could not get your location. Please enable location services.");
});
