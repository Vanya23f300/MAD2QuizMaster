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
              class="form-control bg-dark text-light border-secondary glass"
              :class="{ 'is-invalid': errors.password }"
              :placeholder="'Enter your password'"
              :required="true"
              :value="password"
              @input="password = $event.target.value"
              autocomplete="new-password"
            />
            <button class="btn btn-outline-secondary" type="button" tabindex="-1" @click="showPassword = !showPassword">
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
        <BaseButton :loading="loading" type="submit" class="w-100 mt-2 mb-3">
          Register
        </BaseButton>
      </form>
      <div class="text-center mt-2">
        <span class="text-secondary">Already have an account?</span>
        <router-link to="/login" class="link-primary ms-1">Login</router-link>
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
</style> 