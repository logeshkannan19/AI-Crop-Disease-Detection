/**
 * API Service
 * Handles all HTTP requests to the backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  constructor(baseUrl = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config = {
      ...options,
      headers: {
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Request failed');
      }
      
      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async checkHealth() {
    return this.request('/api/health');
  }

  async predictDisease(file) {
    const formData = new FormData();
    formData.append('file', file);

    return this.request('/api/predict', {
      method: 'POST',
      body: formData,
    });
  }

  async getClasses() {
    return this.request('/api/classes');
  }
}

export const apiService = new ApiService();
export default apiService;