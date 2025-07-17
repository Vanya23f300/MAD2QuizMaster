<template>
  <div class="admin-dashboard">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-lg-3 col-md-4">
        <BaseSidebar user-role="admin" />
      </div>
      
      <!-- Main Content -->
      <div class="col-lg-9 col-md-8">
        <!-- Header -->
        <div class="dashboard-header glass mb-5">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="text-light mb-2">Welcome back, Admin!</h1>
              <p class="text-secondary mb-0 fs-5">Here's what's happening with your quiz platform</p>
            </div>
            <SearchBar v-model="searchQuery" placeholder="Search subjects, quizzes..." />
          </div>
        </div>

        <!-- Statistics Row -->
        <div class="row mb-5">
          <div class="col-xl-3 col-lg-6 mb-4">
            <StatsWidget
              :value="stats.totalSubjects"
              label="Total Subjects"
              icon="bi bi-book"
              color="primary"
              trend="+12"
              trend-direction="up"
            />
          </div>
          <div class="col-xl-3 col-lg-6 mb-4">
            <StatsWidget
              :value="stats.totalQuizzes"
              label="Active Quizzes"
              icon="bi bi-file-text"
              color="success"
              trend="+8%"
              trend-direction="up"
            />
          </div>
          <div class="col-xl-3 col-lg-6 mb-4">
            <StatsWidget
              :value="stats.totalUsers"
              label="Registered Users"
              icon="bi bi-people"
              color="warning"
              trend="+15"
              trend-direction="up"
            />
          </div>
          <div class="col-xl-3 col-lg-6 mb-4">
            <StatsWidget
              :value="stats.totalQuestions"
              label="Total Questions"
              icon="bi bi-question-circle"
              color="info"
              trend="+5%"
              trend-direction="up"
            />
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="row mb-5">
          <div class="col-12">
            <QuickActions @action-click="handleQuickAction" />
          </div>
        </div>

        <!-- Content Sections -->
        <div class="row">
          <!-- Recent Activity -->
          <div class="col-lg-6 mb-4">
            <DashboardCard title="Recent Activity" icon="bi bi-clock-history">
              <div class="activity-list">
                <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                  <div class="activity-icon">
                    <i :class="activity.icon"></i>
                  </div>
                  <div class="activity-content">
                    <div class="activity-text text-light">{{activity.text }}</div>
                    <div class="activity-time text-secondary">{{activity.time }}</div>
                  </div>
                </div>
              </div>
            </DashboardCard>
          </div>

          <!-- Upcoming Quizzes -->
          <div class="col-lg-6 mb-4">
            <DashboardCard title="Upcoming Quizzes" icon="bi bi-calendar-event">
              <div class="quiz-list">
                <div v-for="quiz in upcomingQuizzes" :key="quiz.id" class="quiz-item">
                  <div class="quiz-info">
                    <h6 class="quiz-title text-light mb-1">{{ quiz.title }}</h6>
                    <p class="quiz-subject text-secondary mb-2">{{ quiz.subject }}</p>
                    <div class="quiz-meta">
                      <span class="quiz-date text-secondary me-3">
                        <i class="bi bi-calendar me-1"></i>{{ quiz.date }}
                      </span>
                      <span class="quiz-duration text-secondary">
                        <i class="bi bi-clock me-1"></i>{{ quiz.duration }}
                      </span>
                    </div>
                  </div>
                  <div class="quiz-actions">
                    <button class="btn btn-sm btn-primary">View</button>
                  </div>
                </div>
              </div>
            </DashboardCard>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseSidebar from '../components/BaseSidebar.vue'
import DashboardCard from '../components/DashboardCard.vue'
import SearchBar from '../components/SearchBar.vue'
import StatsWidget from '../components/StatsWidget.vue'
import QuickActions from '../components/QuickActions.vue'

export default {
  name: 'AdminDashboardView',
  components: {
    BaseSidebar,
    DashboardCard,
    SearchBar,
    StatsWidget,
    QuickActions
  },
  data() {
    return {
      searchQuery: '',
      stats: {
        totalSubjects: 12,
        totalQuizzes: 45,
        totalUsers: 234,
        totalQuestions: 567
      },
      recentActivity: [
        {
          id: 1,
          text: 'New quiz "JavaScript Basics" created',
          time: '2 hours ago',
          icon: 'bi bi-file-earmark-plus text-success'
        },
        {
          id: 2,
          text: 'User John Doe completed "HTML Fundamentals"',
          time: '3 hours ago',
          icon: 'bi bi-check-circle text-primary'
        },
        {
          id: 3,
          text: 'New subject "Python Programming" added',
          time: '5 hours ago',
          icon: 'bi bi-plus-circle text-warning'
        },
        {
          id: 4,
          text: 'Quiz "CSS Styling" updated',
          time: '1 day ago',
          icon: 'bi bi-pencil text-info'
        }
      ],
      upcomingQuizzes: [
        {
          id: 1,
          title: 'JavaScript Basics',
          subject: 'Web Development',
          date: '2024-01-15',
          duration: '30 min'
        },
        {
          id: 2,
          title: 'Python Fundamentals',
          subject: 'Programming',
          date: '2024-01-20',
          duration: '45 min'
        },
        {
          id: 3,
          title: 'Database Design',
          subject: 'Computer Science',
          date: '2024-01-25',
          duration: '60 min'
        }
      ]
    }
  },
  methods: {
    handleQuickAction(actionId) {
      console.log('Quick action clicked:', actionId)
      
      // Navigate to appropriate CRUD pages
      switch (actionId) {
        case 'add-subject':
        case 'manage-subjects':
          this.$router.push('/admin/subjects')
          break
        case 'add-quiz':
        case 'manage-quizzes':
          this.$router.push('/admin/quizzes')
          break
        case 'manage-chapters':
          this.$router.push('/admin/chapters')
          break
        case 'manage-questions':
          this.$router.push('/admin/questions')
          break
        case 'view-reports':
          // TODO: Navigate to reports page
          console.log('Reports page not implemented yet')
          break
        case 'manage-users':
          // TODO: Navigate to users management page
          console.log('Users management not implemented yet')
          break
        default:
          console.log('Unknown action:', actionId)
      }
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
}

.dashboard-header {
  background: rgba(35, 43, 51, 0.8);
  border-radius: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  padding: 2rem;
}

.activity-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background-color 0.2s;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.02);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 1.25rem;
  margin-right: 1rem;
  width: 2.5rem;
  text-align: center;
  margin-top: 0.25rem;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
  line-height: 1.4;
}

.activity-time {
  font-size: 0.85rem;
}

.quiz-list {
  max-height: 400px;
  overflow-y: auto;
}

.quiz-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background-color 0.2s;
}

.quiz-item:hover {
  background: rgba(255, 255, 255, 0.02);
}

.quiz-item:last-child {
  border-bottom: none;
}

.quiz-info {
  flex: 1;
}

.quiz-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.quiz-subject {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.quiz-meta {
  display: flex;
  align-items: center;
  font-size: 0.8rem;
}

.quiz-actions {
  margin-left: 1rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    padding: 1.5rem;
  }
  
  .quiz-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .quiz-actions {
    margin-left: 0;
    margin-top: 1rem;
  }
}
</style> 