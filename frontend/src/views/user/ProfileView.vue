<template>
  <div class="profile-view">
    <!-- Header Section -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="text-light mb-1">My Profile</h2>
        <p class="text-muted mb-0">Manage your account and preferences</p>
      </div>
      <button 
        v-if="!editMode" 
        @click="enableEditMode" 
        class="btn btn-primary"
      >
        <i class="bi bi-pencil me-2"></i>Edit Profile
      </button>
      <div v-else class="d-flex gap-2">
        <button @click="saveProfile" class="btn btn-success">
          <i class="bi bi-check me-2"></i>Save Changes
        </button>
        <button @click="cancelEdit" class="btn btn-outline-secondary">
          <i class="bi bi-x me-2"></i>Cancel
        </button>
      </div>
    </div>

    <div class="row">
      <!-- Profile Information -->
      <div class="col-lg-8 mb-4">
        <div class="card glassmorphic">
          <div class="card-header bg-transparent border-0">
            <h5 class="text-light mb-0">Profile Information</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="saveProfile">
              <div class="row">
                <!-- Profile Picture -->
                <div class="col-md-4 mb-4 text-center">
                  <div class="profile-picture-container">
                    <img 
                      :src="profileData.avatar || '/default-avatar.png'" 
                      alt="Profile Picture"
                      class="profile-picture"
                    />
                    <div v-if="editMode" class="profile-picture-overlay">
                      <button type="button" class="btn btn-light btn-sm" @click="openImageUpload">
                        <i class="bi bi-camera"></i>
                      </button>
                    </div>
                  </div>
                  <input 
                    ref="imageUpload" 
                    type="file" 
                    accept="image/*" 
                    style="display: none" 
                    @change="handleImageUpload"
                  />
                </div>

                <!-- Basic Information -->
                <div class="col-md-8">
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label text-light">Full Name</label>
                      <input 
                        v-model="profileData.fullName"
                        type="text"
                        class="form-control glassmorphic"
                        :readonly="!editMode"
                        required
                      />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label text-light">Email</label>
                      <input 
                        v-model="profileData.email"
                        type="email"
                        class="form-control glassmorphic"
                        :readonly="!editMode"
                        required
                      />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label text-light">Username</label>
                      <input 
                        v-model="profileData.username"
                        type="text"
                        class="form-control glassmorphic"
                        :readonly="!editMode"
                        required
                      />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label text-light">Phone</label>
                      <input 
                        v-model="profileData.phone"
                        type="tel"
                        class="form-control glassmorphic"
                        :readonly="!editMode"
                      />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label text-light">Date of Birth</label>
                      <input 
                        v-model="profileData.dateOfBirth"
                        type="date"
                        class="form-control glassmorphic"
                        :readonly="!editMode"
                      />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label text-light">Qualification</label>
                      <select 
                        v-model="profileData.qualification"
                        class="form-select glassmorphic"
                        :disabled="!editMode"
                      >
                        <option value="">Select Qualification</option>
                        <option value="high-school">High School</option>
                        <option value="bachelor">Bachelor's Degree</option>
                        <option value="master">Master's Degree</option>
                        <option value="phd">PhD</option>
                        <option value="other">Other</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Additional Information -->
              <hr class="border-secondary" />
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">Institution</label>
                  <input 
                    v-model="profileData.institution"
                    type="text"
                    class="form-control glassmorphic"
                    :readonly="!editMode"
                    placeholder="Your school/college/university"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">Location</label>
                  <input 
                    v-model="profileData.location"
                    type="text"
                    class="form-control glassmorphic"
                    :readonly="!editMode"
                    placeholder="City, Country"
                  />
                </div>
                <div class="col-12 mb-3">
                  <label class="form-label text-light">Bio</label>
                  <textarea 
                    v-model="profileData.bio"
                    class="form-control glassmorphic"
                    rows="3"
                    :readonly="!editMode"
                    placeholder="Tell us about yourself..."
                  ></textarea>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Quick Stats & Actions -->
      <div class="col-lg-4 mb-4">
        <!-- Account Stats -->
        <div class="card glassmorphic mb-4">
          <div class="card-header bg-transparent border-0">
            <h5 class="text-light mb-0">Account Statistics</h5>
          </div>
          <div class="card-body">
            <div class="stat-item d-flex justify-content-between align-items-center mb-3">
              <div>
                <i class="bi bi-calendar-check text-primary me-2"></i>
                <span class="text-light">Member Since</span>
              </div>
              <span class="text-muted">{{ formatDate(profileData.joinDate) }}</span>
            </div>
            <div class="stat-item d-flex justify-content-between align-items-center mb-3">
              <div>
                <i class="bi bi-clipboard-check text-success me-2"></i>
                <span class="text-light">Quizzes Completed</span>
              </div>
              <span class="badge bg-success">{{ profileData.stats.quizzesCompleted }}</span>
            </div>
            <div class="stat-item d-flex justify-content-between align-items-center mb-3">
              <div>
                <i class="bi bi-graph-up text-info me-2"></i>
                <span class="text-light">Average Score</span>
              </div>
              <span class="badge bg-info">{{ profileData.stats.averageScore }}%</span>
            </div>
            <div class="stat-item d-flex justify-content-between align-items-center">
              <div>
                <i class="bi bi-trophy text-warning me-2"></i>
                <span class="text-light">Best Score</span>
              </div>
              <span class="badge bg-warning">{{ profileData.stats.bestScore }}%</span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card glassmorphic mb-4">
          <div class="card-header bg-transparent border-0">
            <h5 class="text-light mb-0">Quick Actions</h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <button @click="openChangePassword" class="btn btn-outline-warning">
                <i class="bi bi-key me-2"></i>Change Password
              </button>
              <router-link to="/user/summary" class="btn btn-outline-info">
                <i class="bi bi-graph-up me-2"></i>View Performance
              </router-link>
              <router-link to="/user/scores" class="btn btn-outline-success">
                <i class="bi bi-list-check me-2"></i>Quiz History
              </router-link>
              <button @click="downloadData" class="btn btn-outline-secondary">
                <i class="bi bi-download me-2"></i>Download Data
              </button>
            </div>
          </div>
        </div>

        <!-- Security Settings -->
        <div class="card glassmorphic">
          <div class="card-header bg-transparent border-0">
            <h5 class="text-light mb-0">Security & Privacy</h5>
          </div>
          <div class="card-body">
            <div class="form-check form-switch mb-3">
              <input 
                v-model="profileData.settings.emailNotifications"
                class="form-check-input" 
                type="checkbox" 
                id="emailNotifications"
              />
              <label class="form-check-label text-light" for="emailNotifications">
                Email Notifications
              </label>
            </div>
            <div class="form-check form-switch mb-3">
              <input 
                v-model="profileData.settings.profilePublic"
                class="form-check-input" 
                type="checkbox" 
                id="profilePublic"
              />
              <label class="form-check-label text-light" for="profilePublic">
                Public Profile
              </label>
            </div>
            <div class="form-check form-switch mb-3">
              <input 
                v-model="profileData.settings.shareProgress"
                class="form-check-input" 
                type="checkbox" 
                id="shareProgress"
              />
              <label class="form-check-label text-light" for="shareProgress">
                Share Progress
              </label>
            </div>
            <hr class="border-secondary" />
            <button @click="deleteAccount" class="btn btn-outline-danger btn-sm w-100">
              <i class="bi bi-trash me-2"></i>Delete Account
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Change Password Modal -->
    <div class="modal fade" id="changePasswordModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content glassmorphic">
          <div class="modal-header border-0">
            <h5 class="modal-title text-light">Change Password</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="changePassword">
              <div class="mb-3">
                <label class="form-label text-light">Current Password</label>
                <input 
                  v-model="passwordData.currentPassword"
                  type="password"
                  class="form-control glassmorphic"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label text-light">New Password</label>
                <input 
                  v-model="passwordData.newPassword"
                  type="password"
                  class="form-control glassmorphic"
                  required
                  minlength="6"
                />
              </div>
              <div class="mb-3">
                <label class="form-label text-light">Confirm New Password</label>
                <input 
                  v-model="passwordData.confirmPassword"
                  type="password"
                  class="form-control glassmorphic"
                  required
                />
              </div>
              <div class="d-flex justify-content-end gap-2">
                <button type="button" class="btn btn-outline-secondary" @click="closeModal">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  Change Password
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
export default {
  name: 'ProfileView',
  data() {
    return {
      editMode: false,
      originalData: {},
      profileData: {
        fullName: 'John Doe',
        email: 'john.doe@example.com',
        username: 'johndoe',
        phone: '+1 (555) 123-4567',
        dateOfBirth: '1995-06-15',
        qualification: 'bachelor',
        institution: 'University of Technology',
        location: 'New York, USA',
        bio: 'Passionate learner interested in technology and science. Always eager to expand my knowledge through continuous learning.',
        avatar: null,
        joinDate: '2023-09-15',
        stats: {
          quizzesCompleted: 23,
          averageScore: 78,
          bestScore: 95
        },
        settings: {
          emailNotifications: true,
          profilePublic: false,
          shareProgress: true
        }
      },
      passwordData: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    enableEditMode() {
      this.editMode = true
      this.originalData = JSON.parse(JSON.stringify(this.profileData))
    },
    cancelEdit() {
      this.editMode = false
      this.profileData = JSON.parse(JSON.stringify(this.originalData))
    },
    saveProfile() {
      // Validate data
      if (!this.profileData.fullName || !this.profileData.email) {
        alert('Please fill in all required fields')
        return
      }

      // Save to backend (simulate)
      console.log('Saving profile:', this.profileData)
      
      // Show success message
      this.showNotification('Profile updated successfully!', 'success')
      this.editMode = false
    },
    openImageUpload() {
      this.$refs.imageUpload.click()
    },
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (file) {
        // In real app, upload to server
        const reader = new FileReader()
        reader.onload = (e) => {
          this.profileData.avatar = e.target.result
        }
        reader.readAsDataURL(file)
      }
    },
    openChangePassword() {
      // Using vanilla JavaScript instead of bootstrap object
      const modalElement = document.getElementById('changePasswordModal')
      modalElement.classList.add('show')
      modalElement.style.display = 'block'
      document.body.classList.add('modal-open')
      
      // Add backdrop
      const backdrop = document.createElement('div')
      backdrop.className = 'modal-backdrop fade show'
      document.body.appendChild(backdrop)
    },
    changePassword() {
      if (this.passwordData.newPassword !== this.passwordData.confirmPassword) {
        alert('New passwords do not match')
        return
      }

      if (this.passwordData.newPassword.length < 6) {
        alert('Password must be at least 6 characters long')
        return
      }

      // Change password (simulate)
      console.log('Changing password')
      
      // Reset form
      this.passwordData = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }

      // Close modal
      const modalElement = document.getElementById('changePasswordModal')
      modalElement.classList.remove('show')
      modalElement.style.display = 'none'
      document.body.classList.remove('modal-open')
      
      // Remove backdrop
      const backdrop = document.querySelector('.modal-backdrop')
      if (backdrop) {
        backdrop.remove()
      }

      this.showNotification('Password changed successfully!', 'success')
    },
    closeModal() {
      const modalElement = document.getElementById('changePasswordModal')
      modalElement.classList.remove('show')
      modalElement.style.display = 'none'
      document.body.classList.remove('modal-open')
      
      // Remove backdrop
      const backdrop = document.querySelector('.modal-backdrop')
      if (backdrop) {
        backdrop.remove()
      }
      
      // Reset form
      this.passwordData = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    },
    downloadData() {
      // Simulate data download
      const data = {
        profile: this.profileData,
        exportDate: new Date().toISOString()
      }
      
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'profile-data.json'
      a.click()
      URL.revokeObjectURL(url)

      this.showNotification('Data download started!', 'info')
    },
    deleteAccount() {
      if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        // Delete account (simulate)
        console.log('Deleting account')
        this.showNotification('Account deletion initiated. You will receive an email confirmation.', 'warning')
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      })
    },
    showNotification(message, type) {
      // Simple notification (in real app, use toast library)
      console.log(`Notification (${type}): ${message}`)
    }
  }
}
</script>

<style scoped>
.profile-view {
  padding: 1.5rem;
  min-height: 100vh;
}

.glassmorphic {
  background: rgba(35, 39, 43, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

.card.glassmorphic {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.profile-picture-container {
  position: relative;
  display: inline-block;
}

.profile-picture {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.profile-picture-overlay {
  position: absolute;
  bottom: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 50%;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-control.glassmorphic,
.form-select.glassmorphic {
  background: rgba(35, 39, 43, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
}

.form-control.glassmorphic:focus,
.form-select.glassmorphic:focus {
  background: rgba(35, 39, 43, 0.9);
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
  color: #f8f9fa;
}

.form-control.glassmorphic[readonly] {
  background: rgba(35, 39, 43, 0.4);
  border-color: rgba(255, 255, 255, 0.1);
}

.form-select.glassmorphic option {
  background: #23272b;
  color: #f8f9fa;
}

.stat-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item:last-child {
  border-bottom: none;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.modal-content.glassmorphic {
  background: rgba(35, 39, 43, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .profile-view {
    padding: 1rem;
  }
  
  .profile-picture {
    width: 100px;
    height: 100px;
  }
  
  .d-flex.gap-2 {
    flex-direction: column;
    gap: 0.5rem !important;
  }
}
</style> 