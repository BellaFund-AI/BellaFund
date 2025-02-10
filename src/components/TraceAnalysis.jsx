import React, { useState, useEffect } from 'react';
import DurationChart from './DurationChart';
import ErrorTimeline from './ErrorTimeline';
import FeatureImpact from './FeatureImpact';
import LogViewer from './LogViewer';

export default function TraceAnalysis({ traceId }) {
  const [analysis, setAnalysis] = useState(null);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      const trace = await fetch(`/api/tracing/trace/${traceId}`).then(r => r.json());
      const analysis = await fetch(`/api/tracing/analyze?trace_id=${traceId}`).then(r => r.json());
      const logs = await fetch(`/api/tracing/logs/${traceId}`).then(r => r.json());
      
      setAnalysis(analysis);
      setLogs(logs);
    };
    loadData();
  }, [traceId]);

  return (
    <div className="trace-analysis">
      <div className="overview">
        <DurationChart spans={analysis?.performance_stats} />
        <ErrorTimeline errors={analysis?.common_errors} />
      </div>
      <div className="details">
        <FeatureImpact correlations={analysis?.feature_correlations} />
        <LogViewer logs={logs} />
      </div>
    </div>
  );
} 