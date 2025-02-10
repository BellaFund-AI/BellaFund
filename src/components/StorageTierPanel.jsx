import React, { useState, useEffect } from 'react';

export default function StorageTierPanel() {
  const [tiers, setTiers] = useState([]);
  
  useEffect(() => {
    fetch('/api/storage/providers')
      .then(res => res.json())
      .then(data => setTiers(data));
  }, []);

  return (
    <div className="tier-panel">
      <h3>Multi-Cloud Storage Tiers</h3>
      <div className="provider-list">
        {tiers.all?.map(provider => (
          <div key={provider.name} className={`provider-card ${tiers.active.includes(provider.name) ? 'active' : 'standby'}`}>
            <h4>{provider.name}</h4>
            <p>Cost: ${provider.costPerGB}/GB</p>
            <p>Latency: {provider.latency}ms</p>
            <p>Supported Tiers: {provider.supportedTiers.join(', ')}</p>
          </div>
        ))}
      </div>
    </div>
  );
} 