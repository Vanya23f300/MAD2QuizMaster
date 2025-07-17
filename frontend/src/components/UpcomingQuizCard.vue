<template>
  <div class="upcoming-quiz-card glass">
    <div class="quiz-header">
      <div class="quiz-info">
        <h6 class="quiz-title text-light mb-1">{{ quiz.title }}</h6>
        <span class="quiz-subject text-secondary">{{ quiz.subject }}</span>
      </div>
      <div class="quiz-status">
        <span class="badge bg-primary">{{ statusText }}</span>
      </div>
    </div>
    
    <div class="quiz-meta">
      <div class="meta-row">
        <div class="meta-item">
          <i class="bi bi-calendar-event me-2"></i>
          <span class="text-secondary">{{ formattedDate }}</span>
        </div>
        <div class="meta-item">
          <i class="bi bi-clock me-2"></i>
          <span class="text-secondary">{{ quiz.duration }}</span>
        </div>
      </div>
      <div class="meta-row">
        <div class="meta-item">
          <i class="bi bi-question-circle me-2"></i>
          <span class="text-secondary">{{ quiz.questionCount }} questions</span>
        </div>
        <div class="meta-item">
          <i class="bi bi-star me-2"></i>
          <span class="text-secondary">{{ quiz.difficulty }}</span>
        </div>
      </div>
    </div>
    
    <div v-if="showCountdown" class="countdown-section">
      <div class="countdown-label text-secondary mb-2">Starts in:</div>
      <div class="countdown-timer">
        <div class="countdown-item">
          <div class="countdown-value">{{ countdown.days }}</div>
          <div class="countdown-label">Days</div>
        </div>
        <div class="countdown-separator">:</div>
        <div class="countdown-item">
          <div class="countdown-value">{{ countdown.hours }}</div>
          <div class="countdown-label">Hours</div>
        </div>
        <div class="countdown-separator">:</div>
        <div class="countdown-item">
          <div class="countdown-value">{{ countdown.minutes }}</div>
          <div class="countdown-label">Minutes</div>
        </div>
      </div>
    </div>
    
    <div class="quiz-actions">
      <button 
        class="btn btn-primary btn-sm"
        @click="$emit('start-quiz', quiz.id)"
      >
        <i class="bi bi-play me-1"></i>Start Quiz
      </button>
      <button 
        class="btn btn-outline-secondary btn-sm ms-2"
        @click="$emit('view-details', quiz.id)"
      >
        <i class="bi bi-info-circle me-1"></i>Details
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UpcomingQuizCard',
  props: {
    quiz: {
      type: Object,
      required: true,
      default: () => ({
        id: 1,
        title: 'Sample Quiz',
        subject: 'Web Development',
        date: '2024-01-15T10:00:00',
        duration: '30 min',
        questionCount: 15,
        difficulty: 'Medium',
        status: 'upcoming' // upcoming, available, in-progress
      })
    },
    showCountdown: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      countdown: {
        days: 0,
        hours: 0,
        minutes: 0
      },
      countdownInterval: null
    }
  },
  computed: {
    statusText() {
      const statusMap = {
        'upcoming': 'Upcoming',
        'available': 'Available',
        'in-progress': 'In Progress'
      }
      return statusMap[this.quiz.status] || 'Unknown'
    },
    formattedDate() {
      const date = new Date(this.quiz.date)
      return date.toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  },
  mounted() {
    this.updateCountdown()
    if (this.showCountdown) {
      this.countdownInterval = setInterval(this.updateCountdown, 60000) // Update every minute
    }
  },
  beforeUnmount() {
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval)
    }
  },
  methods: {
    updateCountdown() {
      const now = new Date()
      const quizDate = new Date(this.quiz.date)
      const diff = quizDate - now
      
      if (diff <= 0) {
        this.countdown = { days: 0, hours: 0, minutes: 0 }
        return
      }
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      
      this.countdown = { days, hours, minutes }
    }
  }
}
</script>

<style scoped>
.upcoming-quiz-card {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 20px 0 rgba(0,0,0,0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.upcoming-quiz-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px 0 rgba(0,0,0,0.25);
  background: rgba(35, 39, 43, 0.7);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.quiz-title {
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.3;
}

.quiz-subject {
  font-size: 0.9rem;
  font-weight: 500;
}

.quiz-meta {
  margin-bottom: 1.5rem;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.meta-row:last-child {
  margin-bottom: 0;
}

.meta-item {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.countdown-section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(13, 110, 253, 0.1);
  border-radius: 0.75rem;
  border: 1px solid rgba(13, 110, 253, 0.2);
}

.countdown-timer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.countdown-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 50px;
}

.countdown-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0D6EFD;
  line-height: 1;
}

.countdown-label {
  font-size: 0.7rem;
  color: #ADB5BD;
  font-weight: 500;
  text-align: center;
}

.countdown-separator {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0D6EFD;
  margin-top: -0.5rem;
}

.quiz-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: auto;
}

.quiz-actions .btn {
  flex: 1;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .upcoming-quiz-card {
    padding: 1.25rem;
  }
  
  .quiz-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .quiz-status {
    margin-top: 0.5rem;
  }
  
  .meta-row {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .countdown-timer {
    gap: 0.25rem;
  }
  
  .countdown-item {
    min-width: 40px;
  }
  
  .countdown-value {
    font-size: 1.25rem;
  }
  
  .countdown-label {
    font-size: 0.65rem;
  }
  
  .quiz-actions {
    flex-direction: column;
  }
}
</style> 