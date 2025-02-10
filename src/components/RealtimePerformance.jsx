import React, { useState, useEffect } from 'react'
import SparklineChart from './SparklineChart'
import ThresholdAlerts from './ThresholdAlerts'

export default function RealtimePerformance() {
  const [socket] = useState(() => new WebSocket('ws://localhost:8000/performance/stream'))
  const [metrics, setMetrics] = useState([])

  useEffect(() => {
    socket.onmessage = (event) => {
      setMetrics(JSON.parse(event.data))
    }
    return () => socket.close()
  }, [])

  return (
    <div className="realtime-monitor">
      <h3>Real-time Performance Stream</h3>
      <SparklineChart 
        data={metrics}
        metrics={['accuracy', 'precision', 'recall']}
        refreshInterval={5000}
      />
      <ThresholdAlerts 
        metrics={metrics}
        baselines={performance_tracker.baselines}
      />
    </div>
  )
} 