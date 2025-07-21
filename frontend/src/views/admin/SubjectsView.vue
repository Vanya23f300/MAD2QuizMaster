<template>
  <div class="subjects-view">
    <!-- Header Section -->
    <div class="page-header glass mb-4">
      <div class="d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center">
        <button 
            class="btn btn-outline-light me-3"
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
              class="btn btn-primary btn-lg"
              :disabled="loading || !newSubject.name.trim()"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-plus-lg me-2"></i>
              {{ loading ? 'Creating...' : 'Create Subject' }}
            </button>
            
            <button
              type="button"
              class="btn btn-outline-light ms-3"
              @click="resetForm"
            >
              <i class="bi bi-arrow-clockwise me-2"></i>
              Reset
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
        
        <button
          class="btn btn-outline-light btn-sm"
          @click="fetchSubjects"
          :disabled="loading"
        >
          <i class="bi bi-arrow-clockwise me-2"></i>
          Refresh
        </button>
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
                  <span class="text-muted">
                    {{ subject.description || 'No description' }}
                  </span>
                </td>
                <td>
                  <small class="text-muted">
                    {{ formatDate(subject.created_at) }}
                  </small>
                </td>
                <td>
                  <span
                    class="badge"
                    :class="subject.is_active ? 'bg-success' : 'bg-secondary'"
                  >
                    <i :class="subject.is_active ? 'bi bi-check-circle' : 'bi bi-x-circle'" class="me-1"></i>
                    {{ subject.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SubjectService from '@/services/subject-service'

export default {
  name: 'SubjectsView',
  data() {
    return {
      newSubject: {
        name: '',
        description: ''
      },
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
</style> 