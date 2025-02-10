export default function TraceFlameGraph({ trace }) {
  const processData = (spans) => {
    return spans.map(span => ({
      name: span.name,
      value: span.duration * 1000, // Convert to milliseconds
      children: processData(span.children || []),
      tags: span.tags
    }));
  };

  return (
    <div className="flame-graph">
      <ResponsiveFlameGraph
        data={processData([trace])}
        margin={{ top: 20, right: 20, bottom: 20, left: 120 }}
        nodeComponent={({ node, ...rest }) => (
          <FlameGraphNode 
            node={node}
            {...rest}
            fill={node.data.tags.error ? '#ff4444' : '#48bb78'}
          />
        )}
      />
    </div>
  );
} 