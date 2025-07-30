<template>
  <div class="quizzes-management">
    <div class="container-fluid px-4">
      <!-- Page Header -->
      <div class="page-header glass mb-4">
        <div class="d-flex justify-content-between align-items-center">
          <div class="d-flex align-items-center">
        <button 
              class="btn btn-outline-light me-3" 
              @click="goToAdminDashboard"
        >
              <i class="bi bi-arrow-left me-2"></i>
              Back to Dashboard
        </button>
            <div>
              <h1 class="text-light mb-2">
                <i class="bi bi-clipboard-check me-1"></i>
                Quiz & Question Management
              </h1>
              <p class="text-light mb-0">
                Create and manage quizzes, and organize their questions
              </p>
            </div>
      </div>
          <div class="d-flex align-items-center">
            <select 
              v-model="selectedSubject" 
              class="form-select me-2"
              @change="onSubjectChange"
            >
              <option :value="null">All Subjects</option>
              <option 
                v-for="subject in subjects" 
                :key="subject.id" 
                :value="subject.id"
              >
                {{ subject.name }}
              </option>
            </select>
            <select 
              v-model="selectedChapter" 
              class="form-select me-2"
              @change="fetchQuizzes"
              :disabled="!selectedSubject"
            >
              <option :value="null">All Chapters</option>
              <option 
                v-for="chapter in chapters" 
                :key="chapter.id" 
                :value="chapter.id"
              >
                {{ chapter.name }}
              </option>
            </select>
      <button 
              class="btn btn-primary" 
              @click="showCreateQuizModal"
      >
              <i class="bi bi-plus-lg me-2"></i>
              Create Quiz
      </button>
    </div>
        </div>
      </div>

      <!-- Quizzes List -->
      <div class="quizzes-list glass">
        <div class="card-body">
          <!-- Quizzes Table - Always Show Something -->
          <div class="table-responsive">
            <table class="table table-dark table-glass">
              <thead>
                <tr>
                  <th><i class="bi bi-hash me-2"></i>ID</th>
                  <th><i class="bi bi-clipboard-check me-2"></i>Name</th>
                  <th><i class="bi bi-book me-2"></i>Chapter</th>
                  <th><i class="bi bi-calendar me-2"></i>Date</th>
                  <th><i class="bi bi-clock me-2"></i>Duration</th>
                  <th><i class="bi bi-question-circle me-2"></i>Questions</th>
                  <th><i class="bi bi-toggle-on me-2"></i>Status</th>
                  <th><i class="bi bi-gear me-2"></i>Actions</th>
                </tr>
              </thead>
              <tbody>
                <!-- Loading State -->
                <tr v-if="loading">
                  <td colspan="8" class="text-center py-4">
                    <div class="spinner-border text-primary mb-3"></div>
                    <p class="text-light">Loading quizzes...</p>
                  </td>
                </tr>
                
                <!-- Error State -->
                <tr v-else-if="error">
                  <td colspan="8" class="text-center py-4">
                    <div class="alert alert-danger glass-alert d-inline-block">
                      <i class="bi bi-exclamation-triangle me-2"></i>
                      {{ error }}
                    </div>
                  </td>
                </tr>
                
                <!-- Empty State -->
                <tr v-else-if="quizzes.length === 0">
                  <td colspan="8" class="text-center py-4">
                    <i class="bi bi-clipboard-check display-1 text-muted mb-3"></i>
                    <h4 class="text-light">No Quizzes Found</h4>
                    <p class="text-muted">
                      Create your first quiz by selecting a chapter and clicking "Create Quiz"
                    </p>
                  </td>
                </tr>
                
                <!-- Quiz Rows -->
                <tr v-else v-for="quiz in quizzes" :key="quiz.id" class="table-row-glass">
                  <td>
                    <span class="badge bg-primary">{{ quiz.id }}</span>
                  </td>
                  <td>
                    <strong class="text-light">{{ quiz.name }}</strong>
                    <br>
                    <small class="text-light">{{ quiz.description || 'No description' }}</small>
                  </td>
                  <td>
                    <span class="text-light">{{ quiz.chapter_name || 'N/A' }}</span>
                    <br>
                    <small class="text-light">{{ quiz.subject_name || 'N/A' }}</small>
                  </td>
                  <td>
                    <span class="text-light">
                      {{ quiz.date_of_quiz ? formatDate(quiz.date_of_quiz) : 'Not scheduled' }}
                    </span>
                  </td>
                  <td>
                    <span class="badge bg-info">{{ quiz.time_duration || 0 }} min</span>
                  </td>
                  <td>
                    <span class="badge bg-secondary">{{ quiz.questions_count || 0 }}</span>
                  </td>
                  <td>
                    <span :class="quiz.is_active ? 'badge bg-success' : 'badge bg-warning'">
                      {{ quiz.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group" role="group">
                      <button 
                        class="btn btn-sm btn-outline-primary"
                        @click="viewQuestions(quiz)"
                        title="View & Manage Questions"
                      >
                        <i class="bi bi-question-circle"></i>
                      </button>
                      <button 
                        class="btn btn-sm btn-outline-light"
                        @click="editQuiz(quiz)"
                        title="Edit Quiz"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button 
                        class="btn btn-sm btn-outline-danger"
                        @click="triggerDeleteQuiz(quiz.id)"
                        title="Delete Quiz"
                      >
                        <i class="bi bi-trash"></i>
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
            <div class="text-center py-3">
              <i class="bi bi-exclamation-triangle display-4 text-warning mb-3"></i>
              <h5 class="text-light mb-3">Delete Quiz?</h5>
              <p class="text-light">
                Are you sure you want to delete this quiz? 
              </p>
              <p class="text-muted">
                <strong>This action cannot be undone</strong> and will permanently remove:
              </p>
              <ul class="text-muted text-start">
                <li>Quiz details and settings</li>
                <li>All associated questions</li>
                <li>Student scores and attempts</li>
              </ul>
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
              type="button" 
              class="btn btn-danger" 
              @click="confirmDeleteQuiz"
            >
              Delete
            </button>
                </div>
              </div>
            </div>
          </div>

    <!-- Create/Edit Quiz Modal -->
    <div 
      class="modal fade" 
      id="quizModal" 
      tabindex="-1" 
      aria-labelledby="quizModalLabel"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content glass">
          <div class="modal-header">
            <h5 class="modal-title text-light" id="quizModalLabel">
              {{ isEditing ? 'Edit Quiz' : 'Create New Quiz' }}
            </h5>
            <button 
              type="button" 
              class="btn-close btn-close-white" 
              data-bs-dismiss="modal"
            ></button>
              </div>
          <div class="modal-body">
            <!-- Error Display -->
            <div v-if="error" class="alert alert-danger glass-alert mb-3">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ error }}
              </div>
            
            <form @submit.prevent="saveQuiz">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-book me-2"></i>Subject *
                  </label>
                  <select 
                    v-model="currentQuiz.subject_id" 
                    class="form-select glass-input"
                    @change="onSubjectChange"
                    required
                  >
                    <option :value="null">Select Subject</option>
                    <option 
                      v-for="subject in subjects" 
                      :key="subject.id" 
                      :value="subject.id"
                    >
                      {{ subject.name }}
                    </option>
                </select>
              </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-layers me-2"></i>Chapter *
                  </label>
                  <select 
                    v-model="currentQuiz.chapter_id" 
                    class="form-select glass-input"
                    :disabled="!currentQuiz.subject_id"
                    required
                  >
                    <option :value="null">
                      {{ currentQuiz.subject_id ? 'Select Chapter' : 'Select Subject First' }}
                    </option>
                    <option 
                      v-for="chapter in chapters" 
                      :key="chapter.id" 
                      :value="chapter.id"
                    >
                      {{ chapter.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-12 mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-clipboard-check me-2"></i>Quiz Name *
                  </label>
                  <input 
                    type="text" 
                    v-model="currentQuiz.name" 
                    class="form-control glass-input" 
                    placeholder="Enter a descriptive quiz name"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-calendar me-2"></i>Quiz Date (Optional)
                  </label>
                  <input 
                    type="date" 
                    v-model="currentQuiz.date_of_quiz" 
                    class="form-control glass-input"
                  />
              </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-clock me-2"></i>Duration (minutes) *
                  </label>
                  <input 
                    type="number" 
                    v-model.number="currentQuiz.time_duration" 
                    class="form-control glass-input" 
                    placeholder="60"
                    min="10"
                    max="180"
                    required
                  />
                  <small class="text-muted">Between 10 and 180 minutes</small>
              </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-percent me-2"></i>Passing Score (%) *
                  </label>
                  <input 
                    type="number" 
                    v-model.number="currentQuiz.passing_score" 
                    class="form-control glass-input" 
                    placeholder="60"
                    min="0"
                    max="100"
                    required
                  />
                  <small class="text-muted">Minimum score to pass</small>
              </div>
                <div class="col-12 mb-3">
                  <label class="form-label text-light">Description</label>
                  <textarea 
                    v-model="currentQuiz.description" 
                    class="form-control glass-input" 
                    placeholder="Optional quiz description"
                    rows="3"
                  ></textarea>
                </div>
                <div class="col-12 mb-3">
                  <div class="form-check form-switch">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      v-model="currentQuiz.is_active"
                      id="quizActiveSwitch"
                    />
                    <label class="form-check-label text-light" for="quizActiveSwitch">
                      Active Quiz
                    </label>
                  </div>
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
                >
                  {{ isEditing ? 'Update Quiz' : 'Create Quiz' }}
              </button>
            </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Questions Preview Modal -->
    <div 
      class="modal fade" 
      id="questionsModal" 
      tabindex="-1" 
      aria-labelledby="questionsModalLabel"
    >
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content glass">
          <div class="modal-header">
            <h5 class="modal-title text-light" id="questionsModalLabel">
              <i class="bi bi-question-circle me-2"></i>
              Questions for {{ selectedQuiz?.name }}
            </h5>
            <button 
              type="button" 
              class="btn-close btn-close-white" 
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body">
            <!-- Loading State -->
            <div v-if="loadingQuestions" class="text-center py-5">
              <div class="spinner-border text-primary mb-3"></div>
              <p class="text-light">Loading questions...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="questionsError" class="alert alert-danger glass-alert">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ questionsError }}
            </div>

            <!-- Empty State -->
            <div v-else-if="!quizQuestions.length" class="empty-state text-center py-5">
              <i class="bi bi-question-circle display-1 text-muted mb-3"></i>
              <h4 class="text-light">No Questions Added</h4>
              <p class="text-light">
                Add questions to this quiz by clicking the button below
              </p>
              <button 
                class="btn btn-primary mt-3"
                @click="goToQuestions(selectedQuiz.id)"
              >
                <i class="bi bi-plus-lg me-2"></i>
                Add Questions
              </button>
            </div>

            <!-- Questions List -->
            <div v-else class="questions-list">
              <div v-for="(question, index) in quizQuestions" :key="question.id" class="question-card glass mb-4">
                <div class="d-flex justify-content-between align-items-start">
                  <div class="question-content flex-grow-1">
                    <div class="d-flex align-items-center mb-2">
                      <span class="badge bg-primary me-2">Q{{ index + 1 }}</span>
                      <span class="badge bg-info me-2">{{ question.marks }} {{ question.marks === 1 ? 'point' : 'points' }}</span>
                      <span class="badge bg-secondary">{{ question.difficulty_level || 'Medium' }}</span>
                    </div>
                    <h5 class="text-light mb-3">{{ question.question_statement }}</h5>
                    
                    <!-- Options -->
                    <div class="row">
                      <div class="col-md-6 mb-2" v-for="(option, idx) in question.options" :key="idx">
                        <div class="option" :class="{ 'correct-option': question.correct_option === idx + 1 }">
                          <strong>{{ String.fromCharCode(65 + idx) }}.</strong> {{ option }}
                          <i v-if="question.correct_option === idx + 1" class="bi bi-check-circle-fill text-success ms-2"></i>
                        </div>
                      </div>
                    </div>
                  </div>
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
                @click="goToQuestions(selectedQuiz.id)"
              >
                <i class="bi bi-pencil me-2"></i>
                Manage Questions
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Modal from 'bootstrap/js/dist/modal'
import quizService from '@/services/quizService'
import chapterService from '@/services/chapterService'
import subjectService from '@/services/subjectService'

export default {
  name: 'QuizzesView',
  setup() {
    const router = useRouter()
    const quizzes = ref([])
    const chapters = ref([])
    const subjects = ref([])
    const selectedChapter = ref(null)
    const selectedSubject = ref(null)
    const loading = ref(true)  // Start with loading state
    const error = ref(null)
    const isEditing = ref(false)
    const currentQuiz = ref({
      name: '',
      description: '',
      chapter_id: null,
      date_of_quiz: '',
      time_duration: 60,
      passing_score: 60.0,
      remarks: '',
      is_active: true
    })
    const quizToDelete = ref(null)
    
    // New refs for questions preview
    const selectedQuiz = ref(null)
    const quizQuestions = ref([])
    const loadingQuestions = ref(false)
    const questionsError = ref(null)

    // Initialize with default quizzes for immediate display
    quizzes.value = [
      {
        id: 'loading-1',
        name: 'Loading quizzes...',
        description: 'Please wait while we fetch quizzes',
        chapter_name: '...',
        subject_name: '...',
        date_of_quiz: null,
        time_duration: 0,
        is_active: true,
        questions_count: 0
      }
    ]

    const fetchSubjects = async () => {
      try {
        const data = await subjectService.getSubjects()
        subjects.value = data || []
        console.log('✅ Subjects loaded:', subjects.value.length)
        return true
      } catch (err) {
        console.error('Failed to fetch subjects:', err)
        subjects.value = []
        return false
      }
    }

    const fetchChapters = async () => {
      const subjectId = selectedSubject.value
      
      if (!subjectId) {
        chapters.value = []
        return
      }

      try {
        const response = await chapterService.getChaptersBySubject(subjectId)
        chapters.value = response.data || []
        console.log('✅ Chapters loaded:', chapters.value.length)
      } catch (err) {
        console.error('Failed to fetch chapters:', err)
        chapters.value = []
      }
    }

    const fetchQuizzes = async () => {
      loading.value = true
      error.value = null

      try {
        console.log('🔍 Fetching quizzes for chapter:', selectedChapter.value)
        const data = await quizService.getQuizzes(selectedChapter.value)
        quizzes.value = data || []
        console.log('✅ Quizzes loaded:', quizzes.value.length)
      } catch (err) {
        console.error('❌ Failed to fetch quizzes:', err)
        // Set default quizzes if API fails
        quizzes.value = []
        error.value = 'Failed to load quizzes. Please try again.'
      } finally {
        loading.value = false
      }
    }

    const goToAdminDashboard = () => {
      router.push('/admin/dashboard')
    }

    const goToQuestions = (quizId) => {
      // Close any open modals
      document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
      document.body.classList.remove('modal-open');
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
      
      // Navigate to questions
      router.push(`/admin/quizzes/${quizId}/questions`)
    }

    const showCreateQuizModal = () => {
      isEditing.value = false
      error.value = null
      
      // Reset quiz form with defaults
      currentQuiz.value = {
        name: '',
        description: '',
        subject_id: selectedSubject.value || null,
        chapter_id: selectedChapter.value || null,
        date_of_quiz: '',
        time_duration: 60,
        passing_score: 60.0,
        remarks: '',
        is_active: true
      }
      
      // Ensure Bootstrap is available
      if (typeof Modal === 'undefined') {
        console.error('Bootstrap Modal not available')
        alert('Could not open create quiz form. Please refresh the page.')
        return
      }
      
      // Show the modal with error handling
      try {
        // First make sure the element exists
        const modalElement = document.getElementById('quizModal')
        if (!modalElement) {
          throw new Error('Modal element not found')
        }
        
        const modal = new Modal(modalElement)
        modal.show()
      } catch (err) {
        console.error('Could not show modal:', err)
        alert('Could not open create quiz form. Please refresh the page.')
      }
    }

    const editQuiz = (quiz) => {
      isEditing.value = true
      error.value = null
      
      currentQuiz.value = { 
        ...quiz,
        date_of_quiz: quiz.date_of_quiz || ''
      }
      
      try {
        const modal = new Modal(document.getElementById('quizModal'))
        modal.show()
      } catch (err) {
        console.error('Could not show modal:', err)
      }
    }

    const saveQuiz = async () => {
      // Reset error
      error.value = null
      
      // Validate required fields
      if (!currentQuiz.value.name?.trim()) {
        error.value = 'Please enter a quiz name'
        return
      }
      
      if (!currentQuiz.value.chapter_id) {
        error.value = 'Please select a chapter'
        return
      }

      loading.value = true

      try {
        console.log('💾 Saving quiz:', currentQuiz.value)
        
        let result
        if (isEditing.value) {
          result = await quizService.updateQuiz(currentQuiz.value.id, currentQuiz.value)
          console.log('✅ Quiz updated:', result)
        } else {
          result = await quizService.createQuiz(currentQuiz.value)
          console.log('✅ Quiz created:', result)
        }
        
        // Refresh the quizzes list
        await fetchQuizzes()
        
        // Close modal
        try {
          const modal = Modal.getInstance(document.getElementById('quizModal'))
          if (modal) modal.hide()
        } catch (err) {
          console.error('Could not close modal:', err)
        }
        
      } catch (err) {
        console.error('❌ Failed to save quiz:', err)
        error.value = 'Failed to save quiz. Please try again.'
      } finally {
        loading.value = false
      }
    }

    const triggerDeleteQuiz = (quizId) => {
      quizToDelete.value = quizId
      try {
        const modal = new Modal(document.getElementById('deleteConfirmModal'))
        modal.show()
      } catch (err) {
        console.error('Could not show delete modal:', err)
      }
    }

    const confirmDeleteQuiz = async () => {
      if (!quizToDelete.value) return

      loading.value = true
      error.value = null

      try {
        await quizService.deleteQuiz(quizToDelete.value)
        await fetchQuizzes()
        
        // Close modal
        try {
          const modal = Modal.getInstance(document.getElementById('deleteConfirmModal'))
          if (modal) modal.hide()
        } catch (err) {
          console.error('Could not close modal:', err)
        }
      } catch (err) {
        console.error('Failed to delete quiz:', err)
        error.value = 'Failed to delete quiz. Please try again.'
      } finally {
        loading.value = false
        quizToDelete.value = null
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    }

    const viewQuestions = async (quiz) => {
      selectedQuiz.value = quiz;
      loadingQuestions.value = true;
      questionsError.value = null;
      quizQuestions.value = [];

      try {
        const questions = await quizService.getQuizQuestions(quiz.id);
        quizQuestions.value = questions || [];
        
        try {
          const modal = new Modal(document.getElementById('questionsModal'));
          modal.show();
        } catch (err) {
          console.error('Could not show questions modal:', err)
        }
      } catch (err) {
        console.error('Failed to fetch questions:', err);
        questionsError.value = 'Failed to load questions';
      } finally {
        loadingQuestions.value = false;
      }
    };
    
    const onSubjectChange = async () => {
      // Reset chapter selection
      selectedChapter.value = null;
      chapters.value = [];
      
      // Fetch chapters for the selected subject
      if (selectedSubject.value) {
        await fetchChapters();
      }
      
      // Refresh quizzes based on new filters
      await fetchQuizzes();
    };

    // Initialize data
    onMounted(async () => {
      try {
        console.log('📋 Initializing QuizzesView component...')
        
        // Start with loading state
        loading.value = true
        error.value = null
        
        // Fetch subjects in background
        fetchSubjects().catch(err => {
          console.error('Failed to load subjects:', err)
          subjects.value = []
        })
        
        // Fetch initial quizzes
        await fetchQuizzes()
      } catch (err) {
        console.error('💥 Error during component initialization:', err)
        error.value = 'Could not load quiz data. Please try refreshing the page.'
      } finally {
        // Ensure loading state is always cleared
        loading.value = false
      }
    })

    return {
      quizzes,
      chapters,
      subjects,
      selectedChapter,
      selectedSubject,
      loading,
      error,
      isEditing,
      currentQuiz,
      fetchSubjects,
      fetchChapters,
      onSubjectChange,
      fetchQuizzes,
      showCreateQuizModal,
      editQuiz,
      saveQuiz,
      triggerDeleteQuiz,
      confirmDeleteQuiz,
      formatDate,
      goToAdminDashboard,
      goToQuestions,
      selectedQuiz,
      quizQuestions,
      loadingQuestions,
      questionsError,
      viewQuestions
    }
  }
}
</script>

<style scoped>
.quizzes-management {
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

.page-header, .quizzes-list {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.glass-input {
  background: rgba(35, 39, 43, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: white !important;
  transition: all 0.3s ease;
}

.glass-input:focus {
  background: rgba(35, 39, 43, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.1) !important;
}

.table-dark {
  background: transparent;
  margin-bottom: 0;
}

.table-row-glass {
  transition: all 0.3s ease;
  background: rgba(35, 39, 43, 0.4);
}

.table-row-glass:hover {
  background: rgba(35, 39, 43, 0.8) !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-group .btn {
  padding: 0.25rem 0.5rem;
  transition: all 0.3s ease;
}

.btn-group .btn:hover {
  transform: translateY(-1px);
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
}

.modal-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-alert {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 0.5rem;
  color: #fff;
  margin: 0 auto;
  max-width: 80%;
}

.empty-state {
  background: rgba(35, 39, 43, 0.3);
  border-radius: 1rem;
  padding: 3rem;
}

.form-select {
  background: rgba(35, 39, 43, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  transition: all 0.3s ease;
}

.form-select:focus {
  background: rgba(35, 39, 43, 0.8);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.1);
}

.form-select option {
  background: rgba(35, 39, 43, 0.9);
  color: white;
}

.btn-close-white {
  filter: invert(1) grayscale(100%) brightness(200%);
}

.badge {
  padding: 0.5em 0.8em;
  font-weight: 500;
}

.form-check-input {
  background-color: rgba(35, 39, 43, 0.6);
  border-color: rgba(255, 255, 255, 0.3);
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.question-card {
  background: rgba(35, 39, 43, 0.4);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.question-card:hover {
  background: rgba(35, 39, 43, 0.6);
  border-color: rgba(255, 255, 255, 0.2);
}

.option {
  background: rgba(35, 39, 43, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.3s ease;
}

.option.correct-option {
  background: rgba(25, 135, 84, 0.15);
  border-color: rgba(25, 135, 84, 0.3);
}

.question-content {
  padding-right: 1.5rem;
}
</style> 