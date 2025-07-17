<template>
  <div class="summary-view">
    <!-- Header Section -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="text-light mb-1">Performance Summary</h2>
        <p class="text-muted mb-0">Track your quiz performance and progress over time</p>
      </div>
      <div class="d-flex gap-2">
        <select v-model="selectedTimeRange" class="form-select glassmorphic" style="width: auto;">
          <option value="week">Last Week</option>
          <option value="month">Last Month</option>
          <option value="year">Last Year</option>
          <option value="all">All Time</option>
        </select>
      </div>
    </div>

    <!-- Key Metrics Cards -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card glassmorphic h-100">
          <div class="card-body text-center">
            <div class="metric-icon mb-2">
              <i class="bi bi-clipboard-check fs-1 text-primary"></i>
            </div>
            <h3 class="text-light mb-1">{{ metrics.totalQuizzes }}</h3>
            <p class="text-muted mb-0">Total Quizzes</p>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card glassmorphic h-100">
          <div class="card-body text-center">
            <div class="metric-icon mb-2">
              <i class="bi bi-graph-up fs-1 text-success"></i>
            </div>
            <h3 class="text-light mb-1">{{ metrics.averageScore }}%</h3>
            <p class="text-muted mb-0">Average Score</p>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card glassmorphic h-100">
          <div class="card-body text-center">
            <div class="metric-icon mb-2">
              <i class="bi bi-trophy fs-1 text-warning"></i>
            </div>
            <h3 class="text-light mb-1">{{ metrics.highestScore }}%</h3>
            <p class="text-muted mb-0">Best Score</p>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card glassmorphic h-100">
          <div class="card-body text-center">
            <div class="metric-icon mb-2">
              <i class="bi bi-trending-up fs-1 text-info"></i>
            </div>
            <h3 class="text-light mb-1">+{{ metrics.improvement }}%</h3>
            <p class="text-muted mb-0">Improvement</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="row">
      <!-- Performance Over Time Chart -->
      <div class="col-lg-8 mb-4">
        <div class="card glassmorphic h-100">
          <div class="card-header bg-transparent border-0">
            <h5 class="text-light mb-0">Performance Over Time</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas id="performanceChart" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Subject Performance Chart -->
      <div class="col-lg-4 mb-4">
        <div class="card glassmorphic h-100">
          <div class="card-header bg-transparent border-0">
            <h5 class="text-light mb-0">Subject Performance</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas id="subjectChart" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Quiz Attempts Distribution -->
      <div class="col-lg-6 mb-4">
        <div class="card glassmorphic h-100">
          <div class="card-header bg-transparent border-0">
            <h5 class="text-light mb-0">Quiz Attempts by Grade</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas id="gradeChart" height="250"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Performance Trends -->
      <div class="col-lg-6 mb-4">
        <div class="card glassmorphic h-100">
          <div class="card-header bg-transparent border-0">
            <h5 class="text-light mb-0">Recent Trends</h5>
          </div>
          <div class="card-body">
            <div class="trend-items">
              <div v-for="trend in trends" :key="trend.id" class="trend-item d-flex align-items-center mb-3">
                <div class="trend-icon me-3">
                  <i :class="trend.icon" class="fs-4"></i>
                </div>
                <div class="flex-grow-1">
                  <h6 class="text-light mb-1">{{ trend.title }}</h6>
                  <p class="text-muted mb-0">{{ trend.description }}</p>
                </div>
                <div class="trend-value">
                  <span :class="trend.changeClass" class="fw-bold">{{ trend.value }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Performance Table -->
    <div class="card glassmorphic">
      <div class="card-header bg-transparent border-0">
        <h5 class="text-light mb-0">Detailed Performance by Subject</h5>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-dark table-transparent">
            <thead>
              <tr>
                <th>Subject</th>
                <th>Quizzes Taken</th>
                <th>Average Score</th>
                <th>Best Score</th>
                <th>Last Attempt</th>
                <th>Progress</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="subject in subjectPerformance" :key="subject.id">
                <td>
                  <div class="d-flex align-items-center">
                    <div class="subject-icon me-2">
                      <i :class="subject.icon" class="text-primary"></i>
                    </div>
                    {{ subject.name }}
                  </div>
                </td>
                <td>{{ subject.quizzesTaken }}</td>
                <td>
                  <span class="badge" :class="getScoreBadgeClass(subject.averageScore)">
                    {{ subject.averageScore }}%
                  </span>
                </td>
                <td>{{ subject.bestScore }}%</td>
                <td>{{ formatDate(subject.lastAttempt) }}</td>
                <td>
                  <div class="progress" style="height: 8px;">
                    <div 
                      class="progress-bar bg-primary" 
                      :style="{ width: subject.progress + '%' }"
                    ></div>
                  </div>
                  <small class="text-muted">{{ subject.progress }}%</small>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SummaryView',
  data() {
    return {
      selectedTimeRange: 'month',
      performanceChart: null,
      subjectChart: null,
      gradeChart: null,
      metrics: {
        totalQuizzes: 23,
        averageScore: 78,
        highestScore: 95,
        improvement: 12
      },
      trends: [
        {
          id: 1,
          title: 'Mathematics Performance',
          description: 'Improved by 15% this month',
          value: '+15%',
          icon: 'bi bi-arrow-up-circle text-success',
          changeClass: 'text-success'
        },
        {
          id: 2,
          title: 'Science Consistency',
          description: 'Stable performance across attempts',
          value: 'Stable',
          icon: 'bi bi-check-circle text-info',
          changeClass: 'text-info'
        },
        {
          id: 3,
          title: 'History Progress',
          description: 'New subject added to learning',
          value: 'New',
          icon: 'bi bi-plus-circle text-warning',
          changeClass: 'text-warning'
        },
        {
          id: 4,
          title: 'Overall Trend',
          description: 'Upward trajectory maintained',
          value: '+8%',
          icon: 'bi bi-graph-up text-success',
          changeClass: 'text-success'
        }
      ],
      subjectPerformance: [
        {
          id: 1,
          name: 'Mathematics',
          icon: 'bi bi-calculator',
          quizzesTaken: 8,
          averageScore: 85,
          bestScore: 95,
          lastAttempt: '2024-01-20',
          progress: 85
        },
        {
          id: 2,
          name: 'Science',
          icon: 'bi bi-flask',
          quizzesTaken: 6,
          averageScore: 78,
          bestScore: 88,
          lastAttempt: '2024-01-18',
          progress: 78
        },
        {
          id: 3,
          name: 'History',
          icon: 'bi bi-book',
          quizzesTaken: 5,
          averageScore: 72,
          bestScore: 82,
          lastAttempt: '2024-01-15',
          progress: 72
        },
        {
          id: 4,
          name: 'English',
          icon: 'bi bi-pen',
          quizzesTaken: 4,
          averageScore: 80,
          bestScore: 90,
          lastAttempt: '2024-01-12',
          progress: 80
        }
      ]
    }
  },
  mounted() {
    this.initializeCharts()
  },
  watch: {
    selectedTimeRange() {
      this.updateCharts()
    }
  },
  methods: {
    initializeCharts() {
      this.createPerformanceChart()
      this.createSubjectChart()
      this.createGradeChart()
    },
    createPerformanceChart() {
      const ctx = document.getElementById('performanceChart').getContext('2d')
      
      // Simple chart simulation - in real app, you'd use Chart.js
      this.drawLineChart(ctx, {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        data: [65, 72, 78, 85],
        color: '#0d6efd'
      })
    },
    createSubjectChart() {
      const ctx = document.getElementById('subjectChart').getContext('2d')
      
      // Simple pie chart simulation
      this.drawPieChart(ctx, {
        labels: ['Math', 'Science', 'History', 'English'],
        data: [30, 25, 25, 20],
        colors: ['#0d6efd', '#198754', '#ffc107', '#dc3545']
      })
    },
    createGradeChart() {
      const ctx = document.getElementById('gradeChart').getContext('2d')
      
      // Simple bar chart simulation
      this.drawBarChart(ctx, {
        labels: ['A+', 'A', 'B+', 'B', 'C'],
        data: [5, 8, 6, 3, 1],
        color: '#198754'
      })
    },
    drawLineChart(ctx, data) {
      // Simple line chart implementation
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
      ctx.strokeStyle = data.color
      ctx.lineWidth = 3
      ctx.beginPath()
      
      const width = ctx.canvas.width
      const height = ctx.canvas.height
      const stepX = width / (data.data.length - 1)
      const maxValue = Math.max(...data.data)
      
      data.data.forEach((value, index) => {
        const x = index * stepX
        const y = height - (value / maxValue) * height * 0.8
        
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      
      ctx.stroke()
      
      // Add points
      ctx.fillStyle = data.color
      data.data.forEach((value, index) => {
        const x = index * stepX
        const y = height - (value / maxValue) * height * 0.8
        ctx.beginPath()
        ctx.arc(x, y, 4, 0, 2 * Math.PI)
        ctx.fill()
      })
    },
    drawPieChart(ctx, data) {
      // Simple pie chart implementation
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
      
      const centerX = ctx.canvas.width / 2
      const centerY = ctx.canvas.height / 2
      const radius = Math.min(centerX, centerY) * 0.7
      
      let currentAngle = 0
      const total = data.data.reduce((sum, value) => sum + value, 0)
      
      data.data.forEach((value, index) => {
        const sliceAngle = (value / total) * 2 * Math.PI
        
        ctx.fillStyle = data.colors[index]
        ctx.beginPath()
        ctx.moveTo(centerX, centerY)
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle)
        ctx.closePath()
        ctx.fill()
        
        currentAngle += sliceAngle
      })
    },
    drawBarChart(ctx, data) {
      // Simple bar chart implementation
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
      
      const width = ctx.canvas.width
      const height = ctx.canvas.height
      const barWidth = width / data.data.length * 0.8
      const maxValue = Math.max(...data.data)
      
      ctx.fillStyle = data.color
      
      data.data.forEach((value, index) => {
        const barHeight = (value / maxValue) * height * 0.8
        const x = index * (width / data.data.length) + (width / data.data.length - barWidth) / 2
        const y = height - barHeight
        
        ctx.fillRect(x, y, barWidth, barHeight)
      })
    },
    updateCharts() {
      // Update charts based on selected time range
      this.createPerformanceChart()
      this.createSubjectChart()
      this.createGradeChart()
    },
    getScoreBadgeClass(score) {
      if (score >= 90) return 'bg-success'
      if (score >= 80) return 'bg-info'
      if (score >= 70) return 'bg-warning'
      return 'bg-danger'
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.summary-view {
  padding: 1.5rem;
  min-height: 100vh;
}

.glassmorphic {
  background: rgba(35, 39, 43, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

.card.glassmorphic {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.metric-icon {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}

.chart-container canvas {
  width: 100% !important;
  height: 100% !important;
}

.trend-item {
  padding: 0.75rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.trend-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.trend-icon {
  width: 50px;
  text-align: center;
}

.subject-icon {
  width: 30px;
  text-align: center;
}

.table-transparent {
  background: transparent;
}

.table-transparent td,
.table-transparent th {
  border-color: rgba(255, 255, 255, 0.1);
  color: #f8f9fa;
}

.progress {
  background-color: rgba(255, 255, 255, 0.1);
}

.form-select.glassmorphic {
  background: rgba(35, 39, 43, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
}

.form-select.glassmorphic:focus {
  background: rgba(35, 39, 43, 0.9);
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.form-select.glassmorphic option {
  background: #23272b;
  color: #f8f9fa;
}

@media (max-width: 768px) {
  .summary-view {
    padding: 1rem;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .d-flex.gap-2 {
    flex-direction: column;
    gap: 0.5rem !important;
  }
}
</style> 