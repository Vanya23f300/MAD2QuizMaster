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

      const response = await api.post('/api/subjects', {
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
      console.log('🔍 Fetching all subjects...')
      const response = await api.get('/api/subjects')
      console.log('✅ Subjects retrieved:', response.data)
      
      return {
        success: true,
        data: response.data || [],
        message: 'Subjects retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Fetching Subjects Error:', error)
      
      // Return empty array instead of error to avoid UI breaking
      return {
        success: false,
        data: [], // Return empty array as fallback
        message: error.response?.data?.message || 'Failed to retrieve subjects',
        error: error.response?.data
      }
    }
  }

  /**
   * Update an existing subject
   * @param {number} subjectId - ID of the subject to update
   * @param {Object} subjectData - Subject update data
   * @returns {Promise} Subject update result
   */
  async updateSubject(subjectId, subjectData) {
    try {
      console.log('🔄 Updating Subject:', { id: subjectId, data: subjectData })
      
      const response = await api.put(`/api/subjects/${subjectId}`, {
        name: subjectData.name,
        description: subjectData.description || '',
        is_active: subjectData.is_active
      })

      return {
        success: true,
        data: response.data,
        message: 'Subject updated successfully!'
      }
    } catch (error) {
      console.error('❌ Subject Update Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to update subject',
        error: error.response?.data
      }
    }
  }

  /**
   * Delete a subject
   * @param {number} subjectId - ID of the subject to delete
   * @returns {Promise} Subject deletion result
   */
  async deleteSubject(subjectId) {
    try {
      console.log('🗑️ Deleting Subject:', subjectId)
      
      // eslint-disable-next-line no-unused-vars
      const response = await api.delete(`/api/subjects/${subjectId}`)

      return {
        success: true,
        message: 'Subject deleted successfully!'
      }
    } catch (error) {
      console.error('❌ Subject Deletion Error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to delete subject',
        error: error.response?.data
      }
    }
  }
}

export default new SubjectService() 