
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
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
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboardView.vue')
  },
  {
    path: '/user',
    name: 'UserDashboard',
    component: () => import('../views/UserDashboardView.vue')
  },
  // User Quiz Routes
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
  // User Analytics Routes
  {
    path: '/user/scores',
    name: 'UserScores',
    component: () => import('../views/user/ScoresView.vue')
  },
  // Admin CRUD Management Routes
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
    path: '/admin/questions',
    name: 'AdminQuestions',
    component: () => import('../views/admin/QuestionsView.vue')
  },
  {
    path: '/admin/quizzes',
    name: 'AdminQuizzes',
    component: () => import('../views/admin/QuizzesView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 