<template>
  <div class="scores-view">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-lg-3 col-md-4">
        <BaseSidebar user-role="user" />
      </div>
      
      <!-- Main Content -->
      <div class="col-lg-9 col-md-8">
        <div class="container-fluid px-4">
          <!-- Page Header -->
          <div class="page-header glass mb-4">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center">
                <button 
                  class="btn btn-outline-light me-3" 
                  @click="goToDashboard"
                >
                  <i class="bi bi-arrow-left me-2"></i>
                  Back to Dashboard
                </button>
                <div>
                  <h1 class="text-light mb-2">
                    <i class="bi bi-graph-up me-1"></i>
                    My Quiz Scores
                  </h1>
                  <p class="text-light mb-0">
                    Track your quiz performance and progress over time
                  </p>
                </div>
              </div>
              <div class="filter-controls">
                <select v-model="selectedSubject" class="form-select me-2" @change="fetchScores">
                  <option value="">All Subjects</option>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Performance Summary -->
          <div class="performance-summary mb-4">
            <div class="row">
              <div class="col-md-3 mb-3">
                <div class="stats-card glass">
                  <div class="stats-icon">
                    <i class="bi bi-clipboard-check text-primary"></i>
                  </div>
                  <div class="stats-content">
                    <h3 class="text-light">{{ totalAttempts }}</h3>
                    <p class="text-light">Total Attempts</p>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="stats-card glass">
                  <div class="stats-icon">
                    <i class="bi bi-percent text-success"></i>
                  </div>
                  <div class="stats-content">
                    <h3 class="text-light">{{ averageScore }}%</h3>
                    <p class="text-light">Average Score</p>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="stats-card glass">
                  <div class="stats-icon">
                    <i class="bi bi-trophy text-warning"></i>
                  </div>
                  <div class="stats-content">
                    <h3 class="text-light">{{ bestScore }}%</h3>
                    <p class="text-light">Best Score</p>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="stats-card glass">
                  <div class="stats-icon">
                    <i class="bi bi-check-circle text-info"></i>
                  </div>
                  <div class="stats-content">
                    <h3 class="text-light">{{ passedQuizzes }}</h3>
                    <p class="text-light">Quizzes Passed</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Scores List -->
          <div class="scores-list glass">
            <div class="card-body">
              <!-- Loading State -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary mb-3"></div>
                <p class="text-light">Loading your scores...</p>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="alert alert-danger glass-alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
              </div>

              <!-- Empty State -->
              <div v-else-if="scores.length === 0" class="empty-state text-center py-5">
                <i class="bi bi-graph-up display-1 text-light mb-3"></i>
                <h4 class="text-light">No Quiz Attempts Yet</h4>
                <p class="text-light">
                  Start taking quizzes to see your scores and track your progress!
                </p>
                <button class="btn btn-primary mt-3" @click="goToDashboard">
                  <i class="bi bi-play me-2"></i>
                  Take a Quiz
                </button>
              </div>

              <!-- Scores Table -->
              <div v-else>
                <div class="table-responsive">
                  <table class="table table-dark table-glass">
                    <thead>
                      <tr>
                        <th><i class="bi bi-calendar me-2"></i>Date</th>
                        <th><i class="bi bi-clipboard-check me-2"></i>Quiz</th>
                        <th><i class="bi bi-book me-2"></i>Subject</th>
                        <th><i class="bi bi-percent me-2"></i>Score</th>
                        <th><i class="bi bi-clock me-2"></i>Time Taken</th>
                        <th><i class="bi bi-check-circle me-2"></i>Status</th>
                        <th><i class="bi bi-gear me-2"></i>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="score in scores" :key="score.id" class="table-row-glass">
                        <td>
                          <span class="text-light">{{ formatDate(score.time_stamp_of_attempt) }}</span>
                        </td>
                        <td>
                          <strong class="text-light">{{ score.quiz_name || 'Quiz' }}</strong>
                          <br>
                          <small class="text-light">{{ score.chapter_name || 'Chapter' }}</small>
                        </td>
                        <td>
                          <span class="text-light">{{ score.subject_name || 'Subject' }}</span>
                        </td>
                        <td>
                          <div class="score-display">
                            <span class="score-percentage" :class="getScoreClass(score.percentage)">
                              {{ Math.round(score.percentage) }}%
                            </span>
                            <small class="text-light d-block">
                              {{ score.total_scored }}/{{ score.total_possible_score }} points
                            </small>
                          </div>
                        </td>
                        <td>
                          <span class="badge bg-info">
                            {{ formatTime(score.time_taken) }}
                          </span>
                        </td>
                        <td>
                          <span :class="score.passed ? 'badge bg-success' : 'badge bg-danger'">
                            {{ score.passed ? 'Passed' : 'Failed' }}
                          </span>
                        </td>
                        <td>
                          <div class="btn-group" role="group">
                            <button 
                              class="btn btn-sm btn-outline-light"
                              @click="viewDetails(score)"
                              title="View Details"
                            >
                              <i class="bi bi-eye"></i>
                            </button>
                            <button 
                              class="btn btn-sm btn-outline-primary"
                              @click="retakeQuiz(score.quiz_id)"
                              title="Retake Quiz"
                            >
                              <i class="bi bi-arrow-clockwise"></i>
                            </button>
                            <button 
                              class="btn btn-sm btn-outline-info"
                              @click="viewQuizResponses(score)"
                              title="View Quiz Responses"
                            >
                              <i class="bi bi-list-task"></i>
                            </button>
                          </div>
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
    </div>

    <!-- Score Details Modal -->
    <div 
      class="modal fade" 
      id="scoreDetailsModal" 
      tabindex="-1"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass">
          <div class="modal-header">
            <h5 class="modal-title text-light">Quiz Score Details</h5>
            <button 
              type="button" 
              class="btn-close btn-close-white" 
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body" v-if="selectedScore">
            <div class="score-overview mb-4">
              <div class="row">
                <div class="col-md-6">
                  <h6 class="text-light">Quiz Information</h6>
                  <ul class="list-unstyled text-light">
                    <li><strong>Quiz:</strong> {{ selectedScore.quiz_name || 'Quiz' }}</li>
                    <li><strong>Chapter:</strong> {{ selectedScore.chapter_name || 'Chapter' }}</li>
                    <li><strong>Subject:</strong> {{ selectedScore.subject_name || 'Subject' }}</li>
                    <li><strong>Date:</strong> {{ formatDate(selectedScore.time_stamp_of_attempt) }}</li>
                  </ul>
                </div>
                <div class="col-md-6">
                  <h6 class="text-light">Performance</h6>
                  <ul class="list-unstyled text-light">
                    <li><strong>Score:</strong> {{ selectedScore.total_scored }}/{{ selectedScore.total_possible_score }} points</li>
                    <li><strong>Percentage:</strong> {{ Math.round(selectedScore.percentage) }}%</li>
                    <li><strong>Time Taken:</strong> {{ formatTime(selectedScore.time_taken) }}</li>
                    <li><strong>Status:</strong> 
                      <span :class="selectedScore.passed ? 'text-success' : 'text-danger'">
                        {{ selectedScore.passed ? 'Passed' : 'Failed' }}
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="performance-chart mb-4">
              <h6 class="text-light mb-3">Score Breakdown</h6>
              <div class="progress mb-2" style="height: 30px;">
                <div 
                  class="progress-bar" 
                  :class="selectedScore.passed ? 'bg-success' : 'bg-danger'"
                  :style="{ width: selectedScore.percentage + '%' }"
                >
                  {{ Math.round(selectedScore.percentage) }}%
                </div>
              </div>
              <div class="d-flex justify-content-between text-light">
                <span>0%</span>
                <span>{{ Math.round(selectedScore.percentage) }}%</span>
                <span>100%</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button 
              type="button" 
              class="btn btn-outline-light" 
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="retakeQuizFromModal"
            >
              <i class="bi bi-arrow-clockwise me-2"></i>
              Retake Quiz
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Modal } from 'bootstrap'
import ScoreService from '@/services/score-service'
import BaseSidebar from '@/components/BaseSidebar.vue'

export default {
  name: 'ScoresView',
  components: {
    BaseSidebar
  },
  setup() {
    const router = useRouter()
    const scores = ref([])
    const subjects = ref([])
    const selectedSubject = ref('')
    const selectedScore = ref(null)
    const loading = ref(false)
    const error = ref(null)

    const totalAttempts = computed(() => scores.value.length)

    const averageScore = computed(() => {
      if (scores.value.length === 0) return 0
      const total = scores.value.reduce((sum, score) => sum + score.percentage, 0)
      return Math.round(total / scores.value.length)
    })

    const bestScore = computed(() => {
      if (scores.value.length === 0) return 0
      return Math.round(Math.max(...scores.value.map(score => score.percentage)))
    })

    const passedQuizzes = computed(() => {
      return scores.value.filter(score => score.passed).length
    })

    const fetchSubjects = async () => {
      try {
        const response = await ScoreService.getUserScores()
        if (response.success) {
          // Extract unique subjects from the scores
          const uniqueSubjects = new Map()
          response.data.forEach(score => {
            if (score.subject_id && score.subject_name) {
              uniqueSubjects.set(score.subject_id, {
                id: score.subject_id,
                name: score.subject_name
              })
            }
          })
          subjects.value = Array.from(uniqueSubjects.values())
        }
      } catch (err) {
        console.error('Failed to fetch subjects:', err)
      }
    }

    const fetchScores = async () => {
      loading.value = true
      error.value = null

      try {
        // Get all scores for the current user
        const response = await ScoreService.getUserScores()
        
        if (response && response.data) {
          // Ensure we always have an array to work with
          let scoreData = Array.isArray(response.data) ? response.data : [];
          
          // Apply subject filter if selected
          if (selectedSubject.value && scoreData.length > 0) {
            scoreData = scoreData.filter(score => score.subject_id == selectedSubject.value);
          }
          
          scores.value = scoreData;
          console.log('✅ Scores fetched:', scores.value);
          
          // If no scores found after filtering
          if (scores.value.length === 0) {
            if (selectedSubject.value) {
              error.value = 'No quiz results found for the selected subject.';
            } else {
              error.value = 'No quiz results found. Start taking quizzes to see your scores!';
            }
          } else {
            error.value = null;
          }
        } else {
          console.log('No scores found or empty response:', response);
          scores.value = [];
          error.value = 'No quiz results found. Start taking quizzes to see your scores!';
        }
      } catch (err) {
        console.error('Failed to fetch scores:', err);
        error.value = err.response?.data?.message || 'Failed to load scores';
        scores.value = [];
      } finally {
        loading.value = false;
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatTime = (seconds) => {
      if (!seconds) return 'N/A'
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes}m ${remainingSeconds}s`
    }

    const getScoreClass = (percentage) => {
      if (percentage >= 80) return 'text-success'
      if (percentage >= 60) return 'text-warning'
      return 'text-danger'
    }

    const viewDetails = async (score) => {
      selectedScore.value = score
      try {
        // Get detailed information about this score
        const response = await ScoreService.getScoreDetails(score.id)
        if (response.success) {
          selectedScore.value = { ...selectedScore.value, ...response.data }
        }
      } catch (err) {
        console.error('Error fetching score details:', err)
      }
      const modal = new Modal(document.getElementById('scoreDetailsModal'))
      modal.show()
    }

    const retakeQuiz = (quizId) => {
      router.push(`/user/quiz/${quizId}`)
    }

    const retakeQuizFromModal = () => {
      if (selectedScore.value) {
        const modal = Modal.getInstance(document.getElementById('scoreDetailsModal'))
        modal?.hide()
        retakeQuiz(selectedScore.value.quiz_id)
      }
    }
    
    const viewQuizResponses = async (score) => {
      try {
        // First, save the score data to localStorage so it can be used by the result view
        // Format the data in the way expected by the QuizResultView
        const quizResult = {
          quiz: {
            id: score.quiz_id,
            title: score.quiz_name || 'Quiz',
            totalPoints: score.total_possible_score || 0,
            passingScore: 70,
            questions: score.questions || []
          },
          result: {
            score: score.total_scored || 0,
            percentage: score.percentage || 0,
            correctAnswers: score.correct_answers || 0,
            incorrectAnswers: score.incorrect_answers || 0,
            unanswered: score.unanswered || 0,
            passed: score.passed || false,
            grade: getGrade(score.percentage),
            gradeDescription: getGradeDescription(score.percentage),
            timeSpent: formatTime(score.time_taken)
          },
          userAnswers: score.user_answers || {},
          timestamp: Date.now()
        };
        
        // Save to localStorage with the attempt ID as part of the key
        const resultKey = `quiz_result_${score.id}`;
        localStorage.setItem(resultKey, JSON.stringify(quizResult));
        console.log(`Score data saved to localStorage with key: ${resultKey}`);
        
        // Try to get more detailed score data if available
        try {
          const detailsResponse = await ScoreService.getScoreDetails(score.id);
          if (detailsResponse.success && detailsResponse.data) {
            // Update the localStorage data with more details if available
            const updatedQuizResult = {
              ...quizResult,
              quiz: {
                ...quizResult.quiz,
                questions: detailsResponse.data.questions || []
              },
              userAnswers: detailsResponse.data.user_answers || {}
            };
            localStorage.setItem(resultKey, JSON.stringify(updatedQuizResult));
            console.log(`Updated score data in localStorage with more details`);
          }
        } catch (err) {
          console.error('Error fetching detailed score data:', err);
          // Continue with navigation even if detailed data fetch fails
        }
        
        // Navigate to the result page
        router.push(`/user/quiz/${score.quiz_id}/result?attempt=${score.id}`);
      } catch (err) {
        console.error('Error preparing quiz response view:', err);
        // Show error message to user
        error.value = 'Failed to load quiz responses. Please try again.';
      }
    }
    
    // Helper functions for grade calculation
    const getGrade = (percentage) => {
      if (percentage >= 90) return 'A';
      if (percentage >= 80) return 'B';
      if (percentage >= 70) return 'C';
      if (percentage >= 60) return 'D';
      return 'F';
    }
    
    const getGradeDescription = (percentage) => {
      if (percentage >= 90) return 'Excellent! Outstanding performance!';
      if (percentage >= 80) return 'Good job! Above average performance!';
      if (percentage >= 70) return 'Fair performance. Room for improvement.';
      if (percentage >= 60) return 'Below average. Consider reviewing the material.';
      return 'Poor performance. Please review and retake.';
    }

    const goToDashboard = () => {
      router.push('/user/dashboard')
    }

    onMounted(() => {
      fetchSubjects()
      fetchScores()
    })

    return {
      scores,
      subjects,
      selectedSubject,
      selectedScore,
      loading,
      error,
      totalAttempts,
      averageScore,
      bestScore,
      passedQuizzes,
      fetchScores,
      formatDate,
      formatTime,
      getScoreClass,
      viewDetails,
      retakeQuiz,
      retakeQuizFromModal,
      viewQuizResponses,
      goToDashboard
    }
  }
}
</script>

<style scoped>
.scores-view {
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

.glass, .page-header, .scores-list, .stats-card {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
}

.stats-card {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.stats-card:hover {
  background: rgba(35, 39, 43, 0.8);
  border-color: rgba(255, 255, 255, 0.2);
}

.stats-icon {
  font-size: 2.5rem;
  margin-right: 1rem;
  flex-shrink: 0;
}

.stats-content h3 {
  margin: 0;
  font-size: 2rem;
  font-weight: bold;
}

.stats-content p {
  margin: 0;
  font-size: 0.875rem;
}

.scores-list {
  background: rgba(35, 39, 43, 0.7);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  margin-bottom: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.table-dark {
  background: transparent !important;
  color: rgba(255, 255, 255, 0.9) !important;
  margin-bottom: 0;
}

.table-dark th {
  background: rgba(20, 25, 35, 0.5) !important;
  color: rgba(255, 255, 255, 0.9) !important;
  font-weight: 600;
  border-bottom: none !important;
  padding: 1rem 1.25rem;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table-dark td {
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
  vertical-align: middle;
}

.table-row-glass {
  transition: all 0.3s ease;
  background: rgba(35, 39, 43, 0.4);
}

.table-row-glass:hover {
  background: rgba(50, 60, 80, 0.3) !important;
}

.score-display {
  text-align: center;
}

.score-percentage {
  font-size: 1.1rem;
  font-weight: 700;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.text-success {
  color: #00ca72 !important;
}

.text-warning {
  color: #ffb100 !important;
}

.text-danger {
  color: #ff5252 !important;
}

.badge {
  padding: 0.5rem 0.75rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  border-radius: 0.5rem;
}

.filter-controls .form-select {
  background: rgba(35, 39, 43, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  min-width: 200px;
}

.filter-controls .form-select:focus {
  background: rgba(35, 39, 43, 0.8);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.1);
}

.modal-content.glass {
  background: rgba(35, 39, 43, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
}

.glass-alert {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  backdrop-filter: blur(10px);
}

.empty-state {
  color: rgba(255, 255, 255, 0.7);
}

.performance-chart .progress {
  background: rgba(255, 255, 255, 0.1);
}
</style> 