import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'

import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import Feedback from './views/Feedback.vue'
import Services from './views/Services.vue'
import Subscribers from './views/Subscribers.vue'

// Import styles
import './assets/styles/main.css'

// Create Vue app
const app = createApp(App)

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard, name: 'Dashboard' },
    { path: '/feedback', component: Feedback, name: 'Feedback' },
    { path: '/services', component: Services, name: 'Services' },
    { path: '/subscribers', component: Subscribers, name: 'Subscribers' }
  ]
})

// Create Pinia store
const pinia = createPinia()

// Use plugins
app.use(router)
app.use(pinia)

// Mount app
app.mount('#app')