#!/usr/bin/env python3
"""Inject Live Weather + Leaflet map into main destination pages."""
import re

LEAFLET_HEAD = '''<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV/XN/WLc=" crossorigin=""></script>'''

WX_JS = '''
const WMO = {0:'Clear sky',1:'Mainly clear',2:'Partly cloudy',3:'Overcast',45:'Foggy',48:'Icy fog',51:'Light drizzle',53:'Drizzle',55:'Heavy drizzle',61:'Light rain',63:'Rain',65:'Heavy rain',71:'Light snow',73:'Snow',75:'Heavy snow',80:'Rain showers',81:'Rain showers',82:'Heavy showers',85:'Snow showers',86:'Heavy snow showers',95:'Thunderstorm',96:'Thunderstorm',99:'Thunderstorm'};
const WMO_ICON = {0:'☀️',1:'🌤️',2:'⛅',3:'☁️',45:'🌫️',48:'🌫️',51:'🌦️',53:'🌦️',55:'🌧️',61:'🌦️',63:'🌧️',65:'🌧️',71:'🌨️',73:'❄️',75:'❄️',80:'🌦️',81:'🌧️',82:'⛈️',85:'🌨️',86:'❄️',95:'⛈️',96:'⛈️',99:'⛈️'};
const DAYS = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
async function loadWeather(lat, lon) {
  const el = document.getElementById('wxWidget');
  try {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=Asia%2FKarachi&forecast_days=5`;
    const r = await fetch(url);
    const d = await r.json();
    const c = d.current;
    const dy = d.daily;
    const code = c.weather_code;
    const icon = WMO_ICON[code] || '🌡️';
    const desc = WMO[code] || 'Unknown';
    const forecastHTML = dy.time.slice(1).map((t,i) => {
      const dayName = DAYS[new Date(t).getDay()];
      const ic = WMO_ICON[dy.weather_code[i+1]] || '🌡️';
      return `<div class="wx-day"><div class="wx-day-name">${dayName}</div><div class="wx-day-icon">${ic}</div><div class="wx-day-hi">${Math.round(dy.temperature_2m_max[i+1])}°</div><div class="wx-day-lo">${Math.round(dy.temperature_2m_min[i+1])}°</div></div>`;
    }).join('');
    el.innerHTML = `
      <div class="wx-label">Live Conditions</div>
      <div class="wx-now"><div class="wx-temp">${Math.round(c.temperature_2m)}<sup>°C</sup></div><div class="wx-icon">${icon}</div></div>
      <div class="wx-desc">${desc}</div>
      <div class="wx-meta">
        <div class="wx-meta-item"><strong>${Math.round(c.wind_speed_10m)} km/h</strong>Wind</div>
        <div class="wx-meta-item"><strong>${c.relative_humidity_2m}%</strong>Humidity</div>
        <div class="wx-meta-item"><strong>${Math.round(dy.temperature_2m_min[0])}° / ${Math.round(dy.temperature_2m_max[0])}°</strong>Today</div>
      </div>
      <div class="wx-forecast">${forecastHTML}</div>`;
  } catch(e) {
    el.innerHTML = '<div class="wx-loading">Weather unavailable</div>';
  }
}'''

PAGES = [
  {
    'file': 'hunza/index.html',
    'lat': 36.3167,
    'lon': 74.6500,
    'anchor': '<!-- BREADCRUMB -->',
    'insert_after': '</div>\n</div>',
    'map_center': [36.35, 74.72],
    'map_zoom': 10,
    'markers': [
      (36.3178, 74.6528, 'Karimabad', 'Main town · 2,438m · base for all Hunza trips'),
      (36.3494, 74.8167, 'Attabad Lake', 'Turquoise lake formed after 2010 landslide · boat trips available'),
      (36.3333, 74.6500, "Eagle's Nest", 'Best sunrise viewpoint in Hunza · 3,600m'),
      (36.2875, 74.6458, 'Altit Fort', '900+ year old fort · panoramic valley views'),
      (36.3178, 74.6528, 'Baltit Fort', 'UNESCO heritage · 700 years old · above Karimabad'),
      (36.4750, 74.8600, 'Passu', 'Passu Cones trailhead · Hussaini bridge nearby'),
    ],
  },
  {
    'file': 'skardu/index.html',
    'lat': 35.2971,
    'lon': 75.6333,
    'anchor': '<!-- BREADCRUMB -->',
    'insert_after': '</div>\n</div>',
    'map_center': [35.35, 75.65],
    'map_zoom': 9,
    'markers': [
      (35.2971, 75.6333, 'Skardu', 'Main town · 2,228m · K2 expedition base'),
      (35.5167, 75.7167, 'Shigar Fort', 'Restored heritage hotel · finest Baltistani architecture'),
      (35.1833, 75.6333, 'Shangrila Resort', 'Lower Kachura Lake · iconic GB landmark'),
      (35.0500, 75.5333, 'Deosai Plains', '4,114m · wildflowers in July · Himalayan brown bear'),
      (35.2333, 75.6167, 'Satpara Lake', '8km from Skardu · kayaking & fishing'),
      (35.8804, 76.5144, 'K2 Base Camp', '5,100m · 11-14 day trek from Askole'),
    ],
  },
  {
    'file': 'gilgit/index.html',
    'lat': 35.9208,
    'lon': 74.3083,
    'anchor': '<!-- BREADCRUMB -->',
    'insert_after': '</div>\n</div>',
    'map_center': [35.95, 74.30],
    'map_zoom': 10,
    'markers': [
      (35.9208, 74.3083, 'Gilgit City', 'Hub of GB · best banking & transport links'),
      (36.1833, 74.2000, 'Naltar Valley', '3 coloured lakes · ski resort · Apr–Oct trekking'),
      (35.9333, 74.2833, 'Kargah Buddha', '7th century rock carving · 8km from city'),
      (35.9000, 74.3500, 'Gilgit River Confluence', 'Where Gilgit meets Hunza River · scenic point'),
      (35.9167, 74.3000, 'Polo Ground', 'Historic ground · Pakistan\'s wildest polo games'),
    ],
  },
  {
    'file': 'fairy-meadows/index.html',
    'lat': 35.3833,
    'lon': 74.5667,
    'anchor': '<!-- BREADCRUMB -->',
    'insert_after': '</div>\n</div>',
    'map_center': [35.38, 74.57],
    'map_zoom': 11,
    'markers': [
      (35.3833, 74.5667, 'Fairy Meadows', '3,300m · main camp area · wildflowers Jun–Aug'),
      (35.2333, 74.5833, 'Nanga Parbat Base Camp', '3,600m · 3-4h hike from Fairy Meadows'),
      (35.4333, 74.5000, 'Raikot Bridge', 'KKH trailhead · jeep ride starts here'),
      (35.3500, 74.5333, 'Beyal Camp', '3,500m · intermediate camp on the way to base camp'),
      (35.3667, 74.5500, 'Pine Forest', 'Dense conifer forest · best photography zone'),
    ],
  },
]

def make_widget(page):
  lat = page['lat']
  lon = page['lon']
  mc = page['map_center']
  zoom = page['map_zoom']
  markers_js = '\n    '.join(
    f"L.marker([{m[0]},{m[1]}], {{icon:pinIcon}}).addTo(map).bindPopup('<strong>{m[2]}</strong>{m[3]}');"
    for m in page['markers']
  )
  return f'''
<!-- LIVE CONDITIONS -->
<div class="live-conditions">
  <div class="live-inner">
    <div class="live-weather" id="wxWidget"><div class="wx-loading">Fetching conditions…</div></div>
    <div class="live-map"><div id="map"></div></div>
  </div>
</div>
<script>
{WX_JS}
loadWeather({lat}, {lon});
(function(){{
  const map = L.map('map', {{zoomControl:true, scrollWheelZoom:false}}).setView([{mc[0]},{mc[1]}], {zoom});
  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 18
  }}).addTo(map);
  const pinIcon = L.divIcon({{
    className: '',
    html: '<div style="width:12px;height:12px;background:#C8903A;border-radius:50%;border:2px solid #F0E8D5;box-shadow:0 2px 8px rgba(0,0,0,0.6);"></div>',
    iconSize: [12,12], iconAnchor: [6,6], popupAnchor: [0,-10]
  }});
  {markers_js}
}})();
</script>
'''

for page in PAGES:
  path = f'/Users/mac/Desktop/localgb/{page["file"]}'
  with open(path, 'r') as f:
    html = f.read()

  # Remove existing widget if already injected
  html = re.sub(r'\n<!-- LIVE CONDITIONS -->.*?</script>\n', '', html, flags=re.DOTALL)

  # Find insertion point: after the closing breadcrumb </div></div>
  breadcrumb_end = html.find('</div>\n</div>', html.find('class="breadcrumb"'))
  if breadcrumb_end == -1:
    print(f'WARNING: breadcrumb end not found in {page["file"]}')
    continue
  insert_pos = breadcrumb_end + len('</div>\n</div>')

  # Add Leaflet to <head> if not already there
  if 'leaflet.css' not in html:
    html = html.replace('</head>', LEAFLET_HEAD + '\n</head>', 1)

  widget = make_widget(page)
  html = html[:insert_pos] + widget + html[insert_pos:]

  with open(path, 'w') as f:
    f.write(html)
  print(f'✓ Injected into {page["file"]}')

print('Done.')
