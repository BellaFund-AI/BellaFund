/**
 * Real-time Alert Feed Component
 * Displays model monitoring alerts with severity levels
 */
export default function AlertsFeed() {
  const [alerts, setAlerts] = useState([])
  
  useEffect(() => {
    const ws = new WebSocket('wss://api.bellafund.com/alerts')
    ws.onmessage = (event) => {
      setAlerts(prev => [JSON.parse(event.data), ...prev.slice(0, 10)])
    }
    return () => ws.close()
  }, [])

  return (
    <div className="space-y-2">
      {alerts.map((alert, index) => (
        <div key={index} className={`p-3 rounded-lg border-l-4 ${
          alert.severity === 'critical' ? 'border-red-500 bg-red-50' :
          alert.severity === 'warning' ? 'border-yellow-500 bg-yellow-50' :
          'border-blue-500 bg-blue-50'
        }`}>
          <div className="flex justify-between items-center">
            <div>
              <h4 className="font-medium">{alert.title}</h4>
              <p className="text-sm text-gray-600">{alert.message}</p>
            </div>
            <span className="text-xs text-gray-500">
              {new Date(alert.timestamp).toLocaleTimeString()}
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}

function AlertItem({ alert }) {
  const [isAcknowledged, setAcknowledged] = useState(false);
  
  const handleAcknowledge = async () => {
    await fetch('/api/alerts/acknowledge', {
      method: 'POST',
      body: JSON.stringify({ alert_id: alert.id })
    });
    setAcknowledged(true);
  };

  return (
    <div className={`alert-item ${isAcknowledged ? 'opacity-50' : ''}`}>
      <div className="alert-content">
        <h4>{alert.title}</h4>
        <p>{alert.message}</p>
      </div>
      {!isAcknowledged && (
        <button 
          onClick={handleAcknowledge}
          className="ack-button"
        >
          Mark as Resolved
        </button>
      )}
    </div>
  );
} 