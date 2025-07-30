<template>
  <div class="subjects-view">
    <!-- Header Section -->
    <div class="page-header glass mb-4">
      <div class="d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center">
        <button 
            class="btn btn-dark-toggle me-3"
            @click="goBackToAdmin"
            title="Back to Admin Dashboard"
        >
            <i class="bi bi-arrow-left me-2"></i>
          Back
        </button>
          <div>
            <h1 class="text-light mb-2">
              <i class="bi bi-book me-3"></i>
              Subjects Management
            </h1>
            <p class="text-light mb-0">Create and manage subjects for your quiz platform</p>
          </div>
        </div>
        
      </div>
    </div>

    <!-- Create Subject Card -->
    <div class="create-subject-card glass mb-4">
      <div class="card-header">
        <h3 class="text-light mb-0">
          <i class="bi bi-plus-circle me-2"></i>
          Create New Subject
        </h3>
      </div>
      
      <div class="card-body">
        <form @submit.prevent="createSubject">
          <div class="row">
            <div class="col-md-6">
              <div class="form-group mb-3">
                <label class="form-label text-light">
                  <i class="bi bi-tag me-2"></i>Subject Name *
                </label>
      <input 
                  type="text"
                  class="form-control glass-input"
                  v-model="newSubject.name"
                  placeholder="Enter subject name (e.g., Biology, Mathematics)"
                  required
      />
    </div>
            </div>
            
            <div class="col-md-6">
              <div class="form-group mb-3">
                <label class="form-label text-light">
                  <i class="bi bi-file-text me-2"></i>Description (Optional)
                </label>
                <textarea
                  class="form-control glass-input"
                  v-model="newSubject.description"
                  rows="3"
                  placeholder="Enter subject description..."
                ></textarea>
              </div>
            </div>
          </div>
          
          <!-- Error/Success Messages -->
          <div v-if="error" class="alert alert-danger glass-alert mb-3">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ error }}
          </div>
          
          <div v-if="success" class="alert alert-success glass-alert mb-3">
            <i class="bi bi-check-circle me-2"></i>
            {{ success }}
          </div>
          
          <div class="form-actions">
            <button
              type="submit"
              class="btn btn-dark-toggle active-btn"
              :disabled="loading || !newSubject.name.trim()"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-plus-lg me-2"></i>
              {{ loading ? 'Creating...' : 'Create Subject' }}
            </button>
            
            
          </div>
        </form>
      </div>
    </div>

    <!-- Existing Subjects Card -->
    <div class="subjects-list-card glass">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h3 class="text-light mb-0">
          <i class="bi bi-list-ul me-2"></i>
          Existing Subjects
        </h3>
        
        
      </div>
      
      <div class="card-body">
        <!-- Loading State -->
        <div v-if="loading && subjects.length === 0" class="text-center py-5">
          <div class="spinner-border text-primary mb-3"></div>
          <p class="text-muted">Loading subjects...</p>
        </div>
        
        <!-- Empty State -->
        <div v-else-if="!loading && subjects.length === 0" class="empty-state text-center py-5">
          <i class="bi bi-book display-1 text-muted mb-3"></i>
          <h4 class="text-light">No Subjects Created Yet</h4>
          <p class="text-muted">Create your first subject to get started with quiz management.</p>
        </div>
        
        <!-- Subjects Table -->
        <div v-else class="table-responsive">
          <table class="table table-dark table-glass">
            <thead>
              <tr>
                <th><i class="bi bi-hash me-2"></i>ID</th>
                <th><i class="bi bi-book me-2"></i>Name</th>
                <th><i class="bi bi-file-text me-2"></i>Description</th>
                <th><i class="bi bi-calendar me-2"></i>Created At</th>
                <th><i class="bi bi-toggle-on me-2"></i>Status</th>
                <th><i class="bi bi-gear me-2"></i>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="subject in subjects" :key="subject.id" class="table-row-glass">
                <td>
                  <span class="badge bg-primary">{{ subject.id }}</span>
                </td>
                <td>
                  <strong class="text-light">{{ subject.name }}</strong>
                </td>
                <td>
                  <span class="text-light">
                    {{ subject.description || 'No description' }}
                  </span>
                </td>
                <td>
                  <small class="text-light">
                    {{ formatDate(subject.created_at) }}
                  </small>
                </td>
                <td>
                  <span
                    class="badge"
                    :class="subject.is_active ? 'active-btn' : 'btn-dark-toggle'"
                  >
                    <i :class="subject.is_active ? 'bi bi-check-circle' : 'bi bi-x-circle'" class="me-1"></i>
                    {{ subject.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button 
                      class="btn btn-sm btn-dark-toggle"
                      @click="editSubject(subject)"
                      title="Edit Subject"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button 
                      class="btn btn-sm btn-dark-toggle"
                      @click="confirmDelete(subject)"
                      title="Delete Subject"
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

    <!-- Edit Subject Modal -->
    <div class="modal fade" id="editSubjectModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass">
          <div class="modal-header">
            <h5 class="modal-title text-light">Edit Subject</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateSubject">
              <div class="mb-3">
                <label class="form-label text-light">Subject Name *</label>
                <input 
                  type="text" 
                  class="form-control glass-input"
                  v-model="editingSubject.name"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label text-light">Description</label>
                <textarea 
                  class="form-control glass-input"
                  v-model="editingSubject.description"
                  rows="3"
                ></textarea>
              </div>
              <div class="mb-3">
                <div class="form-check form-switch">
                  <input 
                    class="form-check-input" 
                    type="checkbox"
                    v-model="editingSubject.is_active"
                    id="activeSwitch"
                  >
                  <label class="form-check-label text-light" for="activeSwitch">
                    Active
                  </label>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-dark-toggle" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-dark-toggle" @click="updateSubject">Save Changes</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteConfirmModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass">
          <div class="modal-header">
            <h5 class="modal-title text-light">Delete Subject</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <p class="text-light">Are you sure you want to delete this subject? This action cannot be undone.</p>
            <div class="alert alert-warning glass-alert">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Deleting this subject will also remove all associated chapters and quizzes.
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-dark-toggle" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-dark-toggle btn-danger-toggle" @click="deleteSubject">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SubjectService from '@/services/subject-service'
import { Modal } from 'bootstrap'

export default {
  name: 'SubjectsView',
  data() {
    return {
      newSubject: {
        name: '',
        description: ''
      },
      editingSubject: {
        id: null,
        name: '',
        description: '',
        is_active: true
      },
      subjectToDelete: null,
      subjects: [],
      loading: false,
      error: '',
      success: ''
    }
  },
  computed: {
    isTokenPresent() {
      return !!localStorage.getItem('token')
    },
    isAdmin() {
      return localStorage.getItem('isAdmin') === 'true'
    },
    isAuthenticated() {
      return localStorage.getItem('isAuthenticated') === 'true'
    }
  },
  async mounted() {
    await this.fetchSubjects()
  },
  methods: {
    async createSubject() {
      this.loading = true
      this.error = ''
      this.success = ''

      try {
        console.log('🚀 Creating subject:', this.newSubject)
        
        // Validate input
        if (!this.newSubject.name.trim()) {
          this.error = 'Subject name is required'
          this.loading = false
          return
        }
        
        const result = await SubjectService.createSubject(this.newSubject)
        
        console.log('✅ Subject Creation Result:', result)
        
        if (result.success) {
          this.success = result.message
          this.resetForm()
          await this.fetchSubjects()
        } else {
          console.error('❌ Subject Creation Error:', result.message)
          this.error = result.message
        }
      } catch (error) {
        console.error('❌ Unexpected error creating subject:', error)
        
        // More detailed error logging
        if (error.response) {
          console.error('Response Error:', {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers
          })
        }
        
        this.error = error.response?.data?.message || 'Failed to create subject. Please try again.'
      } finally {
        this.loading = false
      }
    },

    async fetchSubjects() {
      this.loading = true
      this.error = ''

      try {
        console.log('Fetching subjects...')
        
        const result = await SubjectService.getAllSubjects()
        
        if (result.success) {
          this.subjects = result.data
          console.log('Subjects fetched:', this.subjects)
        } else {
          this.error = result.message
        }
      } catch (error) {
        console.error('Failed to fetch subjects:', error)
        this.error = 'Failed to retrieve subjects'
      } finally {
        this.loading = false
      }
    },

    resetForm() {
      this.newSubject = {
        name: '',
        description: ''
      }
      this.error = ''
      this.success = ''
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    goBackToAdmin() {
      this.$router.push('/admin')
    },

    editSubject(subject) {
      this.editingSubject = { 
        id: subject.id,
        name: subject.name,
        description: subject.description || '',
        is_active: subject.is_active
      }
      const modal = new Modal(document.getElementById('editSubjectModal'))
      modal.show()
    },

    async updateSubject() {
      if (!this.editingSubject.id) return

      this.loading = true
      this.error = ''
      this.success = ''

      try {
        const result = await SubjectService.updateSubject(
          this.editingSubject.id,
          this.editingSubject
        )

        if (result.success) {
          this.success = result.message
          await this.fetchSubjects()
          const modal = Modal.getInstance(document.getElementById('editSubjectModal'))
          modal.hide()
          // Reset editing subject
          this.editingSubject = {
            id: null,
            name: '',
            description: '',
            is_active: true
          }
        } else {
          this.error = result.message
        }
      } catch (error) {
        console.error('Failed to update subject:', error)
        this.error = 'Failed to update subject'
      } finally {
        this.loading = false
      }
    },

    confirmDelete(subject) {
      this.subjectToDelete = subject
      const modal = new Modal(document.getElementById('deleteConfirmModal'))
      modal.show()
    },

    async deleteSubject() {
      if (!this.subjectToDelete) return

      this.loading = true
      this.error = ''
      this.success = ''

      try {
        const result = await SubjectService.deleteSubject(this.subjectToDelete.id)

        if (result.success) {
          this.success = result.message
          await this.fetchSubjects()
          const modal = Modal.getInstance(document.getElementById('deleteConfirmModal'))
          modal.hide()
        } else {
          this.error = result.message
          // If there are dependencies, show a more specific error
          if (result.error?.error === 'HAS_DEPENDENCIES') {
            this.error = 'Cannot delete subject with existing chapters. Please delete chapters first.'
          }
        }
      } catch (error) {
        console.error('Failed to delete subject:', error)
        this.error = error.response?.data?.message || 'Failed to delete subject'
      } finally {
        this.loading = false
        this.subjectToDelete = null
      }
    }
  }
}
</script>

<style scoped>
.subjects-view {
  padding: 2rem;
  min-height: 100vh;
}

.page-header {
  padding: 2rem;
  border-radius: 1rem;
}

.debug-info {
  border-radius: 0.5rem;
  font-family: 'Courier New', monospace;
}

.create-subject-card,
.subjects-list-card {
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.card-header {
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
}

.card-body {
  padding: 2rem;
}

.glass-input {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 0.75rem !important;
  color: #ffffff !important;
  padding: 0.75rem 1rem !important;
  transition: all 0.3s ease !important;
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(108, 117, 125, 0.5) !important;
  box-shadow: 0 0 0 0.25rem rgba(108, 117, 125, 0.25) !important;
  color: #ffffff !important;
}

.glass-input::placeholder {
  color: rgba(255, 255, 255, 0.5) !important;
}

.glass-alert {
  background: rgba(255, 255, 255, 0.1) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  border-radius: 0.75rem !important;
  backdrop-filter: blur(10px);
}

.form-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.table-glass {
  background: rgba(255, 255, 255, 0.03) !important;
  border-radius: 0.75rem;
  overflow: hidden;
}

.table-glass th {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  color: #ffffff !important;
  font-weight: 600;
  padding: 1rem;
}

.table-row-glass {
  background: rgba(255, 255, 255, 0.02) !important;
  border-color: rgba(255, 255, 255, 0.05) !important;
  transition: all 0.3s ease;
}

.table-row-glass:hover {
  background: rgba(255, 255, 255, 0.05) !important;
  transform: translateX(2px);
}

.table-row-glass td {
  padding: 1rem;
  border-color: rgba(255, 255, 255, 0.05) !important;
  vertical-align: middle;
}

.empty-state {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 1rem;
  margin: 2rem 0;
}

.btn {
  border-radius: 0.75rem !important;
  padding: 0.75rem 1.5rem !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.btn:hover {
  transform: translateY(-1px) !important;
}

.btn-dark-toggle {
  background: rgba(40, 44, 52, 0.8) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(4px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  border-radius: 1.25rem !important;
}

.btn-dark-toggle:hover {
  background: rgba(60, 65, 75, 0.9) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: rgba(255, 255, 255, 1) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.btn-dark-toggle:focus {
  box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.1) !important;
}

.btn-dark-toggle:disabled {
  background: rgba(40, 44, 52, 0.4) !important;
  color: rgba(255, 255, 255, 0.4) !important;
}

.btn-danger-toggle {
  background: rgba(220, 53, 69, 0.2) !important;
  border-color: rgba(220, 53, 69, 0.4) !important;
  color: rgba(220, 53, 69, 0.9) !important;
}

.btn-danger-toggle:hover {
  background: rgba(220, 53, 69, 0.3) !important;
  border-color: rgba(220, 53, 69, 0.5) !important;
  color: rgba(220, 53, 69, 1) !important;
}

/* Active state button styling to match screenshot */
.active-btn {
  background: #24a35a !important;
  color: white !important;
  border: none !important;
  border-radius: 1.25rem !important;
  padding: 0.75rem 2rem !important;
  font-weight: 600 !important;
  font-size: 1.1rem !important;
  box-shadow: 0 4px 12px rgba(36, 163, 90, 0.3) !important;
  transition: all 0.3s ease !important;
}

.active-btn:hover {
  background: #1e8a4a !important;
  box-shadow: 0 6px 16px rgba(36, 163, 90, 0.4) !important;
  transform: translateY(-2px) !important;
}

.active-btn:focus {
  box-shadow: 0 0 0 0.25rem rgba(36, 163, 90, 0.25) !important;
}

.badge {
  font-size: 0.8rem;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

@media (max-width: 768px) {
  .subjects-view {
    padding: 1rem;
  }
  
  .page-header {
    padding: 1.5rem;
  }
  
  .card-body {
    padding: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .form-actions .btn {
    margin-bottom: 0.5rem;
  }
}

.btn-group .btn {
  padding: 0.25rem 0.5rem;
  transition: all 0.3s ease;
  margin: 0 0.125rem;
  border-radius: 1.25rem !important;
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-group .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn-group .btn i {
  font-size: 1rem;
}

.btn-outline-primary {
  color: #0d6efd;
  border-color: #0d6efd;
}

.btn-outline-primary:hover {
  background-color: rgba(13, 110, 253, 0.1);
  border-color: #0d6efd;
  color: #0d6efd;
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  background-color: rgba(220, 53, 69, 0.1);
  border-color: #dc3545;
  color: #dc3545;
}

.form-switch .form-check-input {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  width: 3em;
  height: 1.5em;
  margin-top: 0.2em;
  border-radius: 1.25rem;
}

.form-switch .form-check-input:checked {
  background-color: #24a35a;
  border-color: #24a35a;
}

.form-switch .form-check-input:focus {
  border-color: #24a35a;
  box-shadow: 0 0 0 0.25rem rgba(36, 163, 90, 0.25);
}

.modal-content.glass {
  background: rgba(35, 39, 43, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
}

.glass-alert.alert-warning {
  background: rgba(255, 193, 7, 0.1);
  border-color: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}
</style> 