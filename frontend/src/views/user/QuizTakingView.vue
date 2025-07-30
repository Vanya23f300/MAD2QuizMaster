<template>
  <div class="quiz-taking">
    <div class="container-fluid px-4">
      <!-- Quiz Header -->
      <div class="quiz-header glass mb-4" v-if="quizData">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h1 class="text-light mb-2">{{ quizData.name }}</h1>
            <p class="text-light mb-0">
              {{ quizData.chapter_name }} • {{ quizData.subject_name }}
            </p>
      </div>
          <div class="quiz-timer">
            <div class="timer-display" :class="{ 'timer-warning': timeRemaining <= 300 }">
              <i class="bi bi-clock me-2"></i>
              {{ formatTime(timeRemaining) }}
    </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-light">{{ loadingMessage }}</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger glass-alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <div class="mt-3">
          <button class="btn btn-outline-light" @click="goBack">
            <i class="bi bi-arrow-left me-2"></i>
            Back to Dashboard
          </button>
        </div>
      </div>
      
      <!-- Quiz Content -->
      <div v-else-if="quizData && !quizSubmitted" class="quiz-content">
      <!-- Progress Bar -->
        <div class="progress-section glass mb-4">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-light">
              Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}
            </span>
            <span class="text-light">
              {{ Math.round(((currentQuestionIndex + 1) / questions.length) * 100) }}% Complete
            </span>
        </div>
          <div class="progress quiz-progress">
          <div 
              class="progress-bar" 
              :style="{ width: ((currentQuestionIndex + 1) / questions.length) * 100 + '%' }"
          ></div>
          </div>
        </div>

        <!-- Question Card -->
        <div class="question-card glass mb-4" v-if="currentQuestion">
          <div class="question-header mb-4">
            <div class="d-flex justify-content-between align-items-start">
              <div class="question-info flex-grow-1">
                <div class="d-flex align-items-center mb-3">
                  <span class="badge bg-primary me-2">Q{{ currentQuestionIndex + 1 }}</span>
                  <span class="badge bg-info">{{ currentQuestion.marks }} {{ currentQuestion.marks === 1 ? 'point' : 'points' }}</span>
                </div>
                <h3 class="text-light mb-0">{{ currentQuestion.question_statement }}</h3>
        </div>
      </div>
    </div>

          <!-- Options -->
          <div class="options-section">
            <div class="row">
              <div class="col-md-6 mb-3" v-for="(option, index) in currentQuestion.options" :key="index">
                <div 
                  class="option-card" 
                  :class="{ 'selected': selectedAnswers[currentQuestion.id] === (index + 1) }"
                  @click="selectAnswer(currentQuestion.id, index + 1)"
                >
                  <div class="option-content">
                    <div class="option-letter">{{ String.fromCharCode(65 + index) }}</div>
                    <div class="option-text">{{ option }}</div>
                    <div class="option-check">
                      <i class="bi bi-check-circle-fill" v-if="selectedAnswers[currentQuestion.id] === (index + 1)"></i>
                      <i class="bi bi-circle" v-else></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
      </div>

        <!-- Navigation -->
        <div class="quiz-navigation glass">
          <div class="d-flex justify-content-between align-items-center">
            <button 
              class="btn btn-outline-light"
              @click="previousQuestion"
              :disabled="currentQuestionIndex === 0"
            >
              <i class="bi bi-arrow-left me-2"></i>
              Previous
            </button>

            <div class="question-indicators">
        <button
                v-for="(question, index) in questions"
          :key="question.id"
                class="question-indicator"
          :class="{
            'current': index === currentQuestionIndex,
                  'answered': selectedAnswers[question.id],
                  'unanswered': !selectedAnswers[question.id]
          }"
          @click="goToQuestion(index)"
        >
          {{ index + 1 }}
        </button>
    </div>

            <div>
              <button 
                v-if="currentQuestionIndex < questions.length - 1"
                class="btn btn-primary me-2"
                @click="nextQuestion"
              >
                Next
                <i class="bi bi-arrow-right ms-2"></i>
              </button>
              <button 
                v-else
                class="btn btn-success"
                @click="showSubmitConfirm"
              >
                Submit Quiz
                <i class="bi bi-check-circle ms-2"></i>
              </button>
            </div>
            </div>
          </div>
        </div>

      <!-- Quiz Results -->
      <div v-else-if="quizSubmitted && quizResults" class="quiz-results">
        <div class="results-card glass text-center">
          <div class="results-icon mb-4">
            <i class="bi bi-check-circle-fill text-success display-1" v-if="quizResults.passed"></i>
            <i class="bi bi-x-circle-fill text-danger display-1" v-else></i>
        </div>

          <h2 class="text-light mb-3">
            {{ quizResults.passed ? 'Congratulations!' : 'Quiz Completed' }}
          </h2>
          
          <p class="text-light mb-4">
            {{ quizResults.passed ? 'You have successfully passed the quiz!' : 'Keep practicing to improve your score!' }}
          </p>

          <!-- Score Details -->
          <div class="score-details mb-4">
            <div class="row">
              <div class="col-md-3 mb-3">
                <div class="score-metric">
                  <h3 class="text-primary">{{ Math.round(quizResults.percentage) }}%</h3>
                  <p class="text-light">Final Score</p>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="score-metric">
                  <h3 class="text-info">{{ quizResults.correct_answers }}</h3>
                  <p class="text-light">Correct Answers</p>
            </div>
          </div>
              <div class="col-md-3 mb-3">
                <div class="score-metric">
                  <h3 class="text-secondary">{{ quizResults.total_questions }}</h3>
                  <p class="text-light">Total Questions</p>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="score-metric">
                  <h3 class="text-warning">{{ Math.round(quizResults.score.time_taken / 60) }}</h3>
                  <p class="text-light">Minutes Taken</p>
            </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="results-actions">
            <button class="btn btn-primary me-3" @click="goToDashboard">
              <i class="bi bi-house me-2"></i>
              Back to Dashboard
            </button>
            <button class="btn btn-outline-light" @click="viewScores">
              <i class="bi bi-graph-up me-2"></i>
              View All Scores
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Submit Confirmation Modal -->
    <div 
      class="modal fade" 
      id="submitConfirmModal" 
      tabindex="-1"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass">
          <div class="modal-header">
            <h5 class="modal-title text-light">Submit Quiz</h5>
            <button 
              type="button" 
              class="btn-close btn-close-white" 
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body">
            <div class="submission-summary mb-3">
              <h6 class="text-light">Quiz Summary:</h6>
              <ul class="list-unstyled text-light">
                <li><i class="bi bi-check-circle me-2"></i>Answered: {{ Object.keys(selectedAnswers).length }} questions</li>
                <li><i class="bi bi-circle me-2"></i>Unanswered: {{ questions.length - Object.keys(selectedAnswers).length }} questions</li>
                <li><i class="bi bi-clock me-2"></i>Time remaining: {{ formatTime(timeRemaining) }}</li>
              </ul>
            </div>
            <p class="text-light">
              Are you sure you want to submit your quiz? This action cannot be undone.
            </p>
            <div v-if="questions.length - Object.keys(selectedAnswers).length > 0" class="alert alert-warning">
              <i class="bi bi-exclamation-triangle me-2"></i>
              You have {{ questions.length - Object.keys(selectedAnswers).length }} unanswered questions.
          </div>
          </div>
          <div class="modal-footer">
            <button 
              type="button" 
              class="btn btn-outline-light" 
              data-bs-dismiss="modal"
            >
              Continue Quiz
            </button>
            <button 
              type="button" 
              class="btn btn-success" 
              @click="submitQuiz"
            >
              Submit Quiz
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Modal } from 'bootstrap'
import quizService from '@/services/quizService'

export default {
  name: 'QuizTakingView',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const quizId = route.params.quizId
    
    const loading = ref(true)
    const loadingMessage = ref('Loading quiz...')
    const error = ref(null)
    const quizData = ref(null)
    const questions = ref([])
    const currentQuestionIndex = ref(0)
    const selectedAnswers = ref({})
    const startTime = ref(null)
    const timeRemaining = ref(0)
    const timerInterval = ref(null)
    const quizSubmitted = ref(false)
    const quizResults = ref(null)
    const lastTimestamp = ref(Date.now()) // Track timestamp for timer precision

    const currentQuestion = computed(() => {
      return questions.value[currentQuestionIndex.value]
    })

    // Save quiz state to localStorage
    const saveQuizState = () => {
      const quizState = {
        quizId,
        quizData: quizData.value,
        questions: questions.value,
        currentQuestionIndex: currentQuestionIndex.value,
        selectedAnswers: selectedAnswers.value,
        startTime: startTime.value,
        timeRemaining: timeRemaining.value,
        lastTimestamp: Date.now(),
        quizSubmitted: quizSubmitted.value,
        quizResults: quizResults.value
      }
      localStorage.setItem(`quiz_state_${quizId}`, JSON.stringify(quizState))
      console.log('Quiz state saved to localStorage')
    }

    // Clear stale quiz data from localStorage
    const clearStaleQuizData = () => {
      try {
        const keysToRemove = []
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i)
          if (key && key.startsWith('quiz_state_') && key !== `quiz_state_${quizId}`) {
            keysToRemove.push(key)
          }
          if (key && key.startsWith('quiz_result_') && key !== `quiz_result_${quizId}`) {
            keysToRemove.push(key)
          }
        }
        
        keysToRemove.forEach(key => {
          localStorage.removeItem(key)
          console.log('🗑️ Cleared stale quiz data:', key)
        })
      } catch (error) {
        console.error('Failed to clear stale quiz data:', error)
      }
    }

    // Restore quiz state from localStorage
    const restoreQuizState = () => {
      try {
        const savedStateString = localStorage.getItem(`quiz_state_${quizId}`)
        if (!savedStateString) {
          console.log('💾 No saved state found for quiz:', quizId)
          return false
        }

        const savedState = JSON.parse(savedStateString)
        
        // Verify it's the same quiz ID
        if (savedState.quizId !== quizId) {
          console.log('❌ Quiz ID mismatch. Expected:', quizId, 'Found:', savedState.quizId)
          localStorage.removeItem(`quiz_state_${quizId}`)
          return false
        }
        
        // Verify the quiz data exists and has valid structure
        if (!savedState.quizData || !savedState.quizData.id || savedState.quizData.id != quizId) {
          console.log('❌ Invalid quiz data in saved state')
          localStorage.removeItem(`quiz_state_${quizId}`)
          return false
        }
        
        // Additional validation for questions
        if (!savedState.questions || !Array.isArray(savedState.questions) || savedState.questions.length === 0) {
          console.log('❌ Invalid questions data in saved state')
          localStorage.removeItem(`quiz_state_${quizId}`)
          return false
        }
        
        // Restore state
        quizData.value = savedState.quizData
        questions.value = savedState.questions
        currentQuestionIndex.value = savedState.currentQuestionIndex || 0
        selectedAnswers.value = savedState.selectedAnswers || {}
        startTime.value = savedState.startTime
        quizSubmitted.value = savedState.quizSubmitted || false
        quizResults.value = savedState.quizResults
        
        // Calculate elapsed time since last save
        const elapsedSeconds = Math.floor((Date.now() - savedState.lastTimestamp) / 1000)
        timeRemaining.value = Math.max(0, savedState.timeRemaining - elapsedSeconds)
        
        console.log('✅ Quiz state restored from localStorage for quiz:', quizId)
        return true
      } catch (error) {
        console.error('❌ Failed to restore quiz state:', error)
        localStorage.removeItem(`quiz_state_${quizId}`)
        return false
      }
    }

    const loadQuiz = async () => {
      try {
        loading.value = true
        loadingMessage.value = 'Loading quiz...'
        
        // Clear any stale localStorage data for other quizzes first
        clearStaleQuizData()
        
        // Try to restore state first, but only for the current quiz
        const stateRestored = restoreQuizState()
        
        if (stateRestored && quizData.value && quizData.value.id == quizId) {
          console.log('✅ Restored valid quiz state for quiz:', quizId)
          // If state was restored and quiz was already submitted, don't restart the timer
          if (!quizSubmitted.value && timeRemaining.value > 0) {
            startTimer()
          }
          loading.value = false
          return
        }
        
        // Clear any invalid state and start fresh
        localStorage.removeItem(`quiz_state_${quizId}`)
        console.log('🔄 Starting fresh quiz session for:', quizId)
        
        // Start the quiz and get questions
        const response = await quizService.startQuiz(quizId)
        
        quizData.value = response
        questions.value = response.questions
        startTime.value = response.start_time
        
        console.log('📝 Loaded quiz:', response.name, 'ID:', response.id)
        console.log('📊 Questions loaded:', questions.value.length)
        
        // Set up timer
        if (response.time_duration) {
          timeRemaining.value = response.time_duration * 60 // Convert minutes to seconds
          startTimer()
        }
        
        loading.value = false
      } catch (err) {
        console.error('Failed to load quiz:', err)
        error.value = err.response?.data?.message || 'Failed to load quiz'
        loading.value = false
      }
    }

    const startTimer = () => {
      // Clear any existing interval first
      if (timerInterval.value) {
        clearInterval(timerInterval.value)
      }

      lastTimestamp.value = Date.now()
      
      timerInterval.value = setInterval(() => {
        if (timeRemaining.value > 0) {
          // Calculate elapsed time more precisely
          const now = Date.now()
          const elapsed = Math.floor((now - lastTimestamp.value) / 1000)
          lastTimestamp.value = now
          
          // Update time remaining
          timeRemaining.value = Math.max(0, timeRemaining.value - elapsed)
          
          // Save state periodically (every 10 seconds)
          if (timeRemaining.value % 10 === 0) {
            saveQuizState()
          }
        } else {
          // Time's up, auto-submit
          autoSubmitQuiz()
        }
      }, 1000)
    }

    const formatTime = (seconds) => {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
    }

    const selectAnswer = (questionId, optionIndex) => {
      // Convert from 0-based index to 1-based index for backend
      selectedAnswers.value[questionId] = optionIndex
      // Save state whenever an answer is selected
      saveQuizState()
    }

    const nextQuestion = () => {
      if (currentQuestionIndex.value < questions.value.length - 1) {
        currentQuestionIndex.value++
        saveQuizState()
      }
    }

    const previousQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--
        saveQuizState()
      }
    }

    const goToQuestion = (index) => {
      currentQuestionIndex.value = index
      saveQuizState()
    }

    const showSubmitConfirm = () => {
      const modal = new Modal(document.getElementById('submitConfirmModal'))
      modal.show()
    }

    const submitQuiz = async () => {
      try {
        loading.value = true
        loadingMessage.value = 'Submitting quiz...'

        // Close modal
        const modal = Modal.getInstance(document.getElementById('submitConfirmModal'))
        modal?.hide()

        // Clear timer
        if (timerInterval.value) {
          clearInterval(timerInterval.value)
        }

        const submitData = {
          answers: selectedAnswers.value,
          start_time: startTime.value
        }

        const response = await quizService.submitQuiz(quizId, submitData)
        
        // Log answers for verification
        console.log('Submitted answers:', selectedAnswers.value)
        console.log('Correct answers:', response.question_answers)
        
        quizResults.value = response
        quizSubmitted.value = true
        
        // Save the final result to localStorage for the result page to access
        saveQuizResultForResultPage(response)
        
        // Navigate to result page with attempt ID
        if (response && response.score && response.score.id) {
          // If we have an attempt ID, use it
          router.push({
            name: 'QuizResult',
            params: { quizId },
            query: { attempt: response.score.id }
          })
        } else {
          // Otherwise just pass the quiz ID
          router.push({
            name: 'QuizResult',
            params: { quizId }
          })
        }
        
        loading.value = false
      } catch (err) {
        console.error('Failed to submit quiz:', err)
        error.value = err.response?.data?.message || 'Failed to submit quiz'
        loading.value = false
      }
    }
    
    // Save quiz result for the result page to access
    const saveQuizResultForResultPage = (responseData) => {
      try {
        // Calculate the correct counts based on the actual responses
        let totalCorrect = responseData.correct_answers || 0;
        let totalIncorrect = responseData.incorrect_answers || 0;
        let totalUnanswered = responseData.unanswered || 0;
        
        // If we don't have these values, calculate them from the questions and user answers
        if (totalCorrect === 0 && totalIncorrect === 0 && questions.value.length > 0) {
          questions.value.forEach(question => {
            const userAnswer = selectedAnswers.value[question.id];
            if (userAnswer === undefined) {
              totalUnanswered++;
            } else if (userAnswer === question.correct_option) {
              totalCorrect++;
            } else {
              totalIncorrect++;
            }
          });
        }
        
        // Calculate the accurate percentage
        let calculatedPercentage = 0;
        if (questions.value.length > 0) {
          calculatedPercentage = (totalCorrect / questions.value.length) * 100;
        }
        
        // Format the quiz result data
        const quizResult = {
          quiz: {
            id: quizId,
            title: quizData.value.name,
            totalPoints: questions.value.reduce((acc, q) => acc + (q.marks || 1), 0),
            passingScore: 70,
            questions: questions.value.map(q => ({
              ...q,
              // Add any calculated properties needed for the result page
              type: q.question_type || 'multiple_choice',
              content: q.question_statement,
              correctAnswer: q.correct_option, // Keep the 1-based indexing from backend
              options: q.options ? q.options.map(opt => ({ text: opt })) : []
            }))
          },
          result: {
            score: responseData.total_scored || 0,
            percentage: responseData.percentage || calculatedPercentage,
            correctAnswers: totalCorrect,
            incorrectAnswers: totalIncorrect,
            unanswered: totalUnanswered,
            passed: responseData.passed || (calculatedPercentage >= 70),
            grade: getGrade(responseData.percentage || calculatedPercentage),
            gradeDescription: getGradeDescription(responseData.percentage || calculatedPercentage),
            timeSpent: formatTimeForDisplay(responseData.time_taken || timeRemaining.value)
          },
          userAnswers: selectedAnswers.value,
          timestamp: Date.now()
        }
        
        // Save to localStorage
        const resultKey = `quiz_result_${quizId}`
        localStorage.setItem(resultKey, JSON.stringify(quizResult))
        console.log('Quiz result saved for result page:', resultKey)
      } catch (err) {
        console.error('Error saving quiz result:', err)
      }
    }
    
    // Helper functions for the result data
    const getGrade = (percentage) => {
      if (percentage >= 90) return 'A'
      if (percentage >= 80) return 'B'
      if (percentage >= 70) return 'C'
      if (percentage >= 60) return 'D'
      return 'F'
    }
    
    const getGradeDescription = (percentage) => {
      if (percentage >= 90) return 'Excellent! Outstanding performance!'
      if (percentage >= 80) return 'Good job! Above average performance!'
      if (percentage >= 70) return 'Fair performance. Room for improvement.'
      if (percentage >= 60) return 'Below average. Consider reviewing the material.'
      return 'Poor performance. Please review and retake.'
    }
    
    const formatTimeForDisplay = (seconds) => {
      if (!seconds) return 'N/A'
      const minutes = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${minutes}m ${secs}s`
    }

    const autoSubmitQuiz = () => {
      // Auto-submit when time runs out
      submitQuiz()
    }

    const goBack = () => {
      router.push('/user/dashboard')
    }

    const goToDashboard = () => {
      router.push('/user/dashboard')
    }

    const viewScores = () => {
      router.push('/user/scores')
    }

    // Watch for changes to key quiz properties to save state
    watch([currentQuestionIndex, selectedAnswers], () => {
      if (!loading.value && !quizSubmitted.value) {
        saveQuizState()
      }
    }, { deep: true })

    // Setup visibility change handling to pause/resume timer
    const handleVisibilityChange = () => {
      if (document.hidden) {
        // Page is hidden, save state
        if (timerInterval.value) {
          clearInterval(timerInterval.value)
          timerInterval.value = null
          saveQuizState()
        }
      } else {
        // Page is visible again, restore timer
        if (!timerInterval.value && !quizSubmitted.value && timeRemaining.value > 0) {
          // Recalculate elapsed time
          const savedState = JSON.parse(localStorage.getItem(`quiz_state_${quizId}`))
          if (savedState) {
            const elapsedSeconds = Math.floor((Date.now() - savedState.lastTimestamp) / 1000)
            timeRemaining.value = Math.max(0, savedState.timeRemaining - elapsedSeconds)
          }
          
          startTimer()
        }
      }
    }

    // Cleanup on component unmount
    onUnmounted(() => {
      if (timerInterval.value) {
        clearInterval(timerInterval.value)
      }
      
      // Save state on unmount if quiz is not submitted
      if (!quizSubmitted.value) {
        saveQuizState()
      }
      
      window.removeEventListener('beforeunload', handleBeforeUnload)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    })

    // Prevent page refresh during quiz
    const handleBeforeUnload = (event) => {
      if (!quizSubmitted.value && questions.value.length > 0) {
        saveQuizState() // Save state before unload
        event.preventDefault()
        event.returnValue = ''
      }
    }

    onMounted(() => {
      loadQuiz()
      
      // Add event listeners
      window.addEventListener('beforeunload', handleBeforeUnload)
      document.addEventListener('visibilitychange', handleVisibilityChange)
    })

    return {
      loading,
      loadingMessage,
      error,
      quizData,
      questions,
      currentQuestion,
      currentQuestionIndex,
      selectedAnswers,
      timeRemaining,
      quizSubmitted,
      quizResults,
      formatTime,
      selectAnswer,
      nextQuestion,
      previousQuestion,
      goToQuestion,
      showSubmitConfirm,
      submitQuiz,
      goBack,
      goToDashboard,
      viewScores
    }
  }
}
</script>

<style scoped>
.quiz-taking {
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

.glass, .quiz-header, .progress-section, .question-card, .quiz-navigation, .results-card {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
}

.timer-display {
  background: rgba(13, 110, 253, 0.2);
  border: 1px solid rgba(13, 110, 253, 0.5);
  border-radius: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 1.25rem;
  font-weight: bold;
  color: #0d6efd;
  min-width: 120px;
  text-align: center;
}

.timer-warning {
  background: rgba(220, 53, 69, 0.2) !important;
  border-color: rgba(220, 53, 69, 0.5) !important;
  color: #dc3545 !important;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.quiz-progress {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.quiz-progress .progress-bar {
  background: linear-gradient(90deg, #0d6efd, #6f42c1);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.option-card {
  background: rgba(35, 39, 43, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
}

.option-card:hover {
  border-color: rgba(13, 110, 253, 0.5);
  background: rgba(35, 39, 43, 0.6);
}

.option-card.selected {
  border-color: #0d6efd;
  background: rgba(13, 110, 253, 0.2);
}

.option-content {
  display: flex;
  align-items: center;
}

.option-letter {
  background: rgba(13, 110, 253, 0.2);
  border: 1px solid rgba(13, 110, 253, 0.5);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #0d6efd;
  margin-right: 1rem;
  flex-shrink: 0;
}

.option-card.selected .option-letter {
  background: #0d6efd;
  color: white;
}

.option-text {
  flex-grow: 1;
  color: #f8f9fa;
  font-size: 1rem;
}

.option-check {
  color: #0d6efd;
  font-size: 1.25rem;
  margin-left: 1rem;
}

.question-indicators {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.question-indicator {
  width: 40px;
  height: 40px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  background: rgba(35, 39, 43, 0.6);
  color: #f8f9fa;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.question-indicator.current {
  border-color: #0d6efd;
  background: rgba(13, 110, 253, 0.2);
  color: #0d6efd;
}

.question-indicator.answered {
  border-color: #198754;
  background: rgba(25, 135, 84, 0.2);
  color: #198754;
}

.question-indicator.unanswered {
  border-color: rgba(255, 255, 255, 0.2);
}

.score-metric {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.score-metric h3 {
  margin: 0;
  font-size: 2rem;
  font-weight: bold;
}

.score-metric p {
  margin: 0;
  font-size: 0.875rem;
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

.results-icon {
  animation: fadeInScale 0.5s ease-out;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.5);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style> 