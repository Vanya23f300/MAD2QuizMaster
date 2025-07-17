<template>
  <div class="scores-view">
    <!-- Page Header -->
    <div class="page-header glass-card mb-4">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h2 class="h3 text-light mb-1">My Quiz Scores</h2>
          <p class="text-muted mb-0">Track your quiz performance and progress over time</p>
        </div>
        <div class="header-stats">
          <div class="stat-item">
            <div class="stat-value">{{ totalQuizzes }}</div>
            <div class="stat-label">Total Quizzes</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ averageScore }}%</div>
            <div class="stat-label">Average Score</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section glass-card mb-4">
      <div class="row">
        <div class="col-md-4 mb-3">
          <label class="form-label text-light">Search Quizzes</label>
          <div class="search-input-wrapper">
            <i class="bi bi-search search-icon"></i>
            <input
              v-model="searchQuery"
              type="text"
              class="form-control search-input"
              placeholder="Search by quiz name or subject..."
            >
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <label class="form-label text-light">Subject</label>
          <select v-model="selectedSubject" class="form-select">
            <option value="">All Subjects</option>
            <option v-for="subject in subjects" :key="subject" :value="subject">
              {{ subject }}
            </option>
          </select>
        </div>
        <div class="col-md-3 mb-3">
          <label class="form-label text-light">Date Range</label>
          <select v-model="selectedDateRange" class="form-select">
            <option value="">All Time</option>
            <option value="week">Last Week</option>
            <option value="month">Last Month</option>
            <option value="3months">Last 3 Months</option>
            <option value="year">Last Year</option>
          </select>
        </div>
        <div class="col-md-2 mb-3">
          <label class="form-label text-light">Sort By</label>
          <select v-model="sortBy" class="form-select">
            <option value="date">Date</option>
            <option value="score">Score</option>
            <option value="title">Quiz Name</option>
            <option value="subject">Subject</option>
          </select>
        </div>
      </div>
      <div class="filter-summary" v-if="hasActiveFilters">
        <span class="text-muted">
          Showing {{ filteredScores.length }} of {{ scores.length }} results
        </span>
        <button class="btn btn-sm btn-outline-secondary ms-3" @click="clearFilters">
          Clear Filters
        </button>
      </div>
    </div>

    <!-- Scores List -->
    <div class="scores-list">
      <div v-if="filteredScores.length === 0" class="no-results glass-card text-center">
        <i class="bi bi-inbox display-4 text-muted mb-3"></i>
        <h5 class="text-light">No quiz scores found</h5>
        <p class="text-muted">{{ searchQuery ? 'Try adjusting your search filters' : 'Take some quizzes to see your scores here!' }}</p>
        <router-link to="/user" class="btn btn-primary">
          <i class="bi bi-plus-circle me-2"></i>Take a Quiz
        </router-link>
      </div>

      <div v-else class="scores-grid">
        <div
          v-for="score in filteredScores"
          :key="score.id"
          class="score-card glass-card"
          @click="viewScoreDetails(score)"
        >
          <div class="score-header">
            <div class="quiz-info">
              <h6 class="quiz-title">{{ score.quizTitle }}</h6>
              <span class="quiz-subject">{{ score.subject }}</span>
            </div>
            <div class="score-badge" :class="getScoreClass(score.percentage)">
              {{ score.percentage }}%
            </div>
          </div>

          <div class="score-details">
            <div class="detail-row">
              <span class="detail-label">Score:</span>
              <span class="detail-value">{{ score.correctAnswers }}/{{ score.totalQuestions }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Time:</span>
              <span class="detail-value">{{ score.timeTaken }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Date:</span>
              <span class="detail-value">{{ formatDate(score.completedAt) }}</span>
            </div>
          </div>

          <div class="score-progress">
            <div class="progress" style="height: 6px;">
              <div 
                class="progress-bar" 
                :class="getProgressClass(score.percentage)"
                :style="{ width: score.percentage + '%' }"
              ></div>
            </div>
          </div>

          <div class="score-actions">
            <button class="btn btn-sm btn-outline-primary" @click.stop="retakeQuiz(score.quizId)">
              <i class="bi bi-arrow-clockwise me-1"></i>Retake
            </button>
            <button class="btn btn-sm btn-outline-info" @click.stop="viewScoreDetails(score)">
              <i class="bi bi-eye me-1"></i>Details
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Score Details Modal -->
    <BaseModal
      v-model="showDetailsModal"
      :title="`${selectedScore?.quizTitle} - Results`"
      size="lg"
    >
      <div v-if="selectedScore" class="score-details-modal">
        <div class="modal-header-stats">
          <div class="stat-card">
            <div class="stat-icon text-primary">
              <i class="bi bi-percent"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ selectedScore.percentage }}%</div>
              <div class="stat-label">Score</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon text-success">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ selectedScore.correctAnswers }}</div>
              <div class="stat-label">Correct</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon text-danger">
              <i class="bi bi-x-circle"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ selectedScore.incorrectAnswers }}</div>
              <div class="stat-label">Incorrect</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon text-info">
              <i class="bi bi-clock"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ selectedScore.timeTaken }}</div>
              <div class="stat-label">Time</div>
            </div>
          </div>
        </div>

        <div class="performance-analysis">
          <h6 class="text-light mb-3">Performance Analysis</h6>
          <div class="analysis-item">
            <strong>Grade:</strong> 
            <span :class="getGradeClass(selectedScore.percentage)">
              {{ getGrade(selectedScore.percentage) }}
            </span>
          </div>
          <div class="analysis-item">
            <strong>Completed:</strong> 
            {{ formatFullDate(selectedScore.completedAt) }}
          </div>
          <div class="analysis-item">
            <strong>Subject:</strong> 
            {{ selectedScore.subject }}
          </div>
          <div v-if="selectedScore.feedback" class="analysis-item feedback">
            <strong>Feedback:</strong>
            <p class="feedback-text">{{ selectedScore.feedback }}</p>
          </div>
        </div>
      </div>

      <template #footer>
        <button class="btn btn-outline-primary" @click="retakeQuiz(selectedScore.quizId)">
          <i class="bi bi-arrow-clockwise me-2"></i>Retake Quiz
        </button>
        <button class="btn btn-secondary" @click="showDetailsModal = false">
          Close
        </button>
      </template>
    </BaseModal>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseModal from '@/components/Modal.vue'

export default {
  name: 'ScoresView',
  components: {
    BaseModal
  },
  setup() {
    const router = useRouter()
    
    // Reactive data
    const scores = ref([])
    const searchQuery = ref('')
    const selectedSubject = ref('')
    const selectedDateRange = ref('')
    const sortBy = ref('date')
    const showDetailsModal = ref(false)
    const selectedScore = ref(null)

    // Computed properties
    const subjects = computed(() => {
      return [...new Set(scores.value.map(score => score.subject))]
    })

    const totalQuizzes = computed(() => scores.value.length)

    const averageScore = computed(() => {
      if (scores.value.length === 0) return 0
      const total = scores.value.reduce((sum, score) => sum + score.percentage, 0)
      return Math.round(total / scores.value.length)
    })

    const hasActiveFilters = computed(() => {
      return searchQuery.value || selectedSubject.value || selectedDateRange.value
    })

    const filteredScores = computed(() => {
      let filtered = [...scores.value]

      // Search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(score => 
          score.quizTitle.toLowerCase().includes(query) ||
          score.subject.toLowerCase().includes(query)
        )
      }

      // Subject filter
      if (selectedSubject.value) {
        filtered = filtered.filter(score => score.subject === selectedSubject.value)
      }

      // Date range filter
      if (selectedDateRange.value) {
        const now = new Date()
        const filterDate = new Date()
        
        switch (selectedDateRange.value) {
          case 'week':
            filterDate.setDate(now.getDate() - 7)
            break
          case 'month':
            filterDate.setMonth(now.getMonth() - 1)
            break
          case '3months':
            filterDate.setMonth(now.getMonth() - 3)
            break
          case 'year':
            filterDate.setFullYear(now.getFullYear() - 1)
            break
        }
        
        filtered = filtered.filter(score => new Date(score.completedAt) >= filterDate)
      }

      // Sort
      filtered.sort((a, b) => {
        switch (sortBy.value) {
          case 'score':
            return b.percentage - a.percentage
          case 'title':
            return a.quizTitle.localeCompare(b.quizTitle)
          case 'subject':
            return a.subject.localeCompare(b.subject)
          case 'date':
          default:
            return new Date(b.completedAt) - new Date(a.completedAt)
        }
      })

      return filtered
    })

    // Methods
    const loadScores = () => {
      // Mock data - replace with API call
      scores.value = [
        {
          id: 1,
          quizId: 1,
          quizTitle: 'JavaScript Fundamentals',
          subject: 'Web Development',
          percentage: 85,
          correctAnswers: 17,
          incorrectAnswers: 3,
          totalQuestions: 20,
          timeTaken: '25 min',
          completedAt: '2024-01-15T14:30:00',
          feedback: 'Great performance! You showed strong understanding of JavaScript fundamentals. Consider practicing more on async functions.'
        },
        {
          id: 2,
          quizId: 2,
          quizTitle: 'HTML & CSS Basics',
          subject: 'Web Development',
          percentage: 92,
          correctAnswers: 23,
          incorrectAnswers: 2,
          totalQuestions: 25,
          timeTaken: '20 min',
          completedAt: '2024-01-12T11:15:00',
          feedback: 'Excellent work! Your HTML and CSS knowledge is solid. Keep up the great work!'
        },
        {
          id: 3,
          quizId: 3,
          quizTitle: 'Python Basics',
          subject: 'Programming',
          percentage: 78,
          correctAnswers: 14,
          incorrectAnswers: 4,
          totalQuestions: 18,
          timeTaken: '30 min',
          completedAt: '2024-01-10T16:45:00',
          feedback: 'Good effort! Focus on practicing loops and data structures for better performance.'
        },
        {
          id: 4,
          quizId: 4,
          quizTitle: 'Database Design',
          subject: 'Computer Science',
          percentage: 65,
          correctAnswers: 13,
          incorrectAnswers: 7,
          totalQuestions: 20,
          timeTaken: '35 min',
          completedAt: '2024-01-08T09:20:00',
          feedback: 'Database concepts need more practice. Review normalization and relationships.'
        },
        {
          id: 5,
          quizId: 1,
          quizTitle: 'JavaScript Fundamentals',
          subject: 'Web Development',
          percentage: 90,
          correctAnswers: 18,
          incorrectAnswers: 2,
          totalQuestions: 20,
          timeTaken: '22 min',
          completedAt: '2024-01-05T13:10:00',
          feedback: 'Outstanding improvement! Your JavaScript skills have significantly improved.'
        }
      ]
    }

    const getScoreClass = (percentage) => {
      if (percentage >= 90) return 'score-excellent'
      if (percentage >= 80) return 'score-good'
      if (percentage >= 70) return 'score-fair'
      if (percentage >= 60) return 'score-poor'
      return 'score-fail'
    }

    const getProgressClass = (percentage) => {
      if (percentage >= 90) return 'bg-success'
      if (percentage >= 80) return 'bg-info'
      if (percentage >= 70) return 'bg-warning'
      return 'bg-danger'
    }

    const getGrade = (percentage) => {
      if (percentage >= 90) return 'A'
      if (percentage >= 80) return 'B'
      if (percentage >= 70) return 'C'
      if (percentage >= 60) return 'D'
      return 'F'
    }

    const getGradeClass = (percentage) => {
      if (percentage >= 90) return 'text-success'
      if (percentage >= 80) return 'text-info'
      if (percentage >= 70) return 'text-warning'
      return 'text-danger'
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      })
    }

    const formatFullDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const clearFilters = () => {
      searchQuery.value = ''
      selectedSubject.value = ''
      selectedDateRange.value = ''
    }

    const viewScoreDetails = (score) => {
      selectedScore.value = score
      showDetailsModal.value = true
    }

    const retakeQuiz = (quizId) => {
      router.push(`/quiz/${quizId}/take`)
    }

    // Lifecycle
    onMounted(() => {
      loadScores()
    })

    return {
      scores,
      searchQuery,
      selectedSubject,
      selectedDateRange,
      sortBy,
      showDetailsModal,
      selectedScore,
      subjects,
      totalQuizzes,
      averageScore,
      hasActiveFilters,
      filteredScores,
      getScoreClass,
      getProgressClass,
      getGrade,
      getGradeClass,
      formatDate,
      formatFullDate,
      clearFilters,
      viewScoreDetails,
      retakeQuiz
    }
  }
}
</script>

<style scoped>
.scores-view {
  padding: 2rem;
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(13, 110, 253, 0.1) 0%, rgba(108, 117, 125, 0.05) 100%);
  max-width: 1600px;
  margin: 0 auto;
}

.glass-card {
  background: rgba(35, 39, 43, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

.filters-section {
  margin-bottom: 2.5rem;
}

.scores-list {
  margin-top: 1rem;
}

.header-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0d6efd;
}

.stat-label {
  font-size: 0.9rem;
  color: #adb5bd;
}

.search-input-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #adb5bd;
  z-index: 10;
}

.search-input {
  padding-left: 2.5rem;
  background: rgba(35, 39, 43, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
}

.search-input:focus {
  background: rgba(35, 39, 43, 1);
  border-color: rgba(13, 110, 253, 0.5);
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  color: #f8f9fa;
}

.form-select {
  background: rgba(35, 39, 43, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
}

.form-select:focus {
  background: rgba(35, 39, 43, 1);
  border-color: rgba(13, 110, 253, 0.5);
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  color: #f8f9fa;
}

.scores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.score-card {
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 2rem;
  min-height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.score-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
  background: rgba(35, 39, 43, 0.8);
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.quiz-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #f8f9fa;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.quiz-subject {
  font-size: 1rem;
  color: #adb5bd;
  font-weight: 500;
}

.score-badge {
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  font-weight: 700;
  font-size: 1.25rem;
  min-width: 80px;
  text-align: center;
}

.score-excellent { background: rgba(25, 135, 84, 0.2); color: #198754; border: 1px solid rgba(25, 135, 84, 0.5); }
.score-good { background: rgba(13, 202, 240, 0.2); color: #0dcaf0; border: 1px solid rgba(13, 202, 240, 0.5); }
.score-fair { background: rgba(255, 193, 7, 0.2); color: #ffc107; border: 1px solid rgba(255, 193, 7, 0.5); }
.score-poor { background: rgba(253, 126, 20, 0.2); color: #fd7e14; border: 1px solid rgba(253, 126, 20, 0.5); }
.score-fail { background: rgba(220, 53, 69, 0.2); color: #dc3545; border: 1px solid rgba(220, 53, 69, 0.5); }

.score-details {
  margin-bottom: 1.5rem;
  flex: 1;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  padding: 0.5rem 0;
}

.detail-label {
  color: #adb5bd;
  font-size: 1rem;
  font-weight: 500;
}

.detail-value {
  color: #f8f9fa;
  font-weight: 600;
  font-size: 1rem;
}

.score-progress {
  margin-bottom: 1.5rem;
}

.score-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: auto;
}

.score-actions .btn {
  flex: 1;
  padding: 0.75rem 1rem;
  font-weight: 500;
}

.no-results {
  padding: 3rem;
}

.modal-header-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-icon {
  font-size: 1.5rem;
}

.performance-analysis .analysis-item {
  margin-bottom: 1rem;
  color: #f8f9fa;
}

.feedback {
  margin-top: 1.5rem;
}

.feedback-text {
  margin-top: 0.5rem;
  padding: 1rem;
  background: rgba(13, 110, 253, 0.1);
  border-radius: 0.5rem;
  border: 1px solid rgba(13, 110, 253, 0.2);
  color: #f8f9fa;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .scores-view {
    padding: 1rem;
  }
  
  .glass-card {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .header-stats {
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .scores-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .score-card {
    min-height: auto;
    padding: 1.5rem;
  }
  
  .quiz-title {
    font-size: 1.2rem;
  }
  
  .score-badge {
    font-size: 1.1rem;
    padding: 0.5rem 1rem;
    min-width: 70px;
  }
  
  .modal-header-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .score-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .score-actions .btn {
    padding: 0.75rem;
  }
}
</style> 