import api from './api'

class ExportService {
  /**
   * Start a new quiz data export
   * @returns {Promise} Export task details
   */
  async startExport() {
    try {
      console.log('🚀 Starting quiz export...')
      
      // Check authentication token
      const token = localStorage.getItem('token')
      if (!token) {
        console.error('No authentication token found')
        return {
          success: false,
          message: 'Authentication required. Please log in again.'
        }
      }
      
      // Make the API call
      const response = await api.post('/api/exports/user-quizzes')
      
      console.log('✅ Export started:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Export started successfully'
      }
    } catch (error) {
      console.error('❌ Export start error:', error)
      
      // Get more specific error info
      let errorMessage = 'Failed to start export'
      if (error.response) {
        const status = error.response.status
        if (status === 401 || status === 422) {
          errorMessage = 'Authentication expired. Please log in again.'
        } else {
          errorMessage = `Server error (${status}): ${error.response.data?.message || 'Unknown server error'}`
        }
      } else if (error.message) {
        errorMessage = error.message
      }
      
      return {
        success: false,
        message: errorMessage,
        error: error.response?.data || error
      }
    }
  }

  /**
   * Check the status of an export task
   * @param {string} taskId - The ID of the export task
   * @returns {Promise} Export task status
   */
  async checkStatus(taskId) {
    try {
      console.log('🔍 Checking export status:', taskId)
      
      // Check authentication token
      const token = localStorage.getItem('token')
      if (!token) {
        console.error('No authentication token found for status check')
        return {
          success: false,
          message: 'Authentication required. Please log in again.'
        }
      }
      
      const response = await api.get(`/api/exports/status/${taskId}`)
      
      console.log('📊 Export status:', response.data)
      
      return {
        success: true,
        data: response.data,
        message: 'Status retrieved successfully'
      }
    } catch (error) {
      console.error('❌ Status check error:', error)
      
      let errorMessage = 'Failed to check export status'
      if (error.response) {
        const status = error.response.status
        if (status === 401 || status === 422) {
          errorMessage = 'Authentication expired. Please log in again.'
        } else {
          errorMessage = `Server error (${status}): ${error.response.data?.message || 'Unknown server error'}`
        }
      } else if (error.message) {
        errorMessage = error.message
      }
      
      return {
        success: false,
        message: errorMessage,
        error: error.response?.data || error
      }
    }
  }

  /**
   * Download a completed export file
   * @param {string} filename - The name of the export file
   * @returns {Promise} Export file download
   */
  async downloadExport(filename) {
    try {
      console.log('📥 Downloading export:', filename)
      
      // Check authentication token
      const token = localStorage.getItem('token')
      if (!token) {
        console.error('No authentication token found for download')
        return {
          success: false,
          message: 'Authentication required. Please log in again.'
        }
      }
      
      const response = await api.get(`/api/exports/download/${filename}`, {
        responseType: 'blob'
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      
      console.log('✅ Export downloaded successfully')
      
      return {
        success: true,
        message: 'Export downloaded successfully'
      }
    } catch (error) {
      console.error('❌ Download error:', error)
      
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to download export',
        error: error.response?.data
      }
    }
  }
}

export default new ExportService() 