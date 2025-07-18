<template>
  <div class="summary-view">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-lg-3 col-md-4">
        <BaseSidebar user-role="user" />
      </div>
      
      <!-- Main Content -->
      <div class="col-lg-9 col-md-8">
        <div class="container-fluid p-4">
          <!-- Page Header -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div class="d-flex align-items-center gap-3">
              <button 
                class="btn btn-outline-light d-flex align-items-center gap-2"
                @click="goBack"
              >
                <i class="bi bi-arrow-left"></i>
                Back
              </button>
              <h2 class="text-light mb-0">Summary Charts</h2>
            </div>
          </div>

          <!-- Simple Performance Chart -->
          <div class="row mb-4">
            <div class="col-12">
              <div class="card glass p-4">
                <h5 class="text-light mb-3">Your Performance Over Time</h5>
                <canvas id="performanceChart" width="400" height="100"></canvas>
              </div>
            </div>
          </div>

          <!-- Recent Scores Table -->
          <div class="card glass p-3">
            <h5 class="text-light mb-3">Recent Quiz Results</h5>
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
</template>

<script>
import BaseSidebar from '../../components/BaseSidebar.vue'
import { Chart, registerables } from 'chart.js'

// Register Chart.js components
Chart.register(...registerables)

export default {
  name: 'SummaryView',
  components: {
    BaseSidebar
  },
  data() {
    return {
      chart: null,
      recentScores: [
        { id: 1, quizName: 'Vue.js Basics', subject: 'Web Development', date: '2024-01-15', percentage: 85 },
        { id: 2, quizName: 'JavaScript ES6', subject: 'Programming', date: '2024-01-14', percentage: 92 },
        { id: 3, quizName: 'HTML & CSS', subject: 'Web Development', date: '2024-01-12', percentage: 78 },
        { id: 4, quizName: 'Database Basics', subject: 'Database', date: '2024-01-10', percentage: 88 },
        { id: 5, quizName: 'Python Basics', subject: 'Programming', date: '2024-01-08', percentage: 76 }
      ]
    }
  },
  mounted() {
    this.createChart()
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy()
    }
  },
  methods: {
    createChart() {
      const ctx = document.getElementById('performanceChart').getContext('2d')
      
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Quiz 1', 'Quiz 2', 'Quiz 3', 'Quiz 4', 'Quiz 5'],
          datasets: [{
            label: 'Your Scores',
            data: [76, 88, 78, 92, 85],
            borderColor: '#0d6efd',
            backgroundColor: 'rgba(13, 110, 253, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: {
                color: '#f8f9fa'
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              ticks: {
                color: '#f8f9fa'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            },
            x: {
              ticks: {
                color: '#f8f9fa'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            }
          }
        }
      })
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
.summary-view {
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

.table-dark {
  background: transparent;
}

.table-dark td, .table-dark th {
  border-color: rgba(255, 255, 255, 0.1);
}

#performanceChart {
  height: 300px !important;
}
</style> 