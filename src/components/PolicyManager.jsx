import React, { useState, useEffect } from 'react';

export default function PolicyManager() {
  const [policies, setPolicies] = useState({});
  
  useEffect(() => {
    fetch('/api/policies/current')
      .then(res => res.json())
      .then(setPolicies);
  }, []);

  return (
    <div className="policy-manager">
      <h3>Storage Policies</h3>
      <div className="policy-item">
        <label>Hot Data Retention:</label>
        <span>{policies.hot_data_days} days</span>
      </div>
      <div className="policy-item">
        <label>Archive Frequency:</label>
        <span>Every {policies.archive_frequency} days</span>
      </div>
      <button onClick={() => fetch('/api/policies/optimize', {method: 'POST'})}>
        Run Optimization
      </button>
    </div>
  );
} 