import mitt from 'mitt'
import quizService from './quizService'

const emitter = mitt()

class NotificationService {
  // Show a notification
  show(notification) {
    if (!notification.id) {
      notification.id = Date.now()
    }
    if (!notification.timestamp) {
      notification.timestamp = new Date().toISOString()
    }
    if (!notification.read) {
      notification.read = false
    }
    emitter.emit('notification', notification)
    return notification.id
  }

  // Show a reminder notification
  showReminder(title, message, actionUrl = null) {
    return this.show({
      type: 'reminder',
      title,
      message,
      actionUrl,
      read: false
    })
  }

  // Show a quiz notification
  showQuiz(title, message, actionUrl = null) {
    return this.show({
      type: 'quiz',
      title,
      message,
      actionUrl,
      read: false
    })
  }

  // Show a report notification
  showReport(title, message, actionUrl = null) {
    return this.show({
      type: 'report',
      title,
      message,
      actionUrl,
      read: false
    })
  }

  // Show an export notification
  showExport(title, message, actionUrl = null) {
    return this.show({
      type: 'export',
      title,
      message,
      actionUrl,
      read: false
    })
  }

  // Show a system notification
  showSystem(title, message, actionUrl = null) {
    return this.show({
      type: 'system',
      title,
      message,
      actionUrl,
      read: false
    })
  }

  // Remove a notification
  remove(id) {
    emitter.emit('remove-notification', id)
  }

  // Mark a notification as read
  markAsRead(id) {
    emitter.emit('mark-notification-read', id)
  }

  // Mark all notifications as read
  markAllRead() {
    emitter.emit('mark-all-notifications-read')
  }

  // Subscribe to notification events
  on(event, callback) {
    emitter.on(event, callback)
  }

  // Unsubscribe from notification events
  off(event, callback) {
    emitter.off(event, callback)
  }
  
  // Check for new unattempted quizzes
  async checkForNewQuizzes() {
    try {
      const unattemptedQuizzes = await quizService.getUnattemptedQuizzes();
      
      if (unattemptedQuizzes && unattemptedQuizzes.length > 0) {
        // Show notification for new quizzes
        const count = unattemptedQuizzes.length;
        const message = count === 1 
          ? `You have 1 new quiz available: ${unattemptedQuizzes[0].name}`
          : `You have ${count} new quizzes available! Take them to improve your skills.`;
          
        this.showQuiz(
          'New Quizzes Available',
          message,
          '/user/quizzes'
        );
        
        return unattemptedQuizzes;
      }
      
      return [];
    } catch (error) {
      console.error('Failed to check for new quizzes:', error);
      return [];
    }
  }
}

export default new NotificationService() 