export default function MobileAlertView() {
  return (
    <div className="mobile-alert-container">
      <SwipeableViews enableMouseEvents>
        {alerts.map(alert => (
          <div key={alert.id} className="alert-card">
            <SeverityIndicator level={alert.severity} />
            <AlertContent alert={alert} />
            <ActionButtons alert={alert} />
          </div>
        ))}
      </SwipeableViews>
    </div>
  )
} 