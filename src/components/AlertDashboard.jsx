/**
 * 警报生命周期追踪仪表盘
 */
export default function AlertDashboard() {
  const [stats, setStats] = useState({})
  const [history, setHistory] = useState([])

  useEffect(() => {
    async function loadData() {
      const [statsRes, historyRes] = await Promise.all([
        fetch('/api/alerts/stats'),
        fetch('/api/alerts/history')
      ])
      setStats(await statsRes.json())
      setHistory(await historyRes.json())
    }
    loadData()
  }, [])

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6">
      {/* 实时统计卡片 */}
      <div className="col-span-3 grid grid-cols-4 gap-4">
        <MetricCard 
          title="24小时警报总数" 
          value={stats.total_last_24h}
          icon="⚠️"
        />
        <MetricCard
          title="解决率"
          value={`${(stats.resolution_rate * 100).toFixed(1)}%`}
          icon="✅"
        />
        <MetricCard
          title="最高频类型"
          value={stats.common_types?.[0]?.[0] || 'N/A'}
          icon="📊"
        />
        <MetricCard
          title="进行中事件"
          value={stats.by_severity?.critical || 0}
          icon="🔥"
        />
      </div>

      {/* 趋势可视化 */}
      <div className="lg:col-span-2 bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">警报趋势分析</h3>
        <LineChart
          data={history}
          xKey="timestamp"
          yKeys={['count']}
          labels={['警报数量']}
        />
      </div>

      {/* 分类分布 */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">警报类型分布</h3>
        <PieChart
          data={Object.entries(stats.by_severity || {})}
          labels={['类型', '数量']}
        />
      </div>
    </div>
  )
} 