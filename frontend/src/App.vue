<template>
  <div id="app">
    <h1>Movie Recommendation App</h1>
    <button @click="getRecommendations">Get Recommendations</button>
    <ul v-if="recommendations.length">
      <li v-for="movie in recommendations" :key="movie">{{ movie }}</li>
    </ul>
    <div>
      <input v-model="chatMessage" placeholder="Ask about movies...">
      <button @click="sendChatMessage">Send</button>
      <p v-if="chatResponse">{{ chatResponse }}</p>
    </div>
    <div v-if="dashboardData">
      <h2>User Dashboard</h2>
      <p>User: {{ dashboardData.user }}</p>
      <p>Watched Movies: {{ dashboardData.watched_movies }}</p>
      <p>Favorite Genre: {{ dashboardData.favorite_genre }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      recommendations: [],
      chatMessage: '',
      chatResponse: '',
      dashboardData: null
    }
  },
  methods: {
    async getRecommendations() {
      try {
        const response = await axios.get('/api/movies/recommend')
        this.recommendations = response.data.recommendations
      } catch (error) {
        console.error('Error fetching recommendations:', error)
      }
    },
    async sendChatMessage() {
      try {
        const response = await axios.post('/api/chatbot', { message: this.chatMessage })
        this.chatResponse = response.data.response
        this.chatMessage = ''
      } catch (error) {
        console.error('Error sending chat message:', error)
      }
    },
    async getDashboardData() {
      try {
        const response = await axios.get('/api/user/dashboard')
        this.dashboardData = response.data
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      }
    }
  },
  mounted() {
    this.getDashboardData()
  }
}
</script>