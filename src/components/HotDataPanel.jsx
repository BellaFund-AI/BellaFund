import React, { useState, useEffect } from 'react';

export default function HotDataPanel() {
  const [hotspots, setHotspots] = useState([]);
  
  useEffect(() => {
    fetch('/api/storage/hotspots?top_n=10')
      .then(res => res.json())
      .then(data => setHotspots(data));
  }, []);

  return (
    <div className="hotspot-panel">
      <h3>Top 10 Hot Data</h3>
      <table>
        <thead>
          <tr>
            <th>Data Key</th>
            <th>Access Count</th>
            <th>Last Accessed</th>
          </tr>
        </thead>
        <tbody>
          {hotspots.map(([key, info]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{info.access_count}</td>
              <td>{new Date(info.last_accessed).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
} 