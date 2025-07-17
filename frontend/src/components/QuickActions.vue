<template>
  <div class="quick-actions">
    <div class="quick-actions-header mb-4">
      <h5 class="text-light mb-2">Quick Actions</h5>
      <p class="text-secondary mb-0">Common tasks to get you started</p>
    </div>
    <div class="actions-grid">
      <button
        v-for="action in actions"
        :key="action.id"
        class="action-btn glass"
        @click="$emit('action-click', action.id)"
      >
        <div class="action-icon">
          <i :class="action.icon"></i>
        </div>
        <div class="action-label">{{ action.label }}</div>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuickActions',
  props: {
    actions: {
      type: Array,
      default: () => [
        { id: 'manage-subjects', label: 'Manage Subjects', icon: 'bi bi-book' },
        { id: 'manage-chapters', label: 'Manage Chapters', icon: 'bi bi-collection' },
        { id: 'manage-questions', label: 'Manage Questions', icon: 'bi bi-question-circle' },
        { id: 'manage-quizzes', label: 'Manage Quizzes', icon: 'bi bi-file-earmark-text' }
      ]
    }
  }
}
</script>

<style scoped>
.quick-actions {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 40px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  padding: 2rem;
}

.quick-actions-header h5 {
  font-size: 1.25rem;
  font-weight: 600;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.action-btn {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 20px 0 rgba(0,0,0,0.15);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.action-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px 0 rgba(0,0,0,0.3);
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}

.action-icon {
  font-size: 2rem;
  color: #0D6EFD;
  margin-bottom: 1rem;
  transition: transform 0.2s ease;
}

.action-btn:hover .action-icon {
  transform: scale(1.1);
}

.action-label {
  font-size: 0.95rem;
  color: #F8F9FA;
  font-weight: 500;
  line-height: 1.3;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .quick-actions {
    padding: 1.5rem;
  }
  
  .actions-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }
  
  .action-btn {
    padding: 1.25rem;
    min-height: 100px;
  }
  
  .action-icon {
    font-size: 1.75rem;
    margin-bottom: 0.75rem;
  }
  
  .action-label {
    font-size: 0.9rem;
  }
}
</style> 