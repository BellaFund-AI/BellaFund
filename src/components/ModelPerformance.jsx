import React, { useState, useEffect } from 'react'
import LineChart from './LineChart'
import MetricCard from './MetricCard'

export default function ModelPerformance() {
  const [metrics, setMetrics] = useState([])
  
  useEffect(() => {
    fetch('/api/models/metrics')
      .then(res => res.json())
      .then(data => setMetrics(data))
  }, [])

  return (
    <div className="performance-dashboard">
      <h2>Model Performance Over Time</h2>
      <LineChart
        data={metrics}
        xKey="timestamp"
        yKeys={['accuracy', 'precision', 'recall']}
        labels={['Accuracy', 'Precision', 'Recall']}
      />
      <div className="metric-cards">
        <MetricCard title="Current Accuracy" value={metrics[0]?.accuracy} />
        <MetricCard title="Avg Precision" value={calculateAverage(metrics, 'precision')} />
        <MetricCard title="Peak Recall" value={findMax(metrics, 'recall')} />
      </div>
    </div>
  )
} 