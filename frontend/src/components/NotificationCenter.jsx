import React, { useState } from 'react';

const NotificationCenter = ({ user, onLoginRequired }) => {
  const [settings, setSettings] = useState({
    email_alerts: true,
    sms_alerts: false,
    disease_alerts: true,
    weather_alerts: true,
    weekly_report: false
  });
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');

  const handleSave = () => {
    if (!user) {
      onLoginRequired();
      return;
    }
    alert('Notification settings saved!');
  };

  const handleTestAlert = () => {
    alert('📱 Test notification sent!');
  };

  return (
    <div className="notification-center">
      <h3>🔔 Notification Settings</h3>
      
      <div className="notification-form">
        <div className="form-group">
          <label>📧 Email for Alerts</label>
          <input 
            type="email" 
            placeholder="your@email.com" 
            value={email} 
            onChange={e => setEmail(e.target.value)}
          />
        </div>
        
        <div className="form-group">
          <label>📱 SMS Alerts (Phone Number)</label>
          <input 
            type="tel" 
            placeholder="+1 234 567 8900" 
            value={phone} 
            onChange={e => setPhone(e.target.value)}
          />
        </div>

        <div className="toggle-group">
          <label className="toggle">
            <input 
              type="checkbox" 
              checked={settings.email_alerts}
              onChange={e => setSettings({...settings, email_alerts: e.target.checked})}
            />
            <span>📧 Email Notifications</span>
          </label>
          
          <label className="toggle">
            <input 
              type="checkbox" 
              checked={settings.sms_alerts}
              onChange={e => setSettings({...settings, sms_alerts: e.target.checked})}
            />
            <span>📱 SMS Notifications</span>
          </label>
        </div>

        <div className="alert-types">
          <h4>Alert Types</h4>
          
          <label className="toggle">
            <input 
              type="checkbox" 
              checked={settings.disease_alerts}
              onChange={e => setSettings({...settings, disease_alerts: e.target.checked})}
            />
            <span>🦠 Disease Detection Alerts</span>
          </label>
          
          <label className="toggle">
            <input 
              type="checkbox" 
              checked={settings.weather_alerts}
              onChange={e => setSettings({...settings, weather_alerts: e.target.checked})}
            />
            <span>⚠️ Weather-based Disease Risk Alerts</span>
          </label>
          
          <label className="toggle">
            <input 
              type="checkbox" 
              checked={settings.weekly_report}
              onChange={e => setSettings({...settings, weekly_report: e.target.checked})}
            />
            <span>📊 Weekly Health Report</span>
          </label>
        </div>

        <div className="notification-actions">
          <button className="test-btn" onClick={handleTestAlert}>🧪 Test Alert</button>
          <button className="save-btn" onClick={handleSave}>💾 Save Settings</button>
        </div>
      </div>

      <div className="notification-preview">
        <h4>📬 Preview</h4>
        <div className="preview-card">
          <div className="preview-header">🦠 Disease Alert</div>
          <p>Late blight detected on your tomato crop (92% confidence)</p>
          <small>Recommended: Apply fungicide immediately</small>
        </div>
      </div>
    </div>
  );
};

export default NotificationCenter;
