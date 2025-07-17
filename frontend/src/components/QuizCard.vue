<template>
  <div class="quiz-card glass" :class="statusClass">
    <div class="quiz-header">
      <div class="quiz-title">
        <h6 class="text-light mb-1">{{ quiz.title }}</h6>
        <span class="quiz-subject text-secondary">{{ quiz.subject }}</span>
      </div>
      <div class="quiz-status">
        <span :class="statusBadgeClass">{{ statusText }}</span>
      </div>
    </div>
    
    <div class="quiz-meta">
      <div class="meta-item">
        <i class="bi bi-clock me-2"></i>
        <span class="text-secondary">{{ quiz.duration }}</span>
      </div>
      <div class="meta-item">
        <i class="bi bi-question-circle me-2"></i>
        <span class="text-secondary">{{ quiz.questionCount }} questions</span>
      </div>
      <div class="meta-item">
        <i class="bi bi-star me-2"></i>
        <span class="text-secondary">{{ quiz.difficulty }}</span>
      </div>
    </div>
    
    <div class="quiz-actions">
      <button 
        v-if="quiz.status === 'available'"
        class="btn btn-primary btn-sm"
        @click="$emit('start-quiz', quiz.id)"
      >
        <i class="bi bi-play me-1"></i>Start Quiz
      </button>
      <button 
        v-else-if="quiz.status === 'in-progress'"
        class="btn btn-warning btn-sm"
        @click="$emit('continue-quiz', quiz.id)"
      >
        <i class="bi bi-arrow-right me-1"></i>Continue
      </button>
      <button 
        v-else-if="quiz.status === 'completed'"
        class="btn btn-outline-secondary btn-sm"
        @click="$emit('view-result', quiz.id)"
      >
        <i class="bi bi-eye me-1"></i>View Result
      </button>
      <button 
        class="btn btn-outline-primary btn-sm ms-2"
        @click="$emit('view-details', quiz.id)"
      >
        <i class="bi bi-info-circle me-1"></i>Details
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuizCard',
  props: {
    quiz: {
      type: Object,
      required: true,
      default: () => ({
        id: 1,
        title: 'Sample Quiz',
        subject: 'Web Development',
        duration: '30 min',
        questionCount: 15,
        difficulty: 'Medium',
        status: 'available' // available, in-progress, completed
      })
    }
  },
  computed: {
    statusClass() {
      return {
        'quiz-available': this.quiz.status === 'available',
        'quiz-in-progress': this.quiz.status === 'in-progress',
        'quiz-completed': this.quiz.status === 'completed'
      }
    },
    statusText() {
      const statusMap = {
        'available': 'Available',
        'in-progress': 'In Progress',
        'completed': 'Completed'
      }
      return statusMap[this.quiz.status] || 'Unknown'
    },
    statusBadgeClass() {
      const baseClass = 'badge'
      const statusClasses = {
        'available': 'bg-success',
        'in-progress': 'bg-warning text-dark',
        'completed': 'bg-secondary'
      }
      return `${baseClass} ${statusClasses[this.quiz.status] || 'bg-secondary'}`
    }
  }
}
</script>

<style scoped>
.quiz-card {
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
  justify-content: space-between;
}

.quiz-card:hover {
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

.quiz-title h6 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.quiz-subject {
  font-size: 0.9rem;
  font-weight: 500;
}

.quiz-status {
  margin-left: 1rem;
}

.quiz-meta {
  margin-bottom: 1.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.meta-item:last-child {
  margin-bottom: 0;
}

.quiz-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.quiz-actions .btn {
  flex: 1;
  min-width: 120px;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Status-specific styling */
.quiz-available {
  border-color: rgba(25, 135, 84, 0.3);
}

.quiz-in-progress {
  border-color: rgba(255, 193, 7, 0.3);
}

.quiz-completed {
  border-color: rgba(108, 117, 125, 0.3);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .quiz-card {
    padding: 1.25rem;
  }
  
  .quiz-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .quiz-status {
    margin-left: 0;
    margin-top: 0.5rem;
  }
  
  .quiz-actions {
    flex-direction: column;
  }
  
  .quiz-actions .btn {
    min-width: auto;
  }
}
</style> 