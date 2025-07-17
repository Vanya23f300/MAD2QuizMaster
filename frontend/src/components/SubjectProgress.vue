<template>
  <div class="subject-progress glass">
    <div class="subject-header">
      <div class="subject-info">
        <div class="subject-icon" :style="{ backgroundColor: subjectColor }">
          <i :class="subject.icon"></i>
        </div>
        <div class="subject-details">
          <h6 class="subject-title text-light mb-1">{{ subject.name }}</h6>
          <span class="subject-status text-secondary">{{ completionText }}</span>
        </div>
      </div>
      <div class="progress-percentage">
        <span class="percentage-value">{{ subject.progress }}%</span>
      </div>
    </div>
    
    <div class="progress-bar-container">
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :style="{ 
            width: `${subject.progress}%`,
            backgroundColor: progressColor 
          }"
        ></div>
      </div>
      <div class="progress-stats">
        <span class="stat-item">
          <i class="bi bi-check-circle text-success me-1"></i>
          {{ subject.completedQuizzes }} completed
        </span>
        <span class="stat-item">
          <i class="bi bi-clock text-warning me-1"></i>
          {{ subject.remainingQuizzes }} remaining
        </span>
      </div>
    </div>
    
    <div class="performance-indicator">
      <div class="performance-item">
        <span class="performance-label text-secondary">Average Score:</span>
        <span class="performance-value" :class="averageScoreClass">{{ subject.averageScore }}%</span>
      </div>
      <div class="performance-item">
        <span class="performance-label text-secondary">Best Score:</span>
        <span class="performance-value text-success">{{ subject.bestScore }}%</span>
      </div>
    </div>
    
    <div class="subject-actions">
      <button 
        v-if="subject.remainingQuizzes > 0"
        class="btn btn-primary btn-sm"
        @click="$emit('start-quiz', subject.id)"
      >
        <i class="bi bi-play me-1"></i>Continue Learning
      </button>
      <button 
        v-else
        class="btn btn-outline-success btn-sm"
        @click="$emit('review-subject', subject.id)"
      >
        <i class="bi bi-check-circle me-1"></i>Review Completed
      </button>
      <button 
        class="btn btn-outline-secondary btn-sm ms-2"
        @click="$emit('view-details', subject.id)"
      >
        <i class="bi bi-info-circle me-1"></i>Details
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SubjectProgress',
  props: {
    subject: {
      type: Object,
      required: true,
      default: () => ({
        id: 1,
        name: 'Web Development',
        icon: 'bi bi-code-slash',
        progress: 75,
        completedQuizzes: 6,
        remainingQuizzes: 2,
        averageScore: 82,
        bestScore: 95,
        color: '#0D6EFD'
      })
    }
  },
  computed: {
    subjectColor() {
      return this.subject.color || '#0D6EFD'
    },
    progressColor() {
      const progress = this.subject.progress
      if (progress >= 90) return '#198754' // Success green
      if (progress >= 70) return '#0D6EFD' // Primary blue
      if (progress >= 50) return '#FFC107' // Warning yellow
      return '#DC3545' // Danger red
    },
    completionText() {
      const progress = this.subject.progress
      if (progress === 100) return 'Completed'
      if (progress >= 80) return 'Almost Complete'
      if (progress >= 60) return 'In Progress'
      if (progress >= 40) return 'Getting Started'
      return 'Just Started'
    },
    averageScoreClass() {
      const score = this.subject.averageScore
      if (score >= 90) return 'text-success'
      if (score >= 80) return 'text-primary'
      if (score >= 70) return 'text-warning'
      return 'text-danger'
    }
  }
}
</script>

<style scoped>
.subject-progress {
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

.subject-progress:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px 0 rgba(0,0,0,0.25);
  background: rgba(35, 39, 43, 0.7);
}

.subject-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.subject-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.subject-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  color: white;
  font-size: 1.25rem;
}

.subject-details {
  flex: 1;
}

.subject-title {
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 0.25rem;
}

.subject-status {
  font-size: 0.85rem;
  font-weight: 500;
}

.progress-percentage {
  text-align: right;
}

.percentage-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #F8F9FA;
}

.progress-bar-container {
  margin-bottom: 1.5rem;
}

.progress-bar {
  width: 100%;
  height: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.25rem;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.progress-fill {
  height: 100%;
  border-radius: 0.25rem;
  transition: width 0.5s ease-in-out;
}

.progress-stats {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.stat-item {
  display: flex;
  align-items: center;
  color: #ADB5BD;
}

.performance-indicator {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.performance-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.performance-item:last-child {
  margin-bottom: 0;
}

.performance-label {
  font-weight: 500;
}

.performance-value {
  font-weight: 700;
}

.subject-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: auto;
}

.subject-actions .btn {
  flex: 1;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Animation for progress bar */
.progress-fill {
  animation: progress-fill 1s ease-out;
}

@keyframes progress-fill {
  from {
    width: 0%;
  }
  to {
    width: var(--final-width);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .subject-progress {
    padding: 1.25rem;
  }
  
  .subject-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .progress-percentage {
    margin-top: 0.5rem;
    text-align: left;
  }
  
  .percentage-value {
    font-size: 1.25rem;
  }
  
  .progress-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .performance-indicator {
    padding: 0.75rem;
  }
  
  .performance-item {
    font-size: 0.85rem;
  }
  
  .subject-actions {
    flex-direction: column;
  }
}
</style> 