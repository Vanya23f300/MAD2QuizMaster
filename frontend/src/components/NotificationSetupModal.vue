<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="notification-modal" @click.stop>
      <div class="modal-header">
        <h2>🔔 Welcome to Quiz Master!</h2>
        <p>Let's set up your daily learning reminders</p>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="savePreferences">
          <!-- Daily Reminders Toggle -->
          <div class="preference-group">
            <div class="preference-header">
              <h3>📚 Daily Learning Reminders</h3>
              <label class="toggle-switch">
                <input 
                  type="checkbox" 
                  v-model="preferences.dailyReminders"
                >
                <span class="slider"></span>
              </label>
            </div>
            <p class="preference-description">
              Get daily reminders to keep your learning streak going!
            </p>
          </div>

          <!-- Reminder Time Selection -->
          <div v-if="preferences.dailyReminders" class="preference-group">
            <div class="preference-header">
              <h3>⏰ Preferred Reminder Time</h3>
            </div>
            <p class="preference-description">
              When would you like to receive your daily reminders?
            </p>
            <div class="time-selector">
              <select v-model="preferences.reminderTime" class="time-input" required>
                <option value="" disabled>-- Select your preferred time --</option>
                <option value="09:00">9:00 AM - Morning Motivation</option>
                <option value="12:00">12:00 PM - Lunch Break Learning</option>
                <option value="15:00">3:00 PM - Afternoon Boost</option>
                <option value="18:00">6:00 PM - Evening Study</option>
                <option value="20:00">8:00 PM - Night Learning</option>
                <option value="21:00">9:00 PM - Before Sleep</option>
              </select>
              <div v-if="timeError" class="text-danger mt-2 p-2 rounded" style="background: rgba(220, 53, 69, 0.1); color: #ff8a95;">
                Please select a reminder time
              </div>
            </div>
          </div>

          <!-- Notification Channels -->
          <div v-if="preferences.dailyReminders" class="preference-group">
            <div class="preference-header">
              <h3>📬 How would you like to be notified?</h3>
            </div>
            
            <!-- Email Notifications -->
            <div class="notification-option">
              <label class="checkbox-option">
                <input 
                  type="checkbox" 
                  v-model="preferences.emailNotifications"
                >
                <span class="checkmark"></span>
                <div class="option-content">
                  <span class="option-title">📧 Email Notifications</span>
                  <span class="option-desc">Beautiful emails with quiz previews</span>
                </div>
              </label>
            </div>

            <!-- Google Chat Webhook -->
            <div class="notification-option">
              <label class="checkbox-option">
                <input 
                  type="checkbox" 
                  v-model="preferences.enableGChat"
                >
                <span class="checkmark"></span>
                <div class="option-content">
                  <span class="option-title">💬 Google Chat</span>
                  <span class="option-desc">Interactive messages in your workspace</span>
                </div>
              </label>
              
              <div v-if="preferences.enableGChat" class="sub-option">
                <input 
                  type="url"
                  v-model="preferences.gchatWebhookUrl"
                  placeholder="https://chat.googleapis.com/v1/spaces/.../messages?key=..."
                  class="webhook-input"
                >
                <small class="help-text">
                  <a href="https://developers.google.com/hangouts/chat/how-tos/webhooks" target="_blank">
                    How to get your webhook URL
                  </a>
                </small>
              </div>
            </div>

            <!-- SMS Notifications -->
            <div class="notification-option">
              <label class="checkbox-option">
                <input 
                  type="checkbox" 
                  v-model="preferences.enableSMS"
                >
                <span class="checkmark"></span>
                <div class="option-content">
                  <span class="option-title">📱 SMS Notifications</span>
                  <span class="option-desc">Quick text messages on your phone</span>
                </div>
              </label>
              
              <div v-if="preferences.enableSMS" class="sub-option">
                <input 
                  type="tel"
                  v-model="preferences.smsNumber"
                  placeholder="+1234567890"
                  class="phone-input"
                >
                <small class="help-text">Include country code (e.g., +1 for US)</small>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="modal-actions">
            <button 
              type="button" 
              class="btn-secondary" 
              @click="skipSetup"
            >
              Skip for now
            </button>
            <button 
              type="submit" 
              class="btn-primary"
              :disabled="saving"
            >
              {{ saving ? 'Saving...' : 'Save Preferences' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import api from '@/services/api'

export default {
  name: 'NotificationSetupModal',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const saving = ref(false)
    const timeError = ref(false)
    
    // Default preferences
    const defaultPreferences = {
      dailyReminders: true,
      reminderTime: '',
      emailNotifications: true,
      enableGChat: false,
      gchatWebhookUrl: '',
      enableSMS: false,
      smsNumber: ''
    }
    
    // Use reactive for preferences
    const preferences = reactive({ ...defaultPreferences })

    const closeModal = () => {
      timeError.value = false
      emit('close')
    }

    const skipSetup = () => {
      // Save minimal preferences (just disable reminders)
      preferences.dailyReminders = false
      savePreferences(false)
    }
    
    const resetPreferences = () => {
      // Reset to defaults
      Object.assign(preferences, defaultPreferences)
      timeError.value = false
    }
    
    const savePreferences = async (enableReminders = true) => {
      saving.value = true
      timeError.value = false
      
      try {
        // Validate that a time is selected if reminders are enabled
        if (enableReminders && preferences.dailyReminders && !preferences.reminderTime) {
          timeError.value = true
          saving.value = false
          return
        }

        // Create the preferences data in the expected format
        const preferencesData = {
          // Main preferences fields
          daily_reminders: enableReminders && preferences.dailyReminders,
          email_notifications: preferences.emailNotifications,
          quiz_notifications: true,
          monthly_reports: true,
          
          // Only include reminder_time if it's set
          ...(preferences.dailyReminders && preferences.reminderTime ? 
            { reminder_time: preferences.reminderTime } : 
            {}),
          
          // Only include webhook if enabled
          ...(preferences.enableGChat && preferences.gchatWebhookUrl ? 
            { gchat_webhook_url: preferences.gchatWebhookUrl } : 
            { gchat_webhook_url: null }),
          
          // Only include SMS if enabled
          ...(preferences.enableSMS && preferences.smsNumber ? 
            { sms_number: preferences.smsNumber } : 
            { sms_number: null })
        }

        console.log('🔶 Saving notification preferences:', preferencesData)
        
        try {
          // Log the request details
          console.log('🔷 API Request URL:', '/api/user/preferences')
          console.log('🔷 API Request Method: POST')
          console.log('🔷 API Request Data:', JSON.stringify(preferencesData))
          
          const response = await api.post('/api/user/preferences', preferencesData)
          
          console.log('✅ API Response:', response)
          
          if (response.status === 200 && response.data.success === true) {
            console.log('✅ Preferences saved successfully', response.data)
            // Add a small delay before emitting events to ensure proper rendering
            setTimeout(() => {
              emit('saved', preferencesData)
              emit('close')
            }, 100)
          } else {
            console.error('❌ Failed to save preferences with status:', response.status)
            console.error('❌ Response data:', response.data)
            alert('Failed to save preferences. Please try again. ' + 
                  (response.data && response.data.message ? response.data.message : ''))
          }
        } catch (apiError) {
          console.error('❌ API error:', apiError)
          console.error('❌ API error response:', apiError.response ? apiError.response.data : 'No response data')
          
          let errorMessage = 'An error occurred while saving preferences.'
          
          // Extract the specific error message if available
          if (apiError.response && apiError.response.data && apiError.response.data.message) {
            errorMessage += ' ' + apiError.response.data.message
          } else if (apiError.message) {
            errorMessage += ' ' + apiError.message
          }
          
          alert(errorMessage)
        }
      } catch (error) {
        console.error('❌ General error in savePreferences:', error)
        alert('An unexpected error occurred. Please try again.')
      } finally {
        saving.value = false
      }
    }
    
    // Reset preferences when modal is shown
    watch(() => props.show, (newValue) => {
      console.log('Modal visibility changed to:', newValue)
      if (newValue) {
        resetPreferences()
      }
    })
    
    onMounted(() => {
      console.log('NotificationSetupModal mounted, show status:', props.show)
    })

    // Reset error when dailyReminders changes
    watch(() => preferences.dailyReminders, () => {
      timeError.value = false
    })

    return {
      preferences,
      saving,
      timeError,
      closeModal,
      skipSetup,
      savePreferences
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  backdrop-filter: blur(5px);
}

.notification-modal {
  background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
  border-radius: 20px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header {
  text-align: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
  color: #fff;
  margin: 0 0 0.5rem;
  font-size: 1.8rem;
  font-weight: 600;
}

.modal-header p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 1rem;
}

.modal-body {
  padding: 2rem;
}

.preference-group {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.preference-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.preference-header h3 {
  color: #fff;
  margin: 0;
  font-size: 1.1rem;
  font-weight: 500;
}

.preference-description {
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 1rem;
  font-size: 0.9rem;
  line-height: 1.4;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #444;
  transition: 0.3s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .slider {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

input:checked + .slider:before {
  transform: translateX(26px);
}

/* Time Selector */
.time-selector {
  margin-top: 1rem;
}

.time-input {
  width: 100%;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #fff;
  font-size: 0.9rem;
  cursor: pointer;
}

.time-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

/* Notification Options */
.notification-option {
  margin-bottom: 1rem;
}

.checkbox-option {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  position: relative;
  padding-left: 2rem;
}

.checkbox-option input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 2px;
  left: 0;
  height: 18px;
  width: 18px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  transition: all 0.3s;
}

.checkbox-option:hover input ~ .checkmark {
  background-color: rgba(255, 255, 255, 0.2);
}

.checkbox-option input:checked ~ .checkmark {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-option input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-option .checkmark:after {
  left: 5px;
  top: 1px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.option-content {
  display: flex;
  flex-direction: column;
}

.option-title {
  color: #fff;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

.option-desc {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
}

.sub-option {
  margin-top: 0.75rem;
  margin-left: 2rem;
}

.webhook-input,
.phone-input {
  width: 100%;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: #fff;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.webhook-input:focus,
.phone-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.help-text {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.75rem;
}

.help-text a {
  color: #64b5f6;
  text-decoration: none;
}

.help-text a:hover {
  text-decoration: underline;
}

/* Action Buttons */
.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .notification-modal {
    width: 95%;
    margin: 1rem;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .preference-group {
    padding: 1rem;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .modal-actions button {
    width: 100%;
  }
}
</style> 