import { createRouter, createWebHistory } from 'vue-router'
import AuthService from '../services/auth'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue')
  },
  // Admin Routes
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboardView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/admin/AdminUsersView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/subjects',
    name: 'AdminSubjects',
    component: () => import('../views/admin/SubjectsView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/chapters',
    name: 'AdminChapters',
    component: () => import('../views/admin/ChaptersView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/quizzes',
    name: 'AdminQuizzes',
    component: () => import('../views/admin/QuizzesView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/questions',
    name: 'AdminQuestions',
    component: () => import('../views/admin/QuestionsView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/quizzes/:quizId/questions',
    name: 'AdminQuizQuestions',
    component: () => import('../views/admin/QuestionsView.vue'),
    meta: { requiresAdmin: true }
  },
  // User Routes
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: () => import('../views/UserDashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/scores',
    name: 'UserScores',
    component: () => import('../views/user/ScoresView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/summary',
    name: 'UserSummary',
    component: () => import('../views/user/SummaryView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/quiz/:quizId',
    name: 'QuizTaking',
    component: () => import('../views/user/QuizTakingView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/quiz/:quizId/result',
    name: 'QuizResult',
    component: () => import('../views/user/QuizResultView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/profile',
    name: 'UserProfile',
    component: () => import('../views/user/UserProfileView.vue'),
    meta: { requiresAuth: true }
  },
  // Legacy redirects
  {
    path: '/admin',
    redirect: '/admin/dashboard'
  },
  {
    path: '/user',
    redirect: '/user/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)
  const isAuthenticated = AuthService.isAuthenticated()
  const isAdmin = AuthService.isAdmin()

  if (requiresAdmin) {
    if (!isAuthenticated || !isAdmin) {
      next('/login')
      return
    }
  } else if (requiresAuth) {
    if (!isAuthenticated) {
      next('/login')
      return
    }
  }

  next()
})

export default router