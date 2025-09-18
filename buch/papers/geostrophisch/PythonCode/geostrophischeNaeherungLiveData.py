import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# OpenWeatherMap API-Key
API_KEY = 'Input for API-Key'

# Staedte ueber Mitteleuropa verteilt
locations = {
    'Genf': (46.20, 6.15),
    'Lausanne': (46.52, 6.63),
    'Bern': (46.95, 7.44),
    'Zuerich': (47.37, 8.55),
    'Rapperswil': (47.13, 8.49),
    'Chur': (46.85, 9.53),
    'Lugano': (46.00, 8.95),
    'Mailand': (45.46, 9.19),
    'Lyon': (45.76, 4.84),
    'Muenchen': (48.14, 11.58),
    'Stuttgart': (48.78, 9.18),
    'Innsbruck': (47.27, 11.40),
    'Salzburg': (47.81, 13.04),
    'Wien': (48.21, 16.37),
    'Frankfurt': (50.11, 8.68),
    'Nuernberg': (49.45, 11.08),
    'Basel': (47.56, 7.57),
    'Vaduz': (47.14, 9.52),
    'Konstanz': (47.66, 9.17),
    'Sion': (46.23, 7.36),
    'Graz': (47.07, 15.43),
    'Turin': (45.07, 7.69),
    'Bozen': (46.50, 11.35),
    'Freiburg': (47.99, 7.85),
    'Augsburg': (48.37, 10.90),
    'Venedig' : (45.26, 12.20),
    'Triest' : (45.39, 13.46),
    'Strasbourg' : (48.35, 7.45),
    'Luxemburg' : (49.37, 6.8),
    'Prag' : (50.5, 14.25)
}

# Druck abrufen
def get_pressure(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    r = requests.get(url)
    data = r.json()
    return data['main']['pressure'] * 100  # Pa

# Daten sammeln
lats, lons, ps, names = [], [], [], []
print("Lade Druckdaten...")
for name, (lat, lon) in locations.items():
    try:
        p = get_pressure(lat, lon)
        lats.append(lat)
        lons.append(lon)
        ps.append(p)
        names.append(name)
        print(f"{name}: {p/100:.1f} hPa")
    except Exception as e:
        print(f"{name} fehlgeschlagen: {e}")

# Gitter interpolieren
lats, lons, ps = np.array(lats), np.array(lons), np.array(ps)
grid_lon, grid_lat = np.meshgrid(
    np.linspace(min(lons), max(lons), 50),
    np.linspace(min(lats), max(lats), 50)
)
grid_p = griddata((lons, lats), ps, (grid_lon, grid_lat), method='cubic')

# Druckgradienten berechnen
dx = 111000 * np.cos(np.radians(grid_lat))  # m/deg
dy = 111000
dp_dx = np.gradient(grid_p, axis=1) / dx
dp_dy = np.gradient(grid_p, axis=0) / dy

# Coriolis & geostrophischer Wind
Omega = 7.2921e-5
f = 2 * Omega * np.sin(np.radians(grid_lat))
rho = 1.2
u_g = -(1 / (rho * f)) * dp_dy
v_g = (1 / (rho * f)) * dp_dx



# Windgeschwindigkeit (nur zur Farbgebung)
speed = np.sqrt(u_g**2 + v_g**2)

# Plot
plt.figure(figsize=(14, 10))
plt.contourf(grid_lon, grid_lat, grid_p / 100, levels=40, cmap='coolwarm', alpha=0.6)
plt.colorbar(label='Luftdruck [hPa]')
plt.quiver(grid_lon, grid_lat, u_g, v_g, speed, cmap='plasma', scale=300, width=0.0025)

# Staedte einzeichnen
plt.scatter(lons, lats, c='black', s=20, zorder=5)
for name, lon, lat in zip(names, lons, lats):
    if name == 'Rapperswil':
        plt.text(lon - 0.1, lat - 0.15, name, fontsize=11, color='black')
    else:
        plt.text(lon + 0.1, lat + 0.1, name, fontsize=9, color='black')

plt.title("Geostrophischer Wind ueber Mitteleuropa")
plt.xlabel("Laengengrad")
plt.ylabel("Breitengrad")
plt.grid(True)
plt.tight_layout()
plt.show()
