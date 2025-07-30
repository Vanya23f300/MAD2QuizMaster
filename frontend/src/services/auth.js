import api from './api'

// Error message mapping for user-friendly display
const ERROR_MESSAGES = {
  401: 'Invalid password. Please try again.',
  404: 'User not found. Please check your email.',
  409: 'User already exists. Please login instead.',
  500: 'Server error. Please try again later.',
  network: 'Network error. Please check your connection.'
}

class AuthService {
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @param {string} userData.email - User email
   * @param {string} userData.username - User username
   * @param {string} userData.password - User password
   * @param {string} userData.dob - Date of birth (YYYY-MM-DD)
   * @param {string} userData.qualification - User qualification
   * @returns {Promise} API response
   */
  async signup(userData) {
    try {
      console.log('🚀 Sending signup request to backend:', userData)
      const response = await api.post('/api/signup', userData)
      console.log('✅ Signup response received:', response.data)
      
      // Store auth data in localStorage on successful signup
      if (response.data.token && response.data.user) {
        console.log('💾 Storing token and user data in localStorage...')
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', response.data.user)
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('isAdmin', 'false') // New users are not admins
        
        console.log('✅ Token stored successfully:', localStorage.getItem('token'))
        console.log('✅ All localStorage data:', {
          token: localStorage.getItem('token'),
          user: localStorage.getItem('user'),
          isAuthenticated: localStorage.getItem('isAuthenticated'),
          isAdmin: localStorage.getItem('isAdmin')
        })
      } else {
        console.error('❌ Missing token or user in response:', response.data)
      }
      
      return {
        success: true,
        data: response.data,
        message: 'Account created successfully!'
      }
    } catch (error) {
      console.error('❌ Signup error:', error)
      console.error('❌ Error response:', error.response?.data)
      
      // Handle different error scenarios
      let errorMessage = ERROR_MESSAGES.network
      
      if (error.response) {
        const status = error.response.status
        errorMessage = ERROR_MESSAGES[status] || error.response.data?.message || `Error: ${status}`
      }
      
      return {
        success: false,
        message: errorMessage,
        error: error.response?.data
      }
    }
  }

  /**
   * Login user
   * @param {Object} credentials - User login credentials
   * @param {string} credentials.email - User email
   * @param {string} credentials.password - User password
   * @returns {Promise} API response
   */
  async login(credentials) {
    try {
      console.log('🚀 Sending login request to backend:', { email: credentials.email })
      const response = await api.post('/api/login', credentials)
      console.log('✅ Login response received:', response.data)
      
      // Store auth data in localStorage on successful login
      if (response.data.access_token && response.data.user) {
        console.log('💾 Storing token and user data in localStorage...')
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('isAdmin', response.data.user.is_admin ? 'true' : 'false')
        
        console.log('✅ Token stored successfully:', localStorage.getItem('token'))
        console.log('✅ All localStorage data:', {
          token: localStorage.getItem('token'),
          user: localStorage.getItem('user'),
          isAuthenticated: localStorage.getItem('isAuthenticated'),
          isAdmin: localStorage.getItem('isAdmin')
        })
      } else {
        console.error('❌ Missing token or user in response:', response.data)
        throw new Error('Invalid response format from server')
      }
      
      return {
        success: true,
        data: response.data,
        message: 'Login successful!',
        isAdmin: response.data.user.is_admin,
        user: response.data.user,
        access_token: response.data.access_token
      }
    } catch (error) {
      console.error('❌ Login error:', error)
      console.error('❌ Error response:', error.response?.data)
      
      // Handle different error scenarios
      let errorMessage = ERROR_MESSAGES.network
      
      if (error.response) {
        const status = error.response.status
        errorMessage = ERROR_MESSAGES[status] || error.response.data?.message || `Error: ${status}`
      } else if (error.message) {
        errorMessage = error.message
      }
      
      return {
        success: false,
        message: errorMessage,
        error: error.response?.data
      }
    }
  }

  /**
   * Logout user
   */
  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('isAdmin')
    localStorage.removeItem('isAuthenticated')
  }

  /**
   * Check if user is authenticated
   * @returns {boolean} Authentication status
   */
  isAuthenticated() {
    return localStorage.getItem('isAuthenticated') === 'true' && 
           localStorage.getItem('token') !== null
  }

  /**
   * Check if user is admin
   * @returns {boolean} Admin status
   */
  isAdmin() {
    return localStorage.getItem('isAdmin') === 'true'
  }

  /**
   * Get current user info
   * @returns {Object|null} User info or null
   */
  getCurrentUser() {
    if (this.isAuthenticated()) {
      try {
        const userString = localStorage.getItem('user');
        if (userString) {
          // Try to parse user as JSON
          if (userString.startsWith('{')) {
            return JSON.parse(userString);
          } else {
            // If not JSON, return as string
            return {
              username: userString,
              isAdmin: this.isAdmin()
            };
          }
        }
      } catch (error) {
        console.error('Error parsing user data:', error);
        return null;
      }
    }
    return null;
  }
}

export default new AuthService() 