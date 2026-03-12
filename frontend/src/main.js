import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'

import App from './App.vue'
import Home from './views/Home.vue'
import Contact from './views/Contact.vue'

// Import styles
import './assets/styles/main.css'

// Create Vue app
const app = createApp(App)

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home, name: 'Home' },
    { path: '/contact', component: Contact, name: 'Contact' }
  ]
})

// Create Pinia store
const pinia = createPinia()

// Use plugins
app.use(router)
app.use(pinia)

// Mount app
app.mount('#app')