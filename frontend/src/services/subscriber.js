import api from './api'

export const subscriberService = {
  async subscribe(email) {
    try {
      const response = await api.post('/subscriber/', { email })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async getSubscriber(email) {
    try {
      const response = await api.get(`/subscriber/${email}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  async unsubscribe(email) {
    try {
      const response = await api.delete(`/subscriber/${email}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}