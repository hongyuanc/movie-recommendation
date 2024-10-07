<!-- src/components/MovieDashboard.vue -->
<template>
  <div class="movie-dashboard">
    <h2>New Movies</h2>
    <div v-if="loading">Loading movies...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else class="movie-grid">
      <div v-for="movie in movies" :key="movie.id" class="movie-card">
        <img :src="getImageUrl(movie.poster_path)" :alt="movie.title">
        <h3>{{ movie.title }}</h3>
        <p>Release Date: {{ movie.release_date }}</p>
        <p>Rating: {{ movie.vote_average }}/10</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '@/api/config'

export default {
  name: 'MovieDashboard',
  setup() {
    const movies = ref([])
    const loading = ref(true)
    const error = ref(null)

    const fetchMovies = async () => {
      try {
        const response = await api.get('/api/movies/new')
        movies.value = response.data.results
        loading.value = false
      } catch (err) {
        console.error('Error fetching movies:', err)
        error.value = 'Failed to fetch movies: ' + (err.response?.data?.message || err.message)
        loading.value = false
      }
    }

    const getImageUrl = (path) => {
      return `https://image.tmdb.org/t/p/w500${path}`
    }

    onMounted(fetchMovies)

    return {
      movies,
      loading,
      error,
      getImageUrl
    }
  }
}
</script>

<style scoped>
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}
.movie-card {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}
.movie-card img {
  max-width: 100%;
  height: auto;
}
</style>