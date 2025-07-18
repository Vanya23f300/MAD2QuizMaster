<template>
  <div class="login-view fade-in">
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
      <div class="login-card glass">
        <div class="login-header text-center mb-4">
          <div class="login-icon mb-3">
            <i class="bi bi-person-circle"></i>
          </div>
          <h2 class="text-light mb-2">Welcome Back</h2>
          <p class="text-muted">Sign in to Quiz Master</p>
        </div>
        
        <form @submit.prevent="onSubmit" novalidate class="login-form">
          <BaseInput
            id="login-email"
            label="Email Address"
            type="email"
            v-model="email"
            :error="errors.email"
            required
            placeholder="Enter your email"
            class="mb-3"
          />
          
          <BaseInput
            id="login-password"
            label="Password"
            type="password"
            v-model="password"
            :error="errors.password"
            required
            placeholder="Enter your password"
            class="mb-3"
          />
          
          <div class="mb-4">
            <label class="form-label text-light fw-semibold">Login As</label>
            <select v-model="role" class="form-select" required>
              <option value="user">Student</option>
              <option value="admin">Administrator</option>
            </select>
          </div>
          
          <FormError :error="errors.general" class="mb-3" />
          
          <BaseButton 
            :loading="loading" 
            type="submit" 
            class="w-100 mb-4 btn-login"
          >
            <i class="bi bi-box-arrow-in-right me-2"></i>
            Sign In
          </BaseButton>
        </form>
        
        <div class="text-center">
          <span class="text-muted">Don't have an account?</span>
          <router-link to="/register" class="register-link ms-2">
            Create Account
          </router-link>
        </div>
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
.login-view {
  min-height: 100vh;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  max-width: 400px;
  width: 100%;
  padding: 2rem 1.8rem;
  position: relative;
  overflow: hidden;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(135deg, #4a5568, #2d3748);
  border-radius: 16px 16px 0 0;
}

.login-header {
  position: relative;
}

.login-icon {
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

.login-icon i {
  font-size: 1.8rem;
  color: white;
}

.login-form {
  position: relative;
}

.btn-login {
  font-size: 1rem;
  padding: 14px 24px;
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.register-link {
  color: #cbd5e0;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
}

.register-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: #4a5568;
  transition: width 0.3s ease;
}

.register-link:hover {
  color: #ffffff;
  transform: translateY(-1px);
}

.register-link:hover::after {
  width: 100%;
}

/* Form enhancements */
.form-label {
  color: rgba(255, 255, 255, 0.9) !important;
  font-weight: 500;
  margin-bottom: 8px;
}

/* Responsive */
@media (max-width: 576px) {
  .login-card {
    padding: 2rem 1.5rem;
    margin: 0 1rem;
  }
  
  .login-icon {
    width: 50px;
    height: 50px;
  }
  
  .login-icon i {
    font-size: 1.5rem;
  }
}
</style> 