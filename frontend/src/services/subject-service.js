import api from './api'

class SubjectService {
  /**
   * Create a new subject
   * @param {Object} subjectData - Subject creation data
   * @param {string} subjectData.name - Name of the subject
   * @param {string} [subjectData.description] - Optional description
   * @returns {Promise} Subject creation result
   */
  async createSubject(subjectData) {
    try {
      console.log('🚀 Creating Subject:', subjectData)
      
      // Validate input
      if (!subjectData.name) {
        throw new Error('Subject name is required')
      }

      const response = await api.post('/subjects', {
        name: subjectData.name,
        description: subjectData.description || ''
      })

      console.log('✅ Subject Creation Response:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Subject created successfully!'
      }
    } catch (error) {
      console.error('❌ Subject Creation Error:', error)
      
      // Detailed error handling
      let errorMessage = 'Failed to create subject'
      
      if (error.response) {
        switch (error.response.status) {
          case 400:
            errorMessage = 'Invalid subject data'
            break
          case 403:
            errorMessage = 'Unauthorized. Admin access required.'
            break
          case 409:
            errorMessage = 'Subject with this name already exists'
            break
          default:
            errorMessage = error.response.data?.message || 'Subject creation failed'
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
   * Fetch all subjects
   * @returns {Promise} List of subjects
   */
  async getAllSubjects() {
    try {
      const response = await api.get('/subjects')
      
      return {
        success: true,
        data: response.data,
        message: 'Subjects retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Subjects Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve subjects',
        error: error.response?.data
      }
    }
  }
}

export default new SubjectService() 