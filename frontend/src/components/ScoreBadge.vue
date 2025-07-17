<template>
  <div class="score-badge" :class="scoreClass">
    <div class="score-content">
      <div class="score-value">{{ displayScore }}</div>
      <div class="score-label">{{ label }}</div>
    </div>
    <div v-if="showTrend" class="score-trend">
      <i :class="trendIcon" :style="{ color: trendColor }"></i>
      <span class="trend-text" :style="{ color: trendColor }">{{ trendValue }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScoreBadge',
  props: {
    score: {
      type: Number,
      required: true,
      default: 0
    },
    maxScore: {
      type: Number,
      default: 100
    },
    label: {
      type: String,
      default: 'Score'
    },
    showTrend: {
      type: Boolean,
      default: false
    },
    trendValue: {
      type: String,
      default: ''
    },
    trendDirection: {
      type: String,
      default: 'up' // up, down, neutral
    }
  },
  computed: {
    percentage() {
      return (this.score / this.maxScore) * 100
    },
    displayScore() {
      return `${this.score}/${this.maxScore}`
    },
    scoreClass() {
      const percentage = this.percentage
      if (percentage >= 90) return 'score-excellent'
      if (percentage >= 80) return 'score-good'
      if (percentage >= 70) return 'score-average'
      if (percentage >= 60) return 'score-below-average'
      return 'score-poor'
    },
    trendIcon() {
      const iconMap = {
        'up': 'bi bi-arrow-up',
        'down': 'bi bi-arrow-down',
        'neutral': 'bi bi-dash'
      }
      return iconMap[this.trendDirection] || 'bi bi-dash'
    },
    trendColor() {
      const colorMap = {
        'up': '#198754', // Success green
        'down': '#DC3545', // Danger red
        'neutral': '#6C757D' // Secondary gray
      }
      return colorMap[this.trendDirection] || '#6C757D'
    }
  }
}
</script>

<style scoped>
.score-badge {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 20px 0 rgba(0,0,0,0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  min-width: 140px;
}

.score-badge:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px 0 rgba(0,0,0,0.2);
  background: rgba(35, 39, 43, 0.7);
}

.score-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.score-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #F8F9FA;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.score-label {
  font-size: 0.8rem;
  color: #ADB5BD;
  font-weight: 500;
  line-height: 1.2;
}

.score-trend {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 0.75rem;
}

.score-trend i {
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.trend-text {
  font-size: 0.7rem;
  font-weight: 600;
  line-height: 1;
}

/* Score-specific styling */
.score-excellent {
  border-color: rgba(25, 135, 84, 0.4);
  background: rgba(25, 135, 84, 0.1);
}

.score-good {
  border-color: rgba(13, 110, 253, 0.4);
  background: rgba(13, 110, 253, 0.1);
}

.score-average {
  border-color: rgba(255, 193, 7, 0.4);
  background: rgba(255, 193, 7, 0.1);
}

.score-below-average {
  border-color: rgba(220, 53, 69, 0.4);
  background: rgba(220, 53, 69, 0.1);
}

.score-poor {
  border-color: rgba(108, 117, 125, 0.4);
  background: rgba(108, 117, 125, 0.1);
}

/* Animation for score reveal */
.score-badge {
  animation: score-reveal 0.6s ease-out;
}

@keyframes score-reveal {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .score-badge {
    padding: 0.75rem;
    min-width: 120px;
  }
  
  .score-value {
    font-size: 1.1rem;
  }
  
  .score-label {
    font-size: 0.75rem;
  }
  
  .score-trend i {
    font-size: 0.9rem;
  }
  
  .trend-text {
    font-size: 0.65rem;
  }
}
</style> 