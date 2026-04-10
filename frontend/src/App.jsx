import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import apiService from './services/api';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showCamera, setShowCamera] = useState(false);
  const [cameraStream, setCameraStream] = useState(null);
  const [batchFiles, setBatchFiles] = useState([]);
  const [batchResults, setBatchResults] = useState([]);
  const [showDashboard, setShowDashboard] = useState(false);
  const [dashboardStats, setDashboardStats] = useState(null);
  const [user, setUser] = useState(null);
  const [showAuth, setShowAuth] = useState(false);
  const [authMode, setAuthMode] = useState('login');
  const [authForm, setAuthForm] = useState({ email: '', password: '', name: '' });
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) setUser(JSON.parse(savedUser));
  }, []);

  useEffect(() => {
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }
    };
  }, [cameraStream]);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: 640, height: 480 }
      });
      setCameraStream(stream);
      setShowCamera(true);
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      setError('Camera access denied. Please enable camera permissions.');
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      canvas.toBlob((blob) => {
        const file = new File([blob], 'camera_capture.jpg', { type: 'image/jpeg' });
        setSelectedImage(file);
        setPreviewUrl(canvas.toDataURL('image/jpeg'));
        stopCamera();
        setResult(null);
        setError(null);
      }, 'image/jpeg', 0.9);
    }
  };

  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
      setCameraStream(null);
    }
    setShowCamera(false);
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleBatchSelect = (e) => {
    const files = Array.from(e.target.files);
    setBatchFiles(files);
  };

  const handleBatchUpload = async () => {
    if (batchFiles.length === 0) return;
    setLoading(true);
    setBatchResults([]);
    const results = [];
    for (const file of batchFiles) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        const response = await fetch('http://localhost:8000/api/predict', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();
        results.push({ file: file.name, ...data });
      } catch (err) {
        results.push({ file: file.name, success: false, error: 'Upload failed' });
      }
    }
    setBatchResults(results);
    setLoading(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', selectedImage);
    if (user) formData.append('user_id', user.id);
    try {
      const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.success) {
        setResult(data);
      } else {
        setError(data.detail || 'Failed to analyze image');
      }
    } catch (err) {
      setError('Failed to connect to server.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    setBatchFiles([]);
    setBatchResults([]);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    try {
      const endpoint = authMode === 'login' ? '/api/auth/login' : '/api/auth/register';
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(authForm),
      });
      const data = await response.json();
      if (data.token) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setUser(data.user);
        setShowAuth(false);
      } else {
        setError(data.detail || 'Authentication failed');
      }
    } catch (err) {
      setError('Authentication error');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const loadDashboard = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/dashboard/stats', {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await response.json();
      setDashboardStats(data);
      setShowDashboard(true);
    } catch (err) {
      setError('Failed to load dashboard');
    }
  };

  const isHealthy = result?.disease === 'Healthy';
  const cropIcons = { Tomato: '🍅', Potato: '🥔', Corn: '🌽', Wheat: '🌾', Rice: '🍚', Grape: '🍇', Apple: '🍎' };

  const getCropIcon = (disease) => {
    for (const [crop, icon] of Object.entries(cropIcons)) {
      if (disease.includes(crop)) return icon;
    }
    return disease === 'Healthy' ? '✅' : '🦠';
  };

  if (showDashboard) {
    return (
      <div className="app">
        <header className="header">
          <div className="header-content">
            <div className="logo">
              <span className="logo-icon">🌱</span>
              <h1>AgriScan AI</h1>
            </div>
            <nav className="nav">
              <button onClick={() => setShowDashboard(false)}>Scan</button>
              {user && <button onClick={loadDashboard} className="active">Dashboard</button>}
              {user ? <button onClick={handleLogout}>Logout</button> : <button onClick={() => setShowAuth(true)}>Login</button>}
            </nav>
          </div>
        </header>
        <main className="main">
          <div className="container">
            <div className="dashboard">
              <h2>📊 Detection Dashboard</h2>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">{dashboardStats?.total_scans || 0}</div>
                  <div className="stat-label">Total Scans</div>
                </div>
                <div className="stat-card healthy">
                  <div className="stat-value">{dashboardStats?.healthy_count || 0}</div>
                  <div className="stat-label">Healthy Plants</div>
                </div>
                <div className="stat-card diseased">
                  <div className="stat-value">{dashboardStats?.diseased_count || 0}</div>
                  <div className="stat-label">Diseased</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{dashboardStats?.avg_confidence || 0}%</div>
                  <div className="stat-label">Avg Confidence</div>
                </div>
              </div>
              <h3>Recent Detections</h3>
              <div className="history-list">
                {dashboardStats?.recent?.map((item, idx) => (
                  <div key={idx} className={`history-item ${item.disease === 'Healthy' ? 'healthy' : 'diseased'}`}>
                    <span className="history-icon">{getCropIcon(item.disease)}</span>
                    <div className="history-info">
                      <div className="history-disease">{item.disease.replace(/_/g, ' ')}</div>
                      <div className="history-date">{new Date(item.timestamp).toLocaleDateString()}</div>
                    </div>
                    <div className="history-confidence">{Math.round(item.confidence * 100)}%</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
    );
  }

  if (showCamera) {
    return (
      <div className="app">
        <header className="header">
          <div className="header-content">
            <div className="logo">
              <span className="logo-icon">📷</span>
              <h1>Camera Capture</h1>
            </div>
          </div>
        </header>
        <main className="main camera-view">
          <div className="camera-container">
            <video ref={videoRef} autoPlay playsInline className="camera-video" />
            <canvas ref={canvasRef} style={{ display: 'none' }} />
            <div className="camera-controls">
              <button className="capture-btn" onClick={capturePhoto}>📸 Capture</button>
              <button className="cancel-btn" onClick={stopCamera}>Cancel</button>
            </div>
          </div>
        </main>
      </div>
    );
  }

  if (showAuth) {
    return (
      <div className="app">
        <header className="header">
          <div className="header-content">
            <div className="logo">
              <span className="logo-icon">🌱</span>
              <h1>AgriScan AI</h1>
            </div>
          </div>
        </header>
        <main className="main">
          <div className="container">
            <div className="auth-card">
              <h2>{authMode === 'login' ? '🔐 Login' : '📝 Register'}</h2>
              <form onSubmit={handleAuth}>
                {authMode === 'register' && (
                  <input type="text" placeholder="Name" value={authForm.name} onChange={(e) => setAuthForm({...authForm, name: e.target.value})} required />
                )}
                <input type="email" placeholder="Email" value={authForm.email} onChange={(e) => setAuthForm({...authForm, email: e.target.value})} required />
                <input type="password" placeholder="Password" value={authForm.password} onChange={(e) => setAuthForm({...authForm, password: e.target.value})} required />
                <button type="submit" className="analyze-btn">{authMode === 'login' ? 'Login' : 'Register'}</button>
              </form>
              <p onClick={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}>
                {authMode === 'login' ? "Don't have an account? Register" : 'Already have an account? Login'}
              </p>
              <button className="reset-btn" onClick={() => setShowAuth(false)}>Back</button>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🌱</span>
            <h1>AgriScan AI</h1>
          </div>
          <p className="tagline">AI-Powered Crop Disease Detection</p>
          <nav className="nav">
            {user && <button onClick={loadDashboard}>Dashboard</button>}
            {user ? (
              <button onClick={handleLogout}>👤 {user.name || user.email}</button>
            ) : (
              <button onClick={() => setShowAuth(true)}>Login</button>
            )}
          </nav>
        </div>
      </header>

      <main className="main">
        <div className="container">
          {!result && batchResults.length === 0 ? (
            <div className="upload-section">
              <div className="upload-tabs">
                <button className={!batchFiles.length ? 'active' : ''} onClick={() => setBatchFiles([])}>Single Image</button>
                <button className={batchFiles.length ? 'active' : ''} onClick={() => { setSelectedImage(null); setPreviewUrl(null); }}>Batch Upload</button>
              </div>

              {batchFiles.length === 0 ? (
                <>
                  <div className="upload-toolbar">
                    <button className="camera-btn" onClick={startCamera}>📷 Use Camera</button>
                  </div>
                  <div className="upload-area" onClick={() => fileInputRef.current?.click()} onDrop={handleDrop}>
                    <input ref={fileInputRef} type="file" accept="image/*" onChange={handleImageSelect} style={{ display: 'none' }} />
                    {previewUrl ? (
                      <div className="preview-container">
                        <img src={previewUrl} alt="Preview" className="preview-image" />
                        <button className="change-btn" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>Change</button>
                      </div>
                    ) : (
                      <>
                        <div className="upload-icon">
                          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="17,8 12,3 7,8"/>
                            <line x1="12" y1="3" x2="12" y2="15"/>
                          </svg>
                        </div>
                        <p className="upload-text">Click to upload or drag and drop</p>
                        <p className="upload-hint">Supports: PNG, JPG, JPEG, GIF, BMP, WEBP</p>
                      </>
                    )}
                  </div>
                  {selectedImage && (
                    <div className="file-info">
                      <span className="file-name">📄 {selectedImage.name}</span>
                      <span className="file-size">{(selectedImage.size / 1024).toFixed(1)} KB</span>
                    </div>
                  )}
                  <button className="analyze-btn" onClick={handleAnalyze} disabled={!selectedImage || loading}>
                    {loading ? <span className="loading">Analyzing...</span> : '🔍 Analyze Plant'}
                  </button>
                </>
              ) : (
                <>
                  <div className="batch-upload-area" onClick={() => fileInputRef.current?.click()}>
                    <input ref={fileInputRef} type="file" accept="image/*" multiple onChange={handleBatchSelect} style={{ display: 'none' }} />
                    <p>📁 {batchFiles.length} files selected. Click to add more.</p>
                  </div>
                  <button className="analyze-btn" onClick={handleBatchUpload} disabled={batchFiles.length === 0 || loading}>
                    {loading ? <span className="loading">Processing {batchFiles.length} files...</span> : `📊 Analyze ${batchFiles.length} Files`}
                  </button>
                  {batchResults.length > 0 && (
                    <div className="batch-results">
                      <h3>Batch Results</h3>
                      {batchResults.map((res, idx) => (
                        <div key={idx} className={`batch-result-item ${res.success ? 'success' : 'error'}`}>
                          <span>{res.file}</span>
                          {res.success ? (
                            <span>{res.disease.replace(/_/g, ' ')} ({Math.round(res.confidence)}%)</span>
                          ) : (
                            <span className="error-text">{res.error}</span>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          ) : result ? (
            <div className="result-section">
              <div className={`result-card ${isHealthy ? 'healthy' : 'diseased'}`}>
                <div className="result-header">
                  <h2>Analysis Result</h2>
                  <button className="reset-btn" onClick={handleReset}>New Scan</button>
                </div>
                <div className="result-body">
                  <div className="status-badge">
                    <span className={`status ${isHealthy ? 'healthy' : 'diseased'}`}>
                      {isHealthy ? '✅ Healthy' : '🦠 Disease Detected'}
                    </span>
                    {result.model_type && <span className="model-badge">🤖 {result.model_type}</span>}
                  </div>
                  <div className="result-item">
                    <label>Diagnosis</label>
                    <div className="diagnosis">
                      <span className="crop-icon">{getCropIcon(result.disease)}</span>
                      {result.disease_readable}
                    </div>
                  </div>
                  <div className="result-item">
                    <label>Confidence</label>
                    <div className="confidence-bar">
                      <div className="confidence-fill" style={{ width: `${result.confidence}%` }} />
                      <span className="confidence-text">{result.confidence}%</span>
                    </div>
                  </div>
                  <div className="result-item">
                    <label>💊 Recommended Treatment</label>
                    <div className="treatment">{result.treatment}</div>
                  </div>
                  {result.top_predictions && result.top_predictions.length > 1 && (
                    <div className="alternatives">
                      <label>Other Possibilities</label>
                      <div className="alternatives-list">
                        {result.top_predictions.slice(1).map((pred, idx) => (
                          <span key={idx} className="alt-item">
                            {getCropIcon(pred.disease)} {pred.disease.replace(/_/g, ' ')} ({Math.round(pred.confidence * 100)}%)
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : null}

          {error && (
            <div className="error-message">
              <span>⚠️</span> {error}
            </div>
          )}

          <div className="features">
            <h3>🌾 Supported Crops</h3>
            <div className="crops-grid">
              <div className="crop-item">🍅 Tomato</div>
              <div className="crop-item">🥔 Potato</div>
              <div className="crop-item">🌽 Corn</div>
              <div className="crop-item">🌾 Wheat</div>
              <div className="crop-item">🍚 Rice</div>
              <div className="crop-item">🍇 Grape</div>
              <div className="crop-item">🍎 Apple</div>
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>AgriScan AI © 2026 | EACE 2026 Exhibition Project</p>
      </footer>
    </div>
  );
}

export default App;
