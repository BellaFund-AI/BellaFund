/**
 * 时间线视图展示关联警报
 */
export default function AlertTimeline({ alerts }) {
  const timelineData = alerts.map(a => ({
    timestamp: new Date(a.timestamp),
    content: `${a.type} - ${a.severity}`,
    ...a
  }))

  return (
    <Chrono 
      items={timelineData}
      mode="VERTICAL_ALTERNATING"
      theme={{ primary: '#4CAF50', secondary: '#FFC107' }}
    >
      <div className="timeline-custom-content">
        {alerts.map(alert => (
          <AlertPreview key={alert.id} alert={alert} />
        ))}
      </div>
    </Chrono>
  )
} 