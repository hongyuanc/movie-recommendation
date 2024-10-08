// src/main.js
console.log('Main.js is running');

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

console.log("Router imported:", router);

app.use(router)

app.mount('#app')

console.log('Vue app mounted')