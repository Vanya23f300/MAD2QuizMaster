import api from './api'

class ChapterService {
  /**
   * Create a new chapter
   * @param {Object} chapterData - Chapter creation data
   * @returns {Promise} Chapter creation result
   */
  async createChapter(chapterData) {
    try {
      console.log('🚀 Creating Chapter:', chapterData)
      
      // Validate input
      if (!chapterData.name || !chapterData.subject_id) {
        throw new Error('Chapter name and subject are required')
      }

      // Get token from localStorage
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('No authentication token found')
      }

      const response = await api.post('/api/chapters', chapterData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      console.log('✅ Chapter Creation Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Chapter created successfully!'
      }
    } catch (error) {
      console.error('❌ Chapter Creation Error:', error)
      
      // Detailed error handling
      let errorMessage = 'Failed to create chapter'
      
      if (error.response) {
        switch (error.response.status) {
          case 400:
            errorMessage = 'Invalid chapter data'
            break
          case 403:
            errorMessage = 'Unauthorized. Admin access required.'
            break
          case 409:
            errorMessage = 'Chapter with this name already exists'
            break
          default:
            errorMessage = error.response.data?.message || 'Chapter creation failed'
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
   * Fetch chapters for a specific subject
   * @param {number} subjectId - ID of the subject
   * @returns {Promise} List of chapters
   */
  async getChaptersBySubject(subjectId) {
    try {
      // Get token from localStorage
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('No authentication token found')
      }

      const response = await api.get(`/api/subjects/${subjectId}/chapters`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      return {
        success: true,
        data: response.data,
        message: 'Chapters retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Chapters Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve chapters',
        error: error.response?.data
      }
    }
  }
}

export default new ChapterService() 