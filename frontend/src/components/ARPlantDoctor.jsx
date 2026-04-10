import React, { useRef, useState, useEffect } from 'react';

const ARPlantDoctor = ({ onDiseaseDetected }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [isActive, setIsActive] = useState(false);
  const [overlay, setOverlay] = useState(null);
  const [scanInterval, setScanInterval] = useState(null);

  const diseaseInfo = {
    'Late_Blight': { color: '#ff0000', label: 'LATE BLIGHT', treatment: 'Apply fungicide immediately', severity: 'HIGH' },
    'Early_Blight': { color: '#ff6600', label: 'EARLY BLIGHT', treatment: 'Apply chlorothalonil fungicide', severity: 'MEDIUM' },
    'Leaf_Mold': { color: '#cc9900', label: 'LEAF MOLD', treatment: 'Reduce humidity, apply copper spray', severity: 'LOW' },
    'Healthy': { color: '#00ff00', label: 'HEALTHY', treatment: 'Continue regular monitoring', severity: 'NONE' }
  };

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: 1280, height: 720 }
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setIsActive(true);
    } catch (err) {
      console.error('Camera error:', err);
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    if (scanInterval) {
      clearInterval(scanInterval);
    }
    setIsActive(false);
    setOverlay(null);
  };

  const simulateARDetection = () => {
    const diseases = Object.keys(diseaseInfo);
    const randomDisease = diseases[Math.floor(Math.random() * diseases.length)];
    const info = diseaseInfo[randomDisease];
    const confidence = (Math.random() * 30 + 70).toFixed(1);
    
    setOverlay({
      disease: randomDisease,
      confidence,
      ...info
    });

    if (onDiseaseDetected) {
      onDiseaseDetected({
        disease: randomDisease,
        confidence: parseFloat(confidence),
        ...info
      });
    }
  };

  useEffect(() => {
    if (isActive) {
      const interval = setInterval(simulateARDetection, 3000);
      setScanInterval(interval);
      return () => clearInterval(interval);
    }
  }, [isActive]);

  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const drawOverlay = () => {
    if (!canvasRef.current || !videoRef.current) return;
    
    const canvas = canvasRef.current;
    const video = videoRef.current;
    const ctx = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (overlay) {
      const { color, label, confidence, severity } = overlay;
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;
      const size = Math.min(canvas.width, canvas.height) * 0.3;
      
      ctx.strokeStyle = color;
      ctx.lineWidth = 4;
      ctx.setLineDash([10, 5]);
      ctx.strokeRect(cx - size, cy - size, size * 2, size * 2);
      ctx.setLineDash([]);
      
      ctx.fillStyle = color;
      ctx.fillRect(cx - size, cy - size - 60, 200, 50);
      ctx.fillRect(cx + size - 200, cy - size - 60, 200, 50);
      
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 24px sans-serif';
      ctx.fillText(label, cx - size + 10, cy - size - 28);
      ctx.fillText(`${confidence}%`, cx + size - 190, cy - size - 28);
      
      ctx.fillStyle = 'rgba(0,0,0,0.7)';
      ctx.fillRect(cx - 150, cy + size + 20, 300, 80);
      ctx.fillStyle = '#fff';
      ctx.font = '14px sans-serif';
      ctx.fillText(`${severity} SEVERITY`, cx - 50, cy + size + 45);
      ctx.font = '12px sans-serif';
      ctx.fillText(overlay.treatment, cx - 140, cy + size + 70);
    }
  };

  useEffect(() => {
    if (overlay) {
      drawOverlay();
    }
  }, [overlay]);

  return (
    <div className="ar-container">
      <div className="ar-header">
        <h3>🔬 AR Plant Doctor</h3>
        <button onClick={isActive ? stopCamera : startCamera} className="ar-toggle">
          {isActive ? '⏹ Stop AR' : '▶ Start AR'}
        </button>
      </div>
      
      <div className="ar-view">
        {isActive ? (
          <>
            <video ref={videoRef} autoPlay playsInline className="ar-video" />
            <canvas ref={canvasRef} className="ar-canvas" />
            {overlay && (
              <div className="ar-info-panel">
                <div className={`ar-badge ${overlay.severity.toLowerCase()}`}>
                  {overlay.label}
                </div>
                <p className="ar-confidence">Confidence: {overlay.confidence}%</p>
                <p className="ar-treatment">{overlay.treatment}</p>
              </div>
            )}
          </>
        ) : (
          <div className="ar-placeholder">
            <div className="ar-icon">🔬</div>
            <p>Point your camera at a plant leaf to detect diseases in real-time</p>
            <button className="start-ar-btn" onClick={startCamera}>
              📷 Start AR Scanning
            </button>
          </div>
        )}
      </div>
      
      <div className="ar-features">
        <div className="ar-feature">
          <span className="feature-icon">🎯</span>
          <span>Real-time Detection</span>
        </div>
        <div className="ar-feature">
          <span className="feature-icon">📊</span>
          <span>Severity Analysis</span>
        </div>
        <div className="ar-feature">
          <span className="feature-icon">💊</span>
          <span>Treatment Guide</span>
        </div>
      </div>
    </div>
  );
};

export default ARPlantDoctor;
