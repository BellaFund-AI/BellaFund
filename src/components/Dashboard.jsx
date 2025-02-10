/**
 * Real-time Portfolio Dashboard
 * Integrates risk metrics and AI recommendations
 */
import useRiskMetrics from '../hooks/useRiskMetrics'

export default function Dashboard() {
  const { portfolio, metrics } = useRiskMetrics()
  
  const performanceMetrics = { /* ... */ }
  
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Risk Metrics Card */}
      <div className="p-6 bg-red-50 rounded-xl">
        <h3 className="text-lg font-semibold mb-4">Risk Overview</h3>
        <div className="space-y-2">
          <MetricItem 
            label="Value at Risk (95%)" 
            value={`${metrics.var}%`}
          />
          <MetricItem
            label="Max Drawdown"
            value={`${metrics.drawdown}%`}
          />
        </div>
      </div>

      {/* AI Recommendations */}
      <div className="p-6 bg-blue-50 rounded-xl">
        <h3 className="text-lg font-semibold mb-4">AI Suggestions</h3>
        <div className="space-y-3">
          {portfolio.recommendations.map((rec, index) => (
            <RecommendationCard
              key={index}
              symbol={rec.symbol}
              action={rec.action}
              confidence={rec.confidence}
            />
          ))}
        </div>
      </div>

      {/* Cross-chain Overview */}
      <div className="p-6 bg-green-50 rounded-xl">
        <h3 className="text-lg font-semibold mb-4">Cross-chain Assets</h3>
        <ChainBalance chain="BNB" balance={portfolio.chains.BNB} />
        <ChainBalance chain="Solana" balance={portfolio.chains.Solana} />
      </div>
    </div>
  )
} 