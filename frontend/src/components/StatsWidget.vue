<template>
  <div class="stats-widget glass">
    <div class="stats-header d-flex align-items-center justify-content-between mb-4">
      <div class="stats-icon" :class="iconClass">
        <i :class="icon"></i>
      </div>
      <div class="stats-trend" v-if="trend">
        <span :class="trendClass">{{ trend }}</span>
      </div>
    </div>
    <div class="stats-content">
      <div class="stats-value text-light display-5 fw-bold">{{ displayValue }}</div>
      <div class="stats-label text-secondary">{{ label }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatsWidget',
  props: {
    value: {
      type: Number,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      required: true
    },
    color: {
      type: String,
      default: 'primary'
    },
    trend: {
      type: String,
      default: ''
    },
    trendDirection: {
      type: String,
      default: 'up'
    }
  },
  computed: {
    displayValue() {
      return this.value.toLocaleString()
    },
    iconClass() {
      return `text-${this.color}`
    },
    trendClass() {
      const direction = this.trendDirection === 'up' ? 'text-success' : 'text-danger'
      return `${direction} small`
    }
  }
}
</script>

<style scoped>
.stats-widget {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 40px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  padding: 2rem;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.stats-widget:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 50px 0 rgba(0,0,0,0.35);
  background: rgba(35, 39, 43, 0.7);
}

.stats-icon {
  font-size: 2.5rem;
  opacity: 0.8;
  transition: transform 0.2s ease;
}

.stats-widget:hover .stats-icon {
  transform: scale(1.1);
}

.stats-value {
  font-size: 3rem;
  line-height: 1;
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.stats-label {
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.3;
}

.stats-trend {
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  background: rgba(255, 255, 255, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .stats-widget {
    padding: 1.5rem;
  }
  
  .stats-icon {
    font-size: 2rem;
  }
  
  .stats-value {
    font-size: 2.5rem;
  }
  
  .stats-label {
    font-size: 0.9rem;
  }
}
</style> 