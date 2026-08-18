import {
  MapContainer,
  Marker,
  Polyline,
  Popup,
  TileLayer,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const customIcon = new L.Icon({
  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",

  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",

  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",

  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

const routes = [
  {
    id: "SH-101",
    status: "In Transit",
    from: [19.076, 72.8777] as [number, number],
    to: [28.6139, 77.209] as [number, number],
    color: "#2563eb",
  },
  {
    id: "SH-102",
    status: "Delayed",
    from: [12.9716, 77.5946] as [number, number],
    to: [19.076, 72.8777] as [number, number],
    color: "#f59e0b",
  },
];

const ActiveShipmentsMap = () => {
  return (
    <div
      style={{
        width: "100%",
        height: "320px",
        overflow: "hidden",
        borderRadius: "9px",
        border: "1px solid #e2e8f0",
      }}
    >
      <MapContainer
        center={[20.5937, 78.9629]}
        zoom={4}
        scrollWheelZoom={false}
        style={{
          width: "100%",
          height: "100%",
        }}
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {routes.map((route) => (
          <div key={route.id}>
            <Marker
              position={route.from}
              icon={customIcon}
            >
              <Popup>
                <strong>{route.id}</strong>
                <br />
                Origin
              </Popup>
            </Marker>

            <Marker
              position={route.to}
              icon={customIcon}
            >
              <Popup>
                <strong>{route.id}</strong>
                <br />
                Destination
                <br />
                Status: {route.status}
              </Popup>
            </Marker>

            <Polyline
              positions={[route.from, route.to]}
              pathOptions={{
                color: route.color,
                weight: 3,
                dashArray: "6 6",
              }}
            />
          </div>
        ))}
      </MapContainer>
    </div>
  );
};

export default ActiveShipmentsMap;