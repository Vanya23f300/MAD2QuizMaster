<template>
  <div class="user-dashboard container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-2 sidebar">
        <BaseSidebar 
          user-role="user" 
          @showExports="showExports" 
          @logout="logout"
        />
      </div>

      <!-- Main Content -->
      <div class="col-md-10 main-content">
        <!-- Header with Notification -->
        <div class="dashboard-header glass-card mb-4">
          <div>
            <h1 class="text-light">
              <i class="bi bi-speedometer2 me-2"></i>
              Welcome back, {{ username }}!
            </h1>
            <p class="text-light">Take quizzes and track your progress</p>
          </div>
          
          <!-- User Settings Button -->
          <div class="d-flex align-items-center me-3">
            <button 
              class="btn btn-dark-toggle d-flex align-items-center gap-2 me-3"
              @click="showPreferences"
              title="User Settings"
            >
              <i class="bi bi-sliders"></i>
              <span>Settings</span>
            </button>
          </div>
          
          <!-- Notification button -->
          <div class="notification-area">
            <button 
              class="btn btn-dark-toggle position-relative me-2"
              @click="toggleNotifications"
            >
              <i class="bi bi-bell"></i>
              <span 
                v-if="unreadNotifications > 0" 
                class="notification-badge"
              >
                {{ unreadNotifications }}
              </span>
            </button>
            <button
              class="btn btn-dark-toggle"
              @click="showNotificationSettings"
              title="Notification Settings"
            >
              <i class="bi bi-gear-fill"></i>
            </button>
          </div>
        </div>
        
        <!-- Notification Center (Collapsible) -->
        <div v-if="showNotifications" class="notification-center-wrapper mb-4">
          <NotificationCenter @close="toggleNotifications" />
        </div>

        <!-- Notification Setup Modal for New Users -->
        <NotificationSetupModal 
          :show="showNotificationSetup" 
          @close="hideNotificationSetup"
          @saved="onPreferencesSaved"
        />

        <!-- Daily Reminder (only show if there are unattempted quizzes) -->
        <div v-if="unreadNotifications > 0" class="daily-reminder glass-card mb-4">
          <div class="d-flex align-items-center">
            <div class="reminder-icon">
              <i class="bi bi-alarm"></i>
            </div>
            <div class="reminder-content">
              <h4 class="text-light">Daily Quiz Reminder</h4>
              <p class="text-light mb-0">
                We noticed you have {{ unreadNotifications }} new {{ unreadNotifications === 1 ? 'quiz' : 'quizzes' }} available!
                Take a quiz today to stay on track.
              </p>
            </div>
            <div class="reminder-actions">
              <router-link to="/user/quizzes" class="btn btn-primary">
                View Quizzes
              </router-link>
            </div>
          </div>
        </div>

        <!-- Performance Summary -->
        <div class="performance-summary glass-card mb-4">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h3 class="text-light mb-0">
              <i class="bi bi-graph-up me-2"></i>
              Your Performance Summary
            </h3>
            <button 
              class="btn btn-sm btn-outline-light" 
              @click="fetchStats"
            >
              <i class="bi bi-arrow-clockwise me-2"></i>
              Refresh Stats
            </button>
          </div>
          
          <div class="card-body">
            <!-- Debug Info -->
            <div class="debug-text mb-3">Stats: {{ JSON.stringify(stats) }}</div>
            
            <div class="stats-container">
              <!-- Total Quizzes -->
              <div class="stat-box">
                <div class="stat-icon-wrapper">
                  <i class="bi bi-clipboard-check"></i>
                </div>
                <div class="stat-label-wrapper">TOTAL QUIZZES TAKEN</div>
                <div class="stat-value-wrapper">{{ stats.quizzesTaken }}</div>
              </div>
              
              <!-- Average Score -->
              <div class="stat-box">
                <div class="stat-icon-wrapper">
                  <i class="bi bi-percent"></i>
                </div>
                <div class="stat-label-wrapper">AVERAGE SCORE</div>
                <div class="stat-value-wrapper">{{ stats.averageScore }}%</div>
              </div>
              
              <!-- Time Spent -->
              <div class="stat-box">
                <div class="stat-icon-wrapper">
                  <i class="bi bi-clock-history"></i>
                </div>
                <div class="stat-label-wrapper">TOTAL TIME SPENT</div>
                <div class="stat-value-wrapper">{{ formatTime(stats.timeSpent) }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quiz Selection CTA -->
        <div class="take-quiz-cta glass-card mb-4">
          <div class="row align-items-center">
            <div class="col-md-8">
              <h3 class="text-light">Ready to test your knowledge?</h3>
              <p class="text-light mb-md-0">
                Select a subject, chapter, and quiz to start practicing and improve your scores.
              </p>
            </div>
            <div class="col-md-4 text-md-end">
              <router-link to="/user/select-quiz" class="btn btn-lg btn-primary">
                <i class="bi bi-play-circle me-2"></i>
                Start a Quiz
              </router-link>
            </div>
          </div>
        </div>

        <!-- Available Subjects Section -->
        <div class="available-subjects glass-card mb-4">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h3 class="text-light mb-0">
              <i class="bi bi-book me-2"></i>
              Available Subjects
            </h3>
            <button 
              class="btn btn-sm btn-outline-light" 
              @click="fetchSubjects"
              :disabled="loading"
            >
              <i class="bi bi-arrow-clockwise me-2"></i>
              Refresh
            </button>
          </div>
          
          <div class="card-body">
            <!-- Loading State -->
            <div v-if="loading" class="text-center py-5">
              <div class="spinner-border text-primary mb-3"></div>
              <p class="text-light">Loading subjects...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="alert alert-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ error }}
            </div>

            <!-- Empty State -->
            <div 
              v-else-if="!loading && subjects.length === 0" 
              class="empty-state text-center py-5"
            >
              <i class="bi bi-book display-1 text-light mb-3"></i>
              <h4 class="text-light">No Subjects Available</h4>
              <p class="text-light">
                Subjects will be added by the admin soon. Check back later!
              </p>
            </div>

            <!-- Subjects Grid -->
            <div v-else class="row g-4">
              <div 
                v-for="subject in subjects" 
                :key="subject.id" 
                class="col-md-4 col-lg-3"
              >
                <div class="subject-card glass-card">
                  <div class="card-header">
                    <h4 class="text-light">{{ subject.name }}</h4>
                  </div>
                  <div class="card-body">
                    <p class="text-light mb-3">
                      {{ subject.description || 'No description available' }}
                    </p>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-light">
                        <i class="bi bi-calendar me-2"></i>
                        {{ formatDate(subject.created_at) }}
                      </small>
                      <button 
                        class="btn btn-primary btn-sm"
                        @click="startQuiz"
                      >
                        Start Quiz
                        <i class="bi bi-arrow-right ms-2"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Scores Section -->
        <div class="recent-scores glass-card">
          <div class="card-header">
            <h3 class="text-light mb-0">
              <i class="bi bi-trophy me-2"></i>
              My Recent Scores
            </h3>
          </div>
          <div class="card-body">
            <div v-if="loadingScores" class="text-center py-4">
              <div class="spinner-border text-primary mb-3"></div>
              <p class="text-light">Loading recent scores...</p>
            </div>

            <div v-else-if="!recentScores.length" class="text-center text-light py-5">
              <i class="bi bi-inbox display-4 mb-3"></i>
              <p>No recent quiz attempts. Start a quiz to see your scores!</p>
            </div>
            
            <div v-else class="scores-list">
              <div class="table-responsive">
                <table class="table table-dark table-hover">
                  <thead>
                    <tr>
                      <th>Quiz</th>
                      <th>Score</th>
                      <th>Date</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="score in recentScores" :key="score.id">
                      <td>{{ score.quiz_name }}</td>
                      <td>
                        <span class="badge" :class="getScoreClass(score.percentage)">
                          {{ score.percentage }}%
                        </span>
                      </td>
                      <td>{{ formatDate(score.time_stamp_of_attempt) }}</td>
                      <td>
                        <span class="badge" :class="score.passed ? 'bg-success' : 'bg-danger'">
                          {{ score.passed ? 'PASSED' : 'FAILED' }}
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
    
    <!-- User Preferences Modal -->
    <div 
      class="modal fade" 
      id="userPreferencesModal" 
      tabindex="-1" 
      aria-labelledby="userPreferencesModalLabel" 
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass-card">
          <div class="modal-header border-bottom-0">
            <h5 class="modal-title text-light" id="userPreferencesModalLabel">User Preferences</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <UserPreferences 
              @preferences-saved="onPreferencesSaved"
              @success="showSuccess"
              @error="showError"
            />
          </div>
        </div>
      </div>
    </div>
    
    <!-- Export Manager Modal -->
    <div 
      class="modal fade" 
      id="exportManagerModal" 
      tabindex="-1" 
      aria-labelledby="exportManagerModalLabel" 
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass-card">
          <div class="modal-header border-bottom-0">
            <h5 class="modal-title text-light" id="exportManagerModalLabel">Export Data</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <ExportManager 
              @error="showError" 
              @success="showSuccess"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthService from '@/services/auth'
import SubjectService from '@/services/subject-service'
import DashboardService from '@/services/dashboard-service'
import BaseSidebar from '@/components/BaseSidebar.vue'
import NotificationCenter from '@/components/NotificationCenter.vue'
import UserPreferences from '@/components/UserPreferences.vue'
import ExportManager from '@/components/ExportManager.vue'
import NotificationService from '@/services/notification-service'
import NotificationSetupModal from '@/components/NotificationSetupModal.vue'
import api from '@/services/api'

export default {
  name: 'UserDashboardView',
  components: {
    BaseSidebar,
    NotificationCenter,
    UserPreferences,
    ExportManager,
    NotificationSetupModal
  },
  data() {
    return {
      username: '',
      subjects: [],
      loading: false,
      error: null,
      showNotifications: false,
      showNotificationSetup: false,
      unreadNotifications: 0,
      stats: {
        quizzesTaken: 0,
        averageScore: 0,
        passRate: 0,
        timeSpent: 0
      },
      recentScores: [],
      loadingScores: false,
      preferencesModal: null,
      exportModal: null
    }
  },
  async mounted() {
    try {
      const currentUser = AuthService.getCurrentUser()
      
      // Check if user is logged in
      if (!currentUser || !localStorage.getItem('token')) {
        console.error('No user logged in. Redirecting to login page.')
        this.$router.push('/login')
        return
      }
      
      this.username = currentUser?.username || 'Student'
      
      // Debug log
      console.log('🔎 Current user:', currentUser)
      console.log('🔑 Token from localStorage:', localStorage.getItem('token') ? 'Token exists' : 'No token')
      
      // Initialize modals
      this.initModals()
      
      // First fetch stats directly
      console.log('Fetching stats first...')
      await this.fetchStats()
      
      // Then fetch remaining data
      await Promise.all([
        this.fetchSubjects(),
        this.fetchRecentScores(),
        this.fetchNotificationsCount(),
        this.checkUserPreferences()
      ])
      
      // Check for new unattempted quizzes
      await this.checkForNewQuizzes()
      
    } catch (error) {
      console.error('Error initializing dashboard:', error)
    }
  },
  methods: {
    getUsername() {
      try {
        const userString = localStorage.getItem('user')
        if (userString) {
          const user = JSON.parse(userString)
          return user.username || user.email || 'User'
        }
        return 'User'
      } catch (error) {
        console.error('Error parsing user data:', error)
        return 'User'
      }
    },

    async fetchSubjects() {
      this.loading = true
      this.error = null

      try {
        console.log('🔍 Fetching Subjects...')
        
        const result = await SubjectService.getAllSubjects()
        
        console.log('📊 Subjects Result:', result)
        
        // Always use the data property since we've modified SubjectService to always return an array
        this.subjects = result.data || []
        
        if (!result.success) {
          console.error('❌ Fetch Subjects Error:', result.message)
          this.error = result.message
        } else {
          console.log('✅ Subjects fetched:', this.subjects)
        }
      } catch (error) {
        console.error('❌ Failed to fetch subjects:', error)
        
        // More detailed error logging
        if (error.response) {
          console.error('Response Error Details:', {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers
          })
        }
        
        this.error = 'Failed to retrieve subjects. Check console for details.'
        this.subjects = [] // Ensure subjects is always an array
      } finally {
        this.loading = false
      }
    },

    async fetchNotificationsCount() {
      try {
        // In a real app, you would fetch notifications from API
        // For now, let's set a random number for demonstration
        this.unreadNotifications = 0
        
        // Check for new unattempted quizzes
        await this.checkForNewQuizzes()
      } catch (error) {
        console.error('Failed to fetch notifications count:', error)
      }
    },

    toggleNotifications() {
      this.showNotifications = !this.showNotifications
      
      // If showing notifications, mark them as read
      if (this.showNotifications) {
        this.unreadNotifications = 0
      }
    },
    
    initModals() {
      // We'll initialize the Bootstrap modals when component is mounted
      try {
        // Check if bootstrap is available in the global scope
        if (typeof bootstrap === 'undefined') {
          console.error('Bootstrap JS is not loaded');
          alert('Bootstrap is not available. Please make sure bootstrap.js is loaded.');
          return;
        }
        
        // Find the modal elements
        const preferencesModalEl = document.getElementById('userPreferencesModal');
        const exportModalEl = document.getElementById('exportManagerModal');
        
        if (!preferencesModalEl) {
          console.error('Preferences modal element not found');
        }
        
        if (!exportModalEl) {
          console.error('Export modal element not found');
        }
        
        // Initialize the modals if elements exist
        if (preferencesModalEl) {
          this.preferencesModal = new bootstrap.Modal(preferencesModalEl);
          console.log('Preferences modal initialized');
        }
        
        if (exportModalEl) {
          this.exportModal = new bootstrap.Modal(exportModalEl);
          console.log('Export modal initialized');
        }
      } catch (error) {
        console.error('Error initializing modals:', error);
        alert('Error initializing modals: ' + error.message);
      }
    },
    
    showPreferences() {
      if (this.preferencesModal) {
        this.preferencesModal.show()
      }
    },
    
    showExports() {
      // Check if user is authenticated
      if (!localStorage.getItem('token')) {
        this.showError('You need to be logged in to export data. Please log in again.');
        this.$router.push('/login');
        return;
      }
      
      if (!this.exportModal) {
        console.log('Initializing export modal...');
        const modalElement = document.getElementById('exportManagerModal');
        
        if (!modalElement) {
          console.error('Export modal element not found in DOM');
          this.showError('Could not open export manager. Please try refreshing the page.');
          return;
        }
        
        try {
          this.exportModal = new bootstrap.Modal(modalElement);
        } catch (error) {
          console.error('Error initializing export modal:', error);
          this.showError('Failed to initialize export manager: ' + error.message);
          return;
        }
      }
      
      try {
        console.log('Showing export modal');
        this.exportModal.show();
      } catch (error) {
        console.error('Error showing export modal:', error);
        this.showError('Failed to show export manager: ' + error.message);
      }
    },
    
    onPreferencesSaved(preferences) {
      console.log('Preferences saved:', preferences)
      
      // Apply any needed UI changes based on preferences
      this.showNotificationSetup = false
      
      // Show success notification
      this.showSuccess('Your notification preferences have been saved!')
      
      // Refresh user preferences
      this.checkUserPreferences()
    },
    
    hideNotificationSetup() {
      console.log('Hiding notification setup modal')
      this.showNotificationSetup = false
    },
    
    async checkUserPreferences() {
      try {
        console.log('Checking user preferences...')
        
        // Check if this is the first login by seeing if user preferences exist
        const response = await api.get('/api/user/preferences')
        
        console.log('User preferences response:', response.data)
        
        // If no preferences exist or daily reminders not set, show the modal
        const hasPreferences = response.data && response.data.preferences
        
        // If no preferences found, show the setup modal
        if (!hasPreferences) {
          console.log('No preferences found, showing setup modal')
          this.showNotificationSetup = true
          return
        }
        
        // Check if daily reminders are enabled but no reminder time is set
        try {
          const preferences = response.data.preferences
          const notifications = preferences.notifications || {}
          
          // Check if this is a new user or if notifications haven't been configured
          const isNewUser = !preferences || !preferences.notifications
          
          // Check if reminder time is missing when reminders are enabled
          const needsReminderTime = preferences && 
                                 notifications && 
                                 notifications.dailyReminders && 
                                 !notifications.reminderTime
          
          console.log('Preferences check:', { 
            isNewUser, 
            needsReminderTime,
            dailyReminders: notifications.dailyReminders,
            reminderTime: notifications.reminderTime
          })
          
          // Show setup modal for new users or when reminder time is missing
          if (isNewUser || needsReminderTime) {
            // Show the notification setup modal
            console.log('Notification setup needed. Showing notification setup modal.')
            this.showNotificationSetup = true
          }
        } catch (parseError) {
          console.error('Error parsing preferences:', parseError)
          this.showNotificationSetup = true
        }
      } catch (error) {
        console.error('Error checking user preferences:', error)
        // If error, assume new user and show modal
        this.showNotificationSetup = true
      }
    },
    
    showSuccess(message) {
      // Show success message (could use a toast component)
      alert(message)
    },
    
    showError(message) {
      // Show error message
      alert(message)
    },

    startQuiz() {
      // Redirect to the subject selection view
      this.$router.push('/user/select-quiz')
    },

    logout() {
      AuthService.logout()
      this.$router.push('/login')
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },

    async fetchStats() {
      try {
        // Use the dashboard service to fetch real data
        console.log('🔍 Fetching performance stats...')
        
        const result = await DashboardService.getUserPerformance()
        console.log('📊 Result from API:', result)
        
        // Only use real data from the API
        this.stats = {
          quizzesTaken: result.data?.stats?.quizzes_taken || 0,
          averageScore: result.data?.stats?.average_score || 0,
          passRate: result.data?.stats?.pass_rate || 0,
          timeSpent: result.data?.stats?.time_spent || 0
        }
        console.log('📊 Stats updated from API:', this.stats)
        
        // Force update to ensure the view refreshes
        this.$forceUpdate();
        
      } catch (error) {
        console.error('❌ Error fetching performance stats:', error)
        
        // Reset stats to zero on error
        this.stats = {
          quizzesTaken: 0,
          averageScore: 0,
          passRate: 0,
          timeSpent: 0
        }
      }
    },
    
    formatTime(seconds) {
      console.log('Formatting time from seconds:', seconds);
      if (!seconds || seconds === 0) {
        return '0m'
      }
      
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      
      if (hours > 0) {
        return `${hours}h ${minutes}m`
      }
      return `${minutes}m`
    },

    async fetchRecentScores() {
      this.loadingScores = true
      
      try {
        console.log('🔍 Fetching recent scores...')
        const result = await DashboardService.getRecentScores()
        
        // Only use real data from the API
        this.recentScores = result.data || []
        console.log('✅ Recent scores fetched from API:', this.recentScores)
      } catch (error) {
        console.error('❌ Failed to fetch recent scores:', error)
        // More detailed error logging
        if (error.response) {
          console.error('Response Error Details:', {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers
          })
        }
        this.recentScores = []
      } finally {
        this.loadingScores = false
      }
    },

    getScoreClass(percentage) {
      if (percentage >= 90) return 'bg-success'
      if (percentage >= 70) return 'bg-info'
      if (percentage >= 50) return 'bg-warning'
      return 'bg-danger'
    },

    showNotificationSettings() {
      // Show the notification setup modal directly when needed
      this.showNotificationSetup = true
    },
    
    async checkForNewQuizzes() {
      try {
        // Check for new unattempted quizzes
        const unattemptedQuizzes = await NotificationService.checkForNewQuizzes();
        if (unattemptedQuizzes && unattemptedQuizzes.length > 0) {
          // Update unread notifications count
          this.unreadNotifications += unattemptedQuizzes.length;
          console.log(`Found ${unattemptedQuizzes.length} new quizzes for notifications`);
        }
      } catch (error) {
        console.error('Error checking for new quizzes:', error);
      }
    }
  }
}
</script>

<style scoped>
.user-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, 
    rgba(35, 39, 43, 0.9) 0%, 
    rgba(22, 33, 62, 0.9) 100%
  );
}

.sidebar {
  height: 100vh;
  position: sticky;
  top: 0;
  padding-top: 2rem;
}

.main-content {
  padding: 2rem;
}

.glass-card {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-area {
  position: relative;
}

.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #24a35a;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
}

.notification-center-wrapper {
  position: relative;
  z-index: 10;
}

.btn-dark-toggle {
  background: rgba(40, 44, 52, 0.8) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(4px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  border-radius: 1.25rem;
}

.btn-dark-toggle:hover {
  background: rgba(60, 65, 75, 0.9) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: rgba(255, 255, 255, 1) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.subject-card {
  transition: all 0.3s ease;
}

.subject-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.empty-state {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 1rem;
  padding: 2rem;
}

.stats-summary {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  height: 100%;
  justify-content: center;
}

.stat-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  padding: 1rem;
  text-align: center;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
}

.btn-group .btn {
  padding: 0.25rem 0.75rem;
}

.btn-group .btn.active {
  background-color: #24a35a !important;
  border-color: #24a35a !important;
  color: white !important;
}

.stat-card {
  background: rgba(15, 20, 25, 0.9) !important;
  border-radius: 1rem;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  height: 100%;
  border: 1px solid rgba(255, 255, 255, 0.25);
  margin-bottom: 1rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.35);
}

.stat-card:hover {
  transform: translateY(-5px);
  background: rgba(20, 25, 35, 0.95) !important;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
  border-color: rgba(255, 255, 255, 0.4);
}

.stat-icon {
  font-size: 2.5rem;
  color: #39c0ed;
  margin-bottom: 1.25rem;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.stat-label {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.stat-value {
  color: white;
  font-size: 2.25rem;
  font-weight: 700;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

.daily-reminder {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.daily-reminder .d-flex {
  gap: 1.5rem;
}

.reminder-icon i {
  font-size: 2.5rem;
  color: #24a35a;
}

.reminder-content {
  flex: 1;
}

.reminder-content h4 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.reminder-content p {
  opacity: 0.8;
}

.reminder-actions {
  margin-left: auto;
}

.performance-summary {
  margin-bottom: 1.5rem;
}

.performance-summary .card-body {
  padding: 1.25rem;
}

.performance-summary .row {
  margin: 0 -0.5rem;
}

.performance-summary .col-md-4 {
  padding: 0 0.5rem;
}

@media (max-width: 768px) {
  .sidebar {
    height: auto;
    position: static;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .notification-area {
    margin-top: 1rem;
  }

  .daily-reminder {
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }

  .reminder-icon {
    margin-bottom: 1rem;
  }

  .reminder-actions {
    width: 100%;
    text-align: center;
  }
}

.basic-stat-card {
  background: #1e2a38;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  height: 100%;
}

.stat-icon-basic {
  font-size: 1.75rem;
  color: #39c0ed;
  width: 40px;
  text-align: center;
}

.stat-value-basic {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  margin-top: 1rem;
}

h4 {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  font-weight: 600;
}

.stats-container {
  display: flex;
  justify-content: space-between;
  margin: 0 -15px;
}

.stat-box {
  flex: 1;
  background-color: #1e2a38;
  border-radius: 10px;
  padding: 20px;
  margin: 0 15px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-icon-wrapper {
  font-size: 2.5rem;
  color: #39c0ed;
  margin-bottom: 10px;
}

.stat-label-wrapper {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.75rem;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.stat-value-wrapper {
  font-size: 2.5rem;
  font-weight: 700;
  color: #39c0ed !important;
  text-shadow: 0 0 10px rgba(57, 192, 237, 0.5);
  margin-top: 1rem;
}

/* Add responsive styles for smaller screens */
@media (max-width: 768px) {
  .stats-container {
    flex-direction: column;
  }
  
  .stat-box {
    margin: 10px 15px;
  }
}

.debug-text {
  background: rgba(0,0,0,0.5);
  color: lime;
  padding: 10px;
  border-radius: 5px;
  font-family: monospace;
  word-wrap: break-word;
}
</style> 