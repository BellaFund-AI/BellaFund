import React, { useState, useEffect } from 'react';

export default function ABTestPanel() {
  const [activeTests, setActiveTests] = useState([]);
  
  useEffect(() => {
    fetch('/api/abtest/active')
      .then(res => res.json())
      .then(setActiveTests);
  }, []);

  return (
    <div className="abtest-panel">
      <h3>Active A/B Tests</h3>
      <div className="test-list">
        {activeTests.map(test => (
          <div key={test.name} className="test-card">
            <div className="test-header">
              <h4>{test.name}</h4>
              <span className="duration">
                Running for {Math.floor(test.duration/3600)}h
              </span>
            </div>
            <div className="variants">
              {test.variants.map(variant => (
                <div key={variant} className="variant">
                  <span className="name">{variant}</span>
                  <span className="traffic">{test.traffic_split[variant]*100}%</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
} 