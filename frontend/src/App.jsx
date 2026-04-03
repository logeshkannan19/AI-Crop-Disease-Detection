import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
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

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedImage);

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
      setError('Failed to connect to server. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const isHealthy = result?.disease === 'Healthy';

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🌱</span>
            <h1>AgriScan AI</h1>
          </div>
          <p className="tagline">AI-Powered Crop Disease Detection</p>
        </div>
      </header>

      <main className="main">
        <div className="container">
          {!result ? (
            <div className="upload-section">
              <div 
                className="upload-area"
                onClick={() => fileInputRef.current?.click()}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageSelect}
                  style={{ display: 'none' }}
                />
                
                {previewUrl ? (
                  <div className="preview-container">
                    <img src={previewUrl} alt="Preview" className="preview-image" />
                    <button 
                      className="change-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        fileInputRef.current?.click();
                      }}
                    >
                      Change Image
                    </button>
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

              <button
                className="analyze-btn"
                onClick={handleAnalyze}
                disabled={!selectedImage || loading}
              >
                {loading ? (
                  <span className="loading">Analyzing...</span>
                ) : (
                  '🔍 Analyze Plant'
                )}
              </button>
            </div>
          ) : (
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
                  </div>

                  <div className="result-item">
                    <label>Diagnosis</label>
                    <div className="diagnosis">{result.disease_readable}</div>
                  </div>

                  <div className="result-item">
                    <label>Confidence</label>
                    <div className="confidence-bar">
                      <div 
                        className="confidence-fill" 
                        style={{ width: `${result.confidence}%` }}
                      />
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
                            {pred.disease.replace(/_/g, ' ')} ({Math.round(pred.confidence * 100)}%)
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="error-message">
              <span>⚠️</span> {error}
            </div>
          )}

          <div className="features">
            <h3>Supported Crops</h3>
            <div className="crops-grid">
              <div className="crop-item">🍅 Tomato</div>
              <div className="crop-item">🥔 Potato</div>
              <div className="crop-item">🌿 Healthy</div>
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>AgriScan AI © 2026 | EACE 2026 Exhibition Project</p>
        <p className="disclaimer">For demonstration purposes. Consult experts for real diagnosis.</p>
      </footer>
    </div>
  );
}

export default App;