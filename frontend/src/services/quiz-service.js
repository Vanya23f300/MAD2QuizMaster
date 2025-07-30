import api from './api'

class QuizService {
  /**
   * Fetch available quizzes for users
   * @returns {Promise} List of available quizzes
   */
  async getAvailableQuizzes() {
    try {
      console.log('🚀 Fetching Available Quizzes')
      const response = await api.get('/api/quizzes/available')
      
      console.log('✅ Available Quizzes Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Quizzes retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Available Quizzes Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve quizzes',
        error: error.response?.data
      }
    }
  }

  /**
   * Fetch recent quiz scores for the current user
   * @returns {Promise} List of recent user scores
   */
  async getUserRecentScores() {
    try {
      console.log('🚀 Fetching User Recent Scores')
      const response = await api.get('/api/scores/recent')
      
      console.log('✅ Recent Scores Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Recent scores retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Recent Scores Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve recent scores',
        error: error.response?.data
      }
    }
  }

  /**
   * Start a quiz attempt
   * @param {number} quizId - ID of the quiz to start
   * @returns {Promise} Quiz start details
   */
  async startQuizAttempt(quizId) {
    try {
      console.log(`🚀 Starting Quiz Attempt for Quiz ID: ${quizId}`)
      const response = await api.post(`/api/quizzes/${quizId}/start`)
      
      console.log('✅ Quiz Start Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Quiz started successfully'
      }
    } catch (error) {
      console.error('❌ Starting Quiz Attempt Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to start quiz',
        error: error.response?.data
      }
    }
  }

  /**
   * Submit quiz answers
   * @param {number} quizId - ID of the quiz
   * @param {Array} answers - List of user's answers
   * @returns {Promise} Quiz result
   */
  async submitQuizAnswers(quizId, answers) {
    try {
      console.log(`🚀 Submitting Quiz Answers for Quiz ID: ${quizId}`)
      const response = await api.post(`/api/quizzes/${quizId}/submit`, { answers })
      
      console.log('✅ Quiz Submit Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Quiz submitted successfully'
      }
    } catch (error) {
      console.error('❌ Submitting Quiz Answers Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to submit quiz',
        error: error.response?.data
      }
    }
  }
}

export default new QuizService() 