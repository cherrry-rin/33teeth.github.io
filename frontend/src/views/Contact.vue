<template>
  <div class="contact">
    <div class="container">
      <div class="title-wrap">
        <h1>Контакты</h1>
        <p>Вы можете задать вопросы или записаться на приём</p>
      </div>

      <div class="contact-content">
        <div class="contact-info">
          <div class="contact-card">
            <h3>Наши контакты</h3>
            <div class="contact-item">
              <span class="contact-icon">
                <i class="fas fa-phone-alt"></i>
              </span>
              <div>
                <span>Телефон</span>
                <p class="text">+7 (4922) 33-71-00</p>
              </div>
            </div>
            <div class="contact-item">
              <span class="contact-icon">
                <i class="fas fa-map-marked-alt"></i>
              </span>
              <div>
                <span>Адрес</span>
                <p class="text">г. Владимир, пр-т Строителей, 44Б, 600028</p>
              </div>
            </div>
            <div class="contact-item">
              <span class="contact-icon">
                <i class="fas fa-envelope"></i>
              </span>
              <div>
                <span>Почта</span>
                <p class="text">s3164.stomatlg.ru</p>
              </div>
            </div>
          </div>
        </div>

        <div class="contact-form">
          <h3>Оставить сообщение</h3>
          <form @submit.prevent="submitFeedback">
            <div class="form-row">
              <div class="form-group">
                <input 
                  type="text" 
                  v-model="feedbackForm.name" 
                  placeholder="Ваше имя" 
                  required
                >
              </div>
              <div class="form-group">
                <input 
                  type="email" 
                  v-model="feedbackForm.email" 
                  placeholder="Email" 
                  required
                >
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <input 
                  type="tel" 
                  v-model="feedbackForm.phone" 
                  placeholder="Телефон"
                >
              </div>
              <div class="form-group">
                <input 
                  type="text" 
                  v-model="feedbackForm.subject" 
                  placeholder="Тема сообщения"
                >
              </div>
            </div>
            <div class="form-group">
              <textarea 
                v-model="feedbackForm.message" 
                placeholder="Ваше сообщение" 
                rows="6" 
                required
              ></textarea>
            </div>
            <button type="submit" class="btn" :disabled="isSubmitting">
              {{ isSubmitting ? 'Отправка...' : 'Отправить сообщение' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { feedbackService } from '../services'

export default {
  name: 'Contact',
  data() {
    return {
      feedbackForm: {
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
      },
      isSubmitting: false
    }
  },
  methods: {
    async submitFeedback() {
      if (this.isSubmitting) return
      
      this.isSubmitting = true
      try {
        await feedbackService.createFeedback(this.feedbackForm)
        alert('Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.')
        this.feedbackForm = {
          name: '',
          email: '',
          phone: '',
          subject: '',
          message: ''
        }
      } catch (error) {
        console.error('Error submitting feedback:', error)
        alert('Ошибка при отправке сообщения. Попробуйте позже.')
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
.contact {
  padding: 80px 0;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.title-wrap {
  text-align: center;
  margin-bottom: 60px;
}

.title-wrap h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  color: #333;
}

.title-wrap p {
  font-size: 1.2rem;
  color: #666;
}

.contact-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.contact-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.contact-card h3 {
  margin-bottom: 30px;
  color: #333;
  font-size: 1.5rem;
}

.contact-item {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
}

.contact-icon {
  width: 50px;
  height: 50px;
  background: #007bff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 20px;
  font-size: 1.2rem;
}

.contact-item span {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.contact-item .text {
  font-size: 1.1rem;
  color: #333;
  margin: 0;
}

.contact-form {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.contact-form h3 {
  margin-bottom: 30px;
  color: #333;
  font-size: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

.btn {
  background: #007bff;
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.btn:hover:not(:disabled) {
  background: #0056b3;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .contact-content {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .title-wrap h1 {
    font-size: 2rem;
  }
}
</style>