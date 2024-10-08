<template>
  <div class="login-view">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" type="text" placeholder="Username" required>
      <input v-model="password" type="password" placeholder="Password" required>
      <button type="submit">Login</button>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/config'

export default {
  name: 'LoginView',
  mounted(){
    console.log('LoginView component mounted');
  },
  emits: ['login-success'],
  setup(props, { emit }) {
    const username = ref('')
    const password = ref('')
    const error = ref('')
    const router = useRouter()

    const login = async () => {
      try {
        console.log('Attempting login...')
        const response = await api.post('/api/login', {
          username: username.value,
          password: password.value
        })
        console.log('Login response:', response)
        if (response.data.token) {
          localStorage.setItem('token', response.data.token)
          emit('login-success')
          router.push('/')
        } else {
          error.value = 'Login failed: No token received'
        }
      } catch (err) {
        console.error('Login error:', err)
        error.value = err.response?.data?.message || 'Login failed'
      }
    }

    return {
      username,
      password,
      error,
      login
    }
  }
}
</script>