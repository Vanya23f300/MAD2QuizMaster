<template>
  <BaseModal
    :model-value="modelValue"
    :title="title"
    :size="size"
    @update:model-value="$emit('update:modelValue', $event)"
    @close="handleClose"
  >
    <form @submit.prevent="handleSubmit" class="form-modal">
      <!-- Form Content -->
      <div class="form-content">
        <slot></slot>
      </div>
    </form>
    
    <!-- Form Actions -->
    <template #footer>
      <div class="form-actions">
        <button
          type="button"
          class="btn btn-secondary glass"
          @click="handleCancel"
          :disabled="loading"
        >
          {{ cancelText }}
        </button>
        <button
          type="submit"
          class="btn btn-primary glass"
          :disabled="loading || !isValid"
          @click="handleSubmit"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          <i v-else :class="submitIcon" class="me-2"></i>
          {{ submitText }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from './Modal.vue'

export default {
  name: 'FormModal',
  components: {
    BaseModal
  },
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    size: {
      type: String,
      default: 'md',
      validator: value => ['sm', 'md', 'lg', 'xl'].includes(value)
    },
    loading: {
      type: Boolean,
      default: false
    },
    isValid: {
      type: Boolean,
      default: true
    },
    submitText: {
      type: String,
      default: 'Save'
    },
    cancelText: {
      type: String,
      default: 'Cancel'
    },
    submitIcon: {
      type: String,
      default: 'bi bi-check-circle'
    },
    confirmClose: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'submit', 'cancel', 'close'],
  methods: {
    handleSubmit() {
      if (this.isValid && !this.loading) {
        this.$emit('submit')
      }
    },
    handleCancel() {
      this.$emit('cancel')
      this.$emit('update:modelValue', false)
    },
    handleClose() {
      if (this.confirmClose && this.hasChanges) {
        // Show confirmation dialog
        if (confirm('You have unsaved changes. Are you sure you want to close?')) {
          this.$emit('close')
          this.$emit('update:modelValue', false)
        }
      } else {
        this.$emit('close')
        this.$emit('update:modelValue', false)
      }
    }
  }
}
</script>

<style scoped>
.form-modal {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.form-content {
  flex: 1;
  overflow-y: auto;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  align-items: center;
}

.form-actions .btn {
  min-width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Loading state styles */
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-border {
  width: 1rem;
  height: 1rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .form-actions .btn {
    width: 100%;
  }
}
</style> 