import { MapContainer, TileLayer, Marker, Popup, Polygon } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { api } from '../api';
import { useEffect, useState } from 'react';
import type { Farm } from '../api';
import L from 'leaflet';

// Fix for default leaflet icons in React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export default function FarmsMap() {
  const [farms, setFarms] = useState<Farm[]>([]);

  useEffect(() => {
    api.getFarms().then(res => setFarms(res.data));
  }, []);

  const center: [number, number] = [23.2599, 77.4126]; // Centered on Madhya Pradesh

  return (
    <div className="flex-1 flex flex-col h-full bg-surface">
      <div className="px-8 py-6 flex justify-between items-center border-b border-outline-variant bg-surface z-10">
        <div>
          <h2 className="text-2xl font-bold text-on-surface">Madhya Pradesh Farm Map</h2>
          <p className="text-sm text-on-surface-variant">Real-time geographical tracking of insured properties across MP</p>
        </div>
        <div className="flex gap-2">
          <div className="flex items-center gap-2 text-xs bg-primary/10 text-primary px-3 py-1.5 rounded-full font-medium">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div> Live Satellite Monitoring
          </div>
        </div>
      </div>
      
      <div className="flex-1 relative z-0">
        <MapContainer center={center} zoom={8} className="w-full h-full">
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
          />
          
          {farms.map((farm) => {
            let position: [number, number] | null = null;
            let leafletCoords: [number, number][] | null = null;

            if (farm.centroid) {
              position = [farm.centroid.lat, farm.centroid.lon];
            }
            if (farm.boundary && farm.boundary.coordinates && farm.boundary.coordinates[0]) {
              leafletCoords = farm.boundary.coordinates[0].map(([lon, lat]) => [lat, lon]);
            }

            if (!position) return null;

            return (
              <div key={farm.id}>
                {leafletCoords && (
                  <Polygon 
                    positions={leafletCoords} 
                    pathOptions={{ 
                      color: farm.status === 'VERIFIED' ? '#1B7A3D' : '#F5821F',
                      fillColor: farm.status === 'VERIFIED' ? '#1B7A3D' : '#F5821F',
                      fillOpacity: 0.4
                    }} 
                  />
                )}
                <Marker position={position}>
                  <Popup>
                    <div className="p-1">
                      <h3 className="font-bold text-sm mb-1">{farm.name}</h3>
                      <p className="text-xs mb-1">Crop: {farm.crop || 'Unknown'}</p>
                      <p className="text-xs mb-2">Area: {farm.area_m2.toLocaleString()} m²</p>
                      <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold ${
                        farm.status === 'VERIFIED' ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800'
                      }`}>
                        {farm.status}
                      </span>
                    </div>
                  </Popup>
                </Marker>
              </div>
            );
          })}
        </MapContainer>
      </div>
    </div>
  );
}
