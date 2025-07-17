<template>
  <div class="subjects-view">
    <!-- Header Section -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3 text-light mb-0">Subjects Management</h1>
      <button 
        class="btn btn-primary d-flex align-items-center gap-2"
        @click="showAddModal"
      >
        <i class="bi bi-plus-circle"></i>
        Add Subject
      </button>
    </div>

    <!-- Control Bar -->
    <div class="control-bar glass-card mb-4">
      <input 
        type="search" 
        class="form-control search-input" 
        placeholder="Search subjects by name or description..."
        v-model="searchTerm"
      />
    </div>

    <!-- Subjects Table -->
    <div class="glass-card">
      <DataTable
        :data="filteredSubjects"
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
          <label for="subjectName" class="form-label text-light">Subject Name *</label>
          <input
            id="subjectName"
            v-model="formData.name"
            type="text"
            class="form-control"
            placeholder="e.g., Computer Science"
            required
          >
        </div>
        <div class="mb-3">
          <label for="subjectDescription" class="form-label text-light">Description</label>
          <textarea
            id="subjectDescription"
            v-model="formData.description"
            class="form-control"
            rows="3"
            placeholder="e.g., Programming, algorithms, and software development"
          ></textarea>
        </div>
        <div class="mb-3">
          <label class="form-label text-light">Status</label>
          <select v-model="formData.status" class="form-select">
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
      </form>
    </FormModal>

    <!-- Delete Confirmation -->
    <DeleteConfirm
      v-model="showDeleteModal"
      :item-name="deleteItem?.name"
      item-type="subject"
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
  name: 'SubjectsView',
  components: {
    DataTable,
    FormModal,
    DeleteConfirm
  },
  setup() {
    const subjects = ref([])
    const showModal = ref(false)
    const showDeleteModal = ref(false)
    const editingSubject = ref(null)
    const deleteItem = ref(null)
    const searchTerm = ref('')

    const formData = ref({
      name: '',
      description: '',
      status: 'active'
    })

    const modalTitle = computed(() => 
      editingSubject.value ? 'Edit Subject' : 'Add New Subject'
    )

    const filteredSubjects = computed(() => {
      if (!searchTerm.value) {
        return subjects.value
      }
      return subjects.value.filter(subject =>
        subject.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
        subject.description.toLowerCase().includes(searchTerm.value.toLowerCase())
      )
    })

    const tableColumns = [
      { key: 'name', label: 'Subject Name' },
      { key: 'description', label: 'Description', truncate: true },
      { key: 'status', label: 'Status', badge: true },
      { key: 'chapters', label: 'Chapters' },
      { key: 'questions', label: 'Questions' },
      { key: 'created', label: 'Created' },
      { key: 'actions', label: 'Actions' }
    ]

    const loadSubjects = () => {
      subjects.value = [
        { id: 1, name: 'Biology', description: 'Study of living organisms and their interactions', status: 'inactive', chapters: 6, questions: 80, created: '10/02/2024' },
        { id: 2, name: 'Chemistry', description: 'Chemical reactions, elements, and compounds', status: 'active', chapters: 10, questions: 95, created: '01/02/2024' },
        { id: 3, name: 'Computer Science', description: 'Programming, algorithms, and software development', status: 'active', chapters: 15, questions: 200, created: '15/02/2024' },
        { id: 4, name: 'Mathematics', description: 'Advanced mathematics including algebra, calculus, and geometry', status: 'active', chapters: 12, questions: 150, created: '15/01/2024' },
        { id: 5, name: 'Physics', description: 'Fundamental physics concepts and principles', status: 'active', chapters: 8, questions: 120, created: '20/01/2024' }
      ]
    }

    const resetForm = () => {
      formData.value = {
        name: '',
        description: '',
        status: 'active'
      }
    }

    const showAddModal = () => {
      resetForm()
      editingSubject.value = null
      showModal.value = true
    }

    const handleEdit = (subject) => {
      editingSubject.value = subject
      formData.value = {
        name: subject.name,
        description: subject.description,
        status: subject.status
      }
      showModal.value = true
    }

    const handleDelete = (subject) => {
      deleteItem.value = subject
      showDeleteModal.value = true
    }

    const handleSubmit = () => {
      if (editingSubject.value) {
        const index = subjects.value.findIndex(s => s.id === editingSubject.value.id)
        if (index !== -1) {
          subjects.value[index] = {
            ...editingSubject.value,
            ...formData.value
          }
        }
      } else {
        subjects.value.push({
          id: Date.now(),
          ...formData.value,
          chapters: 0,
          questions: 0,
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
        subjects.value = subjects.value.filter(s => s.id !== deleteItem.value.id)
        deleteItem.value = null
      }
      showDeleteModal.value = false
    }

    onMounted(loadSubjects)

    return {
      subjects,
      showModal,
      showDeleteModal,
      editingSubject,
      deleteItem,
      searchTerm,
      formData,
      modalTitle,
      filteredSubjects,
      tableColumns,
      showAddModal,
      handleEdit,
      handleDelete,
      handleSubmit,
      handleCancel,
      confirmDelete
    }
  }
}
</script>

<style scoped>
.subjects-view {
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

.search-input {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  color: #fff !important;
  border-radius: 0.5rem;
}

.search-input::placeholder {
  color: #adb5bd;
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