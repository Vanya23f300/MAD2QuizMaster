<template>
  <div class="user-dashboard">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-lg-3 col-md-4">
        <BaseSidebar user-role="user" />
      </div>
      
      <!-- Main Content -->
      <div class="col-lg-9 col-md-8">
        <div class="container-fluid p-4">
          <!-- Header -->
          <div class="mb-4">
            <div class="d-flex align-items-center gap-3 mb-2">
              <button 
                class="btn btn-outline-light d-flex align-items-center gap-2"
                @click="goBack"
              >
                <i class="bi bi-arrow-left"></i>
                Back
              </button>
              <h1 class="text-light mb-0">User Dashboard</h1>
            </div>
            <p class="text-secondary">Take quizzes and track your progress</p>
          </div>

          <!-- Basic Stats -->
          <div class="row mb-4">
            <div class="col-md-4 mb-3">
              <div class="card glass text-center p-3">
                <h5 class="text-light">Quizzes Taken</h5>
                <h3 class="text-primary">{{ stats.totalQuizzes }}</h3>
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <div class="card glass text-center p-3">
                <h5 class="text-light">Average Score</h5>
                <h3 class="text-success">{{ stats.averageScore }}%</h3>
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <div class="card glass text-center p-3">
                <h5 class="text-light">Best Score</h5>
                <h3 class="text-warning">{{ stats.bestScore }}%</h3>
              </div>
            </div>
          </div>

          <!-- Available Quizzes -->
          <div class="card glass mb-4">
            <div class="card-header bg-transparent">
              <h5 class="text-light mb-0">Available Quizzes</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-6 col-lg-4 mb-3" v-for="quiz in availableQuizzes" :key="quiz.id">
                  <div class="card glass">
                    <div class="card-body">
                      <h6 class="text-light">{{ quiz.title }}</h6>
                      <p class="text-muted small">{{ quiz.subject }} • {{ quiz.duration }} mins</p>
                      <p class="text-secondary small">{{ quiz.questions }} questions</p>
                      <button class="btn btn-primary btn-sm w-100" @click="startQuiz(quiz.id)">
                        Start Quiz
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Scores -->
          <div class="card glass">
            <div class="card-header bg-transparent">
              <h5 class="text-light mb-0">Recent Quiz Results</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-dark">
                  <thead>
                    <tr>
                      <th>Quiz</th>
                      <th>Subject</th>
                      <th>Date</th>
                      <th>Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="score in recentScores" :key="score.id">
                      <td>{{ score.quizName }}</td>
                      <td>{{ score.subject }}</td>
                      <td>{{ formatDate(score.date) }}</td>
                      <td>
                        <span class="badge" :class="getScoreBadgeClass(score.percentage)">
                          {{ score.percentage }}%
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseSidebar from '../components/BaseSidebar.vue'

export default {
  name: 'UserDashboardView',
  components: {
    BaseSidebar
  },
  data() {
    return {
      stats: {
        totalQuizzes: 12,
        averageScore: 78,
        bestScore: 95
      },
      availableQuizzes: [
        {
          id: 1,
          title: 'Vue.js Fundamentals',
          subject: 'Web Development',
          duration: 30,
          questions: 15
        },
        {
          id: 2,
          title: 'JavaScript ES6',
          subject: 'Programming',
          duration: 25,
          questions: 12
        },
        {
          id: 3,
          title: 'HTML & CSS',
          subject: 'Web Development',
          duration: 20,
          questions: 10
        },
        {
          id: 4,
          title: 'Database Basics',
          subject: 'Database',
          duration: 40,
          questions: 20
        }
      ],
      recentScores: [
        {
          id: 1,
          quizName: 'Vue.js Basics',
          subject: 'Web Development',
          date: '2024-01-15',
          percentage: 85
        },
        {
          id: 2,
          quizName: 'JavaScript ES6',
          subject: 'Programming',
          date: '2024-01-14',
          percentage: 92
        },
        {
          id: 3,
          quizName: 'HTML & CSS',
          subject: 'Web Development',
          date: '2024-01-12',
          percentage: 78
        }
      ]
    }
  },
  methods: {
    startQuiz(quizId) {
      this.$router.push(`/quiz/${quizId}/take`)
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    getScoreBadgeClass(percentage) {
      if (percentage >= 90) return 'bg-success'
      if (percentage >= 75) return 'bg-primary'
      if (percentage >= 60) return 'bg-warning'
      return 'bg-danger'
    },
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.user-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #181A1B 0%, #23272B 100%);
  padding-top: 2rem;
}

.card.glass {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.card-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.table-dark {
  background: transparent;
}

.table-dark td, .table-dark th {
  border-color: rgba(255, 255, 255, 0.1);
}
</style> 