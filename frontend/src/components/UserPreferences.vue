<template>
  <div class="user-preferences glass">
    <div class="preferences-header">
      <h3 class="text-light mb-0">
        <i class="bi bi-gear me-2"></i>
        User Preferences
      </h3>
      <p class="text-muted mb-0">Manage your notification settings</p>
    </div>

    <div class="preferences-content">
      <!-- Notification Settings -->
      <div class="preference-section">
        <h5 class="section-title">
          <i class="bi bi-bell me-2"></i>
          Notification Settings
        </h5>
        
        <div class="setting-item">
          <div class="setting-info">
            <label class="setting-label">Monthly Reports</label>
            <p class="setting-description">Receive monthly performance reports via email</p>
          </div>
          <div class="setting-control">
            <div class="form-check form-switch">
              <input 
                class="form-check-input" 
                type="checkbox" 
                v-model="preferences.notifications.monthlyReports"
                id="monthlyReports"
              />
            </div>
          </div>
        </div>

        <div class="setting-item">
          <div class="setting-info">
            <label class="setting-label">Email Notifications</label>
            <p class="setting-description">Enable email delivery for notifications</p>
          </div>
          <div class="setting-control">
            <div class="form-check form-switch">
              <input 
                class="form-check-input" 
                type="checkbox" 
                v-model="preferences.notificationChannels.emailNotifications"
                id="emailNotifications"
              />
            </div>
          </div>
        </div>
      </div>
      
      <div class="preferences-footer">
        <button 
          class="btn btn-outline-light me-2" 
          @click="resetToDefaults"
        >
          Reset to Default
        </button>
        <button 
          class="btn btn-primary" 
          @click="savePreferences"
          :disabled="saving"
        >
          <span v-if="!saving">Save Preferences</span>
          <span v-else>
            <i class="bi bi-arrow-repeat spin me-2"></i>
            Saving...
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'UserPreferences',
  data() {
    return {
      saving: false,
      preferences: {
        notifications: {
          dailyReminders: true,
          reminderTime: null, 
          quizNotifications: true,
          monthlyReports: true,
          exportNotifications: true
        },
        notificationChannels: {
          emailNotifications: true
        }
      },
      defaultPreferences: null
    }
  },
  methods: {
    async loadPreferences() {
      try {
        const response = await api.get('/api/user/preferences')
        if (response.data.preferences) {
          // Only update the properties we care about
          if (response.data.preferences.notifications) {
            this.preferences.notifications.monthlyReports = 
              response.data.preferences.notifications.monthlyReports;
          }
          if (response.data.preferences.notificationChannels) {
            this.preferences.notificationChannels.emailNotifications = 
              response.data.preferences.notificationChannels.emailNotifications;
          }
        }
      } catch (error) {
        console.error('Failed to load preferences:', error)
      }
    },

    async savePreferences() {
      try {
        this.saving = true
        console.log('Starting to save preferences...');
        
        // First get the current preferences to make sure we don't lose data
        console.log('Fetching current preferences...');
        const currentPrefs = await api.get('/api/user/preferences');
        console.log('Current preferences:', currentPrefs.data);
        
        const fullPreferences = currentPrefs.data.preferences || {};
        
        // Now update only the fields we care about
        if (!fullPreferences.notifications) fullPreferences.notifications = {};
        if (!fullPreferences.notificationChannels) fullPreferences.notificationChannels = {};
        
        fullPreferences.notifications.monthlyReports = this.preferences.notifications.monthlyReports;
        fullPreferences.notificationChannels.emailNotifications = this.preferences.notificationChannels.emailNotifications;
        
        // CRITICAL FIX: Ensure dailyReminders is properly handled with reminderTime
        // If we're keeping dailyReminders enabled, make sure a reminderTime exists
        if (fullPreferences.notifications.dailyReminders) {
          if (!fullPreferences.notifications.reminderTime) {
            // Set a default time if none exists (backend requires this)
            fullPreferences.notifications.reminderTime = '12:00'; // Default to noon
          }
        } else {
          // If we're disabling dailyReminders, no need for reminderTime
          fullPreferences.notifications.dailyReminders = false;
        }
        
        console.log('Sending updated preferences to API:', fullPreferences);
        
        // Send the complete preferences object with our updates
        const response = await api.post('/api/user/preferences', {
          preferences: fullPreferences
        });
        
        console.log('API response:', response.data);
        
        if (response.data.success) {
          console.log('Preferences saved successfully');
          this.$emit('preferences-saved', fullPreferences)
          this.$emit('success', 'Preferences saved successfully!')
        } else {
          console.error('API returned success=false:', response.data);
          this.$emit('error', response.data.message || 'Failed to save preferences');
        }
        
      } catch (error) {
        console.error('Failed to save preferences. Error:', error);
        
        if (error.response) {
          console.error('Error response data:', error.response.data);
          console.error('Error response status:', error.response.status);
          this.$emit('error', error.response.data.message || 'Server error: ' + error.response.status);
        } else if (error.request) {
          console.error('No response received:', error.request);
          this.$emit('error', 'No response from server');
        } else {
          console.error('Error message:', error.message);
          this.$emit('error', 'Error: ' + error.message);
        }
      } finally {
        this.saving = false
      }
    },

    resetToDefaults() {
      this.preferences = {
        notifications: {
          monthlyReports: true
        },
        notificationChannels: {
          emailNotifications: true
        }
      }
    }
  },

  async mounted() {
    // Store default preferences
    this.defaultPreferences = JSON.parse(JSON.stringify(this.preferences))
    
    // Load user preferences
    await this.loadPreferences()
  }
}
</script>

<style scoped>
.user-preferences {
  padding: 0;
}

.preferences-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.preferences-content {
  padding: 1.5rem;
}

.preferences-footer {
  padding-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.preference-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info {
  flex: 1;
}

.setting-label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: rgba(255, 255, 255, 0.9);
}

.setting-description {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0;
}

.setting-control {
  width: 120px;
  text-align: right;
}

.form-check-input {
  width: 3rem;
  height: 1.5rem;
  cursor: pointer;
}

.glass-input {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.1);
}

.glass-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 