import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import { languages } from './i18n';
import './i18n';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WEATHER_API_KEY = 'demo';
const WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast';

function AppContent() {
  const { t, i18n } = useTranslation();
  const { isDark, toggleTheme } = useTheme();
  
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
  const [showLangMenu, setShowLangMenu] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isInstallable, setIsInstallable] = useState(false);
  const [weather, setWeather] = useState(null);
  const [diseaseRisk, setDiseaseRisk] = useState(null);
  
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) setUser(JSON.parse(savedUser));
    
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setIsInstallable(true);
    });
  }, []);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => fetchWeather(pos.coords.latitude, pos.coords.longitude),
        () => fetchWeather(40.7128, -74.0060)
      );
    }
  }, []);

  const fetchWeather = async (lat, lon) => {
    try {
      const res = await fetch(`${WEATHER_API_URL}?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,precipitation&daily=temperature_2m_max,temperature_2m_min,precipitation_sum`);
      const data = await res.json();
      setWeather(data.current);
      calculateDiseaseRisk(data.current);
    } catch (err) {
      console.log('Weather fetch failed');
    }
  };

  const calculateDiseaseRisk = (weatherData) => {
    const temp = weatherData?.temperature_2m;
    const humidity = weatherData?.relative_humidity_2m;
    
    if (!temp || !humidity) return;
    
    let risk = 'low';
    if (temp > 15 && temp < 30 && humidity > 70) {
      risk = 'high';
    } else if (temp > 10 && temp < 35 && humidity > 50) {
      risk = 'medium';
    }
    
    setDiseaseRisk(risk);
  };

  const handleInstall = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      if (outcome === 'accepted') {
        setIsInstallable(false);
      }
      setDeferredPrompt(null);
    }
  };

  const changeLanguage = (langCode) => {
    i18n.changeLanguage(langCode);
    localStorage.setItem('language', langCode);
    setShowLangMenu(false);
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: 640, height: 480 }
      });
      setCameraStream(stream);
      setShowCamera(true);
      if (videoRef.current) videoRef.current.srcObject = stream;
    } catch (err) {
      setError(t('errors.camera'));
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
    setBatchFiles(Array.from(e.target.files));
  };

  const handleBatchUpload = async () => {
    if (!batchFiles.length) return;
    setLoading(true);
    const results = [];
    for (const file of batchFiles) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        const res = await fetch(`${API_URL}/api/predict`, { method: 'POST', body: formData });
        const data = await res.json();
        results.push({ file: file.name, ...data });
      } catch {
        results.push({ file: file.name, success: false, error: 'Upload failed' });
      }
    }
    setBatchResults(results);
    setLoading(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file?.type.startsWith('image/')) {
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
      const res = await fetch(`${API_URL}/api/predict`, { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) setResult(data);
      else setError(data.detail || t('errors.upload'));
    } catch {
      setError(t('errors.connection'));
    }
    setLoading(false);
  };

  const exportPDF = () => {
    if (!result) return;
    const content = `
AGRI SCAN AI - DISEASE DETECTION REPORT
=======================================
Date: ${new Date().toLocaleString()}
Model: ${result.model_type || 'EfficientNetB0'}

DETECTION RESULTS
-----------------
Status: ${result.disease === 'Healthy' ? 'Healthy Plant' : 'Disease Detected'}
Disease: ${result.disease_readable}
Crop: ${result.crop || 'Unknown'}
Confidence: ${result.confidence}%
Severity: ${result.severity || 'Unknown'}

RECOMMENDED TREATMENT
----------------------
${result.treatment}

${result.top_predictions?.length > 1 ? `
OTHER POSSIBILITIES
-------------------
${result.top_predictions.slice(1).map(p => `- ${p.disease.replace(/_/g, ' ')}: ${Math.round(p.confidence * 100)}%`).join('\n')}` : ''}

=====================================
Generated by AgriScan AI
    `;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AgriScan_Report_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
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
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(authForm)
      });
      const data = await res.json();
      if (data.token) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setUser(data.user);
        setShowAuth(false);
      } else setError(data.detail);
    } catch { setError('Auth error'); }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const loadDashboard = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`${API_URL}/api/dashboard/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      setDashboardStats(data);
      setShowDashboard(true);
    } catch { setError('Failed to load dashboard'); }
  };

  const cropIcons = { Tomato: '🍅', Potato: '🥔', Corn: '🌽', Wheat: '🌾', Rice: '🍚', Grape: '🍇', Apple: '🍎' };
  const getCropIcon = (disease) => {
    for (const [crop, icon] of Object.entries(cropIcons)) {
      if (disease?.includes(crop)) return icon;
    }
    return disease === 'Healthy' ? '✅' : '🦠';
  };

  const isHealthy = result?.disease === 'Healthy';

  if (showDashboard) {
    return (
      <div className="app">
        <header className="header">
          <div className="header-content">
            <div className="logo">
              <span className="logo-icon">🌱</span>
              <h1>{t('app.title')}</h1>
            </div>
            <nav className="nav">
              <button onClick={() => setShowDashboard(false)}>{t('nav.scan')}</button>
              {user && <button onClick={loadDashboard} className="active">{t('nav.dashboard')}</button>}
              <button onClick={toggleTheme}>{isDark ? '☀️' : '🌙'}</button>
              <button onClick={() => setShowLangMenu(!showLangMenu)}>🌐</button>
              {showLangMenu && (
                <div className="lang-menu">
                  {languages.map(lang => (
                    <button key={lang.code} onClick={() => changeLanguage(lang.code)}>
                      {lang.flag} {lang.name}
                    </button>
                  ))}
                </div>
              )}
              {user ? <button onClick={handleLogout}>{t('nav.logout')}</button> : <button onClick={() => setShowAuth(true)}>{t('nav.login')}</button>}
            </nav>
          </div>
        </header>
        <main className="main">
          <div className="container">
            <div className="dashboard">
              <h2>📊 {t('dashboard.title')}</h2>
              <div className="stats-grid">
                <div className="stat-card"><div className="stat-value">{dashboardStats?.total_scans || 0}</div><div className="stat-label">{t('dashboard.totalScans')}</div></div>
                <div className="stat-card healthy"><div className="stat-value">{dashboardStats?.healthy_count || 0}</div><div className="stat-label">{t('dashboard.healthy')}</div></div>
                <div className="stat-card diseased"><div className="stat-value">{dashboardStats?.diseased_count || 0}</div><div className="stat-label">{t('dashboard.diseased')}</div></div>
                <div className="stat-card"><div className="stat-value">{dashboardStats?.avg_confidence || 0}%</div><div className="stat-label">{t('dashboard.avgConfidence')}</div></div>
              </div>
              <h3>{t('dashboard.recent')}</h3>
              <div className="history-list">
                {dashboardStats?.recent?.map((item, idx) => (
                  <div key={idx} className={`history-item ${item.disease === 'Healthy' ? 'healthy' : 'diseased'}`}>
                    <span className="history-icon">{getCropIcon(item.disease)}</span>
                    <div className="history-info">
                      <div className="history-disease">{item.disease?.replace(/_/g, ' ')}</div>
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
            <div className="logo"><span className="logo-icon">📷</span><h1>Camera</h1></div>
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
            <div className="logo"><span className="logo-icon">🌱</span><h1>{t('app.title')}</h1></div>
          </div>
        </header>
        <main className="main">
          <div className="container">
            <div className="auth-card">
              <h2>{authMode === 'login' ? '🔐 ' + t('auth.login') : '📝 ' + t('auth.register')}</h2>
              <form onSubmit={handleAuth}>
                {authMode === 'register' && (
                  <input type="text" placeholder={t('auth.name')} value={authForm.name} onChange={e => setAuthForm({...authForm, name: e.target.value})} required />
                )}
                <input type="email" placeholder={t('auth.email')} value={authForm.email} onChange={e => setAuthForm({...authForm, email: e.target.value})} required />
                <input type="password" placeholder={t('auth.password')} value={authForm.password} onChange={e => setAuthForm({...authForm, password: e.target.value})} required />
                <button type="submit" className="analyze-btn">{authMode === 'login' ? t('auth.login') : t('auth.register')}</button>
              </form>
              <p onClick={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}>
                {authMode === 'login' ? t('auth.noAccount') : t('auth.hasAccount')}
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
            <h1>{t('app.title')}</h1>
          </div>
          <p className="tagline">{t('app.tagline')}</p>
          <nav className="nav">
            {user && <button onClick={loadDashboard}>{t('nav.dashboard')}</button>}
            <button onClick={toggleTheme}>{isDark ? '☀️' : '🌙'}</button>
            <div className="lang-wrapper">
              <button onClick={() => setShowLangMenu(!showLangMenu)}>🌐</button>
              {showLangMenu && (
                <div className="lang-menu">
                  {languages.map(lang => (
                    <button key={lang.code} onClick={() => changeLanguage(lang.code)}>
                      {lang.flag} {lang.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
            {isInstallable && <button className="install-btn" onClick={handleInstall}>📲 Install</button>}
            {user ? <button onClick={handleLogout}>{user.name || user.email}</button> : <button onClick={() => setShowAuth(true)}>{t('nav.login')}</button>}
          </nav>
        </div>
      </header>

      {diseaseRisk && (
        <div className={`risk-banner ${diseaseRisk}`}>
          <span>⚠️ {t('weather.title')}: {diseaseRisk === 'high' ? t('weather.highRisk') : diseaseRisk === 'medium' ? t('weather.mediumRisk') : t('weather.lowRisk')}</span>
          <small>{t('weather.basedOn')}</small>
        </div>
      )}

      <main className="main">
        <div className="container">
          {!result && batchResults.length === 0 ? (
            <div className="upload-section">
              <div className="upload-tabs">
                <button className={!batchFiles.length ? 'active' : ''} onClick={() => setBatchFiles([])}>{t('upload.single')}</button>
                <button className={batchFiles.length ? 'active' : ''} onClick={() => { setSelectedImage(null); setPreviewUrl(null); }}>{t('upload.batch')}</button>
              </div>

              {batchFiles.length === 0 ? (
                <>
                  <div className="upload-toolbar">
                    <button className="camera-btn" onClick={startCamera}>📷 {t('upload.camera')}</button>
                  </div>
                  <div className="upload-area" onClick={() => fileInputRef.current?.click()} onDrop={handleDrop}>
                    <input ref={fileInputRef} type="file" accept="image/*" onChange={handleImageSelect} style={{ display: 'none' }} />
                    {previewUrl ? (
                      <div className="preview-container">
                        <img src={previewUrl} alt="Preview" className="preview-image" />
                        <button className="change-btn" onClick={e => { e.stopPropagation(); fileInputRef.current?.click(); }}>Change</button>
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
                        <p className="upload-text">{t('upload.drop')}</p>
                        <p className="upload-hint">{t('upload.hint')}</p>
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
                    {loading ? <span className="loading">{t('upload.analyzing')}</span> : '🔍 ' + t('upload.analyze')}
                  </button>
                </>
              ) : (
                <>
                  <div className="batch-upload-area" onClick={() => fileInputRef.current?.click()}>
                    <input ref={fileInputRef} type="file" accept="image/*" multiple onChange={handleBatchSelect} style={{ display: 'none' }} />
                    <p>📁 {batchFiles.length} files selected</p>
                  </div>
                  <button className="analyze-btn" onClick={handleBatchUpload} disabled={!batchFiles.length || loading}>
                    {loading ? <span className="loading">Processing...</span> : `📊 Analyze ${batchFiles.length} Files`}
                  </button>
                  {batchResults.length > 0 && (
                    <div className="batch-results">
                      <h3>Batch Results</h3>
                      {batchResults.map((res, idx) => (
                        <div key={idx} className={`batch-result-item ${res.success ? 'success' : 'error'}`}>
                          <span>{res.file}</span>
                          {res.success ? <span>{res.disease?.replace(/_/g, ' ')} ({Math.round(res.confidence)}%)</span> : <span className="error-text">{res.error}</span>}
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
                  <h2>{t('result.title')}</h2>
                  <div className="header-actions">
                    <button className="export-btn" onClick={exportPDF}>📄 {t('result.exportPdf')}</button>
                    <button className="reset-btn" onClick={handleReset}>{t('result.newScan')}</button>
                  </div>
                </div>
                <div className="result-body">
                  <div className="status-badge">
                    <span className={`status ${isHealthy ? 'healthy' : 'diseased'}`}>
                      {isHealthy ? '✅ ' + t('result.healthy') : '🦠 ' + t('result.diseased')}
                    </span>
                    {result.model_type && <span className="model-badge">🤖 {result.model_type}</span>}
                  </div>
                  <div className="result-item">
                    <label>{t('result.diagnosis')}</label>
                    <div className="diagnosis">
                      <span className="crop-icon">{getCropIcon(result.disease)}</span>
                      {result.disease_readable}
                    </div>
                  </div>
                  <div className="result-item">
                    <label>{t('result.crop')}</label>
                    <div>{result.crop} {cropIcons[result.crop]}</div>
                  </div>
                  <div className="result-item">
                    <label>{t('result.severity')}</label>
                    <span className={`severity-badge ${result.severity?.toLowerCase()}`}>{result.severity}</span>
                  </div>
                  <div className="result-item">
                    <label>{t('result.confidence')}</label>
                    <div className="confidence-bar">
                      <div className="confidence-fill" style={{ width: `${result.confidence}%` }} />
                      <span className="confidence-text">{result.confidence}%</span>
                    </div>
                  </div>
                  <div className="result-item">
                    <label>💊 {t('result.treatment')}</label>
                    <div className="treatment">{result.treatment}</div>
                  </div>
                  {result.top_predictions?.length > 1 && (
                    <div className="alternatives">
                      <label>{t('result.alternatives')}</label>
                      <div className="alternatives-list">
                        {result.top_predictions.slice(1).map((pred, idx) => (
                          <span key={idx} className="alt-item">
                            {getCropIcon(pred.disease)} {pred.disease?.replace(/_/g, ' ')} ({Math.round(pred.confidence * 100)}%)
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : null}

          {error && <div className="error-message"><span>⚠️</span> {error}</div>}

          <div className="features">
            <h3>🌾 {t('upload.title')}</h3>
            <div className="crops-grid">
              {Object.entries(cropIcons).map(([crop, icon]) => (
                <div key={crop} className="crop-item">{icon} {crop}</div>
              ))}
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>{t('footer.copyright')}</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
