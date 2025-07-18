<template>
  <div class="chapters-view">
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
        <h1 class="h3 text-light mb-0">Chapters Management</h1>
      </div>
      <button 
        class="btn btn-primary d-flex align-items-center gap-2"
        @click="showAddModal"
      >
        <i class="bi bi-plus-circle"></i>
        Add Chapter
      </button>
    </div>

    <!-- Control Bar -->
    <div class="control-bar glass-card mb-4">
      <div class="d-flex gap-3">
        <input 
          type="search" 
          class="form-control search-input flex-grow-1" 
          placeholder="Search chapters by title..."
          v-model="searchTerm"
        />
        <select 
          class="form-select filter-select" 
          v-model="selectedSubject"
        >
          <option value="">All Subjects</option>
          <option 
            v-for="subject in subjects" 
            :key="subject.id" 
            :value="subject.id"
          >
            {{ subject.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Chapters Table -->
    <div class="glass-card">
      <DataTable
        :data="filteredChapters"
        :columns="tableColumns"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>

    <!-- Add/Edit Modal -->
    <FormModal
      v-model="showModal"
      :title="modalTitle"
      @submit="handleSubmit"
      @cancel="handleCancel"
    >
      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="chapterName" class="form-label text-light">Chapter Title *</label>
          <input
            id="chapterName"
            v-model="formData.title"
            type="text"
            class="form-control"
            placeholder="e.g., Introduction to JavaScript"
            required
          >
        </div>
        <div class="mb-3">
          <label for="subject" class="form-label text-light">Subject *</label>
          <select
            id="subject"
            v-model="formData.subjectId"
            class="form-select"
            required
          >
            <option value="">Select a subject</option>
            <option 
              v-for="subject in subjects" 
              :key="subject.id" 
              :value="subject.id"
            >
              {{ subject.name }}
            </option>
          </select>
        </div>
        <div class="mb-3">
          <label for="chapterDescription" class="form-label text-light">Description</label>
          <textarea
            id="chapterDescription"
            v-model="formData.description"
            class="form-control"
            rows="3"
            placeholder="e.g., Variables, data types, and basic syntax"
          ></textarea>
        </div>
      </form>
    </FormModal>

    <!-- Delete Confirmation -->
    <DeleteConfirm
      v-model="showDeleteModal"
      :item-name="deleteItem?.title"
      item-type="chapter"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import FormModal from '@/components/FormModal.vue'
import DeleteConfirm from '@/components/DeleteConfirm.vue'

export default {
  name: 'ChaptersView',
  components: {
    DataTable,
    FormModal,
    DeleteConfirm
  },
  setup() {
    const chapters = ref([])
    const subjects = ref([])
    const showModal = ref(false)
    const showDeleteModal = ref(false)
    const editingChapter = ref(null)
    const deleteItem = ref(null)
    const searchTerm = ref('')
    const selectedSubject = ref('')

    const formData = ref({
      title: '',
      description: '',
      subjectId: ''
    })

    const modalTitle = computed(() => 
      editingChapter.value ? 'Edit Chapter' : 'Add New Chapter'
    )

    const filteredChapters = computed(() => {
      let filtered = chapters.value

      if (searchTerm.value) {
        filtered = filtered.filter(chapter =>
          chapter.title.toLowerCase().includes(searchTerm.value.toLowerCase())
        )
      }

      if (selectedSubject.value) {
        filtered = filtered.filter(chapter => chapter.subjectId === selectedSubject.value)
      }

      return filtered.map(chapter => ({
        ...chapter,
        subjectName: subjects.value.find(s => s.id === chapter.subjectId)?.name || 'N/A'
      }))
    })

    const tableColumns = [
      { key: 'title', label: 'Chapter Title' },
      { key: 'subjectName', label: 'Subject' },
      { key: 'questionsCount', label: 'Questions' },
      { key: 'created', label: 'Created' }
    ]

    const loadData = () => {
      subjects.value = [
        { id: 1, name: 'Computer Science' },
        { id: 2, name: 'Mathematics' },
        { id: 3, name: 'Physics' }
      ]

      chapters.value = [
        { id: 1, title: 'Introduction to Algorithms', subjectId: 1, questionsCount: 25, created: '20/02/2024' },
        { id: 2, title: 'Data Structures', subjectId: 1, questionsCount: 30, created: '22/02/2024' },
        { id: 3, title: 'Calculus I', subjectId: 2, questionsCount: 40, created: '15/02/2024' },
        { id: 4, title: 'Mechanics', subjectId: 3, questionsCount: 20, created: '18/02/2024' }
      ]
    }

    const resetForm = () => {
      formData.value = {
        title: '',
        description: '',
        subjectId: ''
      }
    }

    const showAddModal = () => {
      resetForm()
      editingChapter.value = null
      showModal.value = true
    }

    const handleEdit = (chapter) => {
      editingChapter.value = chapter
      formData.value = {
        title: chapter.title,
        description: chapter.description,
        subjectId: chapter.subjectId
      }
      showModal.value = true
    }

    const handleDelete = (chapter) => {
      deleteItem.value = chapter
      showDeleteModal.value = true
    }

    const handleSubmit = () => {
      if (editingChapter.value) {
        const index = chapters.value.findIndex(c => c.id === editingChapter.value.id)
        if (index !== -1) {
          chapters.value[index] = { ...editingChapter.value, ...formData.value }
        }
      } else {
        chapters.value.push({
          id: Date.now(),
          ...formData.value,
          questionsCount: 0,
          created: new Date().toLocaleDateString()
        })
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
        chapters.value = chapters.value.filter(c => c.id !== deleteItem.value.id)
        deleteItem.value = null
      }
      showDeleteModal.value = false
    }

    onMounted(loadData)

    const goBack = () => {
      // Navigate back to admin dashboard
      // You can use router.push('/admin') or router.go(-1)
      window.history.back()
    }

    return {
      chapters,
      subjects,
      showModal,
      showDeleteModal,
      editingChapter,
      deleteItem,
      searchTerm,
      selectedSubject,
      formData,
      modalTitle,
      filteredChapters,
      tableColumns,
      showAddModal,
      handleEdit,
      handleDelete,
      handleSubmit,
      handleCancel,
      confirmDelete,
      goBack
    }
  }
}
</script>

<style scoped>
.chapters-view {
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

.control-bar {
  padding: 1rem;
}

.search-input, .filter-select {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  color: #fff !important;
  border-radius: 0.5rem;
}

.search-input::placeholder {
  color: #adb5bd;
}

.filter-select {
  width: 200px;
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