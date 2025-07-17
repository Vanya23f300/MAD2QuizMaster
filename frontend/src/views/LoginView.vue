<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card glass p-4 shadow-lg" style="max-width: 400px; width: 100%; background: rgba(35,39,43,0.6); border-radius: 1rem; border: 1px solid rgba(255,255,255,0.15);">
      <h2 class="text-center text-light mb-3">Login</h2>
      <p class="text-secondary text-center mb-4">Welcome back! Please sign in to your account.</p>
      <form @submit.prevent="onSubmit" novalidate>
        <BaseInput
          id="login-email"
          label="Email"
          type="email"
          v-model="email"
          :error="errors.email"
          required
          placeholder="Enter your email"
        />
        <BaseInput
          id="login-password"
          label="Password"
          type="password"
          v-model="password"
          :error="errors.password"
          required
          placeholder="Enter your password"
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
          Login
        </BaseButton>
      </form>
      <div class="text-center mt-2">
        <span class="text-secondary">Don't have an account?</span>
        <router-link to="/register" class="link-primary ms-1">Register</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import BaseInput from '../components/BaseInput.vue'
import BaseButton from '../components/BaseButton.vue'
import FormError from '../components/FormError.vue'

export default {
  name: 'LoginView',
  components: { BaseInput, BaseButton, FormError },
  data() {
    return {
      email: '',
      password: '',
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
      this.errors = errors
      return Object.keys(errors).length === 0
    },
    async onSubmit() {
      if (!this.validate()) return
      this.loading = true
      this.errors.general = ''
      // Simulate authentication delay
      setTimeout(() => {
        this.loading = false
        // Dummy logic: accept any email/password, redirect by role
        if (this.email && this.password) {
          localStorage.setItem('isAuthenticated', 'true')
          localStorage.setItem('role', this.role)
          this.$router.push(this.role === 'admin' ? '/admin' : '/user')
        } else {
          this.errors.general = 'Invalid credentials.'
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