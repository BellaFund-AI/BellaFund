import React, { useState, useEffect } from 'react';

export default function CostDashboard() {
  const [costData, setCostData] = useState({});
  
  useEffect(() => {
    fetch('/api/storage/cost')
      .then(res => res.json())
      .then(setCostData);
  }, []);

  return (
    <div className="cost-dashboard">
      <h3>Storage Cost Analysis</h3>
      <div className="cost-breakdown">
        <div className="cost-category">
          <span className="label">Hot Data:</span>
          <span className="value">${costData.memory?.toFixed(2)}</span>
        </div>
        <div className="cost-category">
          <span className="label">Warm Data:</span>
          <span className="value">${costData.compressed?.toFixed(2)}</span>
        </div>
        <div className="cost-category">
          <span className="label">Cold Data:</span>
          <span className="value">${costData.archived?.toFixed(2)}</span>
        </div>
        <div className="total-cost">
          <span className="label">Total Daily Cost:</span>
          <span className="value">${costData.total?.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
} 