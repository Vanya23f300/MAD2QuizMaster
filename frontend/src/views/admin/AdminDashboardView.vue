<template>
  <div class="admin-dashboard">
    <div class="page-header glass mb-4">
      <h1 class="text-light">
        <i class="bi bi-speedometer2 me-2"></i>
        Admin Dashboard
      </h1>
      <p class="text-light mb-0">Overview of platform statistics and performance</p>
    </div>

    <!-- Stats Overview -->
    <div class="row g-4 mb-4">
      <div class="col-md-3">
        <div class="stat-card glass">
          <div class="stat-icon">
            <i class="bi bi-people"></i>
          </div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.totalUsers || 0 }}</h3>
            <p class="stat-label">Total Users</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stat-card glass">
          <div class="stat-icon">
            <i class="bi bi-book"></i>
          </div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.totalQuizzes || 0 }}</h3>
            <p class="stat-label">Total Quizzes</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stat-card glass">
          <div class="stat-icon">
            <i class="bi bi-pencil-square"></i>
          </div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.totalAttempts || 0 }}</h3>
            <p class="stat-label">Quiz Attempts</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stat-card glass">
          <div class="stat-icon">
            <i class="bi bi-graph-up"></i>
          </div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.avgScore || 0 }}%</h3>
            <p class="stat-label">Avg. Score</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="row g-4">
      <!-- User Activity Chart -->
      <div class="col-md-8">
        <div class="chart-card glass">
          <ChartComponent
            type="line"
            title="User Activity"
            description="Daily active users and quiz attempts"
            :data="userActivityData"
            :options="userActivityOptions"
          />
        </div>
      </div>

      <!-- Subject Distribution Chart -->
      <div class="col-md-4">
        <div class="chart-card glass">
          <ChartComponent
            type="doughnut"
            title="Quiz Distribution"
            description="Quizzes by subject"
            :data="subjectDistributionData"
            :options="subjectDistributionOptions"
          />
        </div>
      </div>

      <!-- Performance Chart -->
      <div class="col-md-6">
        <div class="chart-card glass">
          <ChartComponent
            type="bar"
            title="Quiz Performance"
            description="Average scores by subject"
            :data="performanceData"
            :options="performanceOptions"
          />
        </div>
      </div>

      <!-- User Growth Chart -->
      <div class="col-md-6">
        <div class="chart-card glass">
          <ChartComponent
            type="line"
            title="User Growth"
            description="New user registrations over time"
            :data="userGrowthData"
            :options="userGrowthOptions"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ChartComponent from '@/components/ChartComponent.vue'

export default {
  name: 'AdminDashboardView',
  components: {
    ChartComponent
  },
  data() {
    return {
      stats: {
        totalUsers: 0,
        totalQuizzes: 0,
        totalAttempts: 0,
        avgScore: 0
      },
      userActivityData: {
        labels: [],
        datasets: [
          {
            label: 'Active Users',
            data: [],
            borderColor: '#24a35a',
            backgroundColor: 'rgba(36, 163, 90, 0.1)',
            fill: true
          },
          {
            label: 'Quiz Attempts',
            data: [],
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            fill: true
          }
        ]
      },
      subjectDistributionData: {
        labels: [],
        datasets: [{
          data: [],
          backgroundColor: [
            '#24a35a',
            '#3b82f6',
            '#8b5cf6',
            '#ec4899',
            '#f59e0b'
          ]
        }]
      },
      performanceData: {
        labels: [],
        datasets: [{
          label: 'Average Score',
          data: [],
          backgroundColor: '#24a35a'
        }]
      },
      userGrowthData: {
        labels: [],
        datasets: [{
          label: 'New Users',
          data: [],
          borderColor: '#24a35a',
          backgroundColor: 'rgba(36, 163, 90, 0.1)',
          fill: true
        }]
      }
    }
  },
  computed: {
    userActivityOptions() {
      return {
        plugins: {
          tooltip: {
            mode: 'index',
            intersect: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    },
    subjectDistributionOptions() {
      return {
        cutout: '60%',
        plugins: {
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.label || ''
                const value = context.parsed || 0
                const total = context.dataset.data.reduce((a, b) => a + b, 0)
                const percentage = ((value / total) * 100).toFixed(1)
                return `${label}: ${value} (${percentage}%)`
              }
            }
          }
        }
      }
    },
    performanceOptions() {
      return {
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    },
    userGrowthOptions() {
      return {
        plugins: {
          tooltip: {
            mode: 'index',
            intersect: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    }
  },
  methods: {
    async fetchDashboardData() {
      try {
        // Fetch overall stats
        const statsResponse = await this.$http.get('/api/dashboard/stats')
        this.stats = statsResponse.data

        // Fetch user activity data
        const activityResponse = await this.$http.get('/api/analytics/user-activity')
        const activity = activityResponse.data
        this.userActivityData.labels = activity.dates
        this.userActivityData.datasets[0].data = activity.activeUsers
        this.userActivityData.datasets[1].data = activity.quizAttempts

        // Fetch subject distribution
        const subjectsResponse = await this.$http.get('/api/analytics/subject-distribution')
        const subjects = subjectsResponse.data
        this.subjectDistributionData.labels = subjects.map(s => s.name)
        this.subjectDistributionData.datasets[0].data = subjects.map(s => s.quizCount)

        // Fetch performance data
        const performanceResponse = await this.$http.get('/api/analytics/subject-performance')
        const performance = performanceResponse.data
        this.performanceData.labels = performance.map(p => p.subject)
        this.performanceData.datasets[0].data = performance.map(p => p.avgScore)

        // Fetch user growth data
        const growthResponse = await this.$http.get('/api/analytics/user-growth')
        const growth = growthResponse.data
        this.userGrowthData.labels = growth.dates
        this.userGrowthData.datasets[0].data = growth.newUsers

      } catch (error) {
        console.error('Failed to fetch dashboard data:', error)
      }
    }
  },
  mounted() {
    this.fetchDashboardData()
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
}

.page-header {
  padding: 2rem;
  border-radius: 1rem;
}

.stat-card {
  padding: 1.5rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 1rem;
  background: rgba(36, 163, 90, 0.1);
  color: #24a35a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  margin: 0;
}

.stat-label {
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
  font-size: 0.875rem;
}

.chart-card {
  padding: 1.5rem;
  border-radius: 1rem;
  height: 100%;
}
</style> 