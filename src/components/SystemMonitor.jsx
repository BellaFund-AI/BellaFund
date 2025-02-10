import React, { useState, useEffect } from 'react'
import LineChart from './LineChart'
import ScalingHistory from './ScalingHistory'
import ResourceUsage from './ResourceUsage'

export default function SystemMonitor() {
  const [metrics, setMetrics] = useState([])
  const [scalingHistory, setHistory] = useState([])

  useEffect(() => {
    fetch('/api/system/metrics?hours=1')
      .then(res => res.json())
      .then(setMetrics)
    
    fetch('/api/autoscale/history')
      .then(res => res.json())
      .then(setHistory)
  }, [])

  return (
    <div className="system-monitor">
      <h2>System Resource Monitoring</h2>
      <div className="metrics-grid">
        <LineChart
          title="CPU Utilization"
          data={metrics}
          xKey="timestamp"
          yKey="cpu_usage"
          threshold={autoscaler.scale_up_threshold}
        />
        <LineChart
          title="Request Rate"
          data={metrics}
          xKey="timestamp"
          yKey="request_rate"
        />
        <ScalingHistory history={scalingHistory} />
        <ResourceUsage metrics={metrics} />
      </div>
    </div>
  )
} 