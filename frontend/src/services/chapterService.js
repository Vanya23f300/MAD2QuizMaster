import apiClient from './api';

const chapterService = {
  async getChapters(subjectId = null) {
    try {
      const params = subjectId ? { subject_id: subjectId } : {};
      console.log('🚀 Fetching Chapters with params:', params);
      
      const response = await apiClient.get('/chapters', { params });
      
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

  async createChapter(chapterData) {
    try {
      const response = await apiClient.post('/chapters', chapterData);
      return response.data;
    } catch (error) {
      console.error('Error creating chapter:', error.response || error);
      throw error;
    }
  },

  async updateChapter(chapterId, chapterData) {
    try {
      const response = await apiClient.put(`/chapters/${chapterId}`, chapterData);
      return response.data;
    } catch (error) {
      console.error('Error updating chapter:', error.response || error);
      throw error;
    }
  },

  async deleteChapter(chapterId) {
    try {
      const response = await apiClient.delete(`/chapters/${chapterId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting chapter:', error.response || error);
      throw error;
    }
  }
};

export default chapterService; 