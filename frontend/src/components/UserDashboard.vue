<!-- UserDashboard.vue -->
<template>
    <div class="user-dashboard">
      <h2>User Dashboard</h2>
      <p>User: {{ user.username }}</p>
      <p>Watched Movies: {{ user.watchedMovies }}</p>
      <p>Favorite Genre: {{ user.favoriteGenre }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserDashboard',
    data() {
      return {
        user: {
          username: '',
          watchedMovies: 0,
          favoriteGenre: ''
        }
      }
    },
    mounted() {
      this.fetchUserData();
    },
    methods: {
      async fetchUserData() {
        try {
          const response = await axios.get('/api/user/dashboard');
          this.user = response.data;
        } catch (error) {
          console.error('Error fetching user data:', error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .user-dashboard {
    border: 1px solid #ddd;
    padding: 20px;
    margin-top: 20px;
  }
  </style>