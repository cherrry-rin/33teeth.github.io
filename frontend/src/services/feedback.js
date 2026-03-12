import api from './api'

export const feedbackService = {
  async createFeedback(feedbackData) {
    try {
      const response = await api.post('/feedback/', feedbackData)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async getFeedbacks() {
    try {
      const response = await api.get('/feedback/')
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async getFeedback(id) {
    try {
      const response = await api.get(`/feedback/${id}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async updateFeedback(id, feedbackData) {
    try {
      const response = await api.put(`/feedback/${id}`, feedbackData)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async deleteFeedback(id) {
    try {
      const response = await api.delete(`/feedback/${id}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}