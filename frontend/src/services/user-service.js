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
      const requiredFields = ['email', 'username', 'password', 'qualification']
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

  /**
   * Get user profile data
   * @returns {Promise} User profile data
   */
  async getProfile() {
    try {
      console.log('🔍 Fetching user profile...')
      
      let response;
      try {
        response = await api.get('/api/user/profile')
        console.log('✅ Profile API response:', response)
      } catch (error) {
        console.warn('❌ API Error, falling back to local storage:', error)
        // If API fails, try to get data from localStorage
        const userJson = localStorage.getItem('user')
        if (userJson) {
          try {
            const userData = JSON.parse(userJson)
            console.log('📦 User data from localStorage:', userData)
            response = { 
              data: {
                id: userData.id,
                username: userData.email,
                full_name: userData.username,
                created_at: userData.registration_date || new Date().toISOString(),
                updated_at: userData.last_login || new Date().toISOString()
              }
            }
          } catch (e) {
            console.error('❌ Failed to parse user data from localStorage:', e)
            throw error
          }
        } else {
          throw error
        }
      }
      
      console.log('✅ Final profile data:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Profile retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Profile fetch error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve profile',
        error: error.response?.data
      }
    }
  }

  /**
   * Update user profile
   * @param {Object} profileData - Updated profile data
   * @returns {Promise} Update result
   */
  async updateProfile(profileData) {
    try {
      console.log('🔄 Updating profile:', profileData)
      
      const response = await api.put('/api/user/profile', {
        full_name: profileData.full_name,
        current_password: profileData.current_password
      })
      
      console.log('✅ Profile updated:', response.data)
      
      // Update local storage with new user data
      const userString = localStorage.getItem('user')
      if (userString) {
        try {
          const userData = JSON.parse(userString)
          userData.username = profileData.full_name
          localStorage.setItem('user', JSON.stringify(userData))
        } catch (e) {
          console.error('Failed to update local storage:', e)
        }
      }
      
      return {
        success: true,
        data: response.data,
        message: 'Profile updated successfully'
      }
    } catch (error) {
      console.error('❌ Profile update error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to update profile',
        error: error.response?.data
      }
    }
  }

  /**
   * Change user password
   * @param {Object} passwordData - Password change data
   * @returns {Promise} Password change result
   */
  async changePassword(passwordData) {
    try {
      console.log('🔄 Changing password...')
      
      const response = await api.post('/user/change-password', passwordData)
      
      console.log('✅ Password changed successfully')
      
      return {
        success: true,
        data: response.data,
        message: 'Password changed successfully'
      }
    } catch (error) {
      console.error('❌ Password change error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to change password',
        error: error.response?.data
      }
    }
  }

  /**
   * Get user statistics
   * @returns {Promise} User statistics
   */
  async getStatistics() {
    try {
      console.log('🔍 Fetching user statistics...')
      
      const response = await api.get('/user/statistics')
      
      console.log('✅ Statistics:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Statistics retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Statistics fetch error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve statistics',
        error: error.response?.data
      }
    }
  }

  /**
   * Get user's recent activity
   * @param {number} limit - Maximum number of activities to return
   * @returns {Promise} Recent activity data
   */
  async getRecentActivity(limit = 5) {
    try {
      console.log('🔍 Fetching recent activity...')
      
      const response = await api.get('/user/activity', {
        params: { limit }
      })
      
      console.log('✅ Recent activity:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Recent activity retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Activity fetch error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve activity',
        error: error.response?.data
      }
    }
  }
}

export default new UserService() 