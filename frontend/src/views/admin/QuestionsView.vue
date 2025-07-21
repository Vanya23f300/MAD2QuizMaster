<template>
  <div class="questions-management">
    <div class="container-fluid px-4">
      <!-- Page Header -->
      <div class="page-header glass mb-4">
        <div class="d-flex justify-content-between align-items-center">
          <div class="d-flex align-items-center">
        <button 
              class="btn btn-outline-light me-3" 
          @click="goBack"
        >
              <i class="bi bi-arrow-left me-2"></i>
              Back to {{ selectedQuizId ? 'Quiz' : 'Dashboard' }}
        </button>
            <div>
              <h1 class="text-light mb-2">
                <i class="bi bi-question-circle me-1"></i>
                Questions Management
              </h1>
              <p class="text-light mb-0">
                <template v-if="selectedQuiz && selectedQuiz.chapter_name">
                  <span class="context-path">
                    <i class="bi bi-book me-2"></i>{{ selectedQuiz.subject_name }}
                    <i class="bi bi-chevron-right mx-2"></i>
                    <i class="bi bi-layers me-2"></i>{{ selectedQuiz.chapter_name }}
                    <i class="bi bi-chevron-right mx-2"></i>
                    <i class="bi bi-clipboard-check me-2"></i>{{ selectedQuiz.name }}
                  </span>
                </template>
                <template v-else>
                  Create and manage MCQ questions
                </template>
              </p>
            </div>
      </div>
          <div class="d-flex align-items-center">
            <select 
              v-if="!selectedQuizId"
              v-model="selectedQuizId" 
              class="form-select me-2"
              @change="fetchQuestions"
            >
              <option value="">All Quizzes</option>
              <option 
                v-for="quiz in quizzes" 
                :key="quiz.id" 
                :value="quiz.id"
              >
                {{ quiz.name }} ({{ quiz.chapter_name }})
              </option>
            </select>
      <button 
              class="btn btn-primary" 
              @click="showCreateQuestionModal"
              :disabled="!selectedQuizId"
      >
              <i class="bi bi-plus-lg me-2"></i>
        Add Question
      </button>
    </div>
        </div>
      </div>

      <!-- Questions List -->
      <div class="questions-list glass">
        <div class="card-body">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3"></div>
            <p class="text-muted">Loading questions...</p>
    </div>

          <!-- Error State -->
          <div v-else-if="error" class="alert alert-danger glass-alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ error }}
    </div>

          <!-- Empty State -->
          <div v-else-if="questions.length === 0" class="empty-state text-center py-5">
            <i class="bi bi-question-circle display-1 text-muted mb-3"></i>
            <h4 class="text-light">No Questions Found</h4>
            <p class="text-muted">
              {{ selectedQuizId ? 'Create your first question for this quiz' : 'Select a quiz to manage questions' }}
            </p>
            </div>

          <!-- Questions Cards -->
          <div v-else class="row">
            <div v-for="(question, index) in questions" :key="question.id" class="col-12 mb-4">
              <div class="question-card glass">
                <div class="question-header d-flex justify-content-between align-items-start">
                  <div class="question-info flex-grow-1">
                    <div class="d-flex align-items-center mb-2">
                      <span class="badge bg-primary me-2">Q{{ index + 1 }}</span>
                      <span class="badge bg-info me-2">{{ question.marks }} {{ question.marks === 1 ? 'point' : 'points' }}</span>
                      <span class="badge bg-secondary">{{ question.difficulty_level || 'Medium' }}</span>
            </div>
                    <h5 class="text-light mb-3">{{ question.question_statement }}</h5>
                    
                    <!-- Options -->
                    <div class="row">
                      <div class="col-md-6 mb-2">
                        <div class="option" :class="{ 'correct-option': question.correct_option === 1 }">
                          <strong>A.</strong> {{ question.options[0] }}
                          <i v-if="question.correct_option === 1" class="bi bi-check-circle-fill text-success ms-2"></i>
                        </div>
                      </div>
                      <div class="col-md-6 mb-2">
                        <div class="option" :class="{ 'correct-option': question.correct_option === 2 }">
                          <strong>B.</strong> {{ question.options[1] }}
                          <i v-if="question.correct_option === 2" class="bi bi-check-circle-fill text-success ms-2"></i>
                        </div>
                      </div>
                      <div class="col-md-6 mb-2">
                        <div class="option" :class="{ 'correct-option': question.correct_option === 3 }">
                          <strong>C.</strong> {{ question.options[2] }}
                          <i v-if="question.correct_option === 3" class="bi bi-check-circle-fill text-success ms-2"></i>
                        </div>
                      </div>
                      <div class="col-md-6 mb-2">
                        <div class="option" :class="{ 'correct-option': question.correct_option === 4 }">
                          <strong>D.</strong> {{ question.options[3] }}
                          <i v-if="question.correct_option === 4" class="bi bi-check-circle-fill text-success ms-2"></i>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Actions -->
                  <div class="question-actions">
                    <div class="btn-group-vertical" role="group">
                      <button 
                        class="btn btn-sm btn-outline-light mb-1"
                        @click="editQuestion(question)"
                        title="Edit Question"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                    <button
                      class="btn btn-sm btn-outline-danger"
                        @click="triggerDeleteQuestion(question.id)"
                        title="Delete Question"
                    >
                      <i class="bi bi-trash"></i>
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

    <!-- Delete Confirmation Modal -->
    <div 
      class="modal fade" 
      id="deleteConfirmModal" 
      tabindex="-1" 
      aria-labelledby="deleteConfirmModalLabel"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass">
          <div class="modal-header">
            <h5 class="modal-title text-light" id="deleteConfirmModalLabel">
              Confirm Deletion
            </h5>
            <button 
              type="button" 
              class="btn-close btn-close-white" 
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body">
            <p class="text-light">
              Are you sure you want to delete this question? 
              This action cannot be undone.
            </p>
                </div>
          <div class="modal-footer">
            <button 
              type="button" 
              class="btn btn-outline-light" 
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
            <button 
              type="button" 
              class="btn btn-danger" 
              @click="confirmDeleteQuestion"
            >
              Delete
            </button>
          </div>
                </div>
              </div>
            </div>

    <!-- Create/Edit Question Modal -->
    <div 
      class="modal fade" 
      id="questionModal" 
      tabindex="-1" 
      aria-labelledby="questionModalLabel"
    >
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content glass">
          <div class="modal-header">
            <h5 class="modal-title text-light" id="questionModalLabel">
              {{ isEditing ? 'Edit Question' : 'Create Question' }}
            </h5>
            <button 
              type="button" 
              class="btn-close btn-close-white" 
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveQuestion">
              <!-- Quiz Selection (only if not in quiz-specific view) -->
              <div v-if="!selectedQuizId" class="mb-3">
                <label class="form-label text-light">
                  <i class="bi bi-clipboard-check me-2"></i>Quiz *
                </label>
                <select
                  v-model="currentQuestion.quiz_id" 
                  class="form-select glass-input" 
                  required
                >
                  <option value="">Select Quiz</option>
                  <option
                    v-for="quiz in quizzes" 
                    :key="quiz.id" 
                    :value="quiz.id"
                  >
                    {{ quiz.name }} ({{ quiz.chapter_name }})
                  </option>
                </select>
              </div>

              <!-- Question Statement -->
              <div class="mb-3">
                <label class="form-label text-light">
                  <i class="bi bi-question-circle me-2"></i>Question Statement *
                </label>
                <textarea 
                  v-model="currentQuestion.question_statement" 
                  class="form-control glass-input" 
                  rows="3"
                  required
                  placeholder="Enter your question here..."
                ></textarea>
              </div>

              <!-- Options -->
              <div class="mb-3">
                <label class="form-label text-light">
                  <i class="bi bi-list me-2"></i>Options *
                </label>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label text-light">Option A</label>
                    <div class="input-group">
                      <input 
                        v-model="currentQuestion.option1" 
                        type="text" 
                        class="form-control glass-input" 
                        required
                        placeholder="Enter option A"
                      />
                      <div class="input-group-text glass-input">
                <input
                          type="radio" 
                          v-model="currentQuestion.correct_option" 
                          :value="1"
                          name="correctOption"
                          class="form-check-input"
                        />
                      </div>
                    </div>
              </div>

                  <div class="col-md-6 mb-3">
                    <label class="form-label text-light">Option B</label>
                    <div class="input-group">
                      <input 
                        v-model="currentQuestion.option2" 
                        type="text" 
                        class="form-control glass-input" 
                        required
                        placeholder="Enter option B"
                      />
                      <div class="input-group-text glass-input">
                        <input 
                          type="radio" 
                          v-model="currentQuestion.correct_option" 
                          :value="2"
                          name="correctOption"
                          class="form-check-input"
                        />
            </div>
          </div>
        </div>
                  
                  <div class="col-md-6 mb-3">
                    <label class="form-label text-light">Option C</label>
                    <div class="input-group">
                      <input 
                        v-model="currentQuestion.option3" 
                        type="text" 
                        class="form-control glass-input" 
                        required
                        placeholder="Enter option C"
                      />
                      <div class="input-group-text glass-input">
              <input
                          type="radio" 
                          v-model="currentQuestion.correct_option" 
                          :value="3"
                          name="correctOption"
                class="form-check-input"
                        />
            </div>
          </div>
        </div>

                  <div class="col-md-6 mb-3">
                    <label class="form-label text-light">Option D</label>
                    <div class="input-group">
                      <input 
                        v-model="currentQuestion.option4" 
                        type="text" 
                        class="form-control glass-input" 
                        required
                        placeholder="Enter option D"
                      />
                      <div class="input-group-text glass-input">
              <input
                          type="radio" 
                          v-model="currentQuestion.correct_option" 
                          :value="4"
                          name="correctOption"
                class="form-check-input"
                        />
            </div>
            </div>
          </div>
        </div>

                <small class="text-muted">Select the radio button next to the correct option</small>
              </div>
              
              <!-- Additional Settings -->
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-star me-2"></i>Difficulty Level
                  </label>
                  <select 
                    v-model="currentQuestion.difficulty_level" 
                    class="form-select glass-input"
                  >
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
                
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-award me-2"></i>Points
                  </label>
                  <input 
                    v-model.number="currentQuestion.marks" 
                    type="number" 
                    class="form-control glass-input" 
                    min="0.5" 
                    step="0.5"
                    max="10"
                    placeholder="1"
                  />
                </div>
              </div>
              
              <div class="modal-footer">
                <button 
                  type="button" 
                  class="btn btn-outline-light" 
                  data-bs-dismiss="modal"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  class="btn btn-primary"
                  :disabled="!isFormValid"
                >
                  {{ isEditing ? 'Update Question' : 'Create Question' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import questionService from '@/services/questionService'
import quizService from '@/services/quizService'
import { cleanupModals, showModal, hideModal } from '@/utils/modalUtils'

export default {
  name: 'QuestionsView',
  props: {
    quizId: {
      type: [String, Number],
      default: null
    }
  },
  setup(props) {
    const router = useRouter()
    const route = useRoute()
    const questions = ref([])
    const quizzes = ref([])
    const selectedQuiz = ref(null)
    const selectedQuizId = ref(props.quizId || route.params.quizId || '')
    const loading = ref(false)
    const error = ref(null)
    const isEditing = ref(false)
    const currentQuestion = ref({
      quiz_id: '',
      question_statement: '',
      option1: '',
      option2: '',
      option3: '',
      option4: '',
      correct_option: 1,
      difficulty_level: 'Medium',
      marks: 1.0
    })
    const questionToDelete = ref(null)

    const isFormValid = computed(() => 
      currentQuestion.value.question_statement && 
      currentQuestion.value.option1 && 
      currentQuestion.value.option2 && 
      currentQuestion.value.option3 && 
      currentQuestion.value.option4 && 
      currentQuestion.value.correct_option && 
      (currentQuestion.value.quiz_id || selectedQuizId.value)
    )

    const fetchQuizzes = async () => {
      try {
        quizzes.value = await quizService.getQuizzes()
        
        // Set selected quiz if we're in quiz-specific view
        if (selectedQuizId.value) {
          selectedQuiz.value = quizzes.value.find(quiz => quiz.id == selectedQuizId.value)
        }
      } catch (err) {
        console.error('Failed to fetch quizzes:', err)
        error.value = 'Failed to load quizzes'
      }
    }

    const fetchQuestions = async () => {
      loading.value = true
      error.value = null

      try {
        const quizIdToUse = selectedQuizId.value || currentQuestion.value.quiz_id
        questions.value = await questionService.getQuestions(quizIdToUse)
      } catch (err) {
        console.error('Failed to fetch questions:', err)
        error.value = err.response?.data?.message || 'Failed to load questions'
      } finally {
        loading.value = false
      }
    }

    const fetchQuizDetails = async () => {
      if (selectedQuizId.value) {
        try {
          const quiz = await quizService.getQuiz(selectedQuizId.value);
          selectedQuiz.value = quiz;
        } catch (err) {
          console.error('Failed to fetch quiz details:', err);
          error.value = 'Failed to load quiz details';
        }
      }
    };

    const goBack = () => {
      if (selectedQuizId.value) {
        router.push('/admin/quizzes')
      } else {
        router.push('/admin')
      }
    }

    const showCreateQuestionModal = () => {
      cleanupModals(); // Clean up any existing modals
      
      isEditing.value = false;
      currentQuestion.value = {
        quiz_id: selectedQuizId.value || '',
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: 1,
        difficulty_level: 'Medium',
        marks: 1.0
      };

      showModal('questionModal');
    };

    const editQuestion = (question) => {
      isEditing.value = true
      currentQuestion.value = {
        ...question,
        quiz_id: question.quiz_id,
        option1: question.options[0],
        option2: question.options[1],
        option3: question.options[2],
        option4: question.options[3]
      }
      showModal('questionModal')
    }

    const saveQuestion = async () => {
      loading.value = true;
      error.value = null;

      try {
        const questionData = {
          ...currentQuestion.value,
          quiz_id: currentQuestion.value.quiz_id || selectedQuizId.value
        };

        if (isEditing.value) {
          await questionService.updateQuestion(currentQuestion.value.id, questionData);
        } else {
          const result = await questionService.createQuestion(questionData);
          // Update quiz data if returned
          if (result.quiz) {
            await fetchQuizDetails();
          }
        }
        
        await fetchQuestions();
        hideModal('questionModal');
      } catch (err) {
        console.error('Failed to save question:', err);
        error.value = err.response?.data?.message || 'Failed to save question';
      } finally {
        loading.value = false;
      }
    };

    const triggerDeleteQuestion = (questionId) => {
      questionToDelete.value = questionId
      showModal('deleteConfirmModal')
    }

    const confirmDeleteQuestion = async () => {
      if (!questionToDelete.value) return

      loading.value = true
      error.value = null

      try {
        await questionService.deleteQuestion(questionToDelete.value)
        await fetchQuestions()
        hideModal('deleteConfirmModal')
      } catch (err) {
        console.error('Failed to delete question:', err)
        error.value = err.response?.data?.message || 'Failed to delete question'
      } finally {
        loading.value = false
        questionToDelete.value = null
      }
    }

    // Initialize data
    onMounted(() => {
      cleanupModals(); // Clean up any lingering modals

      // Set quiz ID from route params if available
      if (route.params.quizId) {
        selectedQuizId.value = route.params.quizId;
        fetchQuizDetails();
      }
      
      fetchQuizzes();
      fetchQuestions();
    });

    // Clean up when component unmounts
    onUnmounted(() => {
      cleanupModals();
    });

    return {
      questions,
      quizzes,
      selectedQuiz,
      selectedQuizId,
      loading,
      error,
      isEditing,
      currentQuestion,
      isFormValid,
      fetchQuestions,
      showCreateQuestionModal,
      editQuestion,
      saveQuestion,
      triggerDeleteQuestion,
      confirmDeleteQuestion,
      goBack
    }
  }
}
</script>

<style scoped>
.questions-management {
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
  position: relative;
  z-index: 1;
}

.questions-management::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, 
    rgba(25, 135, 84, 0.1) 0%,
    rgba(13, 110, 253, 0.1) 100%
  );
  z-index: -1;
  pointer-events: none;
}

.page-header {
  background: rgba(35, 39, 43, 0.8);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  margin-bottom: 2rem;
}

.questions-list {
  background: rgba(35, 39, 43, 0.7);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.question-card {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.question-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0) 100%
  );
  pointer-events: none;
}

.question-card:hover {
  background: rgba(35, 39, 43, 0.8);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.option {
  background: rgba(35, 39, 43, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1rem 1.25rem;
  color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.3s ease;
  margin-bottom: 0.75rem;
  cursor: pointer;
}

.option:hover {
  background: rgba(35, 39, 43, 0.7);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateX(5px);
}

.option.correct-option {
  background: rgba(25, 135, 84, 0.15);
  border-color: rgba(25, 135, 84, 0.3);
  position: relative;
}

.option.correct-option::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg,
    rgba(25, 135, 84, 0.1) 0%,
    rgba(25, 135, 84, 0) 100%
  );
  pointer-events: none;
  border-radius: 0.75rem;
}

.option.correct-option:hover {
  background: rgba(25, 135, 84, 0.25);
  border-color: rgba(25, 135, 84, 0.4);
}

.glass-input {
  background: rgba(35, 39, 43, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: white !important;
  transition: all 0.3s ease;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
}

.glass-input:focus {
  background: rgba(35, 39, 43, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.1) !important;
}

.input-group-text.glass-input {
  background: rgba(35, 39, 43, 0.6) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
  border-radius: 0 0.5rem 0.5rem 0;
  padding: 0.5rem 1rem;
}

.modal-content.glass {
  background: rgba(35, 39, 43, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-radius: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.modal-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
}

.glass-alert {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 0.5rem;
  padding: 1rem 1.25rem;
}

.empty-state {
  background: rgba(35, 39, 43, 0.3);
  border-radius: 1rem;
  padding: 3rem;
  text-align: center;
}

.form-select {
  background: rgba(35, 39, 43, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  transition: all 0.3s ease;
  padding: 0.75rem 1rem;
  cursor: pointer;
}

.form-select:focus {
  background: rgba(35, 39, 43, 0.8);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.1);
}

.form-select option {
  background: rgba(35, 39, 43, 0.9);
  color: white;
  padding: 0.5rem;
}

.btn {
  padding: 0.75rem 1.25rem;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0) 100%
  );
  pointer-events: none;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-close-white {
  filter: invert(1) grayscale(100%) brightness(200%);
  opacity: 0.8;
  transition: all 0.3s ease;
}

.btn-close-white:hover {
  opacity: 1;
}

.badge {
  padding: 0.5em 0.8em;
  font-weight: 500;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
}

.form-check-input {
  background-color: rgba(35, 39, 43, 0.6);
  border-color: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  width: 1.25rem;
  height: 1.25rem;
  transition: all 0.3s ease;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.15rem rgba(13, 110, 253, 0.25);
}

.question-actions {
  min-width: 50px;
  margin-left: 1rem;
}

.question-actions .btn {
  transition: all 0.3s ease;
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
}

.question-actions .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn-group-vertical .btn {
  margin-bottom: 0.75rem;
}

.question-header {
  margin-bottom: 1.5rem;
}

.question-info {
  padding-right: 1.5rem;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Dark theme form elements */
textarea.glass-input {
  resize: vertical;
  min-height: 120px;
  line-height: 1.6;
}

.form-label {
  margin-bottom: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.form-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .questions-management {
    padding: 1rem;
  }

  .page-header, .questions-list {
    padding: 1rem;
  }

  .question-card {
    padding: 1rem;
  }
  
  .option {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
  
  .question-info {
    padding-right: 1rem;
  }

  .question-actions {
    margin-left: 0.5rem;
  }

  .question-actions .btn {
    width: 2rem;
    height: 2rem;
  }
}

.context-path {
  display: inline-flex;
  align-items: center;
  background: rgba(35, 39, 43, 0.4);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.context-path:hover {
  background: rgba(35, 39, 43, 0.6);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.context-path i {
  opacity: 0.8;
}

.context-path i.bi-chevron-right {
  font-size: 0.8rem;
  opacity: 0.6;
}
</style> 