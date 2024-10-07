<!-- src/components/Home.vue -->
<template>
    <div class="home">
      <h1>Movie App</h1>
      <div v-if="isAuthenticated">
        <router-link to="/dashboard">Dashboard</router-link>
        <a @click="logout">Logout</a>
      </div>
      <div v-else>
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
      </div>
      
      <main>
        <h2>New Movies</h2>
        <div class="movie-grid">
          <div v-for="movie in movies" :key="movie.id" class="movie-card">
            <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" :alt="movie.title">
            <div class="movie-info">
              <h3>{{ movie.title }}</h3>
              <p>Release Date: {{ movie.release_date }}</p>
              <p>Rating: {{ movie.vote_average }}/10</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Home',
    data() {
      return {
        movies: [],
        isAuthenticated: false,
      };
    },
    mounted() {
      this.fetchMovies();
      this.checkAuth();
    },
    methods: {
      async fetchMovies() {
        try {
          const response = await axios.get('/api/movies/new');
          this.movies = response.data.results;
        } catch (error) {
          console.error('Error fetching movies:', error);
        }
      },
      async checkAuth() {
        // Implement authentication check
      },
      async logout() {
        // Implement logout functionality
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>