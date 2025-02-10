import React, { useState, useEffect } from 'react';
import TraceTree from './TraceTree';
import SpanDetails from './SpanDetails';
import TraceSearch from './TraceSearch';

export default function TraceViewer() {
  const [traces, setTraces] = useState([]);
  const [selectedTrace, setSelected] = useState(null);

  useEffect(() => {
    fetch('/api/tracing/traces?limit=50')
      .then(res => res.json())
      .then(setTraces);
  }, []);

  return (
    <div className="trace-viewer">
      <div className="trace-list">
        <TraceSearch onSearch={setTraces} />
        {traces.map(trace => (
          <div key={trace.trace_id} onClick={() => setSelected(trace)}>
            {trace.root_span.name} - {trace.duration.toFixed(2)}s
          </div>
        ))}
      </div>
      {selectedTrace && (
        <div className="trace-details">
          <TraceTree trace={selectedTrace} />
          <SpanDetails />
        </div>
      )}
    </div>
  );
} 