<template>
  <div class="progress-ring-container">
    <div class="progress-ring" :style="ringStyle">
      <svg class="progress-ring-svg" :width="size" :height="size">
        <circle
          class="progress-ring-bg"
          :stroke-width="strokeWidth"
          :r="radius"
          :cx="center"
          :cy="center"
        />
        <circle
          class="progress-ring-progress"
          :stroke-width="strokeWidth"
          :r="radius"
          :cx="center"
          :cy="center"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="dashOffset"
          :style="{ stroke: progressColor }"
        />
      </svg>
      <div class="progress-content">
        <div class="progress-value">{{ displayValue }}</div>
        <div class="progress-label">{{ label }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProgressRing',
  props: {
    value: {
      type: Number,
      required: true,
      default: 0
    },
    max: {
      type: Number,
      default: 100
    },
    size: {
      type: Number,
      default: 120
    },
    strokeWidth: {
      type: Number,
      default: 8
    },
    label: {
      type: String,
      default: 'Progress'
    },
    showPercentage: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    radius() {
      return (this.size - this.strokeWidth) / 2
    },
    center() {
      return this.size / 2
    },
    circumference() {
      return 2 * Math.PI * this.radius
    },
    progress() {
      return Math.min(Math.max(this.value / this.max, 0), 1)
    },
    dashOffset() {
      return this.circumference * (1 - this.progress)
    },
    displayValue() {
      if (this.showPercentage) {
        return `${Math.round(this.progress * 100)}%`
      }
      return this.value
    },
    progressColor() {
      const percentage = this.progress * 100
      if (percentage >= 80) return '#198754' // Success green
      if (percentage >= 60) return '#0D6EFD' // Primary blue
      if (percentage >= 40) return '#FFC107' // Warning yellow
      return '#DC3545' // Danger red
    },
    ringStyle() {
      return {
        width: `${this.size}px`,
        height: `${this.size}px`
      }
    }
  }
}
</script>

<style scoped>
.progress-ring-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.progress-ring {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.progress-ring-svg {
  transform: rotate(-90deg);
}

.progress-ring-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.1);
}

.progress-ring-progress {
  fill: none;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.5s ease-in-out;
}

.progress-content {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.progress-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #F8F9FA;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.progress-label {
  font-size: 0.8rem;
  color: #ADB5BD;
  font-weight: 500;
  line-height: 1.2;
}

/* Animation for initial load */
.progress-ring-progress {
  animation: progress-animation 1s ease-out;
}

@keyframes progress-animation {
  from {
    stroke-dashoffset: 100%;
  }
  to {
    stroke-dashoffset: var(--final-dashoffset);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .progress-value {
    font-size: 1.25rem;
  }
  
  .progress-label {
    font-size: 0.75rem;
  }
}
</style> 