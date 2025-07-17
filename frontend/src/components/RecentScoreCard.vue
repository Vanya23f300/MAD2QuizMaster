<template>
  <div class="recent-score-card glass">
    <div class="score-header">
      <div class="quiz-info">
        <h6 class="quiz-title text-light mb-1">{{ score.quizTitle }}</h6>
        <span class="quiz-subject text-secondary">{{ score.subject }}</span>
      </div>
      <div class="score-badge" :class="scoreClass">
        {{ score.percentage }}%
      </div>
    </div>
    
    <div class="score-details">
      <div class="detail-row">
        <div class="detail-item">
          <i class="bi bi-check-circle text-success me-2"></i>
          <span class="text-light">{{ score.correctAnswers }}</span>
          <span class="text-secondary">correct</span>
        </div>
        <div class="detail-item">
          <i class="bi bi-x-circle text-danger me-2"></i>
          <span class="text-light">{{ score.incorrectAnswers }}</span>
          <span class="text-secondary">incorrect</span>
        </div>
      </div>
      
      <div class="detail-row">
        <div class="detail-item">
          <i class="bi bi-clock text-primary me-2"></i>
          <span class="text-light">{{ score.timeTaken }}</span>
          <span class="text-secondary">taken</span>
        </div>
        <div class="detail-item">
          <i class="bi bi-calendar text-secondary me-2"></i>
          <span class="text-secondary">{{ formattedDate }}</span>
        </div>
      </div>
    </div>
    
    <div v-if="score.feedback" class="feedback-section">
      <div class="feedback-header">
        <i class="bi bi-lightbulb text-warning me-2"></i>
        <span class="text-light">Performance Insights</span>
      </div>
      <p class="feedback-text text-secondary">{{ score.feedback }}</p>
    </div>
    
    <div class="score-actions">
      <button 
        class="btn btn-outline-primary btn-sm"
        @click="$emit('view-details', score.id)"
      >
        <i class="bi bi-eye me-1"></i>View Details
      </button>
      <button 
        class="btn btn-outline-secondary btn-sm ms-2"
        @click="$emit('retake-quiz', score.quizId)"
      >
        <i class="bi bi-arrow-clockwise me-1"></i>Retake
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecentScoreCard',
  props: {
    score: {
      type: Object,
      required: true,
      default: () => ({
        id: 1,
        quizId: 1,
        quizTitle: 'JavaScript Basics',
        subject: 'Web Development',
        percentage: 85,
        correctAnswers: 17,
        incorrectAnswers: 3,
        totalQuestions: 20,
        timeTaken: '25 min',
        completedAt: '2024-01-10T14:30:00',
        feedback: 'Great performance! You showed strong understanding of JavaScript fundamentals. Consider practicing more on async functions.'
      })
    }
  },
  computed: {
    scoreClass() {
      const percentage = this.score.percentage
      if (percentage >= 90) return 'score-excellent'
      if (percentage >= 80) return 'score-good'
      if (percentage >= 70) return 'score-average'
      if (percentage >= 60) return 'score-below-average'
      return 'score-poor'
    },
    formattedDate() {
      const date = new Date(this.score.completedAt)
      const now = new Date()
      const diffTime = Math.abs(now - date)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays === 1) return 'Yesterday'
      if (diffDays < 7) return `${diffDays} days ago`
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.recent-score-card {
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

.recent-score-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px 0 rgba(0,0,0,0.25);
  background: rgba(35, 39, 43, 0.7);
}

.score-header {
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

.score-badge {
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-weight: 700;
  font-size: 1.1rem;
  min-width: 60px;
  text-align: center;
}

.score-details {
  margin-bottom: 1.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-item {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.detail-item span:first-of-type {
  margin-right: 0.25rem;
  font-weight: 600;
}

.feedback-section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(255, 193, 7, 0.1);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

.feedback-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
}

.feedback-text {
  font-size: 0.85rem;
  line-height: 1.4;
  margin-bottom: 0;
}

.score-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: auto;
}

.score-actions .btn {
  flex: 1;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Score-specific styling */
.score-excellent {
  background: rgba(25, 135, 84, 0.2);
  color: #198754;
  border: 1px solid rgba(25, 135, 84, 0.3);
}

.score-good {
  background: rgba(13, 110, 253, 0.2);
  color: #0D6EFD;
  border: 1px solid rgba(13, 110, 253, 0.3);
}

.score-average {
  background: rgba(255, 193, 7, 0.2);
  color: #FFC107;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.score-below-average {
  background: rgba(220, 53, 69, 0.2);
  color: #DC3545;
  border: 1px solid rgba(220, 53, 69, 0.3);
}

.score-poor {
  background: rgba(108, 117, 125, 0.2);
  color: #6C757D;
  border: 1px solid rgba(108, 117, 125, 0.3);
}

/* Animation for score reveal */
.recent-score-card {
  animation: score-reveal 0.6s ease-out;
}

@keyframes score-reveal {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .recent-score-card {
    padding: 1.25rem;
  }
  
  .score-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .score-badge {
    margin-top: 0.5rem;
    font-size: 1rem;
    padding: 0.4rem 0.8rem;
  }
  
  .detail-row {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .detail-item {
    font-size: 0.85rem;
  }
  
  .feedback-section {
    padding: 0.75rem;
  }
  
  .feedback-text {
    font-size: 0.8rem;
  }
  
  .score-actions {
    flex-direction: column;
  }
}
</style> 