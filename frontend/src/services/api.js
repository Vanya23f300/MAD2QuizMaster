import axios from 'axios'

// Create a custom axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000',  // Use port 8000 to match backend
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Add a request interceptor for authentication
api.interceptors.request.use(
  config => {
    // Get the token from localStorage
    const token = localStorage.getItem('token')
    
    // Add token to all requests if available
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('Added token to request:', config.url, token ? `${token.substring(0, 10)}...` : 'No token')
    } else {
      console.warn('No token available for request:', config.url)
    }
    
    // Log all API requests for debugging
    console.log(`📤 API Request: ${config.method.toUpperCase()} ${config.url}`, config)
    
    return config
  },
  error => {
    console.error('📤 API Request Error:', error)
    return Promise.reject(error)
  }
)

// Add a response interceptor for handling common responses
api.interceptors.response.use(
  response => {
    // Log successful responses
    console.log(`📥 API Response (${response.config.url}):`, response.data)
    
    return response
  },
  error => {
    if (error.response) {
      // Log detailed error information
      console.error(`📥 API Error (${error.config?.url}):`, {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers
      })
      
      // Handle authentication errors
      if (error.response.status === 401) {
        console.warn('Authentication error - redirecting to login')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('isAuthenticated')
        localStorage.removeItem('isAdmin')
        
        // Check if we're already on the login page to avoid redirect loop
        if (!window.location.href.includes('/login')) {
          window.location = '/login'
        }
      }
    } else if (error.request) {
      // Request was made but no response was received
      console.error('📥 API No Response:', error.request)
    } else {
      // Something else caused the error
      console.error('📥 API Setup Error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

export default api