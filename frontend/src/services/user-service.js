import api from './api'

class UserService {
  /**
   * Create a new user
   * @param {Object} userData - User registration data
   * @returns {Promise} User creation result
   */
  async createUser(userData) {
    try {
      console.log('🚀 Creating User:', userData)
      
      // Validate input
      const requiredFields = ['email', 'username', 'password', 'dob', 'qualification']
      for (const field of requiredFields) {
        if (!userData[field]) {
          throw new Error(`${field} is required`)
        }
      }

      // Get token from localStorage
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('No authentication token found')
      }

      const response = await api.post('/users/create', userData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      console.log('✅ User Creation Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'User created successfully!'
      }
    } catch (error) {
      console.error('❌ User Creation Error:', error)
      
      // Detailed error handling
      let errorMessage = 'Failed to create user'
      
      if (error.response) {
        switch (error.response.status) {
          case 400:
            errorMessage = 'Invalid user data'
            break
          case 403:
            errorMessage = 'Unauthorized. Admin access required.'
            break
          case 409:
            errorMessage = 'User with this email or username already exists'
            break
          default:
            errorMessage = error.response.data?.message || 'User creation failed'
        }
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
   * Fetch all users
   * @returns {Promise} List of users
   */
  async getAllUsers() {
    try {
      // Get token from localStorage
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('No authentication token found')
      }

      const response = await api.get('/users', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      return {
        success: true,
        data: response.data,
        message: 'Users retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Users Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve users',
        error: error.response?.data
      }
    }
  }
}

export default new UserService() 