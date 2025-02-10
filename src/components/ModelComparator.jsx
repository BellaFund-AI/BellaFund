import React, { useState, useEffect } from 'react';
import VersionSelector from './VersionSelector';
import ComparisonChart from './ComparisonChart';

export default function ModelComparator() {
  const [versions, setVersions] = useState([]);
  const [selected, setSelected] = useState({ v1: null, v2: null });
  const [results, setResults] = useState(null);

  // Load available versions
  useEffect(() => {
    fetch('/api/models/versions')
      .then(res => res.json())
      .then(data => setVersions(data.versions));
  }, []);

  // Handle comparison request
  const runComparison = () => {
    if (selected.v1 && selected.v2) {
      fetch(`/api/models/compare?version1=${selected.v1}&version2=${selected.v2}`)
        .then(res => res.json())
        .then(setResults);
    }
  };

  return (
    <div className="model-comparator">
      <div className="version-selectors">
        <VersionSelector 
          label="Base Version"
          versions={versions}
          selected={selected.v1}
          onChange={v => setSelected(p => ({ ...p, v1: v }))}
        />
        <VersionSelector
          label="Comparison Version"
          versions={versions}
          selected={selected.v2}
          onChange={v => setSelected(p => ({ ...p, v2: v }))}
        />
        <button 
          className="compare-btn"
          onClick={runComparison}
          disabled={!selected.v1 || !selected.v2}
        >
          Compare Versions
        </button>
      </div>

      {results && (
        <div className="comparison-results">
          <ComparisonChart 
            title="Performance Metrics"
            data={results.performance}
            type="bar"
          />
          <ComparisonChart
            title="Feature Importance Changes"
            data={results.feature_importance}
            type="heatmap"
          />
          <DriftAnalysisPanel driftData={results.data_drift} />
        </div>
      )}
    </div>
  );
} 