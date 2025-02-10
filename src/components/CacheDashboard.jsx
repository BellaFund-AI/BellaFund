import React, { useState, useEffect } from 'react';

export default function CacheDashboard() {
  const [metrics, setMetrics] = useState({});
  
  useEffect(() => {
    const interval = setInterval(() => {
      fetch('/api/cache/metrics')
        .then(res => res.json())
        .then(setMetrics);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="cache-dashboard">
      <h3>Cache Performance</h3>
      <div className="metrics-grid">
        <div className="metric-card">
          <span className="label">Hit Rate</span>
          <span className="value">{(metrics.hit_rate * 100).toFixed(1)}%</span>
        </div>
        <div className="metric-card">
          <span className="label">Latency</span>
          <span className="value">{metrics.avg_latency?.toFixed(2)}ms</span>
        </div>
        <div className="metric-card">
          <span className="label">Exploration Rate</span>
          <span className="value">{(metrics.epsilon * 100).toFixed(1)}%</span>
        </div>
      </div>
      <button onClick={() => fetch('/api/cache/retrain', {method: 'POST'})}>
        Manual Retrain
      </button>
    </div>
  );
} 