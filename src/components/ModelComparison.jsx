import React, { useState, useEffect } from 'react'
import VersionPicker from './VersionPicker'
import PerformanceComparison from './PerformanceComparison'
import FeatureImpact from './FeatureImpact'
import DataDriftReport from './DataDriftReport'

export default function ModelComparison() {
  const [versions, setVersions] = useState([])
  const [selected, setSelected] = useState({v1: null, v2: null})
  const [results, setResults] = useState(null)

  useEffect(() => {
    fetch('/api/models/versions')
      .then(res => res.json())
      .then(data => setVersions(data.versions))
  }, [])

  const compareModels = () => {
    fetch(`/api/models/compare?v1=${selected.v1}&v2=${selected.v2}`)
      .then(res => res.json())
      .then(setResults)
  }

  return (
    <div className="model-comparison">
      <div className="version-selectors">
        <VersionPicker 
          label="Version 1" 
          versions={versions} 
          selected={selected.v1}
          onChange={v => setSelected(p => ({...p, v1: v}))}
        />
        <VersionPicker 
          label="Version 2" 
          versions={versions} 
          selected={selected.v2}
          onChange={v => setSelected(p => ({...p, v2: v}))}
        />
        <button onClick={compareModels}>Compare</button>
      </div>
      
      {results && (
        <div className="comparison-results">
          <PerformanceComparison metrics={results.performance} />
          <FeatureImpact features={results.feature_importance} />
          <DataDriftReport drift={results.data_drift} />
        </div>
      )}
    </div>
  )
} 