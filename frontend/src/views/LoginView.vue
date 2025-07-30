<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div class="login-card glass-card">
        <div class="login-header text-center mb-4">
          <h2 class="text-light mb-2">Quiz Master</h2>
          <p class="text-light">Login to your account</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <!-- Error Alert -->
          <div v-if="error" class="alert alert-danger glass-alert mb-3">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ error }}
          </div>
          
          <!-- Email Input -->
          <div class="mb-3">
            <label class="form-label text-light">
              <i class="bi bi-envelope me-2"></i>Email Address
            </label>
            <input 
            type="email"
            v-model="email"
              class="form-control glass-input" 
              placeholder="Enter your email" 
            required
            />
          </div>
          
          <!-- Password Input -->
          <div class="mb-3">
            <label class="form-label text-light">
              <i class="bi bi-lock me-2"></i>Password
            </label>
            <div class="input-group">
              <input 
                :type="showPassword ? 'text' : 'password'" 
            v-model="password"
                class="form-control glass-input" 
                placeholder="Enter your password" 
            required
              />
              <button 
                type="button" 
                class="btn btn-outline-secondary" 
                @click="togglePasswordVisibility"
              >
                <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
            </div>
          </div>
          
          <!-- Login Button -->
          <div class="d-grid">
            <button 
            type="submit" 
              class="btn btn-primary btn-lg" 
              :disabled="loading"
          >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Logging in...' : 'Login' }}
            </button>
          </div>
        </form>
        
        <!-- Register Link -->
        <div class="text-center mt-4">
          <span class="text-light">Don't have an account?</span>
          <router-link to="/register" class="text-primary ms-2">Create Account</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthService from '@/services/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const loading = ref(false)
    const showPassword = ref(false)

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }

    const handleLogin = async () => {
      loading.value = true
      error.value = ''

      try {
        console.log('Attempting login with:', { email: email.value, password: '***' })
        
        const result = await AuthService.login({ 
          email: email.value, 
          password: password.value 
        })
        
        console.log('Login result:', result)
        
        if (result.success) {
          // Redirect based on user type
          if (result.isAdmin) {
            router.push('/admin/dashboard')
          } else {
            router.push('/user/dashboard')
          }
        } else {
          error.value = result.message
        }
      } catch (err) {
        console.error('Login error:', err)
        error.value = 'Login failed. Please try again.'
      } finally {
        loading.value = false
        }
    }

    return {
      email,
      password,
      error,
      loading,
      showPassword,
      togglePasswordVisibility,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
  padding: 1rem 0;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 1rem;
}

.login-card {
  width: 100%;
  padding: 1.75rem;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.2),
    0 5px 15px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
  position: relative;
  overflow: hidden;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.08) 0%, 
    rgba(255, 255, 255, 0.03) 50%, 
    rgba(255, 255, 255, 0.01) 100%);
  border-radius: 16px;
  pointer-events: none;
}

.login-header {
  position: relative;
  z-index: 2;
  text-align: center;
  margin-bottom: 1.5rem;
}

.login-header h2 {
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.login-header p {
  color: rgba(255, 255, 255, 0.65);
  font-size: 0.875rem;
}

.login-form {
  position: relative;
  z-index: 2;
}

.form-label {
  color: rgba(255, 255, 255, 0.85) !important;
  font-weight: 500;
  margin-bottom: 0.375rem !important;
  font-size: 0.875rem !important;
}

.glass-input {
  background: rgba(255, 255, 255, 0.06) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: white !important;
  border-radius: 8px !important;
  padding: 0.625rem 0.875rem !important;
  font-size: 0.875rem !important;
  transition: all 0.3s ease !important;
  backdrop-filter: blur(10px) !important;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.15) !important;
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
  box-shadow: 
    0 0 0 0.15rem rgba(255, 255, 255, 0.08),
    inset 0 1px 3px rgba(0, 0, 0, 0.15),
    0 3px 15px rgba(255, 255, 255, 0.08) !important;
  transform: translateY(-1px) !important;
}

.glass-input::placeholder {
  color: rgba(255, 255, 255, 0.45) !important;
  font-size: 0.875rem !important;
}

.glass-alert {
  background: rgba(220, 53, 69, 0.12) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(220, 53, 69, 0.25) !important;
  border-radius: 8px !important;
  color: #ff8a95 !important;
  padding: 0.5rem !important;
  font-size: 0.875rem !important;
}

.btn-outline-secondary {
  border-color: rgba(255, 255, 255, 0.15) !important;
  color: rgba(255, 255, 255, 0.5) !important;
  background: rgba(255, 255, 255, 0.06) !important;
  backdrop-filter: blur(10px) !important;
  border-radius: 0 8px 8px 0 !important;
  transition: all 0.3s ease !important;
  font-size: 0.875rem !important;
}

.btn-outline-secondary:hover {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
  color: rgba(255, 255, 255, 0.8) !important;
  transform: translateY(-1px) !important;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 0.75rem !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25) !important;
  margin-top: 0.5rem !important;
}

.btn-primary:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35) !important;
}

.btn-primary:active {
  transform: translateY(0) !important;
}

.text-primary {
  color: #64b5f6 !important;
  text-decoration: none !important;
  transition: all 0.3s ease !important;
  font-weight: 500 !important;
}

.text-primary:hover {
  color: #42a5f5 !important;
  text-shadow: 0 0 8px rgba(100, 181, 246, 0.3) !important;
}

.text-light {
  color: rgba(255, 255, 255, 0.65) !important;
  font-size: 0.875rem !important;
}

.input-group .glass-input {
  border-radius: 8px 0 0 8px !important;
  border-right: none !important;
}

.mb-3 {
  margin-bottom: 1rem !important;
}

.text-center.mt-4 {
  margin-top: 1.25rem !important;
  font-size: 0.875rem !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .login-container {
    padding: 0.75rem;
    max-width: 350px;
  }
  
  .login-card {
    padding: 1.5rem;
    border-radius: 14px;
  }
  
  .login-header h2 {
    font-size: 1.375rem;
  }
}

@media (max-width: 480px) {
  .login-container {
    max-width: 320px;
  }
  
  .login-card {
    padding: 1.25rem;
  }
}
</style> 