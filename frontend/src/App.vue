<template>
  <div class="app-bg">
    <div class="main-content">
      <router-view />
    </div>
    <div class="notification-container">
      <NotificationCenter v-if="showNotifications" />
    </div>
    <button 
      class="notification-toggle glass-button"
      @click="toggleNotifications"
    >
      <i class="bi bi-bell"></i>
      <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
    </button>
  </div>
</template>

<script>
import NotificationCenter from './components/NotificationCenter.vue'
import notificationService from './services/notification-service'
import { ref, onMounted, computed } from 'vue'

export default {
  name: 'App',
  components: {
    NotificationCenter
  },
  setup() {
    const showNotifications = ref(false)
    const notifications = ref([])
    
    const toggleNotifications = () => {
      showNotifications.value = !showNotifications.value
    }
    
    const addNotification = (notification) => {
      notifications.value.unshift(notification)
    }
    
    const unreadCount = computed(() => {
      return notifications.value.filter(n => !n.read).length
    })
    
    onMounted(() => {
      notificationService.on('notification', addNotification)
      
      // Subscribe to mark-as-read and mark-all-read events
      notificationService.on('mark-notification-read', (id) => {
        const notification = notifications.value.find(n => n.id === id)
        if (notification) notification.read = true
      })
      
      notificationService.on('mark-all-notifications-read', () => {
        notifications.value.forEach(n => n.read = true)
      })
    })
    
    return {
      showNotifications,
      toggleNotifications,
      unreadCount,
      notifications
    }
  }
}
</script>

<style>
/* Global Reset & Base Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.app-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, 
    #0a0a0f 0%, 
    #1a1a2e 25%, 
    #16213e 50%, 
    #0f0f23 75%, 
    #0a0a14 100%
  );
  background-size: 400% 400%;
  animation: gradientShift 20s ease infinite;
  position: relative;
  overflow-x: hidden;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Main Content */
.main-content {
  min-height: 100vh;
  padding-top: 80px; /* Space for navbar */
  position: relative;
}

/* Enhanced Glassmorphism */
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.37),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.2),
    0 5px 15px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.glass-navbar {
  background: rgba(0, 0, 0, 0.3) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  z-index: 1050;
  border-radius: 0 0 20px 20px;
}

.glass-input {
  background: rgba(255, 255, 255, 0.06) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: white !important;
  backdrop-filter: blur(10px);
  border-radius: 8px !important;
}

.glass-input::placeholder {
  color: rgba(255, 255, 255, 0.45) !important;
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 0 0 0.15rem rgba(255, 255, 255, 0.08) !important;
  color: white !important;
}

/* Form Controls */
.form-control, .form-select {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  border-radius: 8px;
}

.form-control:focus, .form-select:focus {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 0 0.15rem rgba(255, 255, 255, 0.08);
  color: white;
}

/* Text Colors */
.text-light {
  color: rgba(255, 255, 255, 0.95) !important;
}

.text-muted {
  color: rgba(255, 255, 255, 0.65) !important;
}

/* Buttons */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
  border-radius: 8px;
  font-weight: 600;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
}

.btn-outline-light {
  border-color: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.06);
  border-radius: 8px;
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
}

.btn-outline-secondary {
  border-color: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.06);
}

.btn-outline-secondary:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.25);
  color: rgba(255, 255, 255, 0.8);
}

/* Alerts */
.alert {
  border: none;
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.alert-danger {
  background: rgba(220, 53, 69, 0.12);
  color: #ff8a95;
  border: 1px solid rgba(220, 53, 69, 0.25);
}

.alert-success {
  background: rgba(40, 167, 69, 0.12);
  color: #51cf66;
  border: 1px solid rgba(40, 167, 69, 0.25);
}

.alert-warning {
  background: rgba(255, 193, 7, 0.12);
  color: #ffd43b;
  border: 1px solid rgba(255, 193, 7, 0.25);
}

/* Tables */
.table-dark {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  overflow: hidden;
}

.table-dark th {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.1);
}

.table-dark td {
  color: rgba(255, 255, 255, 0.85);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Cards */
.card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.card-header {
  background: rgba(255, 255, 255, 0.08);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
}

/* Sidebar */
.sidebar {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  color: rgba(255, 255, 255, 0.95);
  background: rgba(255, 255, 255, 0.1);
}

/* Badges */
.badge {
  border-radius: 6px;
}

.bg-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.bg-secondary {
  background: rgba(255, 255, 255, 0.15) !important;
}

/* Links */
.text-primary {
  color: #64b5f6 !important;
}

.text-primary:hover {
  color: #42a5f5 !important;
  text-shadow: 0 0 8px rgba(100, 181, 246, 0.3);
}

/* Modal */
.modal-content {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border-radius: 12px;
}

.modal-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Notification Container */
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1060;
  transition: all 0.3s ease;
  transform: translateX(420px);
  opacity: 0;
}

.notification-container:has(> .notification-center[style*="display: block"]) {
  transform: translateX(0);
  opacity: 1;
}

/* Notification Toggle Button */
.notification-toggle {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1050;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.notification-toggle:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #dc3545;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .container-fluid {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .main-content {
    padding-top: 70px;
  }
  
  .notification-container {
    top: 10px;
    right: 10px;
    left: 10px;
    width: auto;
  }
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>

