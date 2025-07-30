import api from './api'

const questionService = {
  // Get all questions or filter by quiz
  async getQuestions(quizId = null) {
    try {
      const params = quizId ? { quiz_id: quizId } : {}
      const response = await api.get('/api/questions', { params })
      return response.data
    } catch (error) {
      console.error('Error fetching questions:', error)
      throw error
    }
  },

  // Get a specific question by ID
  async getQuestion(questionId) {
    try {
      const response = await api.get(`/api/questions/${questionId}`)
      return response.data
    } catch (error) {
      console.error('Error fetching question:', error)
      throw error
    }
  },

  // Create a new question (Admin only)
  async createQuestion(questionData) {
    try {
      const response = await api.post('/api/questions', questionData)
      return response.data
    } catch (error) {
      console.error('Error creating question:', error)
      throw error
    }
  },

  // Update a question (Admin only)
  async updateQuestion(questionId, questionData) {
    try {
      const response = await api.put(`/api/questions/${questionId}`, questionData)
      return response.data
    } catch (error) {
      console.error('Error updating question:', error)
      throw error
    }
  },

  // Delete a question (Admin only)
  async deleteQuestion(questionId) {
    try {
      const response = await api.delete(`/api/questions/${questionId}`)
      return response.data
    } catch (error) {
      console.error('Error deleting question:', error)
      throw error
    }
  },

  // Create multiple questions for a quiz (Admin only)
  async createBulkQuestions(quizId, questionsData) {
    try {
      const response = await api.post('/api/questions/bulk', {
        quiz_id: quizId,
        questions: questionsData
      })
      return response.data
    } catch (error) {
      console.error('Error creating bulk questions:', error)
      throw error
    }
  },

  // Validate question data before creation
  async validateQuestions(questionsData) {
    try {
      const response = await api.post('/api/questions/validate', {
        questions: questionsData
      })
      return response.data
    } catch (error) {
      console.error('Error validating questions:', error)
      throw error
    }
  }
}

export default questionService 