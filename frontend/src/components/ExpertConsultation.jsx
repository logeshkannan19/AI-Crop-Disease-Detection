import React, { useState } from 'react';

const ExpertConsultation = ({ isLoggedIn, onLoginRequired }) => {
  const [activeTab, setActiveTab] = useState('experts');
  const [selectedExpert, setSelectedExpert] = useState(null);
  const [consultationForm, setConsultationForm] = useState({
    disease: '',
    crop: '',
    description: '',
    urgency: 'normal'
  });

  const experts = [
    { id: 'exp1', name: 'Dr. Rajesh Kumar', spec: 'Tomato & Potato', exp: 15, rating: 4.8, avail: true, lang: ['English', 'Hindi'], rate: 25 },
    { id: 'exp2', name: 'Dr. Maria Santos', spec: 'Fruit Trees & Grapes', exp: 12, rating: 4.9, avail: true, lang: ['English', 'Spanish'], rate: 30 },
    { id: 'exp3', name: 'Dr. Wei Chen', spec: 'Rice & Wheat', exp: 20, rating: 4.7, avail: true, lang: ['English', 'Chinese'], rate: 35 },
    { id: 'exp4', name: 'Dr. John Smith', spec: 'Corn & General', exp: 18, rating: 4.6, avail: false, lang: ['English'], rate: 28 }
  ];

  const consultations = [
    { id: 1, expert: 'Dr. Rajesh Kumar', status: 'pending', disease: 'Tomato Late Blight', date: '2026-04-09' },
    { id: 2, expert: 'Dr. Maria Santos', status: 'answered', disease: 'Grape Black Rot', date: '2026-04-05' }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isLoggedIn) {
      onLoginRequired();
      return;
    }
    alert('Consultation request submitted! Expert will respond within 24 hours.');
  };

  return (
    <div className="expert-consultation">
      <div className="expert-header">
        <h3>👨‍🌾 Expert Consultation</h3>
        <div className="expert-tabs">
          <button className={activeTab === 'experts' ? 'active' : ''} onClick={() => setActiveTab('experts')}>Find Expert</button>
          <button className={activeTab === 'my' ? 'active' : ''} onClick={() => setActiveTab('my')}>My Consultations</button>
        </div>
      </div>

      {activeTab === 'experts' ? (
        <>
          <div className="experts-list">
            {experts.map(expert => (
              <div key={expert.id} className={`expert-card ${!expert.avail ? 'unavailable' : ''}`}>
                <div className="expert-avatar">👨‍🔬</div>
                <div className="expert-info">
                  <h4>{expert.name}</h4>
                  <p className="expert-spec">{expert.spec}</p>
                  <div className="expert-meta">
                    <span>⭐ {expert.rating}</span>
                    <span>📅 {expert.exp} years</span>
                    <span>💬 {expert.lang.join(', ')}</span>
                  </div>
                  <div className="expert-status">
                    <span className={expert.avail ? 'available' : 'busy'}>
                      {expert.avail ? '● Available' : '○ Busy'}
                    </span>
                    <span className="rate">${expert.rate}/hr</span>
                  </div>
                </div>
                {expert.avail && (
                  <button className="consult-btn" onClick={() => setSelectedExpert(expert)}>
                    Consult
                  </button>
                )}
              </div>
            ))}
          </div>

          {selectedExpert && (
            <div className="consultation-modal">
              <div className="modal-content">
                <h4>Consult {selectedExpert.name}</h4>
                <form onSubmit={handleSubmit}>
                  <select value={consultationForm.crop} onChange={e => setConsultationForm({...consultationForm, crop: e.target.value})} required>
                    <option value="">Select Crop</option>
                    <option value="Tomato">🍅 Tomato</option>
                    <option value="Potato">🥔 Potato</option>
                    <option value="Corn">🌽 Corn</option>
                    <option value="Wheat">🌾 Wheat</option>
                  </select>
                  <input type="text" placeholder="Disease/Condition" value={consultationForm.disease} onChange={e => setConsultationForm({...consultationForm, disease: e.target.value})} required />
                  <textarea placeholder="Describe the symptoms..." value={consultationForm.description} onChange={e => setConsultationForm({...consultationForm, description: e.target.value})} required />
                  <select value={consultationForm.urgency} onChange={e => setConsultationForm({...consultationForm, urgency: e.target.value})}>
                    <option value="low">Low Urgency</option>
                    <option value="normal">Normal Urgency</option>
                    <option value="high">High Urgency</option>
                  </select>
                  <div className="modal-actions">
                    <button type="button" className="cancel-btn" onClick={() => setSelectedExpert(null)}>Cancel</button>
                    <button type="submit" className="submit-btn">Submit Request</button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="my-consultations">
          {consultations.map(consult => (
            <div key={consult.id} className="consultation-card">
              <div className="consult-header">
                <span className={`status-badge ${consult.status}`}>{consult.status}</span>
                <span className="consult-date">{consult.date}</span>
              </div>
              <h4>{consult.disease}</h4>
              <p>Expert: {consult.expert}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ExpertConsultation;
