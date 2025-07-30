<template>
  <div class="user-profile-view">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-lg-3 col-md-4">
        <BaseSidebar user-role="user" />
      </div>
      
      <!-- Main Content -->
      <div class="col-lg-9 col-md-8">
        <div class="container-fluid p-4">
          <!-- Page Header -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div class="d-flex align-items-center gap-3">
              <button 
                class="btn btn-outline-light d-flex align-items-center gap-2"
                @click="goBack"
              >
                <i class="bi bi-arrow-left"></i>
                Back
              </button>
              <h2 class="text-light mb-0">My Profile</h2>
            </div>
            <div class="d-flex gap-2">
              <button 
                v-if="!editMode"
                class="btn btn-primary d-flex align-items-center gap-2"
                @click="editMode = true"
              >
                <i class="bi bi-pencil"></i>
                Edit Profile
              </button>
              <button 
                v-if="editMode"
                class="btn btn-success d-flex align-items-center gap-2"
                @click="saveProfile"
                :disabled="loading"
              >
                <i class="bi bi-check"></i>
                {{ loading ? 'Saving...' : 'Save Changes' }}
              </button>
              <button 
                v-if="editMode"
                class="btn btn-outline-secondary d-flex align-items-center gap-2"
                @click="cancelEdit"
              >
                <i class="bi bi-x"></i>
                Cancel
              </button>
            </div>
          </div>

          <div class="row">
            <!-- Profile Card -->
            <div class="col-md-8">
              <div class="card glass p-4 mb-4">
                <div class="d-flex align-items-center mb-4">
                  <div class="profile-avatar me-3">
                    {{ getUserInitials(profile.full_name) }}
                  </div>
                  <div>
                    <h4 class="text-light mb-1">{{ profile.full_name }}</h4>
                    <p class="text-light mb-0">{{ profile.username }}</p>
                  </div>
                </div>

                <!-- Profile Form -->
                <form @submit.prevent="saveProfile">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <FormLabel for="full_name" required>Username</FormLabel>
                      <BaseInput
                        id="full_name"
                        v-model="profile.full_name"
                        :disabled="!editMode"
                        :class="{ 'is-invalid': errors.full_name }"
                        required
                      />
                      <FormError :error="errors.full_name" />
                    </div>

                    <div class="col-md-6">
                      <FormLabel for="username" required>Email Address</FormLabel>
                      <BaseInput
                        id="username"
                        type="email"
                        v-model="profile.username"
                        :disabled="!editMode"
                        :class="{ 'is-invalid': errors.username }"
                        required
                      />
                      <FormError :error="errors.username" />
                    </div>

                    <div class="col-12" v-if="editMode">
                      <FormLabel for="current_password">Current Password (required to save changes)</FormLabel>
                      <BaseInput
                        id="current_password"
                        type="password"
                        v-model="profile.current_password"
                        placeholder="Enter current password to confirm changes"
                        :class="{ 'is-invalid': errors.current_password }"
                        required
                      />
                      <FormError :error="errors.current_password" />
                    </div>
                  </div>
                </form>

                <!-- Account Information -->
                <div class="mt-4 pt-4 border-top border-secondary">
                  <h6 class="text-light mb-3">Account Information</h6>
                  <div class="row g-3">
                    <div class="col-md-6">
                      <small class="text-light">Member Since</small>
                      <p class="text-light mb-0">{{ formatDate(profile.created_at) }}</p>
                    </div>
                    <div class="col-md-6">
                      <small class="text-light">Last Updated</small>
                      <p class="text-light mb-0">{{ formatDate(profile.updated_at) }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Change Password Section -->
              <div class="card glass p-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h6 class="text-light mb-0">Change Password</h6>
                  <button 
                    class="btn btn-outline-warning btn-sm"
                    @click="showChangePassword = !showChangePassword"
                  >
                    {{ showChangePassword ? 'Cancel' : 'Change Password' }}
                  </button>
                </div>

                <div v-if="showChangePassword">
                  <form @submit.prevent="changePassword">
                    <div class="row g-3">
                      <div class="col-12">
                        <FormLabel for="old_password" required>Current Password</FormLabel>
                        <BaseInput
                          id="old_password"
                          type="password"
                          v-model="passwordForm.old_password"
                          :class="{ 'is-invalid': passwordErrors.old_password }"
                          required
                        />
                        <FormError :error="passwordErrors.old_password" />
                      </div>

                      <div class="col-md-6">
                        <FormLabel for="new_password" required>New Password</FormLabel>
                        <BaseInput
                          id="new_password"
                          type="password"
                          v-model="passwordForm.new_password"
                          :class="{ 'is-invalid': passwordErrors.new_password }"
                          required
                        />
                        <FormError :error="passwordErrors.new_password" />
                      </div>

                      <div class="col-md-6">
                        <FormLabel for="confirm_password" required>Confirm New Password</FormLabel>
                        <BaseInput
                          id="confirm_password"
                          type="password"
                          v-model="passwordForm.confirm_password"
                          :class="{ 'is-invalid': passwordErrors.confirm_password }"
                          required
                        />
                        <FormError :error="passwordErrors.confirm_password" />
                      </div>

                      <div class="col-12">
                        <button 
                          type="submit" 
                          class="btn btn-warning"
                          :disabled="passwordLoading"
                        >
                          {{ passwordLoading ? 'Changing...' : 'Change Password' }}
                        </button>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseSidebar from '../../components/BaseSidebar.vue'
import BaseInput from '../../components/BaseInput.vue'
import FormLabel from '../../components/FormLabel.vue'
import FormError from '../../components/FormError.vue'
import UserService from '@/services/user-service'

export default {
  name: 'UserProfileView',
  components: {
    BaseSidebar,
    BaseInput,
    FormLabel,
    FormError
  },
  data() {
    return {
      editMode: false,
      loading: false,
      passwordLoading: false,
      showChangePassword: false,
      profile: {
        id: null,
        username: '',
        full_name: '',
        created_at: '',
        updated_at: '',
        current_password: ''
      },
      originalProfile: {},
      passwordForm: {
        old_password: '',
        new_password: '',
        confirm_password: ''
      },
      errors: {},
      passwordErrors: {}
    }
  },
  async mounted() {
    console.log('UserProfileView mounted - loading profile');
    await this.loadProfile();
    console.log('Profile loaded in mounted:', this.profile);
  },
  methods: {
    async loadProfile() {
      try {
        const result = await UserService.getProfile()
        if (result.success) {
          console.log("Profile data loaded:", result.data);
          this.profile = result.data
          this.originalProfile = { ...this.profile }
        } else {
          console.error("Failed to load profile data:", result.message);
          this.$toast?.error(result.message)
        }
      } catch (error) {
        console.error('Error loading profile:', error)
        this.$toast?.error('Failed to load profile')
      }
    },

    async saveProfile() {
      if (!this.validateProfile()) return

      this.loading = true
      try {
        const result = await UserService.updateProfile({
          full_name: this.profile.full_name,
          current_password: this.profile.current_password
        })
        
        if (result.success) {
          this.editMode = false
          this.errors = {}
          this.profile.current_password = ''
          this.$toast?.success('Profile updated successfully!')
          await this.loadProfile() // Reload profile to get updated data
          this.$router.push('/user/dashboard') // Redirect to dashboard after successful update
        } else {
          if (result.error?.errors) {
            this.errors = result.error.errors
          } else {
            this.$toast?.error(result.message)
          }
        }
      } catch (error) {
        console.error('Error updating profile:', error)
        this.$toast?.error('Failed to update profile')
      } finally {
        this.loading = false
      }
    },

    async changePassword() {
      if (!this.validatePassword()) return

      this.passwordLoading = true
      try {
        const result = await UserService.changePassword(this.passwordForm)
        
        if (result.success) {
          this.passwordForm = {
            old_password: '',
            new_password: '',
            confirm_password: ''
          }
          this.showChangePassword = false
          this.passwordErrors = {}
          this.$toast?.success('Password changed successfully!')
        } else {
          if (result.error?.errors) {
            this.passwordErrors = result.error.errors
          } else {
            this.$toast?.error(result.message)
          }
        }
      } catch (error) {
        console.error('Error changing password:', error)
        this.$toast?.error('Failed to change password')
      } finally {
        this.passwordLoading = false
      }
    },
    validateProfile() {
      this.errors = {}
      
      if (!this.profile.full_name?.trim()) {
        this.errors.full_name = 'Username is required'
      }
      
      if (!this.profile.username?.trim()) {
        this.errors.username = 'Email is required'
      } else if (!/\S+@\S+\.\S+/.test(this.profile.username)) {
        this.errors.username = 'Please enter a valid email address'
      }
      
      if (!this.profile.current_password && this.editMode) {
        this.errors.current_password = 'Current password is required to save changes'
      }
      
      return Object.keys(this.errors).length === 0
    },
    validatePassword() {
      this.passwordErrors = {}
      
      if (!this.passwordForm.old_password) {
        this.passwordErrors.old_password = 'Current password is required'
      }
      
      if (!this.passwordForm.new_password) {
        this.passwordErrors.new_password = 'New password is required'
      } else if (this.passwordForm.new_password.length < 6) {
        this.passwordErrors.new_password = 'Password must be at least 6 characters'
      }
      
      if (!this.passwordForm.confirm_password) {
        this.passwordErrors.confirm_password = 'Please confirm your new password'
      } else if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
        this.passwordErrors.confirm_password = 'Passwords do not match'
      }
      
      return Object.keys(this.passwordErrors).length === 0
    },
    cancelEdit() {
      this.profile = { ...this.originalProfile }
      this.editMode = false
      this.errors = {}
    },
    getUserInitials(name) {
      return name ? name.split(' ').map(n => n[0]).join('').toUpperCase() : ''
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    },
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.user-profile-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #181A1B 0%, #23272B 100%);
  padding-top: 2rem;
}

.card.glass {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0d6efd, #6f42c1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 24px;
  color: white;
}

.form-control:disabled, .form-select:disabled {
  background-color: rgba(108, 117, 125, 0.1);
  border-color: rgba(108, 117, 125, 0.3);
}

.form-control:focus, .form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  background-color: rgba(35, 39, 43, 0.6);
  color: white;
}

.form-select option {
  background-color: #23272B;
  color: white;
}

.stats-grid .stat-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.8rem;
}

.activity-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(13, 110, 253, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.x-small {
  font-size: 0.75rem;
}
</style>