<template>
  <div class="feedback">
    <div class="container">
      <div class="page-header">
        <h1>Сообщения</h1>
        <div class="header-actions">
          <button @click="refreshData" class="btn btn-secondary">
            <i class="fas fa-refresh"></i> Обновить
          </button>
        </div>
      </div>

      <div class="filters">
        <div class="filter-group">
          <label>Статус:</label>
          <select v-model="filters.status" @change="loadFeedbacks">
            <option value="">Все</option>
            <option value="new">Новые</option>
            <option value="in_progress">В работе</option>
            <option value="completed">Завершенные</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Поиск:</label>
          <input 
            type="text" 
            v-model="filters.search" 
            placeholder="Поиск по имени или email..."
            @input="debouncedSearch"
          >
        </div>
      </div>

      <div class="table-container">
        <table class="feedback-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Имя</th>
              <th>Email</th>
              <th>Тема</th>
              <th>Статус</th>
              <th>Дата</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="feedback in feedbacks" :key="feedback.id">
              <td>{{ feedback.id }}</td>
              <td>{{ feedback.name }}</td>
              <td>{{ feedback.email }}</td>
              <td>{{ feedback.subject || 'Без темы' }}</td>
              <td>
                <span :class="['status-badge', feedback.status]">
                  {{ getStatusLabel(feedback.status) }}
                </span>
              </td>
              <td>{{ formatDate(feedback.created_at) }}</td>
              <td>
                <button @click="openModal(feedback)" class="btn btn-secondary btn-sm">
                  <i class="fas fa-eye"></i> Просмотр
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal -->
      <div v-if="selectedFeedback" class="modal-overlay" @click="closeModal">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>Сообщение от {{ selectedFeedback.name }}</h3>
            <button @click="closeModal" class="modal-close">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div class="modal-field">
              <label>Email:</label>
              <p>{{ selectedFeedback.email }}</p>
            </div>
            <div class="modal-field">
              <label>Телефон:</label>
              <p>{{ selectedFeedback.phone || 'Не указан' }}</p>
            </div>
            <div class="modal-field">
              <label>Тема:</label>
              <p>{{ selectedFeedback.subject || 'Без темы' }}</p>
            </div>
            <div class="modal-field">
              <label>Сообщение:</label>
              <p class="message-text">{{ selectedFeedback.message }}</p>
            </div>
            <div class="modal-field">
              <label>Статус:</label>
              <select v-model="selectedFeedback.status" @change="updateFeedbackStatus">
                <option value="new">Новый</option>
                <option value="in_progress">В работе</option>
                <option value="completed">Завершен</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeModal" class="btn btn-secondary">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { feedbackService } from '../services'
import { debounce } from 'lodash'

export default {
  name: 'Feedback',
  data() {
    return {
      feedbacks: [],
      selectedFeedback: null,
      filters: {
        status: '',
        search: ''
      },
      isLoading: false
    }
  },
  async mounted() {
    await this.loadFeedbacks()
  },
  methods: {
    async loadFeedbacks() {
      try {
        this.isLoading = true
        const response = await feedbackService.getFeedbacks()
        this.feedbacks = response
      } catch (error) {
        console.error('Error loading feedbacks:', error)
      } finally {
        this.isLoading = false
      }
    },

    async updateFeedbackStatus() {
      if (!this.selectedFeedback) return
      
      try {
        await feedbackService.updateFeedback(this.selectedFeedback.id, {
          status: this.selectedFeedback.status
        })
        // Update local state
        const index = this.feedbacks.findIndex(f => f.id === this.selectedFeedback.id)
        if (index !== -1) {
          this.feedbacks[index].status = this.selectedFeedback.status
        }
      } catch (error) {
        console.error('Error updating feedback status:', error)
      }
    },

    openModal(feedback) {
      this.selectedFeedback = { ...feedback }
    },

    closeModal() {
      this.selectedFeedback = null
    },

    refreshData() {
      this.loadFeedbacks()
    },

    getStatusLabel(status) {
      const labels = {
        'new': 'Новый',
        'in_progress': 'В работе',
        'completed': 'Завершен'
      }
      return labels[status] || status
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU')
    }
  },
  created() {
    this.debouncedSearch = debounce(() => {
      this.loadFeedbacks()
    }, 300)
  }
}
</script>

<style scoped>
.feedback {
  padding: 40px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0;
  color: #333;
}

.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-weight: 500;
  color: #666;
}

.filter-group select,
.filter-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.feedback-table {
  width: 100%;
  border-collapse: collapse;
}

.feedback-table th,
.feedback-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.feedback-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #333;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.new {
  background: #fff5f5;
  color: #dc3545;
  border: 1px solid #f8d7da;
}

.status-badge.in_progress {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.status-badge.completed {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.9rem;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 600px;
  max-width: 90vw;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.3s;
}

.modal-close:hover {
  background: #eee;
}

.modal-body {
  padding: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.modal-field {
  margin-bottom: 20px;
}

.modal-field label {
  display: block;
  font-weight: 500;
  margin-bottom: 5px;
  color: #666;
}

.modal-field p {
  margin: 0;
  color: #333;
}

.message-text {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  border-left: 4px solid #007bff;
  white-space: pre-wrap;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .feedback-table {
    font-size: 0.9rem;
  }
  
  .feedback-table th,
  .feedback-table td {
    padding: 10px 5px;
  }
  
  .modal {
    width: 95vw;
  }
}
</style>