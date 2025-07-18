<template>
  <div class="quiz-taking-view">
    <!-- Loading State -->
    <div v-if="!quiz.questions?.length" class="loading-state glass-card text-center">
      <div class="spinner-border text-primary mb-3" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <h5 class="text-light">Loading Quiz...</h5>
      <p class="text-muted">Please wait while we prepare your quiz.</p>
    </div>

    <!-- Quiz Content -->
    <div v-else>
    <!-- Quiz Header -->
    <div class="quiz-header glass-card mb-4">
      <div class="d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center gap-3">
          <button 
            class="btn btn-outline-light d-flex align-items-center gap-2"
            @click="goBack"
          >
            <i class="bi bi-arrow-left"></i>
            Back
          </button>
          <div class="quiz-info">
            <h2 class="h4 text-light mb-1">{{ quiz.title }}</h2>
            <p class="text-muted mb-0">{{ quiz.description }}</p>
            <small class="text-info">{{ quiz.chapterTitle }} • {{ quiz.questions?.length || 0 }} Questions • {{ quiz.totalPoints }} Points</small>
          </div>
        </div>
        <div class="quiz-timer">
          <QuizTimer 
            :timeLimit="quiz.timeLimit" 
            :isActive="isQuizActive"
            @timeUp="handleTimeUp"
            @timeUpdate="handleTimeUpdate"
          />
        </div>
      </div>
      
      <!-- Progress Bar -->
      <div class="quiz-progress mt-3">
        <div class="progress-info mb-2">
          <span class="text-light">Question {{ currentQuestionIndex + 1 }} of {{ quiz.questions?.length || 0 }}</span>
          <span class="text-muted">{{ answeredCount }} answered</span>
        </div>
        <div class="progress" style="height: 8px;">
          <div 
            class="progress-bar bg-primary" 
            :style="{ width: progressPercentage + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Question Navigation Grid -->
    <div class="question-nav glass-card mb-4">
      <div class="nav-header mb-3">
        <h6 class="text-light mb-0">Question Navigator</h6>
      </div>
      <div class="question-grid">
        <button
          v-for="(question, index) in quiz.questions || []"
          :key="question.id"
          class="question-nav-btn"
          :class="{
            'current': index === currentQuestionIndex,
            'answered': userAnswers[question.id] !== undefined,
            'unanswered': userAnswers[question.id] === undefined
          }"
          @click="goToQuestion(index)"
        >
          {{ index + 1 }}
        </button>
      </div>
    </div>

    <!-- Main Question Area -->
    <div class="question-area glass-card mb-4">
      <div v-if="currentQuestion" class="question-content">
        <!-- Question Header -->
        <div class="question-header mb-4">
          <div class="d-flex justify-content-between align-items-start">
            <div class="question-meta">
              <span class="badge bg-primary me-2">{{ currentQuestion.type.replace('_', ' ').toUpperCase() }}</span>
              <span class="badge bg-secondary me-2">{{ currentQuestion.difficulty.toUpperCase() }}</span>
              <span class="badge bg-info">{{ currentQuestion.points }} pts</span>
            </div>
            <div class="question-number">
              <span class="text-primary h5">Q{{ currentQuestionIndex + 1 }}</span>
            </div>
          </div>
        </div>

        <!-- Question Content -->
        <div class="question-text mb-4">
          <h5 class="text-light">{{ currentQuestion.content }}</h5>
        </div>

        <!-- Answer Options -->
        <div class="answer-options">
          <!-- Multiple Choice -->
          <div v-if="currentQuestion.type === 'multiple_choice'" class="multiple-choice-options">
            <div
              v-for="(option, index) in currentQuestion.options"
              :key="index"
              class="option-item mb-3"
              @click="selectAnswer(index)"
            >
              <div class="form-check">
                <input
                  :id="`option-${index}`"
                  v-model="userAnswers[currentQuestion.id]"
                  class="form-check-input"
                  type="radio"
                  :value="index"
                  name="currentAnswer"
                >
                <label :for="`option-${index}`" class="form-check-label text-light">
                  <span class="option-letter">{{ String.fromCharCode(65 + index) }}.</span>
                  {{ option.text }}
                </label>
              </div>
            </div>
          </div>

          <!-- True/False -->
          <div v-if="currentQuestion.type === 'true_false'" class="true-false-options">
            <div class="option-item mb-3" @click="selectAnswer('true')">
              <div class="form-check">
                <input
                  id="option-true"
                  v-model="userAnswers[currentQuestion.id]"
                  class="form-check-input"
                  type="radio"
                  value="true"
                  name="currentAnswer"
                >
                <label for="option-true" class="form-check-label text-light">
                  <span class="option-letter">A.</span>
                  True
                </label>
              </div>
            </div>
            <div class="option-item mb-3" @click="selectAnswer('false')">
              <div class="form-check">
                <input
                  id="option-false"
                  v-model="userAnswers[currentQuestion.id]"
                  class="form-check-input"
                  type="radio"
                  value="false"
                  name="currentAnswer"
                >
                <label for="option-false" class="form-check-label text-light">
                  <span class="option-letter">B.</span>
                  False
                </label>
              </div>
            </div>
          </div>


        </div>
      </div>
    </div>

    <!-- Navigation Controls -->
    <div class="quiz-controls glass-card">
      <div class="d-flex justify-content-between align-items-center">
        <button
          class="btn btn-outline-secondary"
          :disabled="currentQuestionIndex === 0"
          @click="previousQuestion"
        >
          <i class="bi bi-chevron-left me-2"></i>Previous
        </button>

        <div class="control-center">
          <button class="btn btn-outline-info me-3" @click="saveProgress">
            <i class="bi bi-save me-2"></i>Save Progress
          </button>
          <button class="btn btn-warning" @click="showSubmitConfirm">
            <i class="bi bi-check-circle me-2"></i>Submit Quiz
          </button>
        </div>

        <button
          class="btn btn-primary"
          @click="nextQuestion"
        >
          {{ currentQuestionIndex === (quiz.questions?.length || 1) - 1 ? 'Review' : 'Next' }}
          <i class="bi bi-chevron-right ms-2"></i>
        </button>
      </div>
    </div>

    <!-- Submit Confirmation Modal -->
    <BaseModal
      v-model="showSubmitModal"
      title="Submit Quiz"
      size="md"
    >
      <div class="submit-confirmation">
        <div class="text-center mb-4">
          <i class="bi bi-exclamation-triangle text-warning" style="font-size: 3rem;"></i>
          <h5 class="text-light mt-3">Are you sure you want to submit?</h5>
          <p class="text-muted">Once submitted, you cannot change your answers.</p>
        </div>
        
        <div class="quiz-summary">
          <div class="summary-item">
            <span class="text-muted">Total Questions:</span>
            <span class="text-light">{{ quiz.questions?.length || 0 }}</span>
          </div>
          <div class="summary-item">
            <span class="text-muted">Answered:</span>
            <span class="text-light">{{ answeredCount }}</span>
          </div>
          <div class="summary-item">
            <span class="text-muted">Unanswered:</span>
            <span class="text-warning">{{ (quiz.questions?.length || 0) - answeredCount }}</span>
          </div>
          <div class="summary-item">
            <span class="text-muted">Time Remaining:</span>
            <span class="text-info">{{ formattedTimeRemaining }}</span>
          </div>
        </div>
      </div>
      
      <template #footer>
        <button class="btn btn-secondary me-3" @click="showSubmitModal = false">
          Continue Quiz
        </button>
        <button class="btn btn-success" @click="submitQuiz">
          <i class="bi bi-check-circle me-2"></i>Submit Final Answers
        </button>
      </template>
    </BaseModal>

    <!-- Auto-save Indicator -->
    <div v-if="autoSaving" class="auto-save-indicator">
      <i class="bi bi-cloud-upload text-info me-2"></i>
      <span class="text-info">Saving...</span>
    </div>
    </div> <!-- End Quiz Content -->
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import QuizTimer from '@/components/QuizTimer.vue'
import BaseModal from '@/components/Modal.vue'

export default {
  name: 'QuizTakingView',
  components: {
    QuizTimer,
    BaseModal
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // Reactive data
    const quiz = ref({})
    const currentQuestionIndex = ref(0)
    const userAnswers = ref({})
    const isQuizActive = ref(true)
    const showSubmitModal = ref(false)
    const autoSaving = ref(false)
    const timeRemaining = ref(0)

    // Computed properties
    const currentQuestion = computed(() => 
      quiz.value.questions ? quiz.value.questions[currentQuestionIndex.value] : null
    )

    const answeredCount = computed(() => 
      Object.keys(userAnswers.value).length
    )

    const progressPercentage = computed(() => 
      quiz.value.questions?.length ? (answeredCount.value / quiz.value.questions.length) * 100 : 0
    )

    const formattedTimeRemaining = computed(() => {
      const minutes = Math.floor(timeRemaining.value / 60)
      const seconds = timeRemaining.value % 60
      return `${minutes}:${seconds.toString().padStart(2, '0')}`
    })

    // Methods
    const loadQuiz = () => {
      // Dummy data - replace with API call
      quiz.value = {
        id: route.params.id,
        title: 'JavaScript Fundamentals Quiz',
        description: 'Test your knowledge of JavaScript basics and concepts',
        chapterTitle: 'JavaScript Basics',
        timeLimit: 30, // minutes
        totalPoints: 10,
        questions: [
          {
            id: 1,
            type: 'multiple_choice',
            difficulty: 'easy',
            points: 2,
            content: 'What is the correct way to declare a variable in JavaScript?',
            options: [
              { text: 'var myVariable;' },
              { text: 'variable myVariable;' },
              { text: 'v myVariable;' },
              { text: 'declare myVariable;' }
            ],
            correctAnswer: 0
          },
          {
            id: 2,
            type: 'true_false',
            difficulty: 'easy',
            points: 2,
            content: 'JavaScript is a case-sensitive language.',
            correctAnswer: 'true'
          },
          {
            id: 3,
            type: 'multiple_choice',
            difficulty: 'medium',
            points: 3,
            content: 'Which of the following is NOT a JavaScript data type?',
            options: [
              { text: 'undefined' },
              { text: 'number' },
              { text: 'boolean' },
              { text: 'float' }
            ],
            correctAnswer: 3
          },
          {
            id: 4,
            type: 'multiple_choice',
            difficulty: 'medium',
            points: 2,
            content: 'What does the typeof operator return for an array in JavaScript?',
            options: [
              { text: 'array' },
              { text: 'object' },
              { text: 'list' },
              { text: 'collection' }
            ],
            correctAnswer: 1
          },
          {
            id: 5,
            type: 'true_false',
            difficulty: 'easy',
            points: 1,
            content: 'In JavaScript, the == operator performs strict equality comparison.',
            correctAnswer: 'false'
          }
        ]
      }
      
      // Initialize user answers
      quiz.value.questions?.forEach(question => {
        userAnswers.value[question.id] = undefined
      })
    }

    const goToQuestion = (index) => {
      currentQuestionIndex.value = index
    }

    const selectAnswer = (answer) => {
      userAnswers.value[currentQuestion.value.id] = answer
      autoSave()
    }

    const nextQuestion = () => {
      if (currentQuestionIndex.value < (quiz.value.questions?.length || 1) - 1) {
        currentQuestionIndex.value++
      }
    }

    const previousQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--
      }
    }

    const autoSave = () => {
      autoSaving.value = true
      // Simulate auto-save
      setTimeout(() => {
        autoSaving.value = false
      }, 1000)
    }

    const saveProgress = () => {
      autoSave()
      // Could show a toast notification here
    }

    const showSubmitConfirm = () => {
      showSubmitModal.value = true
    }

    const submitQuiz = () => {
      // Calculate score and navigate to results
      const result = calculateScore()
      
      // Navigate to results page with score data
      router.push({
        name: 'QuizResult',
        params: { id: quiz.value.id },
        query: { 
          score: result.score,
          percentage: result.percentage,
          totalQuestions: quiz.value.questions?.length || 0,
          correctAnswers: result.correctAnswers,
          answers: JSON.stringify(userAnswers.value)
        }
      })
    }

    const calculateScore = () => {
      let score = 0
      let correctAnswers = 0
      
              quiz.value.questions?.forEach(question => {
        const userAnswer = userAnswers.value[question.id]
        if (userAnswer !== undefined && userAnswer !== null) {
          // For multiple choice, check if the selected index matches correct answer
          if (question.type === 'multiple_choice') {
            if (parseInt(userAnswer) === question.correctAnswer) {
              score += question.points
              correctAnswers++
            }
          } 
          // For true/false, check if the selected string matches correct answer
          else if (question.type === 'true_false') {
            if (userAnswer.toString() === question.correctAnswer.toString()) {
              score += question.points
              correctAnswers++
            }
          }
        }
      })
      
      const percentage = Math.round((score / quiz.value.totalPoints) * 100)
      
      return { score, percentage, correctAnswers }
    }

    const handleTimeUp = () => {
      isQuizActive.value = false
      submitQuiz()
    }

    const handleTimeUpdate = (seconds) => {
      timeRemaining.value = seconds
    }

    const goBack = () => {
      router.back()
    }

    // Lifecycle
    onMounted(() => {
      loadQuiz()
    })

    // Prevent page refresh during quiz
    onBeforeUnmount(() => {
      window.removeEventListener('beforeunload', handleBeforeUnload)
    })

    const handleBeforeUnload = (e) => {
      if (isQuizActive.value) {
        e.preventDefault()
        e.returnValue = ''
      }
    }

    onMounted(() => {
      window.addEventListener('beforeunload', handleBeforeUnload)
    })

    return {
      quiz,
      currentQuestionIndex,
      currentQuestion,
      userAnswers,
      isQuizActive,
      showSubmitModal,
      autoSaving,
      answeredCount,
      progressPercentage,
      formattedTimeRemaining,
      goToQuestion,
      selectAnswer,
      nextQuestion,
      previousQuestion,
      autoSave,
      saveProgress,
      showSubmitConfirm,
      submitQuiz,
      handleTimeUp,
      handleTimeUpdate,
      goBack
    }
  }
}
</script>

<style scoped>
.quiz-taking-view {
  padding: 2rem;
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(13, 110, 253, 0.1) 0%, rgba(108, 117, 125, 0.05) 100%);
}

.loading-state {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.glass-card {
  background: rgba(35, 39, 43, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
}

.quiz-header {
  position: sticky;
  top: 2rem;
  z-index: 100;
}

.quiz-timer {
  text-align: center;
}

.progress {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
}

.question-nav {
  padding: 1rem;
}

.question-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 0.5rem;
}

.question-nav-btn {
  width: 40px;
  height: 40px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.question-nav-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.question-nav-btn.current {
  background: rgba(13, 110, 253, 0.8);
  border-color: #0d6efd;
}

.question-nav-btn.answered {
  background: rgba(25, 135, 84, 0.6);
  border-color: #198754;
}

.question-nav-btn.unanswered {
  background: rgba(220, 53, 69, 0.2);
  border-color: rgba(220, 53, 69, 0.5);
}

.question-area {
  min-height: 400px;
}

.option-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(13, 110, 253, 0.3);
}

.option-letter {
  font-weight: 600;
  color: #0d6efd;
  margin-right: 0.5rem;
}

.essay-textarea {
  background: rgba(35, 39, 43, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
  border-radius: 0.5rem;
}

.essay-textarea:focus {
  background: rgba(35, 39, 43, 1);
  border-color: rgba(13, 110, 253, 0.5);
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  color: #f8f9fa;
}

.quiz-controls {
  position: sticky;
  bottom: 2rem;
  z-index: 100;
}

.submit-confirmation .summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.25rem;
}

.auto-save-indicator {
  position: fixed;
  top: 1rem;
  right: 1rem;
  background: rgba(35, 39, 43, 0.9);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 1000;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

@media (max-width: 768px) {
  .quiz-taking-view {
    padding: 1rem;
  }
  
  .question-grid {
    grid-template-columns: repeat(auto-fill, minmax(35px, 1fr));
  }
  
  .question-nav-btn {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
}
</style> 