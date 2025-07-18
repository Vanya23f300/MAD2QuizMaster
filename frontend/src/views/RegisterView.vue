<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card glass p-4 shadow-lg" style="max-width: 400px; width: 100%; background: rgba(35,39,43,0.6); border-radius: 1rem; border: 1px solid rgba(255,255,255,0.15);">
      <h2 class="text-center text-light mb-3">Register</h2>
      <p class="text-secondary text-center mb-4">Create your account to get started.</p>
      <form @submit.prevent="onSubmit" novalidate>
        <BaseInput
          id="register-email"
          label="Email"
          type="email"
          v-model="email"
          :error="errors.email"
          required
          placeholder="Enter your email"
        />
        <div class="mb-3">
          <FormLabel for-id="register-password" required>Password</FormLabel>
          <div class="input-group">
            <input
              :id="'register-password'"
              :type="showPassword ? 'text' : 'password'"
              class="form-control password-input"
              :class="{ 'is-invalid': errors.password }"
              :placeholder="'Enter your password'"
              :required="true"
              :value="password"
              @input="password = $event.target.value"
              autocomplete="new-password"
            />
            <button class="btn password-toggle-btn" type="button" tabindex="-1" @click="showPassword = !showPassword">
              <span v-if="showPassword" class="bi bi-eye-slash"></span>
              <span v-else class="bi bi-eye"></span>
            </button>
          </div>
          <FormError :error="errors.password" />
        </div>
        <BaseInput
          id="register-fullname"
          label="Full Name"
          type="text"
          v-model="fullName"
          :error="errors.fullName"
          required
          placeholder="Enter your full name"
        />
        <BaseInput
          id="register-qualification"
          label="Qualification"
          type="text"
          v-model="qualification"
          :error="errors.qualification"
          required
          placeholder="Enter your qualification"
        />
        <BaseInput
          id="register-dob"
          label="Date of Birth"
          type="date"
          v-model="dob"
          :error="errors.dob"
          required
        />
        <div class="mb-3">
          <label class="form-label text-light">Role</label>
          <select v-model="role" class="form-select bg-dark text-light border-secondary glass" required>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <FormError :error="errors.general" />
        <BaseButton 
          :loading="loading" 
          type="submit" 
          class="w-100 mt-2 mb-3 btn-register"
        >
          <i class="bi bi-person-plus me-2"></i>
          Create Account
        </BaseButton>
      </form>
      <div class="text-center mt-2">
        <span class="text-secondary">Already have an account?</span>
        <router-link to="/login" class="login-link ms-1">Sign In</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import BaseInput from '../components/BaseInput.vue'
import BaseButton from '../components/BaseButton.vue'
import FormLabel from '../components/FormLabel.vue'
import FormError from '../components/FormError.vue'

export default {
  name: 'RegisterView',
  components: { BaseInput, BaseButton, FormLabel, FormError },
  data() {
    return {
      email: '',
      password: '',
      showPassword: false,
      fullName: '',
      qualification: '',
      dob: '',
      role: 'user',
      errors: {},
      loading: false
    }
  },
  methods: {
    validate() {
      const errors = {}
      if (!this.email) errors.email = 'Email is required.'
      else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(this.email)) errors.email = 'Invalid email format.'
      if (!this.password) errors.password = 'Password is required.'
      else if (this.password.length < 6) errors.password = 'Password must be at least 6 characters.'
      if (!this.fullName) errors.fullName = 'Full name is required.'
      if (!this.qualification) errors.qualification = 'Qualification is required.'
      if (!this.dob) errors.dob = 'Date of birth is required.'
      this.errors = errors
      return Object.keys(errors).length === 0
    },
    async onSubmit() {
      if (!this.validate()) return
      this.loading = true
      this.errors.general = ''
      // Simulate registration delay
      setTimeout(() => {
        this.loading = false
        // Dummy logic: accept any registration, redirect by role
        if (this.email && this.password && this.fullName && this.qualification && this.dob) {
          localStorage.setItem('isAuthenticated', 'true')
          localStorage.setItem('role', this.role)
          this.$router.push(this.role === 'admin' ? '/admin' : '/user')
        } else {
          this.errors.general = 'Registration failed. Please try again.'
        }
      }, 1200)
    }
  }
}
</script>

<style scoped>
.card.glass {
  /* Glassmorphism effect */
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.password-input {
  border-radius: 12px 0 0 12px !important;
  border-right: none !important;
}

.password-toggle-btn {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-left: none !important;
  border-radius: 0 12px 12px 0 !important;
  color: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.password-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  color: #ffffff !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}

.password-toggle-btn:focus {
  box-shadow: none !important;
  border-color: rgba(74, 85, 104, 0.6) !important;
}

.btn-register {
  font-size: 1rem;
  padding: 14px 24px;
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.login-link {
  color: #cbd5e0;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
}

.login-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: #4a5568;
  transition: width 0.3s ease;
}

.login-link:hover {
  color: #ffffff;
  transform: translateY(-1px);
}

.login-link:hover::after {
  width: 100%;
}

.register-view {
  min-height: 100vh;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-card {
  max-width: 400px;
  width: 100%;
  padding: 2rem 1.8rem;
  position: relative;
  overflow: hidden;
}

.register-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(135deg, #4a5568, #2d3748);
  border-radius: 16px 16px 0 0;
}

.register-header {
  position: relative;
}

.register-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #4a5568, #2d3748);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-shadow: 0 6px 20px rgba(74, 85, 104, 0.3);
}

.register-icon i {
  font-size: 1.8rem;
  color: white;
}

.register-form {
  position: relative;
}
</style> 