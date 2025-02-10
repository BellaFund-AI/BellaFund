import React, { useState, useEffect } from 'react';
import StatusBadge from './StatusBadge';
import ActionItem from './ActionItem';
import ConditionEditor from './ConditionEditor';

export default function WorkflowConfigurator() {
  const [policies, setPolicies] = useState([]);
  
  useEffect(() => {
    fetch('/api/workflow/policies')
      .then(res => res.json())
      .then(data => setPolicies(data));
  }, []);

  return (
    <div className="workflow-config">
      <h2>响应策略配置</h2>
      {policies.map(policy => (
        <div key={policy.type} className="policy-card">
          <div className="policy-header">
            <h3>{policy.type}</h3>
            <StatusBadge status={policy.status} />
          </div>
          <div className="policy-actions">
            {policy.actions.map((action, idx) => (
              <ActionItem key={idx} action={action} />
            ))}
          </div>
          <ConditionEditor conditions={policy.conditions} />
        </div>
      ))}
    </div>
  )
} 