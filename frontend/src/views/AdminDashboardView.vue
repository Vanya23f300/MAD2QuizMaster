<template>
  <div class="admin-dashboard">
    <div class="container-fluid px-4">
      <!-- Page Header -->
      <div class="page-header glass mb-4">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h1 class="text-light mb-2">
              <i class="bi bi-shield-lock me-1"></i>
              Admin Dashboard
            </h1>
            <p class="text-light mb-0">
              Welcome back, Quiz Master! Manage your platform here.
            </p>
          </div>
          <div class="header-actions d-flex align-items-center gap-3">
            <!-- Notification button -->
            <div class="notification-area">
              <button 
                class="btn btn-dark-toggle position-relative"
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
            </div>
            
            <button 
              class="btn btn-outline-light" 
              @click="logout"
            >
              <i class="bi bi-box-arrow-right me-2"></i>
              Logout
            </button>
          </div>
        </div>
      </div>
      
      <!-- Notification Center (Collapsible) -->
      <div v-if="showNotifications" class="notification-center-wrapper mb-4">
        <NotificationCenter @close="toggleNotifications" />
      </div>
      
      <!-- Quick Actions -->
      <div class="glass mb-4">
        <div class="card-body">
          <h3 class="text-light mb-3">
            <i class="bi bi-lightning me-2"></i>
            Quick Actions
          </h3>
          <div class="row">
            <div class="col-md-4 mb-3">
              <router-link to="/admin/subjects" class="btn btn-primary w-100 py-3">
                <i class="bi bi-book me-2"></i>
                Manage Subjects
              </router-link>
            </div>
            <div class="col-md-4 mb-3">
              <router-link to="/admin/chapters" class="btn btn-outline-light w-100 py-3">
                <i class="bi bi-layers me-2"></i>
                Manage Chapters
              </router-link>
            </div>
            <div class="col-md-4 mb-3">
              <router-link to="/admin/quizzes" class="btn btn-outline-light w-100 py-3">
                <i class="bi bi-journal-text me-2"></i>
                Manage Quizzes & Questions
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Platform Statistics -->
      <div class="row">
        <div class="col-md-8">
          <div class="glass mb-4">
            <div class="card-body">
              <h3 class="text-light mb-3">
                <i class="bi bi-bar-chart me-2"></i>
                Platform Statistics
              </h3>
              
              <!-- Stats Grid - Always Show -->
              <div class="row">
                <div class="col-md-6 mb-3">
                  <div class="stat-card">
                    <div class="stat-number">{{ stats.totalUsers || 0 }}</div>
                    <div class="stat-label">Total Users</div>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="stat-card">
                    <div class="stat-number">{{ stats.totalQuizzes || 0 }}</div>
                    <div class="stat-label">Total Quizzes</div>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="stat-card">
                    <div class="stat-number">{{ stats.activeUsers || 0 }}</div>
                    <div class="stat-label">Active Users</div>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="stat-card">
                    <div class="stat-number">{{ stats.avgQuizCompletion ? Math.round(stats.avgQuizCompletion) + '%' : '0%' }}</div>
                    <div class="stat-label">Avg. Completion</div>
                  </div>
                </div>
              </div>
              
              <!-- Loading Overlay -->
              <div v-if="loading" class="stats-loading-overlay">
                <div class="spinner-border text-primary"></div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="glass mb-4">
            <div class="card-body">
              <h3 class="text-light mb-3">
                <i class="bi bi-clock-history me-2"></i>
                Recent Activities
              </h3>
              
              <!-- Activities List - Always Show -->
              <div class="activities-list">
                <div 
                  v-for="activity in activities" 
                  :key="activity.id" 
                  class="activity-item"
                >
                  <div class="activity-description text-light">
                    {{ activity.description }}
                  </div>
                  <div class="activity-time text-light">
                    {{ formatTimeAgo(activity.timestamp) }}
                  </div>
                </div>
                
                <!-- Empty State -->
                <div v-if="activities.length === 0" class="text-center py-3">
                  <i class="bi bi-inbox text-light display-4"></i>
                  <p class="text-light mt-2">No recent activities</p>
                </div>
              </div>
              
              <!-- Loading Overlay -->
              <div v-if="loading" class="stats-loading-overlay">
                <div class="spinner-border text-primary"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
import dashboardService from '@/services/dashboard-service'
import authService from '@/services/auth'
import NotificationCenter from '@/components/NotificationCenter.vue'

export default {
  name: 'AdminDashboardView',
  components: {
    NotificationCenter
  },
  data() {
    return {
      adminName: this.getAdminName(),
      stats: {
        totalUsers: 3,            // Default value for better UI
        totalQuizzes: 5,          // Default value for better UI
        activeUsers: 2,           // Default value for better UI
        avgQuizCompletion: 75,    // Default value for better UI
        userGrowth: 10            // Default value for better UI
      },
      activities: [
        {
          id: 1,
          description: 'Dashboard initialized',
          timestamp: new Date().toISOString()
        },
        {
          id: 2,
          description: 'System ready',
          timestamp: new Date(Date.now() - 500000).toISOString()
        }
      ],
      loading: true,
      error: null,
      showNotifications: false,
      unreadNotifications: 0
    }
  },
  mounted() {
    this.fetchDashboardStats()
    this.fetchActivities()
    this.fetchNotificationsCount()
  },
  methods: {
    getAdminName() {
      try {
        const userString = localStorage.getItem('user')
        if (userString) {
          const user = JSON.parse(userString)
          return user.username || user.email || 'Admin'
        }
        return 'Admin'
      } catch (error) {
        console.error('Error parsing admin user data:', error)
        return 'Admin'
      }
    },

    async fetchDashboardStats() {
      this.loading = true
      this.error = null

      try {
        console.log('🔍 Fetching Dashboard Stats...')
        
        const result = await dashboardService.getDashboardStats()
        
        console.log('📊 Dashboard Stats Result:', result)
        
        if (result.success) {
          // Ensure stats are always numbers or 0
          this.stats = {
            totalUsers: result.data.totalUsers || 0,
            activeUsers: result.data.activeUsers || 0,
            userGrowth: result.data.userGrowth || 0,
            totalQuizzes: result.data.totalQuizzes || 0,
            avgQuizCompletion: result.data.avgQuizCompletion || 0
          }

          console.log('🔢 Processed Stats:', this.stats)
        } else {
          console.error('❌ Dashboard Stats Error:', result.message)
          // Set default values if API fails
          this.stats = {
            totalUsers: 0,
            activeUsers: 0,
            userGrowth: 0,
            totalQuizzes: 0,
            avgQuizCompletion: 0
          }
        }
      } catch (error) {
        console.error('❌ Dashboard Stats Fetch Error:', error)
        
        // Set default values if request fails
        this.stats = {
          totalUsers: 0,
          activeUsers: 0,
          userGrowth: 0,
          totalQuizzes: 0,
          avgQuizCompletion: 0
        }
      } finally {
        this.loading = false
      }
    },

    async fetchActivities() {
      try {
        console.log('🔍 Fetching Recent Activities...')
      
        const result = await dashboardService.getRecentActivities()
        
        console.log('📊 Recent Activities Result:', result)
        
        if (result.success) {
          this.activities = result.data || []
          console.log('📋 Processed Activities:', this.activities)
        } else {
          console.error('❌ Recent Activities Error:', result.message)
          // Set default activities if API fails
          this.activities = [
            {
              id: 1,
              description: 'Admin dashboard loaded',
              timestamp: new Date().toISOString()
            },
            {
              id: 2,
              description: 'System monitoring active',
              timestamp: new Date(Date.now() - 300000).toISOString()
            }
          ]
        }
      } catch (error) {
        console.error('❌ Recent Activities Fetch Error:', error)
        
        // Set default activities if request fails
        this.activities = [
          {
            id: 1,
            description: 'Admin dashboard loaded',
            timestamp: new Date().toISOString()
          },
          {
            id: 2,
            description: 'System monitoring active',
            timestamp: new Date(Date.now() - 300000).toISOString()
          }
        ]
      }
    },

    logout() {
      // eslint-disable-next-line no-undef
      authService.logout()
      this.$router.push('/login')
    },

    formatTimeAgo(timestamp) {
      if (!timestamp) return 'N/A'
      
      const now = new Date()
      const past = new Date(timestamp)
      const diff = (now - past) / 1000 // seconds
      
      if (diff < 60) return 'Just now'
      if (diff < 3600) return `${Math.floor(diff/60)} mins ago`
      if (diff < 86400) return `${Math.floor(diff/3600)} hours ago`
      return `${Math.floor(diff/86400)} days ago`
    },

    // Add new methods
    async fetchNotificationsCount() {
      try {
        // Admin doesn't need quiz notifications
        this.unreadNotifications = 0
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
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, 
    #0a0a0f 0%, 
    #1a1a2e 25%, 
    #16213e 50%, 
    #0f0f23 75%, 
    #0a0a14 100%
  );
  background-size: 400% 400%;
  animation: gradientShift 20s ease infinite;
  padding: 2rem 0;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.page-header, .glass {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.activities-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  padding: 0.75rem;
  margin: 0 -0.75rem;
}

.activity-description {
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.activity-time {
  font-size: 0.8rem;
}

.glass-alert {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  backdrop-filter: blur(10px);
}

/* Button styling */
.btn {
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

/* Custom scrollbar for activities */
.activities-list::-webkit-scrollbar {
  width: 4px;
}

.activities-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 2px;
}

.activities-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
}

.activities-list::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Add new styles */
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Loading overlay for statistics */
.stats-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 1rem;
  z-index: 5;
}

/* Make card-body relative for overlay positioning */
.card-body {
  position: relative;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem 0;
  }
  
  .page-header, .glass {
    padding: 1rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
}
</style> 