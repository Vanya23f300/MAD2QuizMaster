<template>
  <div class="quiz-selection container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-2 sidebar glass-card">
        <nav class="user-nav">
          <ul class="nav flex-column">
            <li class="nav-item">
              <router-link to="/user/dashboard" class="nav-link">
                <i class="bi bi-speedometer2 me-2"></i>Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/scores" class="nav-link">
                <i class="bi bi-trophy me-2"></i>My Scores
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/summary" class="nav-link">
                <i class="bi bi-graph-up me-2"></i>Summary Charts
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/select-quiz" class="nav-link active">
                <i class="bi bi-book me-2"></i>Select Quiz
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/profile" class="nav-link">
                <i class="bi bi-person me-2"></i>Profile
              </router-link>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link" @click.prevent="logout">
                <i class="bi bi-box-arrow-right me-2"></i>Logout
              </a>
            </li>
          </ul>
        </nav>
      </div>

      <!-- Main Content -->
      <div class="col-md-10 main-content">
        <div class="dashboard-header glass-card mb-4">
          <div>
            <h1 class="text-light">
              <i class="bi bi-book me-2"></i>
              Select a Subject
            </h1>
            <p class="text-light">Choose a subject to view available chapters and quizzes</p>
          </div>
        </div>

        <!-- Subjects Section -->
        <div class="subjects-container glass-card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h3 class="text-light mb-0">
              <i class="bi bi-grid me-2"></i>
              Available Subjects
            </h3>
            
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
                        <i class="bi bi-calendar"></i>
                        {{ formatDate(subject.created_at) }}
                      </small>
                      <button 
                        class="btn btn-primary btn-sm"
                        @click="viewChapters(subject)"
                      >
                        Select
                        <i class="bi bi-arrow-right ms-2"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SubjectService from '@/services/subject-service'
import AuthService from '@/services/auth'

export default {
  name: 'SelectQuizView',
  data() {
    return {
      subjects: [],
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchSubjects()
  },
  methods: {
    async fetchSubjects() {
      this.loading = true
      this.error = null

      try {
        console.log('🔍 Fetching Subjects...')
        
        const result = await SubjectService.getAllSubjects()
        
        if (result.success) {
          this.subjects = result.data
          console.log('✅ Subjects fetched:', this.subjects)
        } else {
          console.error('❌ Fetch Subjects Error:', result.message)
          this.error = result.message
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
      } finally {
        this.loading = false
      }
    },

    viewChapters(subject) {
      this.$router.push(`/user/subject/${subject.id}/chapters`)
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },

    logout() {
      AuthService.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.quiz-selection {
  min-height: 100vh;
  background: linear-gradient(135deg, 
    rgba(35, 39, 43, 0.9) 0%, 
    rgba(22, 33, 62, 0.9) 100%
  );
}

.sidebar {
  background: rgba(35, 39, 43, 0.6);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem 0;
  height: 100vh;
  position: sticky;
  top: 0;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  border-left: 3px solid transparent;
}

.nav-link:hover, .nav-link.active {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
  border-left-color: #4a5568;
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

.subject-card {
  transition: all 0.3s ease;
  height: 100%;
}

.subject-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .sidebar {
    height: auto;
    position: static;
  }
}
</style> 