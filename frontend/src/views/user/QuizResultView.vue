<template>
  <div class="quiz-result-view">
    <!-- Results Header -->
    <div class="result-header glass-card mb-4">
      <div class="text-center">
        <div class="result-icon mb-3">
          <i v-if="result.passed" class="bi bi-check-circle-fill text-success" style="font-size: 4rem;"></i>
          <i v-else class="bi bi-x-circle-fill text-danger" style="font-size: 4rem;"></i>
        </div>
        <h2 class="h3 text-light mb-2">
          {{ result.passed ? 'Congratulations!' : 'Keep Trying!' }}
        </h2>
        <p class="text-muted mb-4">{{ quiz.title }}</p>
        
        <div class="score-display">
          <div class="score-circle" :class="{ 'passed': result.passed, 'failed': !result.passed }">
            <div class="score-percentage">{{ result.percentage }}%</div>
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
              <i class="bi bi-list-check"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value text-light">{{ result.correctAnswers }}</div>
              <div class="stat-label text-muted">Correct</div>
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
              <div class="stat-label text-muted">Incorrect</div>
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
              <div class="stat-label text-muted">Unanswered</div>
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
              <div class="stat-label text-muted">Time Spent</div>
            </div>
          </div>
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
    <div class="question-results glass-card mb-4">
      <h5 class="text-light mb-4">Question Results</h5>
      <div class="questions-list">
        <div
          v-for="(question, index) in quiz.questions"
          :key="question.id"
          class="question-result-item"
          :class="{
            'correct': isQuestionCorrect(question),
            'incorrect': !isQuestionCorrect(question) && getUserAnswer(question.id) !== undefined,
            'unanswered': getUserAnswer(question.id) === undefined
          }"
        >
          <div class="question-header">
            <div class="question-number">
              <span class="question-index">Q{{ index + 1 }}</span>
              <div class="result-icon">
                <i v-if="isQuestionCorrect(question)" class="bi bi-check-circle-fill text-success"></i>
                <i v-else-if="getUserAnswer(question.id) !== undefined" class="bi bi-x-circle-fill text-danger"></i>
                <i v-else class="bi bi-dash-circle-fill text-warning"></i>
              </div>
            </div>
            <div class="question-meta">
              <span class="badge bg-primary me-2">{{ question.type.replace('_', ' ').toUpperCase() }}</span>
              <span class="badge bg-info">{{ question.points }} pts</span>
            </div>
          </div>
          
          <div class="question-content">
            <h6 class="question-text">{{ question.content }}</h6>
            
            <!-- Multiple Choice Results -->
            <div v-if="question.type === 'multiple_choice'" class="answer-options">
              <div
                v-for="(option, optionIndex) in question.options"
                :key="optionIndex"
                class="option-result"
                :class="{
                  'correct-answer': optionIndex === question.correctAnswer,
                  'user-answer': optionIndex === getUserAnswer(question.id),
                  'wrong-answer': optionIndex === getUserAnswer(question.id) && optionIndex !== question.correctAnswer
                }"
              >
                <span class="option-letter">{{ String.fromCharCode(65 + optionIndex) }}.</span>
                <span class="option-text">{{ option.text }}</span>
                <div class="option-indicators">
                  <i v-if="optionIndex === question.correctAnswer" class="bi bi-check text-success"></i>
                  <span v-if="optionIndex === getUserAnswer(question.id)" class="badge bg-primary ms-2">Your Answer</span>
                </div>
              </div>
            </div>

            <!-- True/False Results -->
            <div v-if="question.type === 'true_false'" class="answer-options">
              <div
                class="option-result"
                :class="{
                  'correct-answer': 'true' === question.correctAnswer,
                  'user-answer': 'true' === getUserAnswer(question.id),
                  'wrong-answer': 'true' === getUserAnswer(question.id) && 'true' !== question.correctAnswer
                }"
              >
                <span class="option-letter">A.</span>
                <span class="option-text">True</span>
                <div class="option-indicators">
                  <i v-if="'true' === question.correctAnswer" class="bi bi-check text-success"></i>
                  <span v-if="'true' === getUserAnswer(question.id)" class="badge bg-primary ms-2">Your Answer</span>
                </div>
              </div>
              <div
                class="option-result"
                :class="{
                  'correct-answer': 'false' === question.correctAnswer,
                  'user-answer': 'false' === getUserAnswer(question.id),
                  'wrong-answer': 'false' === getUserAnswer(question.id) && 'false' !== question.correctAnswer
                }"
              >
                <span class="option-letter">B.</span>
                <span class="option-text">False</span>
                <div class="option-indicators">
                  <i v-if="'false' === question.correctAnswer" class="bi bi-check text-success"></i>
                  <span v-if="'false' === getUserAnswer(question.id)" class="badge bg-primary ms-2">Your Answer</span>
                </div>
              </div>
            </div>

            <!-- Show if unanswered -->
            <div v-if="getUserAnswer(question.id) === undefined" class="unanswered-message">
              <span class="text-warning">
                <i class="bi bi-exclamation-triangle me-2"></i>
                This question was not answered
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons glass-card mb-4">
      <div class="d-flex justify-content-center gap-3 flex-wrap">
        <button class="btn btn-outline-success" @click="retakeQuiz">
          <i class="bi bi-arrow-clockwise me-2"></i>Retake Quiz
        </button>
        <button class="btn btn-outline-info" @click="goToDashboard">
          <i class="bi bi-house me-2"></i>Back to Dashboard
        </button>
        <button class="btn btn-outline-secondary" @click="shareResult">
          <i class="bi bi-share me-2"></i>Share Result
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'QuizResultView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const quiz = ref({})
    const result = ref({})
    const userAnswers = ref({})

    // Computed properties
    const gradeClass = computed(() => {
      if (result.value.percentage >= 90) return 'grade-a'
      if (result.value.percentage >= 80) return 'grade-b'
      if (result.value.percentage >= 70) return 'grade-c'
      if (result.value.percentage >= 60) return 'grade-d'
      return 'grade-f'
    })

    // Methods
    const loadQuizResult = () => {
      // Get quiz data (dummy data)
      quiz.value = {
        id: route.params.id,
        title: 'JavaScript Fundamentals Quiz',
        totalPoints: 10,
        passingScore: 70,
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
            correctAnswer: 0,
            explanation: 'The "var" keyword is used to declare variables in JavaScript.'
          },
          {
            id: 2,
            type: 'true_false',
            difficulty: 'easy',
            points: 2,
            content: 'JavaScript is a case-sensitive language.',
            correctAnswer: 'true',
            explanation: 'JavaScript is indeed case-sensitive, meaning "Variable" and "variable" are different.'
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
            correctAnswer: 3,
            explanation: 'JavaScript does not have a "float" data type. Numbers are just "number" type.'
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
            correctAnswer: 1,
            explanation: 'Arrays in JavaScript are actually objects, so typeof returns "object".'
          },
          {
            id: 5,
            type: 'true_false',
            difficulty: 'easy',
            points: 1,
            content: 'In JavaScript, the == operator performs strict equality comparison.',
            correctAnswer: 'false',
            explanation: 'The == operator performs loose equality comparison. Use === for strict equality.'
          }
        ]
      }

      // Get user answers from query parameters or use defaults
      if (route.query.answers) {
        try {
          userAnswers.value = JSON.parse(route.query.answers)
          console.log('User answers from quiz:', userAnswers.value)
        } catch (e) {
          console.error('Error parsing user answers:', e)
          userAnswers.value = {}
        }
      } else {
        console.log('No answers in query params, using test data')
        // Test data based on the quiz structure
        userAnswers.value = {
          1: 0,       // A. var myVariable; (correct)
          2: 'true',  // True (correct)  
          3: 3,       // D. float (correct - this is NOT a JS data type)
          4: 1,       // B. object (correct - typeof array returns "object")
          5: 'false'  // False (correct - == does NOT perform strict equality)
        }
      }

      // Calculate results
      calculateResults()
    }

    const calculateResults = () => {
      let correctAnswers = 0
      let incorrectAnswers = 0
      let unanswered = 0
      let score = 0

      quiz.value.questions.forEach(question => {
        const userAnswer = userAnswers.value[question.id]
        
        if (userAnswer === undefined) {
          unanswered++
        } else {
          // For multiple choice, check if the selected index matches correct answer
          if (question.type === 'multiple_choice') {
            if (parseInt(userAnswer) === question.correctAnswer) {
              correctAnswers++
              score += question.points
            } else {
              incorrectAnswers++
            }
          } 
          // For true/false, check if the selected string matches correct answer
          else if (question.type === 'true_false') {
            if (userAnswer.toString() === question.correctAnswer.toString()) {
              correctAnswers++
              score += question.points
            } else {
              incorrectAnswers++
            }
          }
        }
      })

      const percentage = Math.round((score / quiz.value.totalPoints) * 100)
      const passed = percentage >= quiz.value.passingScore

      let grade, gradeDescription
      if (percentage >= 90) {
        grade = 'A'
        gradeDescription = 'Excellent! Outstanding performance!'
      } else if (percentage >= 80) {
        grade = 'B'
        gradeDescription = 'Good job! Above average performance!'
      } else if (percentage >= 70) {
        grade = 'C'
        gradeDescription = 'Fair performance. Room for improvement.'
      } else if (percentage >= 60) {
        grade = 'D'
        gradeDescription = 'Below average. Consider reviewing the material.'
      } else {
        grade = 'F'
        gradeDescription = 'Poor performance. Please review and retake.'
      }

      result.value = {
        score,
        percentage,
        correctAnswers,
        incorrectAnswers,
        unanswered,
        passed,
        grade,
        gradeDescription,
        timeSpent: '25:30' // Mock time spent
      }
    }

    const retakeQuiz = () => {
      router.push(`/quiz/${quiz.value.id}/take`)
    }

    const goToDashboard = () => {
      router.push('/user')
    }

    const getUserAnswer = (questionId) => {
      return userAnswers.value[questionId]
    }

    const isQuestionCorrect = (question) => {
      const userAnswer = getUserAnswer(question.id)
      if (userAnswer === undefined) return false
      
      if (question.type === 'multiple_choice') {
        return parseInt(userAnswer) === question.correctAnswer
      } else if (question.type === 'true_false') {
        return userAnswer.toString() === question.correctAnswer.toString()
      }
      return false
    }

    const shareResult = () => {
      // Implementation for sharing results
      const shareText = `I scored ${result.value.percentage}% on ${quiz.value.title}!`
      if (navigator.share) {
        navigator.share({
          title: 'Quiz Result',
          text: shareText,
          url: window.location.href
        })
      } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(shareText)
        alert('Result copied to clipboard!')
      }
    }

    // Lifecycle
    onMounted(() => {
      loadQuizResult()
    })

    return {
      quiz,
      result,
      userAnswers,
      gradeClass,
      getUserAnswer,
      isQuestionCorrect,
      retakeQuiz,
      goToDashboard,
      shareResult
    }
  }
}
</script>

<style scoped>
.quiz-result-view {
  padding: 2rem;
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(13, 110, 253, 0.1) 0%, rgba(108, 117, 125, 0.05) 100%);
}

.glass-card {
  background: rgba(35, 39, 43, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 2rem;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  border: 4px solid;
  position: relative;
}

.score-circle.passed {
  border-color: #198754;
  background: rgba(25, 135, 84, 0.1);
}

.score-circle.failed {
  border-color: #dc3545;
  background: rgba(220, 53, 69, 0.1);
}

.score-percentage {
  font-size: 2.5rem;
  font-weight: 700;
  color: #f8f9fa;
}

.score-label {
  font-size: 0.9rem;
  color: #adb5bd;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-icon {
  font-size: 1.5rem;
  width: 40px;
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
}

.stat-label {
  font-size: 0.9rem;
}

.grade-bar {
  position: relative;
  margin: 1rem 0;
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
}

.grade-letter {
  font-size: 3rem;
  font-weight: 700;
  color: #f8f9fa;
  margin-right: 1rem;
}

.grade-description {
  font-size: 1.1rem;
  color: #adb5bd;
}

.question-results {
  margin-top: 2rem;
}

.question-result-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.question-result-item.correct {
  border-color: rgba(25, 135, 84, 0.3);
  background: rgba(25, 135, 84, 0.1);
}

.question-result-item.incorrect {
  border-color: rgba(220, 53, 69, 0.3);
  background: rgba(220, 53, 69, 0.1);
}

.question-result-item.unanswered {
  border-color: rgba(255, 193, 7, 0.3);
  background: rgba(255, 193, 7, 0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-number {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.question-index {
  font-weight: 600;
  color: #0d6efd;
  font-size: 1.1rem;
}

.result-icon {
  font-size: 1.25rem;
}

.question-text {
  color: #f8f9fa;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.answer-options {
  margin-top: 1rem;
}

.option-result {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.option-result.correct-answer {
  border-color: rgba(25, 135, 84, 0.5);
  background: rgba(25, 135, 84, 0.2);
}

.option-result.wrong-answer {
  border-color: rgba(220, 53, 69, 0.5);
  background: rgba(220, 53, 69, 0.2);
}

.option-result.user-answer:not(.correct-answer) {
  border-color: rgba(220, 53, 69, 0.5);
}

.option-letter {
  font-weight: 600;
  color: #0d6efd;
  margin-right: 0.75rem;
  min-width: 30px;
}

.option-text {
  color: #f8f9fa;
  flex: 1;
}

.option-indicators {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.unanswered-message {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 0.5rem;
}

@media (max-width: 768px) {
  .quiz-result-view {
    padding: 1rem;
  }
  
  .glass-card {
    padding: 1.5rem;
  }
  
  .score-circle {
    width: 120px;
    height: 120px;
  }
  
  .score-percentage {
    font-size: 2rem;
  }
  
  .grade-letter {
    font-size: 2rem;
    margin-right: 0.5rem;
  }
}
</style> 