import axios from 'axios'
import AuthService from './auth'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000, // 10 second timeout
  // Retry configuration
  retry: 3,
  retryDelay: (retryCount) => {
    return retryCount * 1000 // 1s, 2s, 3s
  }
})

// Request interceptor for adding token
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    console.log('API Request:', config.method.toUpperCase(), config.url, config.data)
    return config
  },
  error => {
    console.error('Request setup error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  response => {
    console.log('API Response:', response.status, response.data)
    return response
  },
  async error => {
    console.error('API Error:', error.response || error)
    
    // Get the original request configuration
    const originalRequest = error.config

    // Handle retry logic for network errors or 5xx responses
    if ((error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK' || 
        (error.response && error.response.status >= 500)) && 
        originalRequest && !originalRequest._retry &&
        originalRequest.retry > 0) {
      
      originalRequest._retry = true
      originalRequest.retry--

      // Wait for the retry delay
      await new Promise(resolve => 
        setTimeout(resolve, originalRequest.retryDelay(originalRequest.retry))
      )

      // Retry the request
      return apiClient(originalRequest)
    }
    
    // Handle specific error scenarios
    if (error.response) {
      // The request was made and the server responded with a status code
      switch (error.response.status) {
        case 401: // Unauthorized
          // Only logout if not already on login page and token exists
          if (window.location.pathname !== '/login' && localStorage.getItem('token')) {
            AuthService.logout()
            window.location.href = '/login'
          }
          break
        case 403: // Forbidden
          console.error('Access denied:', error.response.data?.message)
          break
        case 404: // Not Found
          console.error('Resource not found:', error.response.data?.message)
          break
        case 500: // Internal Server Error
          console.error('Server error:', error.response.data?.message)
          break
      }
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - server took too long to respond')
    } else if (error.code === 'ERR_NETWORK') {
      console.error('Network error - please check your internet connection')
    } else {
      console.error('Error setting up request:', error.message)
    }
    
    return Promise.reject(error)
  }
)

export default apiClient