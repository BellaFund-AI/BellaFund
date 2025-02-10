import React, { useState, useEffect } from 'react';

export default function RepairExplanation({ dataKey }) {
  const [explanation, setExplanation] = useState(null);

  useEffect(() => {
    fetch(`/api/repair/explain/${dataKey}`)
      .then(res => res.json())
      .then(setExplanation);
  }, [dataKey]);

  return (
    <div className="explanation-panel">
      <h4>策略决策解释</h4>
      <div className="feature-importance">
        {explanation?.feature_contributions.map(([feature, value]) => (
          <div key={feature} className="feature-row">
            <span className="feature-name">{feature}</span>
            <div className="value-bar" style={{width: `${Math.abs(value)*100}%`}}>
              {value.toFixed(2)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
} 