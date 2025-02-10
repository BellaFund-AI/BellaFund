import React, { useState, useEffect } from 'react';

export default function RepairDashboard() {
  const [stats, setStats] = useState({});
  
  useEffect(() => {
    fetch('/api/repair/stats')
      .then(res => res.json())
      .then(data => setStats(data));
  }, []);

  return (
    <div className="repair-dashboard">
      <h3>Auto-Repair Statistics</h3>
      <div className="metrics">
        <div className="metric-card success-rate">
          <span className="label">Success Rate</span>
          <span className="value">{stats.successRate}%</span>
        </div>
        <div className="metric-card common-strategies">
          <span className="label">Top Strategies</span>
          <ul>
            {stats.commonStrategies?.map(([strategy, count]) => (
              <li key={strategy}>
                {strategy}: {count}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
} 