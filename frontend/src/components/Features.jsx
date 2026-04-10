import React, { useState } from 'react';
import ARPlantDoctor from './ARPlantDoctor';
import ExpertConsultation from './ExpertConsultation';
import BlockchainTrace from './BlockchainTrace';
import CommunityForum from './CommunityForum';
import NotificationCenter from './NotificationCenter';

const Features = ({ user, isLoggedIn, onLoginRequired, detections }) => {
  const [activeFeature, setActiveFeature] = useState(null);

  const features = [
    { id: 'ar', icon: '🔬', name: 'AR Plant Doctor', desc: 'Real-time disease detection with augmented reality' },
    { id: 'expert', icon: '👨‍🌾', name: 'Expert Consult', desc: 'Connect with agricultural experts' },
    { id: 'blockchain', icon: '⛓️', name: 'Blockchain Trace', desc: 'Track crop health on blockchain' },
    { id: 'forum', icon: '🌐', name: 'Community Forum', desc: 'Connect with other farmers' },
    { id: 'notifications', icon: '🔔', name: 'Notifications', desc: 'SMS & Email alerts' }
  ];

  const renderFeature = () => {
    switch (activeFeature) {
      case 'ar':
        return <ARPlantDoctor />;
      case 'expert':
        return <ExpertConsultation isLoggedIn={isLoggedIn} onLoginRequired={onLoginRequired} />;
      case 'blockchain':
        return <BlockchainTrace isLoggedIn={isLoggedIn} detections={detections} />;
      case 'forum':
        return <CommunityForum isLoggedIn={isLoggedIn} />;
      case 'notifications':
        return <NotificationCenter user={user} onLoginRequired={onLoginRequired} />;
      default:
        return null;
    }
  };

  if (activeFeature) {
    return (
      <div className="feature-page">
        <button className="back-btn" onClick={() => setActiveFeature(null)}>
          ← Back to Features
        </button>
        {renderFeature()}
      </div>
    );
  }

  return (
    <div className="features-grid-page">
      <h2>🚀 Premium Features</h2>
      <div className="features-cards">
        {features.map(feature => (
          <div key={feature.id} className="feature-card" onClick={() => setActiveFeature(feature.id)}>
            <div className="feature-icon">{feature.icon}</div>
            <h3>{feature.name}</h3>
            <p>{feature.desc}</p>
            <button className="feature-btn">Try Now →</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Features;
