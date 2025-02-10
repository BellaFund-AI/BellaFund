/**
 * Model Performance Dashboard
 * Shows accuracy metrics and training history
 */
export default function ModelMonitor() {
  const [metrics, setMetrics] = useState({})
  const [trainingHistory, setHistory] = useState([])

  useEffect(() => {
    fetch('/api/model/metrics')
      .then(res => res.json())
      .then(data => setMetrics(data))
      
    fetch('/api/model/history')
      .then(res => res.json())
      .then(history => setHistory(history))
  }, [])

  return (
    <div className="p-6 space-y-6">
      <div className="grid grid-cols-3 gap-4">
        <MetricCard title="Accuracy" value={metrics.accuracy} delta={metrics.accuracyChange} />
        <MetricCard title="Data Drift" value={metrics.dataDrift} threshold={0.15} />
        <MetricCard title="Training Frequency" value={metrics.trainingFreq} unit="days" />
      </div>
      
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Training History</h3>
        <LineChart
          data={trainingHistory}
          xKey="versionDate"
          yKeys={['accuracy', 'precision']}
          labels={['Accuracy', 'Precision']}
        />
      </div>

      <AlertSection>
        <AlertItem 
          type={metrics.accuracy < 0.7 ? 'critical' : 'warning'}
          title="Accuracy Alert"
          message={`Current accuracy ${metrics.accuracy} below threshold`}
        />
        <AlertItem
          type={metrics.dataDrift > 0.2 ? 'critical' : 'info'}
          title="Data Drift Detected"
          message={`Feature drift of ${metrics.dataDrift} detected`}
        />
      </AlertSection>
    </div>
  )
} 