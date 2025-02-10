import React, { useState, useEffect } from 'react'
import MultiAxisLineChart from './charts/MultiAxisLineChart'
import BenchmarkIndicator from './BenchmarkIndicator'
import VersionSelector from './VersionSelector'

export default function PerformanceDashboard() {
  const [metrics, setMetrics] = useState([])
  const [versions, setVersions] = useState([])
  const [selectedVersion, setVersion] = useState('all')
  const [benchmarks, setBenchmarks] = useState({})
  
  useEffect(() => {
    Promise.all([
      fetch('/api/models/versions'),
      fetch('/api/models/benchmarks')
    ]).then(([versionsRes, benchmarksRes]) => {
      versionsRes.json().then(data => setVersions(data.versions))
      benchmarksRes.json().then(setBenchmarks)
    })
  }, [])

  useEffect(() => {
    const url = selectedVersion === 'all' 
      ? '/api/models/metrics' 
      : `/api/models/metrics?version=${selectedVersion}`
    
    fetch(url)
      .then(res => res.json())
      .then(data => setMetrics(data))
  }, [selectedVersion])

  return (
    <div className="performance-dashboard">
      <div className="dashboard-header">
        <h2>Model Performance Monitoring</h2>
        <VersionSelector 
          versions={['all', ...versions]}
          selected={selectedVersion}
          onChange={setVersion}
        />
      </div>
      
      <div className="metrics-grid">
        <div className="main-chart">
          <MultiAxisLineChart
            data={metrics}
            xKey="timestamp"
            yKeys={['accuracy', 'precision', 'recall']}
            yLabels={['Accuracy (%)', 'Precision (%)', 'Recall (%)']}
            benchmarks={benchmarks.benchmarks}
          />
        </div>
        
        <div className="benchmark-cards">
          {Object.entries(benchmarks.benchmarks || {}).map(([metric, target]) => (
            <BenchmarkIndicator
              key={metric}
              metric={metric}
              current={benchmarks.current_values?.[metric]}
              target={target}
            />
          ))}
        </div>
      </div>
    </div>
  )
} 