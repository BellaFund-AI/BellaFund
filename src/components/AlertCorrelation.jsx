/**
 * 警报关联分析可视化组件
 */
export default function AlertCorrelation({ alertId }) {
  const [relatedAlerts, setRelated] = useState([])
  const [rootCause, setRootCause] = useState(null)

  useEffect(() => {
    async function fetchData() {
      const response = await fetch(`/api/alerts/related/${alertId}`)
      const data = await response.json()
      setRelated(data)
      
      // 自动触发根因分析
      const rcResponse = await fetch('/api/analyze/root-cause', {
        method: 'POST',
        body: JSON.stringify({ 
          features: data.map(a => a.type) 
        })
      })
      setRootCause(await rcResponse.json())
    }
    fetchData()
  }, [alertId])

  return (
    <div className="correlation-view">
      <h3>关联事件分析 (共{relatedAlerts.length}条)</h3>
      <ForceGraph
        nodes={relatedAlerts.map(a => ({
          id: a.id,
          type: a.type,
          severity: a.severity
        }))}
        links={relatedAlerts.map(a => ({
          source: alertId,
          target: a.id
        }))}
      />
      
      {rootCause && <RootCauseAnalysis analysis={rootCause} />}
    </div>
  )
} 