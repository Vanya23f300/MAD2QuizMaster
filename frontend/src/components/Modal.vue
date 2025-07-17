<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="modal-overlay"
        @click="handleBackdropClick"
        @keydown.esc="handleEscape"
        tabindex="-1"
        ref="modalRef"
      >
        <div class="modal-container" @click.stop>
          <!-- Modal Header -->
          <div class="modal-header glass">
            <div class="d-flex align-items-center justify-content-between w-100">
              <h5 class="modal-title mb-0">
                <slot name="header">
                  {{ title }}
                </slot>
              </h5>
              <button
                type="button"
                class="btn-close btn-close-white"
                @click="$emit('update:modelValue', false)"
                aria-label="Close"
              ></button>
            </div>
          </div>

          <!-- Modal Body -->
          <div class="modal-body glass">
            <slot></slot>
          </div>

          <!-- Modal Footer -->
          <div v-if="$slots.footer" class="modal-footer glass">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
export default {
  name: 'BaseModal',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: ''
    },
    closeOnBackdrop: {
      type: Boolean,
      default: true
    },
    closeOnEscape: {
      type: Boolean,
      default: true
    },
    size: {
      type: String,
      default: 'md',
      validator: value => ['sm', 'md', 'lg', 'xl'].includes(value)
    },
    centered: {
      type: Boolean,
      default: true
    },
    scrollable: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'close'],
  mounted() {
    if (this.modelValue) {
      this.handleModalOpen()
    }
  },
  watch: {
    modelValue(newVal) {
      if (newVal) {
        this.handleModalOpen()
      } else {
        this.handleModalClose()
      }
    }
  },
  methods: {
    handleModalOpen() {
      // Prevent body scroll
      document.body.style.overflow = 'hidden'
      document.body.style.paddingRight = this.getScrollbarWidth() + 'px'
      
      // Focus modal for keyboard navigation
      this.$nextTick(() => {
        if (this.$refs.modalRef) {
          this.$refs.modalRef.focus()
        }
      })
    },
    handleModalClose() {
      // Restore body scroll
      document.body.style.overflow = ''
      document.body.style.paddingRight = ''
      
      this.$emit('close')
    },
    handleBackdropClick() {
      if (this.closeOnBackdrop) {
        this.$emit('update:modelValue', false)
      }
    },
    handleEscape() {
      if (this.closeOnEscape) {
        this.$emit('update:modelValue', false)
      }
    },
    getScrollbarWidth() {
      const outer = document.createElement('div')
      outer.style.visibility = 'hidden'
      outer.style.overflow = 'scroll'
      document.body.appendChild(outer)
      
      const inner = document.createElement('div')
      outer.appendChild(inner)
      
      const scrollbarWidth = outer.offsetWidth - inner.offsetWidth
      outer.parentNode.removeChild(outer)
      
      return scrollbarWidth
    }
  },
  beforeUnmount() {
    // Clean up body styles
    document.body.style.overflow = ''
    document.body.style.paddingRight = ''
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 1rem;
  outline: none;
}

.modal-container {
  background: rgba(35, 39, 43, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.modal-container[data-size="sm"] {
  width: 400px;
}

.modal-container[data-size="md"] {
  width: 600px;
  min-width: 600px;
}

.modal-container[data-size="lg"] {
  width: 800px;
  min-width: 800px;
}

.modal-container[data-size="xl"] {
  width: 1200px;
  min-width: 1200px;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  color: #f8f9fa;
  font-weight: 600;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  color: #f8f9fa;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: all 0.2s ease;
  opacity: 0.7;
}

.btn-close:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.1);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(-20px);
}

.modal-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(-20px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 0.5rem;
  }
  
  .modal-container {
    width: 100% !important;
    max-width: 100%;
    max-height: 100%;
    border-radius: 0;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem;
  }
}

/* Scrollbar styling for modal body */
.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style> 