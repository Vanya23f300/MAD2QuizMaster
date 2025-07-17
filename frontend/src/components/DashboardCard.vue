<template>
  <div class="dashboard-card glass" :class="cardClass">
    <div class="card-header d-flex align-items-center justify-content-between mb-3">
      <h5 class="card-title text-light mb-0">{{ title }}</h5>
      <div v-if="icon" class="card-icon">
        <i :class="icon" class="text-primary"></i>
      </div>
    </div>
    <div class="card-body p-0">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardCard',
  props: {
    title: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      default: ''
    },
    cardClass: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.dashboard-card {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
}

.dashboard-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 40px 0 rgba(0,0,0,0.3);
}

.card-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.card-title {
  font-weight: 600;
  font-size: 1.1rem;
}
</style> 