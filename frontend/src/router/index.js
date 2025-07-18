
import { createRouter, createWebHistory } from 'vue-router'

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
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboardView.vue')
  },
  {
    path: '/admin/subjects',
    name: 'AdminSubjects',
    component: () => import('../views/admin/SubjectsView.vue')
  },
  {
    path: '/admin/chapters',
    name: 'AdminChapters',
    component: () => import('../views/admin/ChaptersView.vue')
  },
  {
    path: '/admin/quizzes',
    name: 'AdminQuizzes',
    component: () => import('../views/admin/QuizzesView.vue')
  },
  {
    path: '/admin/questions',
    name: 'AdminQuestions',
    component: () => import('../views/admin/QuestionsView.vue')
  },
  // User Routes
  {
    path: '/user',
    name: 'UserDashboard',
    component: () => import('../views/UserDashboardView.vue')
  },
  {
    path: '/quiz/:id/take',
    name: 'QuizTaking',
    component: () => import('../views/user/QuizTakingView.vue')
  },
  {
    path: '/quiz/:id/result',
    name: 'QuizResult',
    component: () => import('../views/user/QuizResultView.vue')
  },
  {
    path: '/user/scores',
    name: 'UserScores',
    component: () => import('../views/user/ScoresView.vue')
  },
  {
    path: '/user/summary',
    name: 'UserSummary',
    component: () => import('../views/user/SummaryView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 