import apiClient from './api';

const authService = {
  async login(email, password) {
    try {
      const response = await apiClient.post('/login', { email, password })
      
      // Store token and user info properly
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
      }
      if (response.data.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      
      return response.data
    } catch (error) {
      console.error('Login error:', error.response || error)
      throw error
    }
  },

  async signup(userData) {
    try {
      const response = await apiClient.post('/signup', userData)
      return response.data
    } catch (error) {
      console.error('Signup error:', error.response || error)
      throw error
    }
  },

  async initializeAdmin(email, username, password) {
    try {
      const response = await apiClient.post('/admin/initialize', {
        email,
        username,
        password
      })
      return response.data
    } catch (error) {
      console.error('Admin initialization error:', error)
      throw error
    }
  },

  logout() {
    // Clear local storage
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },

  getCurrentUser() {
    const userJson = localStorage.getItem('user')
    return userJson ? JSON.parse(userJson) : null
  },

  isAuthenticated() {
    return !!localStorage.getItem('token')
  },

  isAdmin() {
    const user = this.getCurrentUser()
    return user && user.is_admin
  }
}

export default authService 