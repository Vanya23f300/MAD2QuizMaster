import apiClient from './api';

const subjectService = {
  async getSubjects() {
    try {
      const response = await apiClient.get('/api/subjects');
      return response.data;
    } catch (error) {
      console.error('Error fetching subjects:', error.response || error);
      throw error;
    }
  },

  async createSubject(subjectData) {
    try {
      const response = await apiClient.post('/api/subjects', subjectData);
      return response.data;
    } catch (error) {
      console.error('Error creating subject:', error.response || error);
      throw error;
    }
  },

  // New method to fetch available subjects for students
  async getAvailableSubjects() {
    try {
      const response = await apiClient.get('/api/subjects/available');
      return response.data;
    } catch (error) {
      console.error('Error fetching available subjects:', error.response || error);
      throw error;
    }
  }
};

export default subjectService; 