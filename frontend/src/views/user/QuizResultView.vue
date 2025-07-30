<template>
  <div class="quiz-result-view">
    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay glass-card">
      <div class="spinner-border text-primary mb-3"></div>
      <p class="text-light">Loading quiz result...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-message glass-card">
      <div class="text-center">
        <i class="bi bi-exclamation-triangle text-warning display-1 mb-3"></i>
        <h3 class="text-light">Failed to Load Quiz Result</h3>
        <p class="text-light mb-4">{{ error }}</p>
        <button class="btn btn-outline-light" @click="goBack">
          <i class="bi bi-arrow-left me-2"></i>Go Back
        </button>
      </div>
    </div>
    
    <template v-else>
      <!-- Results Header -->
      <div class="result-header glass-card mb-4">
        <div class="d-flex justify-content-between align-items-start mb-3">
          <button 
            class="btn btn-outline-light d-flex align-items-center gap-2"
            @click="goBack"
          >
            <i class="bi bi-arrow-left"></i>
            Back
          </button>
          <div v-if="isAttemptView" class="badge bg-info">
            <i class="bi bi-clock-history me-1"></i>
            Previous Attempt
          </div>
        </div>
        <div class="text-center">
          <div class="result-icon mb-3">
            <i v-if="result.passed" class="bi bi-check-circle-fill text-success" style="font-size: 4rem;"></i>
            <i v-else class="bi bi-x-circle-fill text-danger" style="font-size: 4rem;"></i>
          </div>
          <h2 class="h3 text-light mb-2">
            {{ result.passed ? 'Congratulations!' : 'Keep Trying!' }}
          </h2>
          <p class="text-light mb-4">{{ quiz.title }}</p>
          
          <div class="score-display">
            <div class="score-circle" :class="{ 'passed': result.passed, 'failed': !result.passed }">
              <div class="score-percentage">{{ formatPercentage(result.percentage) }}%</div>
              <div class="score-label">{{ result.score }}/{{ quiz.totalPoints }} pts</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Performance Summary -->
      <div class="performance-summary glass-card mb-4">
        <h5 class="text-light mb-4">Performance Summary</h5>
        <div class="row">
          <div class="col-md-3 mb-3">
            <div class="stat-item">
              <div class="stat-icon text-primary">
                <i class="bi bi-check-circle"></i>
              </div>
              <div class="stat-content">
                <div class="stat-value text-light">{{ result.correctAnswers }}</div>
                <div class="stat-label text-light">Correct</div>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="stat-item">
              <div class="stat-icon text-danger">
                <i class="bi bi-x-circle"></i>
              </div>
              <div class="stat-content">
                <div class="stat-value text-light">{{ result.incorrectAnswers }}</div>
                <div class="stat-label text-light">Incorrect</div>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="stat-item">
              <div class="stat-icon text-warning">
                <i class="bi bi-dash-circle"></i>
              </div>
              <div class="stat-content">
                <div class="stat-value text-light">{{ result.unanswered }}</div>
                <div class="stat-label text-light">Unanswered</div>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="stat-item">
              <div class="stat-icon text-info">
                <i class="bi bi-clock"></i>
              </div>
              <div class="stat-content">
                <div class="stat-value text-light">{{ result.timeSpent }}</div>
                <div class="stat-label text-light">Time Spent</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Question Analysis -->
        <div class="question-analysis mt-4">
          <h6 class="text-light mb-3">Question Analysis</h6>
          <div class="progress mb-3" style="height: 25px;">
            <div 
              class="progress-bar bg-success" 
              :style="{ width: getPercentage(result.correctAnswers, totalQuestions) + '%' }"
              :title="`${result.correctAnswers} Correct`"
            >
              {{ result.correctAnswers }} Correct
            </div>
            <div 
              class="progress-bar bg-danger" 
              :style="{ width: getPercentage(result.incorrectAnswers, totalQuestions) + '%' }"
              :title="`${result.incorrectAnswers} Incorrect`"
            >
              {{ result.incorrectAnswers }} Incorrect
            </div>
            <div 
              class="progress-bar bg-warning" 
              :style="{ width: getPercentage(result.unanswered, totalQuestions) + '%' }"
              :title="`${result.unanswered} Unanswered`"
            >
              {{ result.unanswered }} Unanswered
            </div>
          </div>
          <div class="d-flex justify-content-between text-light small">
            <span>Total Questions: {{ totalQuestions }}</span>
            <span>Attempted: {{ totalQuestions - result.unanswered }}</span>
            <span>Accuracy: {{ formatPercentage(getAccuracyPercentage()) }}%</span>
          </div>
        </div>
      </div>

      <!-- Grade Breakdown -->
      <div class="grade-breakdown glass-card mb-4">
        <h5 class="text-light mb-3">Grade Breakdown</h5>
        <div class="grade-bar">
          <div class="grade-progress">
            <div 
              class="grade-fill" 
              :class="gradeClass"
              :style="{ width: result.percentage + '%' }"
            ></div>
          </div>
          <div class="grade-markers">
            <div class="grade-marker" style="left: 0%">
              <span class="marker-label">F</span>
              <span class="marker-value">0%</span>
            </div>
            <div class="grade-marker" style="left: 60%">
              <span class="marker-label">D</span>
              <span class="marker-value">60%</span>
            </div>
            <div class="grade-marker" style="left: 70%">
              <span class="marker-label">C</span>
              <span class="marker-value">70%</span>
            </div>
            <div class="grade-marker" style="left: 80%">
              <span class="marker-label">B</span>
              <span class="marker-value">80%</span>
            </div>
            <div class="grade-marker" style="left: 90%">
              <span class="marker-label">A</span>
              <span class="marker-value">90%</span>
            </div>
          </div>
        </div>
        <div class="grade-info mt-3">
          <div class="current-grade">
            <span class="grade-letter">{{ result.grade }}</span>
            <span class="grade-description">{{ result.gradeDescription }}</span>
          </div>
        </div>
      </div>

      <!-- Question Results -->
      <div class="question-results glass-card">
        <h5 class="text-light mb-3">Question Results</h5>
        <div v-if="quiz.questions && quiz.questions.length > 0" class="questions-list">
          <div 
            v-for="(question, index) in quiz.questions" 
            :key="question.id"
            class="question-item"
          >
            <div class="question-header">
              <div class="question-number">
                Question {{ index + 1 }} of {{ quiz.questions.length }}
              </div>
              <div 
                class="question-status"
                :class="{
                  'correct': isQuestionCorrect(question),
                  'incorrect': !isQuestionCorrect(question) && getUserAnswer(question.id),
                  'unanswered': !getUserAnswer(question.id)
                }"
              >
                <i 
                  class="bi"
                  :class="{
                    'bi-check-circle-fill': isQuestionCorrect(question),
                    'bi-x-circle-fill': !isQuestionCorrect(question) && getUserAnswer(question.id),
                    'bi-dash-circle-fill': !getUserAnswer(question.id)
                  }"
                ></i>
                <span>
                  {{ 
                    isQuestionCorrect(question) ? 'Correct' : 
                    getUserAnswer(question.id) ? 'Incorrect' : 'Unanswered'
                  }}
                </span>
              </div>
            </div>
            
            <div class="question-content">
              {{ question.content || question.question_statement }}
            </div>
            
            <div class="options-list">
              <div 
                v-for="(option, optionIndex) in question.options" 
                :key="optionIndex"
                class="option-item"
                :class="{
                  'selected': getUserAnswer(question.id) === (optionIndex + 1),
                  'correct': (optionIndex + 1) === question.correctAnswer,
                  'incorrect': getUserAnswer(question.id) === (optionIndex + 1) && (optionIndex + 1) !== question.correctAnswer
                }"
              >
                <span class="option-letter">{{ String.fromCharCode(65 + optionIndex) }}</span>
                <span class="option-text">{{ option.text || option }}</span>
                <span class="option-indicator">
                  <i 
                    v-if="(optionIndex + 1) === question.correctAnswer"
                    class="bi bi-check text-success"
                  ></i>
                  <i 
                    v-else-if="getUserAnswer(question.id) === (optionIndex + 1)"
                    class="bi bi-x text-danger"
                  ></i>
                </span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center text-light py-3">
          No question data available
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <button class="btn btn-outline-success" @click="retakeQuiz">
          <i class="bi bi-arrow-clockwise me-2"></i>Retake Quiz
        </button>
        <button class="btn btn-outline-info" @click="goToDashboard">
          <i class="bi bi-house me-2"></i>Back to Dashboard
        </button>
        <button class="btn btn-outline-primary" @click="goToScores">
          <i class="bi bi-trophy me-2"></i>All Scores
        </button>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ScoreService from '@/services/score-service'

export default {
  name: 'QuizResultView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const quiz = ref({})
    const result = ref({})
    const userAnswers = ref({})
    const loading = ref(false)
    const error = ref(null)
    const isAttemptView = ref(false)

    // Computed properties
    const gradeClass = computed(() => {
      if (result.value.percentage >= 90) return 'grade-a'
      if (result.value.percentage >= 80) return 'grade-b'
      if (result.value.percentage >= 70) return 'grade-c'
      if (result.value.percentage >= 60) return 'grade-d'
      return 'grade-f'
    })

    // Add these computed properties
    const totalQuestions = computed(() => {
      return quiz.value.questions ? quiz.value.questions.length : 0
    })

    const performanceSummary = computed(() => {
      let correct = 0
      let incorrect = 0
      let unanswered = 0

      if (quiz.value.questions) {
        quiz.value.questions.forEach(question => {
          const userAnswer = getUserAnswer(question.id)
          if (userAnswer === undefined) {
            unanswered++
          } else if (userAnswer === question.correctAnswer) {
            correct++
          } else {
            incorrect++
          }
        })
      }

      return {
        correct,
        incorrect,
        unanswered,
        total: totalQuestions.value
      }
    })

    // Calculate accuracy percentage
    const getAccuracyPercentage = () => {
      const summary = performanceSummary.value
      const attempted = summary.total - summary.unanswered
      if (!attempted) return 0
      return (summary.correct / attempted) * 100
    }

    const loadQuizResult = async () => {
      loading.value = true
      error.value = null;
      
      try {
        // Check if we're viewing a previous attempt
        const attemptId = route.query.attempt;
        isAttemptView.value = !!attemptId;
        
        if (attemptId) {
          try {
            const response = await ScoreService.getScoreDetails(attemptId);
            
            if (response.success) {
              const scoreData = response.data;
              
              quiz.value = {
                id: scoreData.quiz_id,
                title: scoreData.quiz_name || 'Quiz',
                totalPoints: scoreData.total_possible_score,
                passingScore: 70,
                questions: scoreData.questions || []
              };
              
              // Set user answers from the score data
              userAnswers.value = {};
              if (scoreData.user_answers) {
                Object.entries(scoreData.user_answers).forEach(([questionId, answer]) => {
                  userAnswers.value[questionId] = parseInt(answer);
                });
              }
              
              // Calculate performance metrics
              let totalQuestions = quiz.value.questions?.length || 0;
              let storedCorrect = scoreData.correct_answers || 0;
              
              result.value = {
                score: scoreData.total_scored,
                percentage: scoreData.percentage,
                correctAnswers: storedCorrect,
                incorrectAnswers: scoreData.incorrect_answers || (totalQuestions - storedCorrect),
                unanswered: scoreData.unanswered || 0,
                passed: scoreData.passed,
                grade: getGrade(scoreData.percentage),
                gradeDescription: getGradeDescription(scoreData.percentage),
                timeSpent: formatTime(scoreData.time_taken)
              };
            } else {
              throw new Error(response.message || 'Failed to load quiz attempt');
            }
          } catch (err) {
            console.error('Error loading quiz attempt:', err);
            
            // Get results from localStorage if available
            const savedResultKey = `quiz_result_${route.params.quizId || attemptId}`;
            const savedResult = localStorage.getItem(savedResultKey);
            
            if (savedResult) {
              const parsedResult = JSON.parse(savedResult);
              console.log('Restored quiz result from localStorage:', parsedResult);
              
              quiz.value = parsedResult.quiz;
              userAnswers.value = parsedResult.userAnswers;
              
              // Debug the data structure
              console.log('🔍 Quiz questions structure:', quiz.value.questions);
              console.log('🔍 User answers structure:', userAnswers.value);
              
              if (quiz.value.questions && quiz.value.questions.length > 0) {
                console.log('🔍 First question example:', quiz.value.questions[0]);
              }
              
              // Use the saved result data
              result.value = {
                ...parsedResult.result
              };
            } else {
              error.value = 'Failed to retrieve score details';
            }
          }
        } else {
          // Handle current quiz result...
          const quizId = route.params.quizId;
          const savedResultKey = `quiz_result_${quizId}`;
          const savedResult = localStorage.getItem(savedResultKey);
          
          if (savedResult) {
            const parsedResult = JSON.parse(savedResult);
            console.log('Restored quiz result from localStorage:', parsedResult);
            
            quiz.value = parsedResult.quiz;
            userAnswers.value = parsedResult.userAnswers;
            
            // Use the saved result data directly
            result.value = {
              ...parsedResult.result
            };
          } else {
            error.value = 'No quiz result found';
          }
        }
      } catch (err) {
        console.error('Error loading quiz result:', err);
        error.value = 'Failed to load quiz result. Please try again.';
      } finally {
        loading.value = false;
      }
    }

    const getUserAnswer = (questionId) => {
      return userAnswers.value[questionId]
    }

    const isQuestionCorrect = (question) => {
      const userAnswer = getUserAnswer(question.id)
      if (userAnswer === undefined) return false
      
      // Debug logging
      console.log('🔍 Checking question:', question.id)
      console.log('👤 User answer:', userAnswer, typeof userAnswer)
      console.log('✅ Correct answer (correct_option):', question.correct_option, typeof question.correct_option)
      console.log('✅ Correct answer (correctAnswer):', question.correctAnswer, typeof question.correctAnswer)
      
      // Check if correct_option property exists (from backend) - this is 1-based
      if (question.correct_option !== undefined) {
        const isCorrect = userAnswer === question.correct_option
        console.log('📊 Comparison result (correct_option):', isCorrect)
        return isCorrect
      } 
      // Check if correctAnswer property exists - this is also 1-based
      else if (question.correctAnswer !== undefined) {
        const isCorrect = userAnswer === question.correctAnswer
        console.log('📊 Comparison result (correctAnswer):', isCorrect)
        return isCorrect
      }
      
      console.log('❌ No correct answer property found')
      return false
    }

    const formatTime = (seconds) => {
      if (!seconds) return 'N/A'
      const minutes = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${minutes}m ${secs}s`
    }

    const formatPercentage = (value) => {
      if (typeof value !== 'number') return '0.0'
      return value.toFixed(1)
    }

    const getPercentage = (value, total) => {
      if (!total) return 0
      return (value / total) * 100
    }

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

    const retakeQuiz = () => {
      router.push(`/user/quiz/${quiz.value.id}`)
    }

    const goToDashboard = () => {
      router.push('/user/dashboard')
    }

    const goBack = () => {
      router.go(-1)
    }

    const goToScores = () => {
      router.push('/user/scores')
    }

    onMounted(() => {
      loadQuizResult()
    })

    return {
      quiz,
      result,
      userAnswers,
      loading,
      error,
      isAttemptView,
      gradeClass,
      totalQuestions,
      performanceSummary,
      getUserAnswer,
      isQuestionCorrect,
      retakeQuiz,
      goToDashboard,
      goBack,
      goToScores,
      formatPercentage,
      getPercentage,
      getAccuracyPercentage
    }
  }
}
</script>

<style scoped>
.quiz-result-view {
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

.glass, .glass-card {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.7);
}

.error-message {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.7);
}

.score-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  border: 3px solid;
  position: relative;
  transition: all 0.3s ease;
}

.score-circle.passed {
  border-color: #198754;
  background: rgba(25, 135, 84, 0.1);
  box-shadow: 0 0 20px rgba(25, 135, 84, 0.2);
}

.score-circle.failed {
  border-color: #dc3545;
  background: rgba(220, 53, 69, 0.1);
  box-shadow: 0 0 20px rgba(220, 53, 69, 0.2);
}

.score-percentage {
  font-size: 2rem;
  font-weight: 700;
  color: #f8f9fa;
  margin-bottom: 0.25rem;
}

.score-label {
  font-size: 0.9rem;
  color: #adb5bd;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 1.5rem;
  width: 32px;
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
}

.stat-label {
  font-size: 0.85rem;
  opacity: 0.8;
}

.question-analysis {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  padding: 1rem;
  margin-top: 1.5rem;
}

.question-analysis .progress {
  height: 20px;
}

.question-analysis .progress-bar {
  text-align: center;
  padding: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: width 1s ease;
}

.grade-bar {
  position: relative;
  margin: 2rem 0;
}

.grade-progress {
  height: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

.grade-fill {
  height: 100%;
  transition: width 1s ease;
  border-radius: 10px;
}

.grade-fill.grade-a { background: linear-gradient(45deg, #198754, #20c997); }
.grade-fill.grade-b { background: linear-gradient(45deg, #0dcaf0, #0d6efd); }
.grade-fill.grade-c { background: linear-gradient(45deg, #ffc107, #fd7e14); }
.grade-fill.grade-d { background: linear-gradient(45deg, #fd7e14, #dc3545); }
.grade-fill.grade-f { background: linear-gradient(45deg, #dc3545, #6f42c1); }

.grade-markers {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  position: relative;
}

.grade-marker {
  position: absolute;
  text-align: center;
  transform: translateX(-50%);
}

.marker-label {
  display: block;
  font-weight: 600;
  color: #f8f9fa;
  font-size: 0.9rem;
}

.marker-value {
  display: block;
  font-size: 0.8rem;
  color: #adb5bd;
}

.current-grade {
  text-align: center;
  margin-top: 1.5rem;
}

.grade-letter {
  font-size: 2.5rem;
  font-weight: 700;
  color: #f8f9fa;
  margin-right: 0.75rem;
}

.grade-description {
  font-size: 1rem;
  color: #adb5bd;
}

/* Question Results Section */
.question-results {
  margin-top: 1rem;
}

.question-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.question-number {
  font-size: 0.9rem;
  color: #adb5bd;
}

.question-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.question-status.correct {
  color: #198754;
}

.question-status.incorrect {
  color: #dc3545;
}

.question-status.unanswered {
  color: #ffc107;
}

.question-content {
  color: #f8f9fa;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.option-item.selected {
  background: rgba(13, 110, 253, 0.2);
  border-color: rgba(13, 110, 253, 0.3);
}

.option-item.correct {
  background: rgba(25, 135, 84, 0.2);
  border-color: rgba(25, 135, 84, 0.3);
}

.option-item.incorrect {
  background: rgba(220, 53, 69, 0.2);
  border-color: rgba(220, 53, 69, 0.3);
}

.option-letter {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  margin-right: 0.75rem;
  font-size: 0.85rem;
  color: #f8f9fa;
}

.option-text {
  flex-grow: 1;
  color: #f8f9fa;
  font-size: 0.9rem;
}

.option-indicator {
  margin-left: 0.75rem;
  font-size: 1rem;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.action-buttons .btn {
  flex: 1;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .quiz-result-view {
    padding: 1rem;
  }
  
  .glass-card {
    padding: 1.25rem;
  }
  
  .score-circle {
    width: 150px;
    height: 150px;
  }
  
  .score-percentage {
    font-size: 2rem;
  }
  
  .grade-letter {
    font-size: 2.5rem;
  }
}
</style> 