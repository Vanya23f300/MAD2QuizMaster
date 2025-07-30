<template>
  <div class="quizzes-view container-fluid">
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
              <i class="bi bi-file-earmark-text me-2"></i>
              Quizzes - {{ chapterName }}
            </h1>
            <p class="text-light">Select a quiz to begin</p>
          </div>
          <div>
            <button class="btn btn-dark-toggle" @click="goBack">
              <i class="bi bi-arrow-left me-2"></i>
              Back to Chapters
            </button>
          </div>
        </div>

        <!-- Quizzes Section -->
        <div class="quizzes-container glass-card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h3 class="text-light mb-0">
              <i class="bi bi-question-circle me-2"></i>
              Available Quizzes
            </h3>
            <button 
              class="btn btn-sm btn-outline-light" 
              @click="fetchQuizzes"
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
              <p class="text-light">Loading quizzes...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="alert alert-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ error }}
            </div>

            <!-- Empty State -->
            <div 
              v-else-if="!loading && quizzes.length === 0" 
              class="empty-state text-center py-5"
            >
              <i class="bi bi-clipboard-x display-1 text-light mb-3"></i>
              <h4 class="text-light">No Quizzes Available</h4>
              <p class="text-light">
                This chapter doesn't have any quizzes yet. Please check back later.
              </p>
            </div>

            <!-- Quizzes List -->
            <div v-else class="row">
              <div class="col-12">
                <div class="quiz-list">
                  <div 
                    v-for="quiz in quizzes" 
                    :key="quiz.id" 
                    class="quiz-item glass-card mb-3"
                  >
                    <div class="quiz-content">
                      <div>
                        <h4 class="text-light mb-2">{{ quiz.name }}</h4>
                        <p class="text-light mb-2">{{ quiz.description || 'No description available' }}</p>
                        <div class="quiz-details">
                          <span class="badge bg-primary me-2">
                            <i class="bi bi-question-circle me-1"></i>
                            {{ quiz.questions_count || quiz.total_questions || 0 }} questions
                          </span>
                          <span class="badge bg-info me-2">
                            <i class="bi bi-clock me-1"></i>
                            {{ quiz.time_duration || 0 }} minutes
                          </span>
                          <span class="badge bg-secondary">
                            <i class="bi bi-percent me-1"></i>
                            Pass: {{ quiz.passing_score }}%
                          </span>
                        </div>
                      </div>
                      <div class="quiz-actions">
                        <button 
                          class="btn btn-primary" 
                          @click="startQuiz(quiz)"
                        >
                          Start Quiz
                          <i class="bi bi-play-fill ms-2"></i>
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
  </div>
</template>

<script>
import QuizService from '@/services/quizService'
import ChapterService from '@/services/chapter-service'
import AuthService from '@/services/auth'

export default {
  name: 'QuizzesView',
  data() {
    return {
      chapterId: null,
      chapterName: 'Loading...',
      quizzes: [],
      loading: false,
      error: null
    }
  },
  created() {
    this.chapterId = parseInt(this.$route.params.chapterId)
    this.fetchChapterDetails()
    this.fetchQuizzes()
  },
  methods: {
    async fetchChapterDetails() {
      try {
        // Assuming we need to search through all chapters to find the current one
        // In a real-world scenario, you might have an endpoint to get a single chapter
        const subjectsResult = await ChapterService.getChaptersBySubject(null)
        if (subjectsResult.success) {
          // Find the chapter in all available chapters
          const chapters = subjectsResult.data
          const chapter = chapters.find(c => c.id === this.chapterId)
          if (chapter) {
            this.chapterName = chapter.name
          }
        }
      } catch (error) {
        console.error('Failed to fetch chapter details:', error)
      }
    },

    async fetchQuizzes() {
      this.loading = true
      this.error = null

      try {
        console.log('🔍 Fetching Quizzes for Chapter ID:', this.chapterId)
        
        const quizzes = await QuizService.getQuizzes(this.chapterId)
        this.quizzes = quizzes
        console.log('✅ Quizzes fetched:', this.quizzes)
      } catch (error) {
        console.error('❌ Failed to fetch quizzes:', error)
        
        // More detailed error logging
        if (error.response) {
          console.error('Response Error Details:', {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers
          })
        }
        
        this.error = 'Failed to retrieve quizzes. Check console for details.'
      } finally {
        this.loading = false
      }
    },

    startQuiz(quiz) {
      this.$router.push(`/user/quiz/${quiz.id}`)
    },

    goBack() {
      // We need to get the subject ID to go back to the chapters view
      // For now, we'll go back to the previous page in history
      this.$router.go(-1)
    },

    logout() {
      AuthService.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.quizzes-view {
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

.quiz-item {
  transition: all 0.3s ease;
}

.quiz-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.quiz-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quiz-details {
  margin-top: 0.75rem;
}

.quiz-actions {
  margin-left: 1rem;
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
  
  .quiz-content {
    flex-direction: column;
  }
  
  .quiz-actions {
    margin-left: 0;
    margin-top: 1rem;
    width: 100%;
  }
  
  .quiz-actions button {
    width: 100%;
  }
}
</style> 