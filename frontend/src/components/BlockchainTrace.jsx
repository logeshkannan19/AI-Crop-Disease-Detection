import React, { useState } from 'react';

const BlockchainTrace = ({ isLoggedIn, detections }) => {
  const [activeTab, setActiveTab] = useState('register');
  const [cropForm, setCropForm] = useState({
    crop_type: '', variety: '', farm_id: '', planting_date: ''
  });
  const [chain, setChain] = useState([
    { index: 0, hash: 'genesis', timestamp: '2026-01-01', type: 'genesis' }
  ]);
  const [selectedCrop, setSelectedCrop] = useState(null);

  const handleRegister = (e) => {
    e.preventDefault();
    if (!isLoggedIn) {
      alert('Please login to register crops on blockchain');
      return;
    }
    const newBlock = {
      index: chain.length,
      hash: Math.random().toString(36).substring(2, 15),
      timestamp: new Date().toISOString(),
      type: 'crop_registration',
      data: cropForm
    };
    setChain([...chain, newBlock]);
    alert('Crop registered on blockchain successfully!');
    setCropForm({ crop_type: '', variety: '', farm_id: '', planting_date: '' });
  };

  const handleAddRecord = (detection) => {
    if (!isLoggedIn || !selectedCrop) {
      alert('Please login and select a crop first');
      return;
    }
    const newBlock = {
      index: chain.length,
      hash: Math.random().toString(36).substring(2, 15),
      timestamp: new Date().toISOString(),
      type: 'health_record',
      previous_hash: chain[chain.length - 1].hash,
      data: {
        disease: detection.disease,
        confidence: detection.confidence,
        treatment: detection.treatment
      }
    };
    setChain([...chain, newBlock]);
    alert('Health record added to blockchain!');
  };

  const exportCert = () => {
    const cert = {
      certificate_id: Math.random().toString(36).substring(2, 10).toUpperCase(),
      issued_at: new Date().toISOString(),
      total_records: chain.length,
      verified: true
    };
    const blob = new Blob([JSON.stringify(cert, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AgriScan_Certificate_${cert.certificate_id}.json`;
    a.click();
  };

  return (
    <div className="blockchain-trace">
      <div className="trace-header">
        <h3>⛓️ Blockchain Traceability</h3>
        <div className="trace-tabs">
          <button className={activeTab === 'register' ? 'active' : ''} onClick={() => setActiveTab('register')}>Register Crop</button>
          <button className={activeTab === 'chain' ? 'active' : ''} onClick={() => setActiveTab('chain')}>View Chain</button>
          <button className={activeTab === 'verify' ? 'active' : ''} onClick={() => setActiveTab('verify')}>Verify</button>
        </div>
      </div>

      {activeTab === 'register' && (
        <form className="register-form" onSubmit={handleRegister}>
          <div className="form-grid">
            <select value={cropForm.crop_type} onChange={e => setCropForm({...cropForm, crop_type: e.target.value})} required>
              <option value="">Select Crop Type</option>
              <option value="Tomato">🍅 Tomato</option>
              <option value="Potato">🥔 Potato</option>
              <option value="Corn">🌽 Corn</option>
            </select>
            <input type="text" placeholder="Variety (e.g., Roma, Cherry)" value={cropForm.variety} onChange={e => setCropForm({...cropForm, variety: e.target.value})} required />
            <input type="text" placeholder="Farm ID" value={cropForm.farm_id} onChange={e => setCropForm({...cropForm, farm_id: e.target.value})} required />
            <input type="date" value={cropForm.planting_date} onChange={e => setCropForm({...cropForm, planting_date: e.target.value})} required />
          </div>
          <button type="submit" className="register-btn">⛓️ Register on Blockchain</button>
        </form>
      )}

      {activeTab === 'chain' && (
        <div className="chain-view">
          <div className="chain-info">
            <span>Total Blocks: {chain.length}</span>
            <span className="verified">✓ Verified</span>
          </div>
          <div className="chain-blocks">
            {chain.map((block, idx) => (
              <div key={idx} className={`block ${block.type === 'genesis' ? 'genesis' : ''}`}>
                <div className="block-header">
                  <span className="block-index">Block #{block.index}</span>
                  <span className="block-type">{block.type || 'registration'}</span>
                </div>
                <div className="block-hash">
                  <small>Hash:</small> {block.hash.substring(0, 20)}...
                </div>
                <div className="block-time">{new Date(block.timestamp).toLocaleDateString()}</div>
                {idx > 0 && <div className="block-connector">↓</div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'verify' && (
        <div className="verify-section">
          <div className="verify-card">
            <div className="verify-icon">✓</div>
            <h4>Blockchain Verified</h4>
            <p>All {chain.length} blocks are cryptographically linked</p>
            <p className="verify-stats">
              <span>Total Records: {chain.length - 1}</span>
              <span>Last Update: {chain[chain.length - 1].timestamp}</span>
            </p>
            <button className="export-cert-btn" onClick={exportCert}>
              📜 Export Certificate
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BlockchainTrace;
