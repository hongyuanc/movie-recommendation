<!-- src/App.vue -->
<template>
  <div id="app">
    <h1>Movie Recommendation App</h1>
    <nav>
      <router-link to="/" v-if="!isLoggedIn">Home</router-link> |
      <router-link to="/login" v-if="!isLoggedIn">Login</router-link>
      <button v-else @click="logout">Logout</button>
    </nav>

    <router-view @login-success="handleLoginSuccess"></router-view>

    <div v-if="$route.path === '/'">
      <MovieDashboard />
      <UserDashboard v-if="isLoggedIn" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MovieDashboard from '@/components/MovieDashboard.vue'
import UserDashboard from '@/components/UserDashboard.vue'

export default {
  name: 'App',
  mounted() {
    console.log("app component mounted (App.vue)")
    console.log("current route(app.vue)", this.$route)
    console.log("router object (app.vue):", this.$router)
  },
  components: {
    MovieDashboard,
    UserDashboard
  },
  setup() {
    const isLoggedIn = ref(false)
    const router = useRouter()

    onMounted(() => {
      const token = localStorage.getItem('token')
      if (token) {
        isLoggedIn.value = true
      }
    })

    const logout = () => {
      localStorage.removeItem('token')
      isLoggedIn.value = false
      router.push('/login')
    }

    const handleLoginSuccess = () => {
      isLoggedIn.value = true
      router.push('/')
    }

    return {
      isLoggedIn,
      logout,
      handleLoginSuccess
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>