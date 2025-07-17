<template>
  <BaseModal
    :model-value="modelValue"
    title="Confirm Delete"
    size="sm"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div class="delete-confirm">
      <!-- Warning Icon -->
      <div class="warning-icon">
        <i class="bi bi-exclamation-triangle-fill text-warning"></i>
      </div>

      <!-- Warning Message -->
      <div class="warning-message">
        <h6 class="text-danger mb-2">Are you sure you want to delete this item?</h6>
        <p class="text-muted mb-0">
          {{ message || 'This action cannot be undone. Please confirm your choice.' }}
        </p>
      </div>

      <!-- Item Details (if provided) -->
      <div v-if="itemDetails" class="item-details glass mt-3">
        <div class="item-info">
          <template v-for="(value, key) in itemDetails" :key="key">
            <div class="item-row">
              <span class="item-label">{{ key }}:</span>
              <span class="item-value">{{ value }}</span>
            </div>
          </template>
        </div>
      </div>

      <!-- Cascade Warning -->
      <div v-if="cascadeWarning" class="cascade-warning glass mt-3">
        <div class="d-flex align-items-start">
          <i class="bi bi-info-circle text-info me-2 mt-1"></i>
          <div>
            <small class="text-info fw-bold">Cascade Delete Warning</small>
            <p class="text-muted mb-0 small">
              {{ cascadeWarning }}
            </p>
          </div>
        </div>
      </div>

      <!-- Confirmation Input -->
      <div v-if="requireConfirmation" class="confirmation-input glass mt-3">
        <label class="form-label small text-muted">
          Type "{{ confirmationText }}" to confirm deletion:
        </label>
        <input
          type="text"
          class="form-control glass"
          v-model="confirmationInput"
          :placeholder="confirmationText"
          :class="{ 'is-invalid': showConfirmationError }"
        />
        <div v-if="showConfirmationError" class="invalid-feedback">
          Please type the confirmation text exactly as shown.
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <template #footer>
      <div class="delete-actions">
        <button
          type="button"
          class="btn btn-secondary glass"
          @click="$emit('update:modelValue', false)"
          :disabled="loading"
        >
          Cancel
        </button>
        <button
          type="button"
          class="btn btn-danger glass"
          @click="handleConfirm"
          :disabled="loading || (requireConfirmation && !isConfirmationValid)"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          <i v-else class="bi bi-trash me-2"></i>
          {{ loading ? 'Deleting...' : 'Delete' }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from './Modal.vue'

export default {
  name: 'DeleteConfirm',
  components: {
    BaseModal
  },
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    message: {
      type: String,
      default: ''
    },
    itemDetails: {
      type: Object,
      default: null
    },
    cascadeWarning: {
      type: String,
      default: ''
    },
    requireConfirmation: {
      type: Boolean,
      default: false
    },
    confirmationText: {
      type: String,
      default: 'DELETE'
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'confirm'],
  data() {
    return {
      confirmationInput: ''
    }
  },
  computed: {
    isConfirmationValid() {
      return this.confirmationInput === this.confirmationText
    },
    showConfirmationError() {
      return this.requireConfirmation && 
             this.confirmationInput.length > 0 && 
             !this.isConfirmationValid
    }
  },
  watch: {
    modelValue(newVal) {
      if (!newVal) {
        this.confirmationInput = ''
      }
    }
  },
  methods: {
    handleConfirm() {
      if (this.requireConfirmation && !this.isConfirmationValid) {
        return
      }
      
      this.$emit('confirm')
    }
  }
}
</script>

<style scoped>
.delete-confirm {
  text-align: center;
}

.warning-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.warning-message {
  margin-bottom: 1rem;
}

.item-details {
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: left;
}

.item-info {
  max-height: 200px;
  overflow-y: auto;
}

.item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.item-row:last-child {
  border-bottom: none;
}

.item-label {
  font-weight: 600;
  color: #adb5bd;
  text-transform: capitalize;
}

.item-value {
  color: #f8f9fa;
  font-weight: 500;
}

.cascade-warning {
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: left;
}

.confirmation-input {
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: left;
}

.delete-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  align-items: center;
}

.delete-actions .btn {
  min-width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .delete-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .delete-actions .btn {
    width: 100%;
  }
  
  .item-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}

/* Scrollbar styling for item details */
.item-info::-webkit-scrollbar {
  width: 4px;
}

.item-info::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.item-info::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.item-info::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style> 