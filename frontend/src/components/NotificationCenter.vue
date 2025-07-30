<template>
  <div class="notification-center glass">
    <div class="notification-header">
      <h3 class="text-light mb-0">
        <i class="bi bi-bell me-2"></i>
        Notifications
      </h3>
      <div class="notification-actions">
        <button 
          class="btn btn-dark-toggle btn-sm"
          @click="markAllRead"
          v-if="unreadCount > 0"
        >
          <i class="bi bi-check-all me-1"></i>
          Mark All Read
        </button>
      </div>
    </div>

    <div class="notification-list" v-if="notifications.length > 0">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        :class="['notification-item glass', { 'unread': !notification.read }]"
        @click="markAsRead(notification.id)"
      >
        <div class="notification-icon">
          <i :class="getNotificationIcon(notification.type)"></i>
        </div>
        <div class="notification-content">
          <h5 class="notification-title">{{ notification.title }}</h5>
          <p class="notification-message">{{ notification.message }}</p>
          <small class="notification-time">{{ formatTime(notification.timestamp) }}</small>
        </div>
        <div class="notification-actions">
          <button 
            class="btn btn-dark-toggle btn-sm"
            v-if="notification.actionUrl"
            @click.stop="handleAction(notification)"
          >
            <i class="bi bi-arrow-right"></i>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state text-center py-4">
      <i class="bi bi-bell-slash display-4 text-muted"></i>
      <p class="text-muted mt-2">No notifications</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import notificationService from '../services/notification-service'
import AuthService from '../services/auth'

export default {
  name: 'NotificationCenter',
  setup() {
    const notifications = ref([])
    const loading = ref(false)
    const error = ref(null)
    const isAdmin = ref(AuthService.isAdmin())

    const addNotification = (notification) => {
      notifications.value.unshift({
        ...notification,
        id: notification.id || Date.now(),
        timestamp: notification.timestamp || new Date().toISOString()
      })
    }

    const removeNotification = (id) => {
      const index = notifications.value.findIndex(n => n.id === id)
      if (index !== -1) {
        notifications.value.splice(index, 1)
      }
    }

    const markAsRead = (id) => {
      const notification = notifications.value.find(n => n.id === id)
      if (notification) {
        notification.read = true
        notificationService.markAsRead(id)
      }
    }

    const markAllRead = () => {
      notifications.value.forEach(n => n.read = true)
      notificationService.markAllRead()
    }

    const unreadCount = computed(() => {
      return notifications.value.filter(n => !n.read).length
    })

    onMounted(() => {
      // Subscribe to notification events
      notificationService.on('notification', addNotification)
      notificationService.on('remove-notification', removeNotification)
      notificationService.on('mark-notification-read', markAsRead)
      notificationService.on('mark-all-notifications-read', markAllRead)
      
      // Demo notification for daily reminders - only for regular users
      if (!isAdmin.value) {
        setTimeout(() => {
          notificationService.showReminder(
            'Daily Quiz Reminder',
            'We noticed you have new quizzes available! Take a quiz today to stay on track.',
            '/user/quizzes'
          )
        }, 2000)
        
        // Also check for new quizzes
        checkForNewQuizzes()
      }
    })
    
    const checkForNewQuizzes = async () => {
      // Only check for new quizzes for regular users
      if (!isAdmin.value) {
        try {
          await notificationService.checkForNewQuizzes()
        } catch (err) {
          console.error('Error checking for new quizzes:', err)
        }
      }
    }

    onBeforeUnmount(() => {
      // Clean up event listeners
      notificationService.off('notification', addNotification)
      notificationService.off('remove-notification', removeNotification)
      notificationService.off('mark-notification-read', markAsRead)
      notificationService.off('mark-all-notifications-read', markAllRead)
    })

    return {
      notifications,
      loading,
      error,
      removeNotification,
      markAsRead,
      markAllRead,
      unreadCount
    }
  },
  methods: {
    getNotificationIcon(type) {
      const icons = {
        reminder: 'bi bi-alarm',
        quiz: 'bi bi-pencil-square',
        report: 'bi bi-file-earmark-text',
        export: 'bi bi-download',
        system: 'bi bi-gear'
      }
      return icons[type] || 'bi bi-bell'
    },
    formatTime(timestamp) {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date
      
      // Less than 24 hours
      if (diff < 24 * 60 * 60 * 1000) {
        return date.toLocaleTimeString('en-US', { 
          hour: 'numeric', 
          minute: '2-digit',
          hour12: true 
        })
      }
      
      // Less than 7 days
      if (diff < 7 * 24 * 60 * 60 * 1000) {
        return date.toLocaleDateString('en-US', { weekday: 'short' })
      }
      
      // Older
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
      })
    },
    handleAction(notification) {
      if (notification.actionUrl) {
        this.$router.push(notification.actionUrl)
      }
    }
  }
}
</script>

<style scoped>
.notification-center {
  width: 100%;
  max-width: 400px;
  border-radius: 1rem;
  overflow: hidden;
}

.notification-header {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-list {
  max-height: 500px;
  overflow-y: auto;
}

.notification-item {
  padding: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.notification-item.unread {
  background: rgba(36, 163, 90, 0.1);
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #fff;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 0.9rem;
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
}

.notification-message {
  font-size: 0.8rem;
  margin: 0.25rem 0;
  color: rgba(255, 255, 255, 0.7);
}

.notification-time {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
}

.empty-state {
  color: rgba(255, 255, 255, 0.5);
}

.empty-state i {
  font-size: 3rem;
}
</style> 