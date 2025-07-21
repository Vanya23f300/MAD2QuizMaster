<template>
  <!-- Bootstrap Modal -->
  <div 
    class="modal fade" 
    :id="modalId"
    tabindex="-1" 
    aria-hidden="true"
    ref="modalElement"
  >
    <div class="modal-dialog modal-sm modal-dialog-centered">
      <div class="modal-content bg-dark">
        <div class="modal-header border-secondary">
          <h5 class="modal-title text-light">
            <i class="bi bi-exclamation-triangle-fill text-warning me-2"></i>
            Confirm Delete
          </h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        
        <div class="modal-body text-center">
          <div class="delete-confirm">
            <!-- Warning Message -->
            <div class="warning-message mb-3">
              <h6 class="text-danger mb-2">Are you sure you want to delete this {{ itemType }}?</h6>
              <p class="text-muted mb-0" v-if="itemName">
                <strong>"{{ itemName }}"</strong>
              </p>
              <p class="text-muted mb-0">
                This action cannot be undone.
              </p>
            </div>
          </div>
        </div>
        
        <div class="modal-footer border-secondary">
          <button
            type="button"
            class="btn btn-outline-secondary"
            data-bs-dismiss="modal"
            :disabled="loading"
          >
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-danger"
            @click="handleConfirm"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-trash me-2"></i>
            {{ loading ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'

export default {
  name: 'DeleteConfirm',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    itemName: {
      type: String,
      default: ''
    },
    itemType: {
      type: String,
      default: 'item'
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['confirm', 'cancel'],
  data() {
    return {
      modal: null,
      modalId: `deleteModal_${Math.random().toString(36).substr(2, 9)}`
    }
  },
  mounted() {
    this.modal = new Modal(this.$refs.modalElement)
    this.$refs.modalElement.addEventListener('hidden.bs.modal', () => {
      this.$emit('cancel')
    })
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.modal.show()
      } else {
        this.modal.hide()
      }
    }
  },
  methods: {
    handleConfirm() {
      this.$emit('confirm')
      this.modal.hide()
    }
  },
  beforeUnmount() {
    if (this.modal) {
      this.modal.dispose()
    }
  }
}
</script>

<style scoped>
.warning-message {
  margin-bottom: 1rem;
}

.modal-content {
  background: rgba(35, 39, 43, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-border {
  width: 1rem;
  height: 1rem;
}
</style>