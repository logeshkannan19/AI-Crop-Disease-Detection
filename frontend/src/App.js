import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post('http://localhost:5000/api/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetApp = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🌱</span>
          <h1>AgriScan AI</h1>
        </div>
        <p className="tagline">AI-Powered Crop Disease Detection</p>
      </header>

      <main className="main-content">
        <div className="upload-section">
          <div className="upload-container">
            <div className="upload-area">
              {previewUrl ? (
                <div className="image-preview">
                  <img src={previewUrl} alt="Preview" />
                  <button className="change-btn" onClick={() => document.getElementById('fileInput').click()}>
                    Change Image
                  </button>
                </div>
              ) : (
                <label className="upload-label">
                  <input
                    id="fileInput"
                    type="file"
                    accept="image/*"
                    onChange={handleImageSelect}
                    style={{ display: 'none' }}
                  />
                  <div className="upload-icon">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="17,8 12,3 7,8"/>
                      <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                  </div>
                  <p className="upload-text">Click to upload or drag and drop</p>
                  <p className="upload-hint">Supports: PNG, JPG, JPEG, GIF, BMP, WEBP</p>
                </label>
              )}
            </div>

            {selectedImage && (
              <div className="image-info">
                <span className="file-name">📄 {selectedImage.name}</span>
                <span className="file-size">{(selectedImage.size / 1024).toFixed(1)} KB</span>
              </div>
            )}

            <button
              className="analyze-btn"
              onClick={handleSubmit}
              disabled={!selectedImage || loading}
            >
              {loading ? (
                <span className="loading-spinner">🔄 Analyzing...</span>
              ) : (
                <>🔍 Analyze Plant</>
              )}
            </button>
          </div>
        </div>

        {error && (
          <div className="result-section">
            <div className="error-box">
              <span className="error-icon">⚠️</span>
              <p>{error}</p>
            </div>
          </div>
        )}

        {result && result.success && (
          <div className="result-section">
            <div className={`result-card ${result.disease === 'Healthy' ? 'healthy' : 'diseased'}`}>
              <div className="result-header">
                <h2>Analysis Result</h2>
                <button className="reset-btn" onClick={resetApp}>New Scan</button>
              </div>

              <div className="result-body">
                <div className="disease-status">
                  <span className="status-label">Status:</span>
                  <span className={`status-value ${result.disease === 'Healthy' ? 'healthy' : 'diseased'}`}>
                    {result.disease === 'Healthy' ? '✅ Healthy' : '🦠 Disease Detected'}
                  </span>
                </div>

                <div className="disease-name">
                  <span className="label">Diagnosis:</span>
                  <span className="value">{result.disease.replace(/_/g, ' ')}</span>
                </div>

                <div className="confidence">
                  <span className="label">Confidence:</span>
                  <div className="confidence-bar">
                    <div className="confidence-fill" style={{ width: `${result.confidence}%` }}></div>
                    <span className="confidence-text">{result.confidence}%</span>
                  </div>
                </div>

                <div className="treatment">
                  <span className="label">💊 Recommended Treatment:</span>
                  <p className="treatment-text">{result.treatment}</p>
                </div>

                {result.top_predictions && result.top_predictions.length > 1 && (
                  <div className="alternatives">
                    <span className="label">Other Possibilities:</span>
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

        <div className="features-section">
          <h3>Supported Crops</h3>
          <div className="crops-grid">
            <div className="crop-item">🍅 Tomato</div>
            <div className="crop-item">🥔 Potato</div>
            <div className="crop-item">🌿 Healthy Leaf</div>
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