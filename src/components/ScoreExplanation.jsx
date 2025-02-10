/**
 * Interactive Feature Importance Visualization
 */
export default function ScoreExplanation({ explanation }) {
  return (
    <div className="p-4 bg-gray-50 rounded-lg">
      <h3 className="text-lg font-semibold mb-3">AI Score Breakdown</h3>
      <div className="space-y-2">
        {Object.entries(explanation.feature_importances).map(([feature, value]) => (
          <div key={feature} className="flex items-center justify-between">
            <span className="capitalize">{feature.replace('_', ' ')}</span>
            <div className="w-48 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-full ${value > 0 ? 'bg-green-500' : 'bg-red-500'} rounded-full`} 
                style={{ width: `${Math.abs(value)*20}%` }}
              />
            </div>
            <span className="w-12 text-right">
              {value > 0 ? '+' : ''}{value.toFixed(2)}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
} 