import api from './api'

const dashboardService = {
  /**
   * Get dashboard statistics for admin
   */
  async getDashboardStats() {
    try {
      const response = await api.get('/api/dashboard/stats')
      return {
        success: true,
        data: {
          totalUsers: response.data.users?.total || 0,
          activeUsers: response.data.users?.active || 0,
          adminUsers: response.data.users?.admin || 0,
          totalSubjects: response.data.subjects?.total || 0,
          activeSubjects: response.data.subjects?.active || 0,
          totalChapters: response.data.chapters?.total || 0,
          totalQuizzes: response.data.quizzes?.total || 0,
          activeQuizzes: response.data.quizzes?.active || 0,
          totalAttempts: response.data.scores?.total_attempts || 0,
          avgScore: response.data.scores?.avg_score || 0,
          avgQuizCompletion: response.data.scores?.avg_score || 0,
          userGrowth: 12 // Placeholder for now
        }
      }
    } catch (error) {
      console.error('Dashboard stats error:', error)
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to fetch dashboard statistics',
        data: null
      }
    }
  },

  /**
   * Get recent activities for admin dashboard
   */
  async getRecentActivities() {
    try {
      const response = await api.get('/api/dashboard/activities')
      
      // Format the activities data
      const activities = response.data.map((activity, index) => ({
        id: index + 1,
        description: activity.description || 'Unknown activity',
        timestamp: activity.timestamp || new Date().toISOString()
      }))

      return {
        success: true,
        data: activities
      }
    } catch (error) {
      console.error('Recent activities error:', error)
      
      // Return empty array on error
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to fetch recent activities',
        data: []
      }
    }
  },

  /**
   * Get user performance statistics
   */
  async getUserPerformance() {
    try {
      console.log('Fetching user performance data')
      
      // Ensure we have a token
      // const token = localStorage.getItem('token')
      // if (!token) {
      //   console.error('No token available for authentication')
      //   throw new Error('Authentication token is required')
      // }
      
      const response = await api.get('/api/dashboard/user/performance')
      console.log('User performance response:', response.data)
      
      // Use only real data from the API
      //if (!response.data || !response.data.stats) {
       // console.warn('API returned invalid format, using empty stats object')
      //  return {
       //   success: true,
         // data: {
      //  /     stats: {
      //  /       quizzes_taken: 0,
      //  /      average_score: 0,
      //  /      pass_rate: 0,
           //   time_spent: 0
      //      }
      //    }
      //  }
      //   }
      
      // Return the real data from API
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('User performance error:', error)
      // Log more detailed error info
      if (error.response) {
        console.error('Response details:', {
          status: error.response.status,
          data: error.response.data,
          headers: error.response.headers
        })
      } else if (error.request) {
        console.error('No response received:', error.request)
      } else {
        console.error('Error setting up request:', error.message)
      }
      
      // Return empty data on error
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to fetch performance data',
        data: {
          stats: {
            quizzes_taken: 0,
            average_score: 0,
            pass_rate: 0,
            time_spent: 0
          }
        }
      }
    }
  },

  /**
   * Get recent scores for the user
   */
  async getRecentScores() {
    try {
      const response = await api.get('/api/dashboard/user/recent-scores', {
        params: { limit: 5 } // Get latest 5 scores
      })
      
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Recent scores error:', error)
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to fetch recent scores',
        data: []
      }
    }
  }
}

export default dashboardService 