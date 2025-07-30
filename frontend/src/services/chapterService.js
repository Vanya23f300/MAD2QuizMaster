import apiClient from './api';

const chapterService = {
  async getChapters(subjectId = null) {
    try {
      const params = subjectId ? { subject_id: subjectId } : {};
      console.log('🚀 Fetching Chapters with params:', params);
      
      const response = await apiClient.get('/api/chapters', { params });
      
      console.log('📡 API Response:', {
        status: response.status,
        data: response.data,
        headers: response.headers
      });
      
      return response.data;
    } catch (error) {
      console.error('❌ Error fetching chapters:', {
        response: error.response,
        request: error.request,
        message: error.message
      });
      throw error;
    }
  },
  
  async getChaptersBySubject(subjectId) {
    try {
      const response = await apiClient.get(`/api/subjects/${subjectId}/chapters`);
      return {
        success: true,
        data: response.data,
        message: 'Chapters retrieved successfully'
      };
    } catch (error) {
      console.error('Error fetching chapters by subject:', error.response || error);
      return {
        success: false,
        message: error.response?.data?.message || 'Failed to retrieve chapters',
        data: []
      };
    }
  },

  async createChapter(chapterData) {
    try {
      const response = await apiClient.post('/api/chapters', chapterData);
      return response.data;
    } catch (error) {
      console.error('Error creating chapter:', error.response || error);
      throw error;
    }
  },

  async updateChapter(chapterId, chapterData) {
    try {
      const response = await apiClient.put(`/api/chapters/${chapterId}`, chapterData);
      return response.data;
    } catch (error) {
      console.error('Error updating chapter:', error.response || error);
      throw error;
    }
  },

  async deleteChapter(chapterId) {
    try {
      const response = await apiClient.delete(`/api/chapters/${chapterId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting chapter:', error.response || error);
      throw error;
    }
  }
};

export default chapterService; 