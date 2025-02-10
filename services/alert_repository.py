"""
Alert History Storage with Time-based Archiving
"""
from datetime import datetime, timedelta
import sqlite3

class AlertRepository:
    def __init__(self, db_path='alerts.db'):
        self.conn = sqlite3.connect(db_path)
        self._init_db()
        
    def _init_db(self):
        """Initialize database schema"""
        self.conn.execute('''CREATE TABLE IF NOT EXISTS alerts
             (id TEXT PRIMARY KEY,
              title TEXT,
              message TEXT,
              severity TEXT,
              type TEXT,
              timestamp DATETIME,
              acknowledged BOOLEAN)''')
              
    def store_alert(self, alert):
        """Persist alert to database"""
        self.conn.execute('''
            INSERT INTO alerts VALUES 
            (?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert['id'],
            alert['title'],
            alert['message'],
            alert['severity'],
            alert.get('type', 'general'),
            datetime.now(),
            False
        ))
        self.conn.commit()
        
    def get_recent_alerts(self, hours=24):
        """Retrieve alerts from past time window"""
        cutoff = datetime.now() - timedelta(hours=hours)
        cursor = self.conn.execute('''
            SELECT * FROM alerts 
            WHERE timestamp > ?
            ORDER BY timestamp DESC
        ''', (cutoff,))
        return [dict(row) for row in cursor.fetchall()]

    def get_alert_count(self, hours=24):
        cutoff = datetime.now() - timedelta(hours=hours)
        return self.conn.execute('''
            SELECT COUNT(*) FROM alerts 
            WHERE timestamp > ?
        ''', (cutoff,)).fetchone()[0]

    def get_severity_distribution(self):
        return dict(self.conn.execute('''
            SELECT severity, COUNT(*) 
            FROM alerts 
            GROUP BY severity
        ''').fetchall())

    def get_resolution_rate(self):
        total = self.conn.execute('SELECT COUNT(*) FROM alerts').fetchone()[0]
        resolved = self.conn.execute('SELECT COUNT(*) FROM alerts WHERE acknowledged = 1').fetchone()[0]
        return resolved / total if total > 0 else 0

    def get_common_alert_types(self, limit=5):
        return dict(self.conn.execute(f'''
            SELECT type, COUNT(*) 
            FROM alerts 
            GROUP BY type 
            ORDER BY COUNT(*) DESC 
            LIMIT {limit}
        ''').fetchall())

    def get_alert(self, alert_id: str) -> dict:
        cursor = self.conn.execute('''
            SELECT * FROM alerts WHERE id = ?
        ''', (alert_id,))
        result = cursor.fetchone()
        return dict(result) if result else None 