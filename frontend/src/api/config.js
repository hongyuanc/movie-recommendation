// src/api/config.js
import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000'  // Make sure this matches your Flask server's address

const api = axios.create({
  baseURL: API_BASE_URL,
})

export default {
  get(url) {
    return api.get(url)
  },
  post(url, data) {
    return api.post(url, data)
  },
}