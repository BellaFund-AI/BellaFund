import React, { useState, useEffect } from 'react';
import LineChart from './LineChart';
import auto_rollback from '../services/auto_rollback';

export default function StabilityMonitor() {
  const [stabilityData, setData] = useState([]);

  useEffect(() => {
    fetch('/api/stability-metrics')
      .then(res => res.json())
      .then(data => setData(data));
  }, []);

  return (
    <div className="stability-monitor">
      <h3>Model Stability Tracking</h3>
      <LineChart
        data={stabilityData}
        xKey="timestamp"
        yKeys={['stability', 'error_rate']}
        yLabels={['Stability Score', 'Error Rate']}
        thresholds={{stability: auto_rollback.stability_threshold}}
      />
      <div className="metrics-summary">
        <div>Current Stability: {stabilityData[0]?.stability.toFixed(2)}</div>
        <div>Error Rate: {(stabilityData[0]?.error_rate * 100).toFixed(1)}%</div>
      </div>
    </div>
  );
} 