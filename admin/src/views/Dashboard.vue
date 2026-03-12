<template>
  <div class="dashboard">
    <div class="container">
      <div class="dashboard-header">
        <h1>Панель управления</h1>
        <p>Добро пожаловать в админку 33 Зуб</p>
      </div>

      <div class="dashboard-grid">
        <div class="card">
          <div class="card-icon">
            <i class="fas fa-comments"></i>
          </div>
          <div class="card-content">
            <h3>Сообщения</h3>
            <p>{{ feedbackStats.total }} всего</p>
            <p class="status-new">{{ feedbackStats.new }} новых</p>
          </div>
          <router-link to="/feedback" class="card-link">Перейти</router-link>
        </div>

        <div class="card">
          <div class="card-icon">
            <i class="fas fa-tooth"></i>
          </div>
          <div class="card-content">
            <h3>Услуги</h3>
            <p>{{ servicesStats.total }} активных</p>
            <p class="status-info">{{ servicesStats.inactive }} неактивных</p>
          </div>
          <router-link to="/services" class="card-link">Перейти</router-link>
        </div>

        <div class="card">
          <div class="card-icon">
            <i class="fas fa-envelope"></i>
          </div>
          <div class="card-content">
            <h3>Подписчики</h3>
            <p>{{ subscribersStats.total }} всего</p>
            <p class="status-active">{{ subscribersStats.active }} активных</p>
          </div>
          <router-link to="/subscribers" class="card-link">Перейти</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { feedbackService, subscriberService } from '../services'

export default {
  name: 'Dashboard',
  data() {
    return {
      feedbackStats: {
        total: 0,
        new: 0
      },
      servicesStats: {
        total: 0,
        inactive: 0
      },
      subscribersStats: {
        total: 0,
        active: 0
      }
    }
  },
  async mounted() {
    await this.loadStats()
  },
  methods: {
    async loadStats() {
      try {
        // Load feedback stats
        const feedbackResponse = await feedbackService.getFeedbacks()
        this.feedbackStats.total = feedbackResponse.length
        this.feedbackStats.new = feedbackResponse.filter(f => f.status === 'new').length

        // Load services stats (mock data for now)
        this.servicesStats.total = 5
        this.servicesStats.inactive = 1

        // Load subscribers stats
        // Note: We would need to add endpoint to get subscribers count
        this.subscribersStats.total = 150
        this.subscribersStats.active = 120
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 40px 0;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 40px;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #333;
}

.dashboard-header p {
  font-size: 1.2rem;
  color: #666;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: relative;
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}

.card-icon {
  position: absolute;
  top: -20px;
  right: 30px;
  width: 60px;
  height: 60px;
  background: #007bff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.card-content h3 {
  margin-bottom: 10px;
  color: #333;
}

.card-content p {
  margin-bottom: 5px;
  color: #666;
}

.status-new {
  color: #dc3545;
  font-weight: bold;
}

.status-active {
  color: #28a745;
  font-weight: bold;
}

.status-info {
  color: #17a2b8;
  font-weight: bold;
}

.card-link {
  position: absolute;
  bottom: 20px;
  right: 30px;
  background: #007bff;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.3s;
}

.card-link:hover {
  background: #0056b3;
}

@media (max-width: 768px) {
  .dashboard-header h1 {
    font-size: 2rem;
  }
  
  .card {
    padding: 20px;
  }
}
</style>