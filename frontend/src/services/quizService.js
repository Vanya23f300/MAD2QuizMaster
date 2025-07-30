import api from './api'

const quizService = {
  // Get all quizzes or filter by chapter
  async getQuizzes(chapterId = null) {
    try {
      const params = chapterId ? { chapter_id: chapterId } : {}
      const response = await api.get('/api/quizzes', { params })
      return response.data
    } catch (error) {
      console.error('Error fetching quizzes:', error)
      throw error
    }
  },

  // Get a specific quiz by ID
  async getQuiz(quizId) {
    try {
      const response = await api.get(`/api/quizzes/${quizId}`)
      return response.data
    } catch (error) {
      console.error('Error fetching quiz:', error)
      throw error
    }
  },

  // Create a new quiz (Admin only)
  async createQuiz(quizData) {
    try {
      const response = await api.post('/api/quizzes', quizData)
      return response.data
    } catch (error) {
      console.error('Error creating quiz:', error)
      throw error
    }
  },

  // Update a quiz (Admin only)
  async updateQuiz(quizId, quizData) {
    try {
      const response = await api.put(`/api/quizzes/${quizId}`, quizData)
      return response.data
    } catch (error) {
      console.error('Error updating quiz:', error)
      throw error
    }
  },

  // Delete a quiz (Admin only)
  async deleteQuiz(quizId) {
    try {
      const response = await api.delete(`/api/quizzes/${quizId}`)
      return response.data
    } catch (error) {
      console.error('Error deleting quiz:', error)
      throw error
    }
  },

  // Get questions for a quiz
  async getQuizQuestions(quizId) {
    try {
      const response = await api.get(`/api/quizzes/${quizId}/questions`)
      return response.data
    } catch (error) {
      console.error('Error fetching quiz questions:', error)
      throw error
    }
  },

  // Start a quiz attempt
  async startQuiz(quizId) {
    try {
      const response = await api.post(`/api/quizzes/${quizId}/start`)
      return response.data
    } catch (error) {
      console.error('Error starting quiz:', error)
      throw error
    }
  },

  // Submit quiz answers
  async submitQuiz(quizId, submitData) {
    try {
      // Make sure all answers are stored as strings or numbers consistently for backend comparison
      if (submitData.answers) {
        Object.keys(submitData.answers).forEach(key => {
          if (submitData.answers[key] !== undefined && submitData.answers[key] !== null) {
            // Ensure answers are represented as numbers (backend expects numbers for comparison)
            submitData.answers[key] = Number(submitData.answers[key]);
          }
        });
      }
      
      const response = await api.post(`/api/quizzes/${quizId}/submit`, submitData)
      return response.data
    } catch (error) {
      console.error('Error submitting quiz:', error)
      throw error
    }
  },

  // Get quiz attempts
  async getQuizAttempts(quizId) {
    try {
      const response = await api.get(`/api/quizzes/${quizId}/attempts`)
      return response.data
    } catch (error) {
      console.error('Error fetching quiz attempts:', error)
      throw error
    }
  },

  // Get unattempted quizzes
  async getUnattemptedQuizzes() {
    try {
      const response = await api.get('/api/quizzes/unattempted')
      return response.data
    } catch (error) {
      console.error('Error fetching unattempted quizzes:', error)
      throw error
    }
  }
}

export default quizService 