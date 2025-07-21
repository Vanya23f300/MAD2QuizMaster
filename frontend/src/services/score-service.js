import api from './api'

class ScoreService {
  /**
   * Fetch all user scores
   * @returns {Promise} List of user scores
   */
  async getUserScores() {
    try {
      console.log('🚀 Fetching User Scores')
      const response = await api.get('/scores')
      
      console.log('✅ User Scores Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Scores retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching User Scores Error:', error)
      
      return {
        success: false,
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
      const response = await api.get(`/scores/${scoreId}`)
      
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
      const response = await api.get('/scores/summary')
      
      console.log('✅ Performance Summary Response:', response.data)
      
      return {
        success: true,
        data: response.data,
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
}

export default new ScoreService() 