import React, { useState, useEffect } from 'react';

export default function StorageMonitor() {
  const [stats, setStats] = useState({});
  
  useEffect(() => {
    fetch('/api/tracing/storage/stats')
      .then(res => res.json())
      .then(setStats);
  }, []);

  return (
    <div className="storage-monitor">
      <h4>Tracing Storage</h4>
      <div className="metrics">
        <div>Memory Traces: {stats.memory_traces}</div>
        <div>Compressed Batches: {stats.compressed_batches}</div>
        <div>Storage Size: {(stats.estimated_size / 1024).toFixed(1)} KB</div>
      </div>
    </div>
  );
} 