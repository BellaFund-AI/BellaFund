export default function RootCauseAnalysis({ analysis }) {
  return (
    <div className="root-cause-panel">
      <h3>根本原因分析</h3>
      {analysis.map((cause, index) => (
        <div key={index} className="cause-item">
          <div className="cause-header">
            <span className="feature">{cause.feature}</span>
            <span className="score">漂移分数: {cause.drift_score.toFixed(2)}</span>
          </div>
          <div className="related-features">
            相关特征: {cause.related_features.join(', ')}
          </div>
          <div className="potential-source">
            可能数据源: {cause.potential_cause}
          </div>
        </div>
      ))}
    </div>
  )
} 