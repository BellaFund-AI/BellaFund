import React, { useState, useEffect } from 'react'
import { LineChart } from '@/components/LineChart'

export default function FeatureImportanceTrend({ feature }) {
  const [trendData, setData] = useState([])
  
  useEffect(() => {
    fetch(`/api/features/importance?feature=${feature}&days=90`)
      .then(res => res.json())
      .then(setData)
  }, [feature])

  return (
    <div className="feature-trend-card">
      <h3>{feature} 重要性趋势</h3>
      <LineChart
        data={trendData}
        xKey="timestamp"
        yKeys={['importance']}
        labels={['重要性分数']}
        timeFormat="%Y-%m"
      />
      <div className="stats-overview">
        <span>当前值: {trendData[0]?.importance.toFixed(2)}</span>
        <span>均值: {(trendData.reduce((a,b) => a + b.importance, 0)/trendData.length).toFixed(2)}</span>
        <span>变化率: {calculateChangeRate(trendData)}%</span>
      </div>
    </div>
  )
} 