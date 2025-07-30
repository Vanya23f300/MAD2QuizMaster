<template>
  <div class="chapters-view container-fluid">
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
              <i class="bi bi-journal-bookmark me-2"></i>
              Chapters - {{ subjectName }}
            </h1>
            <p class="text-light">Select a chapter to view available quizzes</p>
          </div>
          <div>
            <button class="btn btn-dark-toggle" @click="goBack">
              <i class="bi bi-arrow-left me-2"></i>
              Back to Subjects
            </button>
          </div>
        </div>

        <!-- Chapters Section -->
        <div class="chapters-container glass-card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h3 class="text-light mb-0">
              <i class="bi bi-journal-text me-2"></i>
              Available Chapters
            </h3>
            <button 
              class="btn btn-sm btn-outline-light" 
              @click="fetchChapters"
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
              <p class="text-light">Loading chapters...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="alert alert-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ error }}
            </div>

            <!-- Empty State -->
            <div 
              v-else-if="!loading && chapters.length === 0" 
              class="empty-state text-center py-5"
            >
              <i class="bi bi-journal-x display-1 text-light mb-3"></i>
              <h4 class="text-light">No Chapters Available</h4>
              <p class="text-light">
                This subject doesn't have any chapters yet. Please check back later.
              </p>
            </div>

            <!-- Chapters Grid -->
            <div v-else class="row g-4">
              <div 
                v-for="chapter in chapters" 
                :key="chapter.id" 
                class="col-md-4 col-lg-3"
              >
                <div class="chapter-card glass-card">
                  <div class="card-header">
                    <h4 class="text-light">{{ chapter.name }}</h4>
                  </div>
                  <div class="card-body">
                    <p class="text-light mb-3">
                      {{ chapter.description || 'No description available' }}
                    </p>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-light">
                        <i class="bi bi-calendar me-2"></i>
                        {{ formatDate(chapter.created_at) }}
                      </small>
                      <button 
                        class="btn btn-primary btn-sm"
                        @click="viewQuizzes(chapter)"
                      >
                        View Quizzes
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
import ChapterService from '@/services/chapter-service'
import SubjectService from '@/services/subject-service'
import AuthService from '@/services/auth'

export default {
  name: 'ChaptersView',
  data() {
    return {
      subjectId: null,
      subjectName: 'Loading...',
      chapters: [],
      loading: false,
      error: null
    }
  },
  created() {
    this.subjectId = parseInt(this.$route.params.subjectId)
    this.fetchSubjectDetails()
    this.fetchChapters()
  },
  methods: {
    async fetchSubjectDetails() {
      try {
        // Fetch subject details to get the name
        const result = await SubjectService.getAllSubjects()
        if (result.success) {
          const subject = result.data.find(s => s.id === this.subjectId)
          if (subject) {
            this.subjectName = subject.name
          }
        }
      } catch (error) {
        console.error('Failed to fetch subject details:', error)
      }
    },

    async fetchChapters() {
      this.loading = true
      this.error = null

      try {
        console.log('🔍 Fetching Chapters for Subject ID:', this.subjectId)
        
        const result = await ChapterService.getChaptersBySubject(this.subjectId)
        
        if (result.success) {
          this.chapters = result.data
          console.log('✅ Chapters fetched:', this.chapters)
        } else {
          console.error('❌ Fetch Chapters Error:', result.message)
          this.error = result.message
        }
      } catch (error) {
        console.error('❌ Failed to fetch chapters:', error)
        
        // More detailed error logging
        if (error.response) {
          console.error('Response Error Details:', {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers
          })
        }
        
        this.error = 'Failed to retrieve chapters. Check console for details.'
      } finally {
        this.loading = false
      }
    },

    viewQuizzes(chapter) {
      this.$router.push(`/user/chapter/${chapter.id}/quizzes`)
    },

    goBack() {
      this.$router.push('/user/select-quiz')
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
.chapters-view {
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

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.chapter-card {
  transition: all 0.3s ease;
  height: 100%;
}

.chapter-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
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
  
  .dashboard-header > div:last-child {
    margin-top: 1rem;
  }
}
</style> 