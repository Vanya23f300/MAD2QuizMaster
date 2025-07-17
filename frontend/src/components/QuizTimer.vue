<template>
  <div class="quiz-timer">
    <div class="timer-display" :class="timerColorClass">
      <div class="timer-icon">
        <i class="bi bi-clock"></i>
      </div>
      <div class="timer-text">
        <div class="time-remaining">{{ formattedTime }}</div>
        <div class="timer-label">{{ timeLabel }}</div>
      </div>
    </div>
    <div v-if="showWarning" class="timer-warning">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ warningMessage }}
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'

export default {
  name: 'QuizTimer',
  props: {
    timeLimit: {
      type: Number,
      required: true // in minutes
    },
    isActive: {
      type: Boolean,
      default: true
    }
  },
  emits: ['timeUp', 'timeUpdate'],
  setup(props, { emit }) {
    const timeRemaining = ref(0) // in seconds
    const interval = ref(null)
    const showWarning = ref(false)

    // Computed properties
    const formattedTime = computed(() => {
      const minutes = Math.floor(timeRemaining.value / 60)
      const seconds = timeRemaining.value % 60
      return `${minutes}:${seconds.toString().padStart(2, '0')}`
    })

    const timeLabel = computed(() => {
      if (timeRemaining.value <= 0) return 'Time\'s Up!'
      if (timeRemaining.value <= 300) return 'Hurry Up!' // 5 minutes
      if (timeRemaining.value <= 600) return 'Time Running Low' // 10 minutes
      return 'Time Remaining'
    })

    const timerColorClass = computed(() => {
      if (timeRemaining.value <= 0) return 'timer-expired'
      if (timeRemaining.value <= 300) return 'timer-critical' // 5 minutes
      if (timeRemaining.value <= 600) return 'timer-warning' // 10 minutes
      return 'timer-normal'
    })

    const warningMessage = computed(() => {
      if (timeRemaining.value <= 60) return 'Less than 1 minute remaining!'
      if (timeRemaining.value <= 300) return 'Only 5 minutes left!'
      if (timeRemaining.value <= 600) return '10 minutes remaining'
      return ''
    })

    // Methods
    const startTimer = () => {
      if (interval.value) clearInterval(interval.value)
      
      timeRemaining.value = props.timeLimit * 60 // Convert minutes to seconds
      
      interval.value = setInterval(() => {
        if (timeRemaining.value > 0 && props.isActive) {
          timeRemaining.value--
          emit('timeUpdate', timeRemaining.value)
          
          // Show warnings
          if (timeRemaining.value <= 600 && timeRemaining.value > 300) {
            showWarning.value = true
            setTimeout(() => showWarning.value = false, 3000)
          } else if (timeRemaining.value <= 300 && timeRemaining.value > 60) {
            showWarning.value = true
          } else if (timeRemaining.value <= 60) {
            showWarning.value = true
          }
          
          // Time's up
          if (timeRemaining.value <= 0) {
            clearInterval(interval.value)
            emit('timeUp')
          }
        }
      }, 1000)
    }

    const stopTimer = () => {
      if (interval.value) {
        clearInterval(interval.value)
        interval.value = null
      }
    }

    // Watchers
    watch(() => props.isActive, (newValue) => {
      if (!newValue) {
        stopTimer()
      }
    })

    watch(() => props.timeLimit, () => {
      if (props.isActive) {
        startTimer()
      }
    })

    // Lifecycle
    onMounted(() => {
      if (props.timeLimit > 0) {
        startTimer()
      }
    })

    onBeforeUnmount(() => {
      stopTimer()
    })

    return {
      timeRemaining,
      formattedTime,
      timeLabel,
      timerColorClass,
      showWarning,
      warningMessage
    }
  }
}
</script>

<style scoped>
.quiz-timer {
  text-align: center;
}

.timer-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 1rem;
  transition: all 0.3s ease;
  min-width: 200px;
}

.timer-normal {
  background: rgba(25, 135, 84, 0.2);
  border: 2px solid rgba(25, 135, 84, 0.5);
  color: #198754;
}

.timer-warning {
  background: rgba(255, 193, 7, 0.2);
  border: 2px solid rgba(255, 193, 7, 0.6);
  color: #ffc107;
  animation: pulse-warning 2s infinite;
}

.timer-critical {
  background: rgba(220, 53, 69, 0.2);
  border: 2px solid rgba(220, 53, 69, 0.6);
  color: #dc3545;
  animation: pulse-critical 1s infinite;
}

.timer-expired {
  background: rgba(220, 53, 69, 0.3);
  border: 2px solid #dc3545;
  color: #dc3545;
  animation: flash 0.5s infinite;
}

.timer-icon {
  font-size: 1.5rem;
}

.timer-text {
  text-align: left;
}

.time-remaining {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
}

.timer-label {
  font-size: 0.85rem;
  opacity: 0.8;
  margin-top: 0.25rem;
}

.timer-warning {
  margin-top: 0.75rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 0.5rem;
  color: #ffc107;
  font-size: 0.9rem;
  animation: slideDown 0.3s ease;
}

@keyframes pulse-warning {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.4);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(255, 193, 7, 0);
  }
}

@keyframes pulse-critical {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(220, 53, 69, 0);
  }
}

@keyframes flash {
  0%, 50%, 100% {
    opacity: 1;
  }
  25%, 75% {
    opacity: 0.5;
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .timer-display {
    min-width: 150px;
    padding: 0.75rem;
    gap: 0.75rem;
  }
  
  .timer-icon {
    font-size: 1.25rem;
  }
  
  .time-remaining {
    font-size: 1.25rem;
  }
  
  .timer-label {
    font-size: 0.75rem;
  }
}
</style> 