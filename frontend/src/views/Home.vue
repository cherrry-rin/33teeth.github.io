<template>
  <div class="home">
    <div class="hero">
      <div class="container">
        <div class="hero-content">
          <h1>Считаем зубы, дарим улыбки!</h1>
          <p>Стоматологические услуги от опытных специалистов</p>
        </div>
        
        <!-- Feedback Form in Hero Section -->
        <div class="feedback-form">
          <h3>Оставить отзыв</h3>
          <form @submit.prevent="submitFeedback">
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
                placeholder="Тема"
              >
            </div>
            <div class="form-group">
              <textarea 
                v-model="feedbackForm.message" 
                placeholder="Ваше сообщение" 
                rows="4" 
                required
              ></textarea>
            </div>
            <button type="submit" class="btn" :disabled="isSubmitting">
              {{ isSubmitting ? 'Отправка...' : 'Отправить' }}
            </button>
          </form>
        </div>
      </div>
    </div>

    <!-- Services Section -->
    <section class="services">
      <div class="container">
        <h2>Наши услуги</h2>
        <div class="services-grid">
          <div class="service-card" v-for="service in services" :key="service.id">
            <h3>{{ service.title }}</h3>
            <p>{{ service.description }}</p>
            <div class="service-meta">
              <span class="price">{{ service.price }} ₽</span>
              <span class="duration">{{ service.duration }} мин</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter Section -->
    <section class="newsletter">
      <div class="container">
        <h3>Подпишитесь на рассылку</h3>
        <form @submit.prevent="subscribeToNewsletter" class="newsletter-form">
          <input 
            type="email" 
            v-model="newsletterEmail" 
            placeholder="Введите ваш email" 
            required
          >
          <button type="submit" class="btn" :disabled="isSubscribing">
            {{ isSubscribing ? 'Подписка...' : 'Подписаться' }}
          </button>
        </form>
      </div>
    </section>
  </div>
</template>

<script>
import { feedbackService, subscriberService } from '../services'

export default {
  name: 'Home',
  data() {
    return {
      feedbackForm: {
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
      },
      newsletterEmail: '',
      isSubmitting: false,
      isSubscribing: false,
      services: [
        {
          id: 1,
          title: 'Консультация',
          description: 'Первичный осмотр и консультация стоматолога',
          price: 500,
          duration: 30
        },
        {
          id: 2,
          title: 'Ультразвуковая чистка',
          description: 'Профессиональная чистка зубов ультразвуком',
          price: 2000,
          duration: 45
        },
        {
          id: 3,
          title: 'Пломбирование',
          description: 'Лечение кариеса и установка пломбы',
          price: 1500,
          duration: 60
        }
      ]
    }
  },
  methods: {
    async submitFeedback() {
      if (this.isSubmitting) return
      
      this.isSubmitting = true
      try {
        await feedbackService.createFeedback(this.feedbackForm)
        alert('Спасибо за ваш отзыв!')
        this.feedbackForm = {
          name: '',
          email: '',
          phone: '',
          subject: '',
          message: ''
        }
      } catch (error) {
        console.error('Error submitting feedback:', error)
        alert('Ошибка при отправке отзыва. Попробуйте позже.')
      } finally {
        this.isSubmitting = false
      }
    },

    async subscribeToNewsletter() {
      if (this.isSubscribing) return
      
      this.isSubscribing = true
      try {
        await subscriberService.subscribe(this.newsletterEmail)
        alert('Вы успешно подписались на рассылку!')
        this.newsletterEmail = ''
      } catch (error) {
        console.error('Error subscribing:', error)
        alert('Ошибка при подписке. Возможно, вы уже подписаны.')
      } finally {
        this.isSubscribing = false
      }
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('/images/header-bg.jpg');
  background-size: cover;
  background-position: center;
  color: white;
  padding: 100px 0;
  text-align: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  color: #fff;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 40px;
}

.feedback-form {
  background: white;
  padding: 40px;
  border-radius: 8px;
  color: #333;
  max-width: 600px;
  margin: 0 auto;
}

.feedback-form h3 {
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
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

.services {
  padding: 80px 0;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.services h2 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2.5rem;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.service-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.service-card:hover {
  transform: translateY(-5px);
}

.service-card h3 {
  color: #333;
  margin-bottom: 15px;
}

.service-card p {
  color: #666;
  margin-bottom: 20px;
}

.service-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-weight: bold;
  color: #007bff;
  font-size: 1.2rem;
}

.duration {
  color: #666;
  font-size: 0.9rem;
}

.newsletter {
  background: #333;
  color: white;
  padding: 60px 0;
  text-align: center;
}

.newsletter h3 {
  margin-bottom: 30px;
  font-size: 1.5rem;
}

.newsletter-form {
  display: flex;
  max-width: 500px;
  margin: 0 auto;
  gap: 10px;
}

.newsletter-form input {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .feedback-form {
    padding: 20px;
  }
  
  .newsletter-form {
    flex-direction: column;
  }
}
</style>