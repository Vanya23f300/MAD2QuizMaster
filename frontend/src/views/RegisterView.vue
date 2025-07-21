<template>
  <div class="register-wrapper">
    <div class="register-container">
      <div class="register-box">
        <div class="register-header">
          <h2>Create Account</h2>
          <p>Sign up to start your learning journey</p>
        </div>
        
        <form @submit.prevent="register">
          <div class="form-group">
            <label for="email">Email</label>
            <input 
          type="email"
              id="email" 
          v-model="email"
          required
          placeholder="Enter your email"
        />
          </div>
          
          <div class="form-group">
            <label for="username">Username</label>
            <input
              type="text" 
              id="username" 
              v-model="username" 
              required 
              placeholder="Choose a username"
            />
          </div>
          
          <div class="form-group">
            <label for="password">Password</label>
            <div class="password-wrapper">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                v-model="password" 
                required 
                placeholder="Create a password"
            />
              <button 
                type="button" 
                class="toggle-password" 
                @click="togglePasswordVisibility"
              >
                <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="confirm-password">Confirm Password</label>
            <div class="password-wrapper">
              <input 
                :type="showConfirmPassword ? 'text' : 'password'" 
                id="confirm-password" 
                v-model="confirmPassword" 
          required
                placeholder="Confirm your password"
        />
              <button 
                type="button" 
                class="toggle-password" 
                @click="toggleConfirmPasswordVisibility"
              >
                <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="qualification">Qualification</label>
            <input 
          type="text"
              id="qualification" 
          v-model="qualification"
          required
              placeholder="Your highest qualification"
        />
          </div>
          
          <div class="form-group">
            <label for="dob">Date of Birth</label>
            <input 
          type="date"
              id="dob" 
          v-model="dob"
          required
        />
          </div>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
          
          <button 
          type="submit" 
            class="register-button" 
            :disabled="loading"
        >
            {{ loading ? 'Creating Account...' : 'Register' }}
          </button>
      </form>
        
        <div class="login-link">
          Already have an account? 
          <router-link to="/login">Login</router-link>
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
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const error = ref('')
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    
    const email = ref('')
    const username = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const dob = ref('')
    const qualification = ref('')

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }

    const toggleConfirmPasswordVisibility = () => {
      showConfirmPassword.value = !showConfirmPassword.value
    }

    const register = async () => {
      loading.value = true
      error.value = ''

      // Basic validation
      if (!email.value || !username.value || !password.value || !confirmPassword.value || !qualification.value || !dob.value) {
        error.value = 'Please fill in all fields'
        loading.value = false
        return
      }

      if (password.value !== confirmPassword.value) {
        error.value = 'Passwords do not match'
        loading.value = false
        return
      }

      try {
        const result = await AuthService.signup({
          email: email.value,
          username: username.value,
          password: password.value,
          dob: dob.value,
          qualification: qualification.value
        })
        
        if (result.success) {
          // Clear sensitive data
          password.value = ''
          confirmPassword.value = ''
          
          // Redirect to login
          router.push('/login')
        } else {
          error.value = result.message
        }
      } catch (err) {
        error.value = 'Registration failed. Please try again.'
      } finally {
        loading.value = false
        }
    }

    return {
      email,
      username,
      password,
      confirmPassword,
      dob,
      qualification,
      loading,
      error,
      showPassword,
      showConfirmPassword,
      togglePasswordVisibility,
      toggleConfirmPasswordVisibility,
      register
    }
  }
}
</script>

<style scoped>
.register-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
  padding: 1rem 0;
}

.register-container {
  width: 100%;
  max-width: 400px;
  padding: 1rem;
}

.register-box {
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

.register-box::before {
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

.register-header {
  position: relative;
  z-index: 2;
  text-align: center;
  margin-bottom: 1.5rem;
}

.register-header h2 {
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.register-header p {
  color: rgba(255, 255, 255, 0.65);
  font-size: 0.875rem;
}

.form-group {
  margin-bottom: 1rem;
  position: relative;
  z-index: 2;
}

.form-group label {
  display: block;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 0.375rem;
  font-weight: 500;
  font-size: 0.875rem;
}

.form-group input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.06);
  color: white;
  border-radius: 8px;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.15);
}

.form-group input:focus {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 0 0 0.15rem rgba(255, 255, 255, 0.08),
    inset 0 1px 3px rgba(0, 0, 0, 0.15),
    0 3px 15px rgba(255, 255, 255, 0.08);
  transform: translateY(-1px);
  outline: none;
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.45);
  font-size: 0.875rem;
}

.password-wrapper {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0.25rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.toggle-password:hover {
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.08);
}

.register-button {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25);
  position: relative;
  z-index: 2;
  margin-top: 0.5rem;
}

.register-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
}

.register-button:active {
  transform: translateY(0);
}

.register-button:disabled {
  background: rgba(108, 117, 125, 0.4);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.error-message {
  color: #ff8a95;
  text-align: center;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: rgba(220, 53, 69, 0.12);
  border: 1px solid rgba(220, 53, 69, 0.25);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  font-size: 0.875rem;
}

.login-link {
  text-align: center;
  color: rgba(255, 255, 255, 0.65);
  margin-top: 1.25rem;
  position: relative;
  z-index: 2;
  font-size: 0.875rem;
}

.login-link a {
  color: #64b5f6;
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: 500;
}

.login-link a:hover {
  color: #42a5f5;
  text-shadow: 0 0 8px rgba(100, 181, 246, 0.3);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .register-container {
    padding: 0.75rem;
    max-width: 350px;
  }
  
  .register-box {
    padding: 1.5rem;
    border-radius: 14px;
  }
  
  .form-group {
    margin-bottom: 0.875rem;
  }
  
  .register-header h2 {
    font-size: 1.375rem;
  }
}

@media (max-width: 480px) {
  .register-container {
    max-width: 320px;
  }
  
  .register-box {
    padding: 1.25rem;
  }
}
</style> 