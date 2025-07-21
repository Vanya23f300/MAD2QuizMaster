import api from './api'

class DashboardService {
  /**
   * Fetch dashboard statistics
   * @returns {Promise} Dashboard statistics
   */
  async getDashboardStats() {
    try {
      console.log('🔍 Fetching Dashboard Stats...')
      
      const response = await api.get('/dashboard/stats')
      
      console.log('📊 Dashboard Stats Raw Response:', response.data)
      
      // Ensure data is always present and has default values
      const stats = {
        totalUsers: response.data.totalUsers || 0,
        activeUsers: response.data.activeUsers || 0,
        userGrowth: response.data.userGrowth || 0,
        totalQuizzes: response.data.totalQuizzes || 0,
        avgQuizCompletion: response.data.avgQuizCompletion || 0
      }
      
      console.log('📈 Processed Dashboard Stats:', stats)
      
      return {
        success: true,
        data: stats,
        message: 'Dashboard statistics retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Dashboard Stats Error:', error)
      
      // Detailed error logging
      if (error.response) {
        console.error('Response Error Details:', {
          status: error.response.status,
          data: error.response.data,
          headers: error.response.headers
        })
      }
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve dashboard statistics',
        error: error.response?.data
      }
    }
  }

  /**
   * Fetch recent platform activities
   * @returns {Promise} Recent activities
   */
  async getRecentActivities() {
    try {
      console.log('🔍 Fetching Recent Activities...')
      
      const response = await api.get('/dashboard/activities')
      
      console.log('📊 Recent Activities Raw Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Recent activities retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Recent Activities Error:', error)
      
      // Detailed error logging
      if (error.response) {
        console.error('Response Error Details:', {
          status: error.response.status,
          data: error.response.data,
          headers: error.response.headers
        })
      }
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve recent activities',
        error: error.response?.data
      }
    }
  }
}

export default new DashboardService() 