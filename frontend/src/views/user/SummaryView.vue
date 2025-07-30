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

          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3"></div>
            <p class="text-light">Loading your performance data...</p>
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="alert alert-danger glass-alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ error }}
          </div>
          
          <!-- Empty State -->
          <div v-else-if="recentScores.length === 0" class="empty-state text-center py-5">
            <i class="bi bi-graph-up display-1 text-light mb-3"></i>
            <h4 class="text-light">No Quiz Results Yet</h4>
            <p class="text-light">
              Start taking quizzes to see your performance charts and summary data!
            </p>
            <button class="btn btn-primary mt-3" @click="goBack">
              <i class="bi bi-play-circle me-2"></i>
              Go to Dashboard
            </button>
          </div>

          <!-- Leaderboard Chart -->
          <div v-else class="row mb-4">
            <div class="col-12">
              <div class="card glass p-4">
                <h5 class="text-light mb-3">Class Performance Ranking</h5>
                
                <p class="text-light small mb-3">
                  This chart shows how you compare to other students. Your bar is highlighted in blue. 
                  Hover over any bar to see detailed metrics. All data is anonymous.
                </p>
                <div style="height: 400px;">
                  <ChartComponent
                    type="bar"
                    :data="leaderboardChartData"
                    :options="leaderboardChartOptions"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Performance Chart -->
          <div v-if="!loading && !error && recentScores.length > 0" class="row mb-4">
            <div class="col-12">
              <div class="card glass p-4">
                <h5 class="text-light mb-3">Your Performance Over Time</h5>
                <div style="height: 400px;">
                  <ChartComponent
                    type="line"
                    :data="chartData"
                    :options="chartOptions"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Scores Table -->
          <div v-if="!loading && !error && recentScores.length > 0" class="card glass p-3">
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
import ChartComponent from '../../components/ChartComponent.vue'
import ScoreService from '@/services/score-service'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'SummaryView',
  components: {
    BaseSidebar,
    ChartComponent
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const error = ref(null)
    const recentScores = ref([])
    const leaderboardData = ref([])
    const currentUserId = ref(null)
    
    const chartData = ref({
      labels: [],
      datasets: [{
        label: 'Your Scores',
        data: [],
        borderColor: '#0d6efd',
        backgroundColor: 'rgba(13, 110, 253, 0.1)',
        borderWidth: 3,
        tension: 0.4,
        pointBackgroundColor: '#0d6efd',
        pointBorderColor: '#ffffff',
        pointRadius: 4,
        fill: {
          target: 'origin',
          above: 'rgba(13, 110, 253, 0.1)'
        }
      }]
    })
    
    // Leaderboard chart data
    const leaderboardChartData = computed(() => {
      // Extract data from leaderboardData
      const scores = leaderboardData.value.map(user => user.avg_score)
      const backgroundColor = leaderboardData.value.map(user => 
        user.isCurrentUser ? '#0d6efd' : 'rgba(255, 193, 7, 0.6)'
      )
      const borderColor = leaderboardData.value.map(user => 
        user.isCurrentUser ? '#0953c4' : '#d9a406'
      )
      
      // Use empty strings for labels to avoid "Student X" text
      const labels = leaderboardData.value.map(() => '')
      
      return {
        labels,
        datasets: [{
          label: '',  // Empty label to avoid legend issues
          data: scores,
          backgroundColor,
          borderColor,
          borderWidth: 1,
          borderRadius: 5,
          barPercentage: 0.6,
          categoryPercentage: 0.9,
          maxBarThickness: 50
        }]
      }
    })
    
    // Leaderboard chart options
    const leaderboardChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false // Explicitly disable the legend
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: 'rgba(255, 255, 255, 0.9)',
          bodyColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            title: function(context) {
              const user = leaderboardData.value[context[0].dataIndex];
              return user.isCurrentUser ? 'You' : `User #${user.rank}`;
            },
            label: function(context) {
              const user = leaderboardData.value[context.dataIndex];
              // Calculate percentile based on rank
              const totalUsers = leaderboardData.value.length;
              const percentile = Math.round(((totalUsers - user.rank + 1) / totalUsers) * 100);
              
              const lines = [
                `Score: ${user.avg_score}%`,
                `Percentile: ${percentile}%`,
                `Rank: ${user.rank} of ${totalUsers}`,
              ];
              
              if (user.isCurrentUser) {
                lines.unshift('👤 This is you');
              }
              
              return lines;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: 'Average Score (%)',
            color: '#f8f9fa',
            font: {
              size: 14
            }
          },
          ticks: {
            color: '#f8f9fa'
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Users',
            color: '#f8f9fa',
            font: {
              size: 14
            }
          },
          ticks: {
            color: '#f8f9fa',
            callback: function(value, index) {
              // Only mark the current user
              const user = leaderboardData.value[index];
              return user.isCurrentUser ? '👤' : '';
            }
          },
          grid: {
            display: false
          }
        }
      },
      // Remove all event handlers to prevent errors
      events: []
    }
    
    // Performance chart options
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false  // Explicitly disable the legend
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: 'rgba(255, 255, 255, 0.8)',
          bodyColor: 'rgba(255, 255, 255, 0.8)',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          padding: 10
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
      },
      // Remove all event handlers to prevent errors
      events: []
    }

    const fetchUserPerformance = async () => {
      loading.value = true
      error.value = null
      
      try {
        // Get current user ID
        const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
        currentUserId.value = storedUser.id
        
        // Get user performance summary
        const response = await ScoreService.getUserPerformanceSummary()
        
        if (response.success && response.data) {
          // Process recent scores for table
          if (response.data.scores && response.data.scores.length > 0) {
            recentScores.value = response.data.scores.map(score => ({
              id: score.id,
              quizName: score.quiz_name || `Quiz ${score.quiz_id}`,
              subject: score.subject_name || '',
              date: score.time_stamp_of_attempt,
              percentage: Math.round(score.percentage) || 0
            }))
            
            // Update chart data
            chartData.value.labels = response.data.scores.map(score => score.quiz_name || `Quiz ${score.quiz_id}`)
            chartData.value.datasets[0].data = response.data.scores.map(score => Math.round(score.percentage) || 0)
            
            console.log('✅ Performance data processed:', recentScores.value)
          } else {
            console.log('No scores data found')
            // Show empty data state
            chartData.value.labels = []
            chartData.value.datasets[0].data = []
            recentScores.value = []
          }
        } else {
          console.log('No performance data found, showing empty chart/table')
          // Show empty data state
          chartData.value.labels = []
          chartData.value.datasets[0].data = []
          recentScores.value = []
          
          // Set error only if API returned an error
          if (!response.success) {
            error.value = response.message
          }
        }
        
        // Fetch leaderboard data
        await fetchLeaderboardData()
      } catch (err) {
        console.error('❌ Failed to fetch performance data:', err)
        error.value = 'Failed to load performance data. Please try again later.'
      } finally {
        loading.value = false
      }
    }
    
    const fetchLeaderboardData = async () => {
      try {
        const response = await ScoreService.getLeaderboardData()
        
        if (response.success && response.data) {
          // Process leaderboard data
          leaderboardData.value = response.data
          console.log('✅ Leaderboard data processed:', leaderboardData.value)
        } else {
          console.log('No leaderboard data found')
          leaderboardData.value = []
        }
      } catch (err) {
        console.error('❌ Failed to fetch leaderboard data:', err)
        // Don't set the main error since the performance data might still load
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    }
    
    const getScoreBadgeClass = (percentage) => {
      if (percentage >= 90) return 'bg-success'
      if (percentage >= 75) return 'bg-primary'
      if (percentage >= 60) return 'bg-warning'
      return 'bg-danger'
    }
    
    const goBack = () => {
      router.go(-1)
    }
    
    onMounted(() => {
      fetchUserPerformance()
    })
    
    return {
      loading,
      error,
      chartData,
      chartOptions,
      recentScores,
      formatDate,
      getScoreBadgeClass,
      goBack,
      leaderboardChartData,
      leaderboardChartOptions
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

.card.glass, .empty-state {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.glass-alert {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
}

.table-dark {
  background: transparent;
}

.table-dark td, .table-dark th {
  border-color: rgba(255, 255, 255, 0.1);
}

/* Chart specific styles */
:deep(.chartjs-tooltip) {
  opacity: 1;
  position: absolute;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  border-radius: 6px;
  padding: 10px;
  pointer-events: none;
  transform: translate(-50%, 0);
  transition: all .3s ease;
  z-index: 10;
}

:deep(.chartjs-render-monitor) {
  animation: chartFadeIn 0.5s;
}

@keyframes chartFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style> 