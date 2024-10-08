// src/router/index.js
console.log('Router file is being exceuted (index.js)')

import { createRouter, createWebHistory } from 'vue-router';
// import Home from '@/components/HomeMenu.vue';
import Dashboard from '@/components/MovieDashboard.vue';
import LoginView from '@/views/LoginView.vue';
// import Register from '@/views/RegisterView.vue';

const routes = [
  // {
  //   path: '/',
  //   name: 'Home',
  //   component: Home,
  // },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  // {
  //   path: '/register',
  //   name: 'Register',
  //   component: RegisterView,
  // },
];
console.log("routes defined (index.js):", routes)

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});
console.log("router created: (index.js)", router)

// Add navigation guard for protected routes
router.beforeEach((to, from, next) => {
  console.log('Navigation guard triggered, going to:', to.path);
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated()) {
      console.log('Authentication required, redirecting to login');
      next({ name: 'Login', query: { redirect: to.fullPath } });
    } else {
      console.log('User authenticated, proceeding to:', to.path);
      next();
    }
  } else {
    console.log('No authentication required, proceeding to:', to.path);
    next();
  }
});

function isAuthenticated() {
  const token = localStorage.getItem('token');
  return !!token;
}

console.log("end of index.js")

export default router;