<template>
  <div class="questions-view">
    <!-- Header Section -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div class="d-flex align-items-center gap-3">
        <button 
          class="btn btn-outline-light d-flex align-items-center gap-2"
          @click="goBack"
        >
          <i class="bi bi-arrow-left"></i>
          Back
        </button>
        <h1 class="h3 text-light mb-0">Questions Management</h1>
      </div>
      <button 
        class="btn btn-primary d-flex align-items-center gap-2"
        @click="showAddModal"
      >
        <i class="bi bi-plus-circle"></i>
        Add Question
      </button>
    </div>

    <!-- Control Bar -->
    <div class="control-bar glass-card mb-4">
      <div class="d-flex flex-wrap gap-3">
        <input 
          type="search" 
          class="form-control search-input flex-grow-1" 
          placeholder="Search questions by content..."
          v-model="searchTerm"
        />
        <select class="form-select filter-select" v-model="selectedChapter">
          <option value="">All Chapters</option>
          <option v-for="c in chapters" :key="c.id" :value="c.id">{{ c.title }}</option>
        </select>
        <select class="form-select filter-select" v-model="selectedType">
          <option value="">All Types</option>
          <option value="multiple_choice">Multiple Choice</option>
          <option value="true_false">True/False</option>
          <option value="essay">Essay</option>
        </select>
        <select class="form-select filter-select" v-model="selectedDifficulty">
          <option value="">All Difficulties</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>
    </div>

    <!-- Questions Table -->
    <div class="glass-card">
      <DataTable
        :data="filteredQuestions"
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
          <div class="col-md-8">
            <!-- Question Content -->
            <div class="mb-3">
              <label class="form-label text-light">Question Content *</label>
              <textarea
                v-model="formData.content"
                class="form-control"
                rows="4"
                placeholder="Enter your question here..."
                required
              ></textarea>
            </div>

            <!-- Question Type -->
            <div class="mb-3">
              <label class="form-label text-light">Question Type *</label>
              <select
                v-model="formData.type"
                class="form-select"
                required
                @change="handleTypeChange"
              >
                <option value="">Select question type</option>
                <option value="multiple_choice">Multiple Choice</option>
                <option value="true_false">True/False</option>
                <option value="essay">Essay</option>
              </select>
            </div>

            <!-- Multiple Choice Options -->
            <div v-if="formData.type === 'multiple_choice'" class="mb-3">
              <label class="form-label text-light">Answer Options *</label>
              <div class="options-container">
                <div
                  v-for="(option, index) in formData.options"
                  :key="index"
                  class="option-item mb-2"
                >
                  <div class="d-flex gap-3 align-items-center">
                    <div class="form-check">
                      <input
                        :id="`option-${index}`"
                        v-model="formData.correctAnswer"
                        class="form-check-input"
                        type="radio"
                        :value="index"
                        name="correctAnswer"
                      >
                      <label :for="`option-${index}`" class="form-check-label text-light">
                        Correct
                      </label>
                    </div>
                    <input
                      v-model="option.text"
                      type="text"
                      class="form-control"
                      :placeholder="`Option ${index + 1}`"
                      required
                    >
                    <button
                      v-if="formData.options.length > 2"
                      type="button"
                      class="btn btn-sm btn-outline-danger"
                      @click="removeOption(index)"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </div>
                <button
                  v-if="formData.options.length < 6"
                  type="button"
                  class="btn btn-sm btn-outline-primary mt-2"
                  @click="addOption"
                >
                  <i class="bi bi-plus"></i> Add Option
                </button>
              </div>
            </div>

            <!-- True/False Options -->
            <div v-if="formData.type === 'true_false'" class="mb-3">
              <label class="form-label text-light">Correct Answer *</label>
              <div class="d-flex gap-3">
                <div class="form-check">
                  <input
                    id="true-option"
                    v-model="formData.correctAnswer"
                    class="form-check-input"
                    type="radio"
                    value="true"
                    name="trueFalseAnswer"
                  >
                  <label for="true-option" class="form-check-label text-light">
                    True
                  </label>
                </div>
                <div class="form-check">
                  <input
                    id="false-option"
                    v-model="formData.correctAnswer"
                    class="form-check-input"
                    type="radio"
                    value="false"
                    name="trueFalseAnswer"
                  >
                  <label for="false-option" class="form-check-label text-light">
                    False
                  </label>
                </div>
              </div>
            </div>

            <!-- Explanation -->
            <div class="mb-3">
              <label class="form-label text-light">Explanation (Optional)</label>
              <textarea
                v-model="formData.explanation"
                class="form-control"
                rows="3"
                placeholder="Provide explanation for the correct answer..."
              ></textarea>
            </div>
          </div>

          <div class="col-md-4">
            <!-- Question Details -->
            <div class="question-details">
              <h6 class="text-light mb-3">Question Details</h6>
              
              <!-- Chapter -->
              <div class="mb-3">
                <label class="form-label text-light">Chapter *</label>
                <select
                  v-model="formData.chapterId"
                  class="form-select"
                  required
                >
                  <option value="">Select chapter</option>
                  <option
                    v-for="chapter in chapters"
                    :key="chapter.id"
                    :value="chapter.id"
                  >
                    {{ chapter.title }} ({{ chapter.subjectName }})
                  </option>
                </select>
              </div>

              <!-- Difficulty -->
              <div class="mb-3">
                <label class="form-label text-light">Difficulty</label>
                <select v-model="formData.difficulty" class="form-select">
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>

              <!-- Points -->
              <div class="mb-3">
                <label class="form-label text-light">Points</label>
                <input
                  v-model.number="formData.points"
                  type="number"
                  class="form-control"
                  min="1"
                  max="10"
                >
              </div>

              <!-- Preview Button -->
              <button
                type="button"
                class="btn btn-outline-info w-100 mt-3"
                @click="showPreview"
              >
                <i class="bi bi-eye"></i> Preview Question
              </button>
            </div>
          </div>
        </div>
      </form>
    </FormModal>

    <!-- Preview Modal -->
    <BaseModal
      v-model="showPreviewModal"
      title="Question Preview"
      size="lg"
    >
      <div class="question-preview">
        <div class="question-content mb-4">
          <h5 class="text-light mb-3">{{ previewData.content }}</h5>
          <span class="badge bg-primary me-2">{{ previewData.type?.replace('_', ' ').toUpperCase() }}</span>
          <span class="badge bg-secondary me-2">{{ previewData.difficulty?.toUpperCase() }}</span>
          <span class="badge bg-info">{{ previewData.points }} pts</span>
        </div>

        <div v-if="previewData.type === 'multiple_choice'" class="options-preview">
          <div
            v-for="(option, index) in previewData.options"
            :key="index"
            class="option-preview-item mb-2"
            :class="{ 'correct': index === previewData.correctAnswer }"
          >
            <div class="form-check">
              <input
                :id="`preview-option-${index}`"
                class="form-check-input"
                type="radio"
                disabled
                :checked="index === previewData.correctAnswer"
              >
              <label :for="`preview-option-${index}`" class="form-check-label text-light">
                {{ option.text }}
                <i v-if="index === previewData.correctAnswer" class="bi bi-check-circle text-success ms-2"></i>
              </label>
            </div>
          </div>
        </div>

        <div v-if="previewData.type === 'true_false'" class="true-false-preview">
          <div class="d-flex gap-3">
            <div class="form-check">
              <input
                id="preview-true"
                class="form-check-input"
                type="radio"
                disabled
                :checked="previewData.correctAnswer === 'true'"
              >
              <label for="preview-true" class="form-check-label text-light">
                True
                <i v-if="previewData.correctAnswer === 'true'" class="bi bi-check-circle text-success ms-2"></i>
              </label>
            </div>
            <div class="form-check">
              <input
                id="preview-false"
                class="form-check-input"
                type="radio"
                disabled
                :checked="previewData.correctAnswer === 'false'"
              >
              <label for="preview-false" class="form-check-label text-light">
                False
                <i v-if="previewData.correctAnswer === 'false'" class="bi bi-check-circle text-success ms-2"></i>
              </label>
            </div>
          </div>
        </div>

        <div v-if="previewData.explanation" class="explanation-preview mt-4">
          <h6 class="text-light">Explanation:</h6>
          <p class="text-muted">{{ previewData.explanation }}</p>
        </div>
      </div>
    </BaseModal>

    <!-- Delete Confirmation -->
    <DeleteConfirm
      v-model="showDeleteModal"
      :item-name="deleteItem?.content"
      item-type="question"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import FormModal from '@/components/FormModal.vue'
import BaseModal from '@/components/Modal.vue'
import DeleteConfirm from '@/components/DeleteConfirm.vue'

export default {
  name: 'QuestionsView',
  components: {
    DataTable,
    FormModal,
    BaseModal,
    DeleteConfirm
  },
  setup() {
    // Reactive data
    const questions = ref([])
    const chapters = ref([])
    const showModal = ref(false)
    const showPreviewModal = ref(false)
    const showDeleteModal = ref(false)
    const editingQuestion = ref(null)
    const deleteItem = ref(null)
    const searchTerm = ref('')
    const selectedChapter = ref('')
    const selectedType = ref('')
    const selectedDifficulty = ref('')

    // Form data
    const formData = ref({
      content: '',
      type: '',
      chapterId: '',
      difficulty: 'medium',
      points: 1,
      options: [
        { text: '' },
        { text: '' }
      ],
      correctAnswer: '',
      explanation: ''
    })

    const previewData = ref({})

    // Computed properties
    const modalTitle = computed(() => 
      editingQuestion.value ? 'Edit Question' : 'Add New Question'
    )

    const filteredQuestions = computed(() => {
      let filtered = questions.value

      if (searchTerm.value) {
        filtered = filtered.filter(q =>
          q.content.toLowerCase().includes(searchTerm.value.toLowerCase())
        )
      }

      if (selectedChapter.value) {
        filtered = filtered.filter(q => q.chapterId === selectedChapter.value)
      }

      if (selectedType.value) {
        filtered = filtered.filter(q => q.type === selectedType.value)
      }

      if (selectedDifficulty.value) {
        filtered = filtered.filter(q => q.difficulty === selectedDifficulty.value)
      }

      return filtered.map(q => ({
        ...q,
        chapterTitle: chapters.value.find(c => c.id === q.chapterId)?.title || 'N/A'
      }))
    })

    // Table columns
    const tableColumns = [
      { key: 'content', label: 'Question', truncate: true },
      { key: 'type', label: 'Type', badge: true },
      { key: 'chapterTitle', label: 'Chapter' },
      { key: 'difficulty', label: 'Difficulty', badge: true },
      { key: 'points', label: 'Points' }
    ]

    // Methods
    const loadData = () => {
      chapters.value = [
        { id: 1, title: 'European Geography', subjectName: 'Geography' },
        { id: 2, title: 'Basic Science', subjectName: 'Science' },
        { id: 3, title: 'Plant Biology', subjectName: 'Biology' },
      ]
      questions.value = [
        { id: 1, content: 'What is the capital of France?', type: 'multiple_choice', chapterId: 1, difficulty: 'easy', points: 1, options: [{text:'London'}, {text:'Paris'}], correctAnswer: 1 },
        { id: 2, content: 'The Earth is flat.', type: 'true_false', chapterId: 2, difficulty: 'easy', points: 1, correctAnswer: 'false' },
        { id: 3, content: 'Explain the process of photosynthesis.', type: 'essay', chapterId: 3, difficulty: 'hard', points: 5 },
      ]
    }

    const resetForm = () => {
      formData.value = {
        content: '', type: '', chapterId: '', difficulty: 'medium', points: 1,
        options: [{ text: '' }, { text: '' }], correctAnswer: '', explanation: ''
      }
    }

    const showAddModal = () => {
      resetForm()
      editingQuestion.value = null
      showModal.value = true
    }

    const handleEdit = (question) => {
      editingQuestion.value = question
      formData.value = { ...question }
      showModal.value = true
    }

    const handleDelete = (question) => {
      deleteItem.value = question
      showDeleteModal.value = true
    }

    const handlePreview = (question) => {
      previewData.value = { ...question }
      showPreviewModal.value = true
    }

    const handleTypeChange = () => {
      if (formData.value.type === 'multiple_choice') {
        formData.value.options = [{ text: '' }, { text: '' }]
        formData.value.correctAnswer = ''
      } else if (formData.value.type === 'true_false') {
        formData.value.correctAnswer = ''
      }
    }

    const addOption = () => {
      if (formData.value.options.length < 6) formData.value.options.push({ text: '' })
    }

    const removeOption = (index) => {
      if (formData.value.options.length > 2) {
        formData.value.options.splice(index, 1)
        if (formData.value.correctAnswer === index) formData.value.correctAnswer = ''
        else if (formData.value.correctAnswer > index) formData.value.correctAnswer--
      }
    }

    const showPreview = () => {
      previewData.value = { ...formData.value }
      showPreviewModal.value = true
    }

    const handleSubmit = () => {
      if (editingQuestion.value) {
        const index = questions.value.findIndex(q => q.id === editingQuestion.value.id)
        if (index !== -1) questions.value[index] = { ...editingQuestion.value, ...formData.value }
      } else {
        questions.value.push({ id: Date.now(), ...formData.value })
      }
      showModal.value = false
      resetForm()
    }

    const handleCancel = () => {
      showModal.value = false
      resetForm()
    }

    const confirmDelete = () => {
      if (deleteItem.value) {
        questions.value = questions.value.filter(q => q.id !== deleteItem.value.id)
        deleteItem.value = null
      }
      showDeleteModal.value = false
    }

    onMounted(loadData)

    const goBack = () => {
      window.history.back()
    }

    return {
      questions, chapters, showModal, showPreviewModal, showDeleteModal,
      editingQuestion, deleteItem, searchTerm, selectedChapter, selectedType,
      selectedDifficulty, formData, previewData, modalTitle, filteredQuestions,
      tableColumns, showAddModal, handleEdit, handleDelete, handlePreview,
      handleTypeChange, addOption, removeOption, showPreview, handleSubmit,
      handleCancel, confirmDelete, goBack
    }
  }
}
</script>

<style scoped>
.questions-view {
  padding: 2rem;
  min-height: 100vh;
}
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
.filter-select { min-width: 150px; }
.options-container {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1rem;
}
.question-details {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1.5rem;
  position: sticky;
  top: 2rem;
}
.question-preview .option-preview-item.correct {
  border-color: #198754;
  background: rgba(25, 135, 84, 0.1);
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