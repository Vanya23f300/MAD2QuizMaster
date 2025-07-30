import api from './api'

class ScoreService {
  /**
   * Fetch all user scores
   * @returns {Promise} List of user scores
   */
  async getUserScores() {
    try {
      console.log('🚀 Fetching User Scores')
      // Use the correct API endpoint from the backend
      const response = await api.get('/api/dashboard/user/recent-scores', {
        params: { limit: 100 } // Get a large number to have all scores
      })
      
      console.log('✅ User Scores Response:', response.data)
      
      // Use only the real data from API
      const scoreData = response.data || [];
      
      if (!scoreData || scoreData.length === 0) {
        console.log('No scores found in API response')
      }
      
      return {
        success: true,
        data: scoreData,
        message: 'Scores retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching User Scores Error:', error)
      
      // Return empty array on error
      return {
        success: false,
        data: [],
        message: error.response?.data?.message || 'Failed to retrieve scores',
        error: error.response?.data
      }
    }
  }

  /**
   * Get detailed score report for a specific quiz attempt
   * @param {number} scoreId - ID of the score/attempt
   * @returns {Promise} Detailed score report
   */
  async getScoreDetails(scoreId) {
    try {
      console.log(`🚀 Fetching Score Details for Score ID: ${scoreId}`)
      const response = await api.get(`/api/scores/${scoreId}`)
      
      console.log('✅ Score Details Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Score details retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Score Details Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve score details',
        error: error.response?.data
      }
    }
  }

  /**
   * Get performance summary for the user
   * @returns {Promise} User performance summary
   */
  async getUserPerformanceSummary() {
    try {
      console.log('🚀 Fetching User Performance Summary')
      const response = await api.get('/api/dashboard/user/performance')
      
      console.log('✅ Performance Summary Response:', response.data)
      
      // Process the data to match expected format for the chart
      const userData = response.data;
      
      // Get recent scores to include in the performance summary
      const recentScoresResponse = await api.get('/api/dashboard/user/recent-scores', {
        params: { limit: 10 }  // Get up to 10 recent scores
      });
      
      const processedData = {
        stats: userData.stats || {
          quizzes_taken: 0,
          average_score: 0,
          pass_rate: 0,
          time_spent: 0
        },
        scores: recentScoresResponse.data || []
      };
      
      return {
        success: true,
        data: processedData,
        message: 'Performance summary retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Performance Summary Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve performance summary',
        error: error.response?.data
      }
    }
  }

  /**
   * Get leaderboard data showing all users' rankings
   * @returns {Promise} Leaderboard data with user rankings
   */
  async getLeaderboardData() {
    try {
      console.log('🚀 Fetching Leaderboard Data')
      const response = await api.get('/api/analytics/top-performers')
      
      console.log('✅ Leaderboard Data Response:', response.data)
      
      return {
        success: true,
        data: response.data || [],
        message: 'Leaderboard data retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Leaderboard Data Error:', error)
      
      // If API fails, try fallback approach by getting user list and their scores
      try {
        console.log('🔄 Attempting fallback for leaderboard data')
        
        // Get current user ID
        const currentUser = JSON.parse(localStorage.getItem('user') || '{}')
        const currentUserId = currentUser.id
        
        const usersResponse = await api.get('/api/users')
        
        if (!usersResponse.data || !Array.isArray(usersResponse.data)) {
          throw new Error('Invalid users data')
        }
        
        // Filter out admin users
        const users = usersResponse.data.filter(user => !user.is_admin)
        
        // For each user, calculate average score
        const leaderboardData = []
        
        for (const user of users) {
          // Highlight if this is the current user
          const isCurrentUser = user.id === currentUserId
          
          // Push to leaderboard with placeholder score
          leaderboardData.push({
            id: user.id,
            username: user.username,
            avg_score: user.avg_score || 0,
            total_quizzes: user.total_quizzes || 0,
            pass_rate: user.pass_rate || 0,
            isCurrentUser
          })
        }
        
        // Sort by average score descending
        leaderboardData.sort((a, b) => b.avg_score - a.avg_score)
        
        // Add rank
        leaderboardData.forEach((user, index) => {
          user.rank = index + 1
        })
        
        return {
          success: true,
          data: leaderboardData,
          message: 'Leaderboard data generated from user data'
        }
      } catch (fallbackError) {
        console.error('❌ Leaderboard Fallback Error:', fallbackError)
        return {
          success: false,
          data: [],
          message: error.response?.data?.message || 'Failed to retrieve leaderboard data',
          error: error.response?.data
        }
      }
    }
  }
}

export default new ScoreService() 