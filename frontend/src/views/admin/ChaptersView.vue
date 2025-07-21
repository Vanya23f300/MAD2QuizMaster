<template>
  <div class="chapters-management">
    <div class="container-fluid px-4">
      <!-- Page Header -->
      <div class="page-header glass mb-4">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h1 class="text-light mb-2">
              <i class="bi bi-layers me-1"></i>
              Chapters Management
            </h1>
            <p class="text-light mb-0">
              Create, edit, and manage chapters for your quiz platform
            </p>
          </div>
          <div class="d-flex align-items-center">
            <select 
              v-model="selectedSubject" 
              class="form-select me-2"
              @change="fetchChapters"
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
            <button 
              class="btn btn-primary" 
              @click="showCreateChapterModal"
            >
              <i class="bi bi-plus-lg me-2"></i>
              Create Chapter
            </button>
          </div>
        </div>
      </div>

      <!-- Chapters List -->
      <div class="chapters-list glass">
        <div class="card-body">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3"></div>
            <p class="text-muted">Loading chapters...</p>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="alert alert-danger glass-alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ error }}
          </div>

          <!-- Empty State -->
          <div v-else-if="chapters.length === 0" class="empty-state text-center py-5">
            <i class="bi bi-layers display-1 text-muted mb-3"></i>
            <h4 class="text-light">No Chapters Found</h4>
            <p class="text-muted">
              Create your first chapter by selecting a subject and clicking "Create Chapter"
            </p>
          </div>

          <!-- Chapters Table -->
          <div v-else class="table-responsive">
            <table class="table table-dark table-glass">
              <thead>
                <tr>
                  <th style="width: 80px;"><i class="bi bi-hash me-2"></i>ID</th>
                  <th style="width: 200px;"><i class="bi bi-book me-2"></i>Name</th>
                  <th style="width: 300px;"><i class="bi bi-file-text me-2"></i>Description</th>
                  <th style="width: 150px;"><i class="bi bi-calendar me-2"></i>Created At</th>
                  <th style="width: 120px;"><i class="bi bi-gear me-2"></i>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chapter in chapters" :key="chapter.id" class="table-row-glass">
                  <td>
                    <span class="badge bg-primary">{{ chapter.id }}</span>
                  </td>
                  <td>
                    <strong class="text-light">{{ chapter.name }}</strong>
                  </td>
                  <td>
                    <span 
                      class="text-light" 
                      v-if="chapter.description"
                    >
                      {{ chapter.description }}
                    </span>
                    <span 
                      v-else 
                      class="text-warning"
                    >
                      No Description
                    </span>
                  </td>
                  <td>
                    <small class="text-muted">
                      {{ formatDate(chapter.created_at) }}
                    </small>
                  </td>
                  <td>
                    <div class="btn-group" role="group">
                      <button 
                        class="btn btn-sm btn-outline-light"
                        @click="editChapter(chapter)"
                        title="Edit Chapter"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button 
                        class="btn btn-sm btn-outline-danger"
                        @click="deleteChapter(chapter.id)"
                        title="Delete Chapter"
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

      <!-- Create/Edit Chapter Modal -->
      <div 
        class="modal fade" 
        id="chapterModal" 
        tabindex="-1" 
        aria-labelledby="chapterModalLabel"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content glass">
            <div class="modal-header">
              <h5 class="modal-title text-light" id="chapterModalLabel">
                {{ isEditing ? 'Edit Chapter' : 'Create Chapter' }}
              </h5>
              <button 
                type="button" 
                class="btn-close btn-close-white" 
                data-bs-dismiss="modal"
              ></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveChapter">
                <div class="mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-book me-2"></i>Chapter Name *
                  </label>
                  <input 
                    v-model="currentChapter.name" 
                    type="text" 
                    class="form-control glass-input" 
                    required
                  />
                </div>
                
                <div class="mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-file-text me-2"></i>Description
                  </label>
                  <textarea 
                    v-model="currentChapter.description" 
                    class="form-control glass-input" 
                    rows="3"
                  ></textarea>
                </div>

                <div class="mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-list-ol me-2"></i>Order
                  </label>
                  <input 
                    v-model.number="currentChapter.order" 
                    type="number" 
                    class="form-control glass-input" 
                    min="0"
                  />
                </div>
                
                <div class="mb-3">
                  <label class="form-label text-light">
                    <i class="bi bi-book-half me-2"></i>Subject *
                  </label>
                  <select 
                    v-model="currentChapter.subject_id" 
                    class="form-select glass-input" 
                    required
                  >
                    <option 
                      v-for="subject in subjects" 
                      :key="subject.id" 
                      :value="subject.id"
                    >
                      {{ subject.name }}
                    </option>
                  </select>
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
                    {{ isEditing ? 'Update Chapter' : 'Create Chapter' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import chapterService from '@/services/chapterService';
import subjectService from '@/services/subjectService';

export default {
  name: 'ChaptersView',
  data() {
    return {
      chapters: [],
      subjects: [],
      selectedSubject: null,
      loading: false,
      error: null,
      isEditing: false,
      currentChapter: {
        name: '',
        description: '',
        order: 0,
        subject_id: null
      }
    }
  },
  computed: {
    isFormValid() {
      return this.currentChapter.name && this.currentChapter.subject_id !== null;
    }
  },
  methods: {
    async fetchSubjects() {
      try {
        this.subjects = await subjectService.getSubjects();
      } catch (error) {
        console.error('Failed to fetch subjects:', error);
      }
    },
    async fetchChapters() {
      this.loading = true;
      this.error = null;

      try {
        console.log('🔍 Fetching chapters...');
        const rawChapters = await chapterService.getChapters(this.selectedSubject);
        
        // Detailed logging
        console.log('📊 Raw Chapters Data:', rawChapters);
        console.log('📊 Chapters Type:', typeof rawChapters);
        console.log('📊 Chapters Keys:', Object.keys(rawChapters));
        
        // Defensive check and transformation with explicit logging
        this.chapters = rawChapters.map(chapter => {
          console.log(`🔍 Processing Chapter: ${chapter.name}`, chapter);
          
          // Explicitly log description and all potential description paths
          console.log(`📝 Chapter Description Paths:`, {
            directDescription: chapter.description,
            nestedDescription: chapter['description'],
            fullChapterObject: chapter
          });
          
          return {
            ...chapter,
            description: chapter.description || chapter['description'] || 'No description provided'
          };
        });
        
        console.log('🔢 Processed Chapters:', this.chapters);
        console.log('📝 First Chapter Description:', this.chapters[0]?.description);
      } catch (error) {
        console.error('❌ Failed to fetch chapters:', error);
        this.error = error.response?.data?.message || 'Failed to load chapters';
      } finally {
        this.loading = false;
      }
    },
    showCreateChapterModal() {
      this.isEditing = false;
      this.currentChapter = {
        name: '',
        description: '',
        order: 0,
        subject_id: null
      };
      const modal = new Modal(document.getElementById('chapterModal'));
      modal.show();
    },
    editChapter(chapter) {
      this.isEditing = true;
      this.currentChapter = { ...chapter };
      const modal = new Modal(document.getElementById('chapterModal'));
      modal.show();
    },
    async saveChapter() {
      this.loading = true;
      this.error = null;

      try {
        const chapterData = {
          name: this.currentChapter.name.trim(),
          description: this.currentChapter.description.trim(),
          order: this.currentChapter.order || 0,
          subject_id: this.currentChapter.subject_id
        };

        if (this.isEditing) {
          await chapterService.updateChapter(this.currentChapter.id, chapterData);
        } else {
          await chapterService.createChapter(chapterData);
        }
        
        await this.fetchChapters();
        
        // Close modal
        const modal = Modal.getInstance(document.getElementById('chapterModal'));
        modal.hide();

        // Reset form
        this.currentChapter = {
          name: '',
          description: '',
          order: 0,
          subject_id: null
        };
      } catch (error) {
        console.error('Failed to save chapter:', error);
        this.error = error.response?.data?.message || 'Failed to save chapter';
      } finally {
        this.loading = false;
      }
    },
    async deleteChapter(chapterId) {
      if (!confirm('Are you sure you want to delete this chapter?')) return;

      this.loading = true;
      this.error = null;

      try {
        await chapterService.deleteChapter(chapterId);
        await this.fetchChapters();
      } catch (error) {
        console.error('Failed to delete chapter:', error);
        this.error = error.response?.data?.message || 'Failed to delete chapter';
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    // Removed getChapterDescription as we're handling it directly in template
  },
  mounted() {
    this.fetchSubjects();
    this.fetchChapters();
  }
}
</script>

<style scoped>
.chapters-management {
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

.page-header, .chapters-list {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
}

.glass-input {
  background: rgba(35, 39, 43, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: white !important;
}

.glass-input:focus {
  background: rgba(35, 39, 43, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.1) !important;
}

.table-dark {
  background: transparent;
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
}

.glass-alert {
  background: rgba(35, 39, 43, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.form-select {
  background: rgba(35, 39, 43, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
}

.form-select:focus {
  background: rgba(35, 39, 43, 0.8);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.1);
}

.empty-state {
  background: rgba(35, 39, 43, 0.3);
  border-radius: 1rem;
  padding: 3rem;
}

/* Modal Glassmorphism Styling */
.modal-content.glass {
  background: rgba(35, 39, 43, 0.85);
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

.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.7);
}

.form-select.glass-input option {
  background: rgba(35, 39, 43, 0.9);
  color: white;
}

.btn-close-white {
  filter: invert(1) grayscale(100%) brightness(200%);
}

.btn-outline-light {
  border-color: rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.8);
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  color: white;
}
</style> 