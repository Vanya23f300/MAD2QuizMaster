import apiClient from './api';

const dashboardService = {
  async getDashboardStats() {
    try {
      const response = await apiClient.get('/api/dashboard/stats');
      return response.data;
    } catch (error) {
      console.error('Failed to retrieve dashboard stats:', error.response || error)
      throw error
    }
  },

  async getRecentActivities() {
    try {
      const response = await apiClient.get('/api/dashboard/recent-activities')
      return response.data
    } catch (error) {
      console.error('Failed to retrieve recent activities:', error.response || error)
      throw error
    }
  }
}

export default dashboardService 