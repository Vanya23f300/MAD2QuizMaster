<template>
  <div class="quizzes-view">
    <!-- Header Section -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3 text-light mb-0">Quizzes Management</h1>
      <button 
        class="btn btn-primary d-flex align-items-center gap-2"
        @click="showAddModal"
      >
        <i class="bi bi-plus-circle"></i>
        Add Quiz
      </button>
    </div>

    <!-- Control Bar -->
    <div class="control-bar glass-card mb-4">
      <div class="d-flex gap-3">
        <input 
          type="search" 
          class="form-control search-input flex-grow-1" 
          placeholder="Search quizzes by title..."
          v-model="searchTerm"
        />
        <select class="form-select filter-select" v-model="selectedStatus">
          <option value="">All Statuses</option>
          <option value="draft">Draft</option>
          <option value="active">Active</option>
          <option value="scheduled">Scheduled</option>
          <option value="completed">Completed</option>
        </select>
      </div>
    </div>

    <!-- Quizzes Table -->
    <div class="glass-card">
      <DataTable
        :data="filteredQuizzes"
        :columns="tableColumns"
        @edit="handleEdit"
        @delete="handleDelete"
        @view="handlePreview"
      />
    </div>

    <!-- Add/Edit Modal -->
    <FormModal
      v-model="showModal"
      :title="modalTitle"
      size="xl"
      @submit="handleSubmit"
      @cancel="handleCancel"
    >
      <form @submit.prevent="handleSubmit">
        <div class="row">
          <div class="col-md-7">
            <!-- Basic Info & Question Selection -->
            <div class="mb-3">
              <label class="form-label text-light">Quiz Title *</label>
              <input v-model="formData.title" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label text-light">Chapter *</label>
              <select v-model="formData.chapterId" class="form-select" required @change="handleChapterChange">
                <option value="">Select chapter</option>
                <option v-for="c in chapters" :key="c.id" :value="c.id">{{ c.title }}</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label text-light">Description</label>
              <textarea v-model="formData.description" class="form-control" rows="3"></textarea>
            </div>
            
            <div class="question-selection-container glass-card p-3 mt-4">
              <h6 class="text-light mb-3">Question Selection</h6>
              <div class="available-questions mb-3">
                <h6 class="text-light small">Available ({{ availableQuestions.length }})</h6>
                <div class="questions-list">
                  <div v-for="q in availableQuestions" :key="q.id" 
                       class="question-item"
                       :class="{ 'selected': isQuestionSelected(q.id) }"
                       @click="toggleQuestion(q)">
                    {{ q.content }}
                    <i v-if="isQuestionSelected(q.id)" class="bi bi-check-circle-fill text-success"></i>
                  </div>
                  <div v-if="!availableQuestions.length" class="text-muted small p-2">Select a chapter to see questions.</div>
                </div>
              </div>
              <div class="selected-questions">
                <h6 class="text-light small">Selected ({{ formData.questions.length }})</h6>
                <div class="questions-list">
                  <div v-for="(q, i) in formData.questions" :key="q.id" class="question-item selected">
                    {{ q.content }}
                    <button type="button" class="btn btn-sm btn-outline-danger" @click="removeQuestion(i)"><i class="bi bi-trash"></i></button>
                  </div>
                  <div v-if="!formData.questions.length" class="text-muted small p-2">No questions selected.</div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-5">
            <!-- Settings -->
            <div class="settings-container glass-card p-3">
              <h6 class="text-light mb-3">Quiz Settings</h6>
              <div class="mb-3">
                <label class="form-label text-light">Time Limit (minutes)</label>
                <input v-model.number="formData.timeLimit" type="number" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label text-light">Passing Score (%)</label>
                <input v-model.number="formData.passingScore" type="number" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label text-light">Status</label>
                <select v-model="formData.status" class="form-select">
                  <option value="draft">Draft</option>
                  <option value="active">Active</option>
                  <option value="scheduled">Scheduled</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div v-if="formData.status === 'scheduled'">
                <div class="mb-3">
                  <label class="form-label text-light">Start Date</label>
                  <input v-model="formData.startDate" type="datetime-local" class="form-control" />
                </div>
                <div class="mb-3">
                  <label class="form-label text-light">End Date</label>
                  <input v-model="formData.endDate" type="datetime-local" class="form-control" />
                </div>
              </div>
              <div class="form-check form-switch mb-2">
                <input v-model="formData.shuffleQuestions" class="form-check-input" type="checkbox" id="shuffleQ">
                <label class="form-check-label text-light" for="shuffleQ">Shuffle Questions</label>
              </div>
              <div class="form-check form-switch mb-2">
                <input v-model="formData.allowRetake" class="form-check-input" type="checkbox" id="retake">
                <label class="form-check-label text-light" for="retake">Allow Retake</label>
              </div>
              <div class="quiz-summary mt-3">
                <div class="d-flex justify-content-between">
                  <span class="text-muted">Total Questions:</span>
                  <span class="text-light">{{ formData.questions.length }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-muted">Total Points:</span>
                  <span class="text-light">{{ totalPoints }}</span>
                </div>
              </div>
              <button type="button" class="btn btn-outline-info w-100 mt-3" @click="showPreview" :disabled="!formData.questions.length">
                <i class="bi bi-eye"></i> Preview
              </button>
            </div>
          </div>
        </div>
      </form>
    </FormModal>

    <!-- Preview & Delete Modals -->
    <BaseModal v-model="showPreviewModal" title="Quiz Preview" size="lg">...</BaseModal>
    <DeleteConfirm v-model="showDeleteModal" :item-name="deleteItem?.title" item-type="quiz" @confirm="confirmDelete" />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import FormModal from '@/components/FormModal.vue'
import BaseModal from '@/components/Modal.vue'
import DeleteConfirm from '@/components/DeleteConfirm.vue'

export default {
  name: 'QuizzesView',
  components: { DataTable, FormModal, BaseModal, DeleteConfirm },
  setup() {
    const quizzes = ref([])
    const chapters = ref([])
    const allQuestions = ref([])
    const availableQuestions = ref([])
    const showModal = ref(false)
    const showPreviewModal = ref(false)
    const showDeleteModal = ref(false)
    const editingQuiz = ref(null)
    const deleteItem = ref(null)
    const searchTerm = ref('')
    const selectedStatus = ref('')

    const formData = ref({
      title: '', description: '', chapterId: '', questions: [],
      timeLimit: 30, passingScore: 70, shuffleQuestions: false,
      allowRetake: false, status: 'draft', startDate: '', endDate: ''
    })
    const previewData = ref({})

    const modalTitle = computed(() => editingQuiz.value ? 'Edit Quiz' : 'Create Quiz')
    const totalPoints = computed(() => formData.value.questions.reduce((sum, q) => sum + q.points, 0))

    const filteredQuizzes = computed(() => {
      let filtered = quizzes.value
      if (searchTerm.value) {
        filtered = filtered.filter(q => q.title.toLowerCase().includes(searchTerm.value.toLowerCase()))
      }
      if (selectedStatus.value) {
        filtered = filtered.filter(q => q.status === selectedStatus.value)
      }
      return filtered.map(q => ({
        ...q,
        chapterTitle: chapters.value.find(c => c.id === q.chapterId)?.title || 'N/A'
      }))
    })

    const tableColumns = [
      { key: 'title', label: 'Quiz Title' },
      { key: 'chapterTitle', label: 'Chapter' },
      { key: 'questionCount', label: 'Questions' },
      { key: 'totalPoints', label: 'Points' },
      { key: 'status', label: 'Status', badge: true },
      { key: 'actions', label: 'Actions' }
    ]
    
    const loadData = () => {
      chapters.value = [
        { id: 1, title: 'JavaScript Basics' }, { id: 2, title: 'HTML Fundamentals' }
      ]
      allQuestions.value = [
        { id: 1, content: 'What is a variable?', chapterId: 1, points: 1 },
        { id: 2, content: 'Explain hoisting.', chapterId: 1, points: 2 },
        { id: 3, content: 'What does HTML stand for?', chapterId: 2, points: 1 },
      ]
      quizzes.value = [
        { id: 1, title: 'JS Fundamentals', chapterId: 1, questionCount: 2, totalPoints: 3, status: 'active', questions: [1,2] },
        { id: 2, title: 'HTML Structure', chapterId: 2, questionCount: 1, totalPoints: 1, status: 'draft', questions: [3] },
      ]
    }

    const resetForm = () => {
      formData.value = {
        title: '', description: '', chapterId: '', questions: [], timeLimit: 30,
        passingScore: 70, shuffleQuestions: false, allowRetake: false, status: 'draft'
      }
      availableQuestions.value = []
    }

    const showAddModal = () => {
      resetForm()
      editingQuiz.value = null
      showModal.value = true
    }

    const handleEdit = (quiz) => {
      editingQuiz.value = quiz
      formData.value = { 
        ...quiz,
        questions: allQuestions.value.filter(q => quiz.questions.includes(q.id))
      }
      handleChapterChange()
      showModal.value = true
    }
    
    const handleChapterChange = () => {
      if (formData.value.chapterId) {
        availableQuestions.value = allQuestions.value.filter(q => q.chapterId === formData.value.chapterId)
      } else {
        availableQuestions.value = []
      }
      formData.value.questions = [] // Reset selection on chapter change
    }

    const isQuestionSelected = (qId) => formData.value.questions.some(q => q.id === qId)
    const toggleQuestion = (q) => {
      const index = formData.value.questions.findIndex(sq => sq.id === q.id)
      if (index === -1) formData.value.questions.push(q)
      else formData.value.questions.splice(index, 1)
    }
    const removeQuestion = (index) => formData.value.questions.splice(index, 1)

    const handleSubmit = () => {
      const payload = {
        ...formData.value,
        questions: formData.value.questions.map(q => q.id),
        questionCount: formData.value.questions.length,
        totalPoints: totalPoints.value
      }
      if (editingQuiz.value) {
        const index = quizzes.value.findIndex(q => q.id === editingQuiz.value.id)
        if (index !== -1) quizzes.value[index] = { ...editingQuiz.value, ...payload }
      } else {
        quizzes.value.push({ id: Date.now(), ...payload })
      }
      showModal.value = false
    }

    const confirmDelete = () => {
      if (deleteItem.value) {
        quizzes.value = quizzes.value.filter(q => q.id !== deleteItem.value.id)
        showDeleteModal.value = false
      }
    }

    const handleDelete = (quiz) => { deleteItem.value = quiz; showDeleteModal.value = true }
    const handlePreview = (quiz) => { 
      previewData.value = {
        ...quiz,
        questions: allQuestions.value.filter(q => quiz.questions.includes(q.id))
      }
      showPreviewModal.value = true 
    }
    const showPreview = () => { previewData.value = formData.value; showPreviewModal.value = true }
    const handleCancel = () => { showModal.value = false }
    
    onMounted(loadData)

    return {
      quizzes, chapters, availableQuestions, showModal, showPreviewModal,
      showDeleteModal, editingQuiz, deleteItem, searchTerm, selectedStatus,
      formData, previewData, modalTitle, totalPoints, filteredQuizzes, tableColumns,
      loadData, resetForm, showAddModal, handleEdit, handleDelete, handlePreview,
      handleSubmit, handleCancel, confirmDelete, handleChapterChange,
      isQuestionSelected, toggleQuestion, removeQuestion, showPreview
    }
  }
}
</script>

<style scoped>
.quizzes-view { padding: 2rem; min-height: 100vh; }
.glass-card {
  background: rgba(35, 39, 43, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
}
.control-bar { padding: 1rem; }
.search-input, .filter-select {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  color: #fff !important;
  border-radius: 0.5rem;
}
.search-input::placeholder { color: #adb5bd; }
.filter-select { width: 200px; }
.settings-container, .question-selection-container {
  height: 100%;
}
.questions-list {
  max-height: 200px;
  overflow-y: auto;
  background: rgba(0,0,0,0.2);
  border-radius: 0.5rem;
  padding: 0.5rem;
}
.question-item {
  padding: 0.5rem;
  border-radius: 0.25rem;
  cursor: pointer;
  margin-bottom: 0.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s;
  border: 1px solid transparent;
}
.question-item:hover { background-color: rgba(255,255,255,0.1); }
.question-item.selected {
  background-color: rgba(13, 110, 253, 0.2);
  border-color: rgba(13, 110, 253, 0.5);
}
.form-control, .form-select {
  background: rgba(35, 39, 43, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
}
.form-control:focus, .form-select:focus {
  background: rgba(35, 39, 43, 1);
  border-color: rgba(13, 110, 253, 0.5);
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  color: #f8f9fa;
}
</style> 