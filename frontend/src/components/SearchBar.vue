<template>
  <div class="search-container position-relative">
    <div class="input-group">
      <span class="input-group-text search-icon-glass">
        <i class="bi bi-search"></i>
      </span>
      <input
        type="text"
        class="form-control search-input-glass"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        @focus="showSuggestions = true"
        @blur="handleBlur"
      />
    </div>
    <div v-if="showSuggestions && suggestions.length > 0" class="suggestions-dropdown glass">
      <div
        v-for="suggestion in suggestions"
        :key="suggestion"
        class="suggestion-item"
        @click="selectSuggestion(suggestion)"
      >
        {{ suggestion }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    modelValue: String,
    placeholder: {
      type: String,
      default: 'Search...'
    },
    suggestions: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      showSuggestions: false
    }
  },
  methods: {
    selectSuggestion(suggestion) {
      this.$emit('update:modelValue', suggestion)
      this.showSuggestions = false
    },
    handleBlur() {
      setTimeout(() => {
        this.showSuggestions = false
      }, 200)
    }
  }
}
</script>

<style scoped>
.search-container {
  position: relative;
}

.search-icon-glass {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-right: none !important;
  border-radius: 12px 0 0 12px !important;
  backdrop-filter: blur(10px);
  color: rgba(255, 255, 255, 0.7) !important;
}

.search-input-glass {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-left: none !important;
  border-radius: 0 12px 12px 0 !important;
  color: #ffffff !important;
  backdrop-filter: blur(10px);
}

.search-input-glass:focus {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: rgba(74, 85, 104, 0.6) !important;
  box-shadow: 0 0 0 0.25rem rgba(74, 85, 104, 0.25) !important;
  color: #ffffff !important;
}

.search-input-glass::placeholder {
  color: rgba(255, 255, 255, 0.5) !important;
}

.form-control {
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-control:focus {
  border-color: #0D6EFD !important;
  box-shadow: 0 0 0 2px rgba(13, 110, 253, 0.15);
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(35, 39, 43, 0.8);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  margin-top: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
}

.suggestion-item {
  padding: 0.75rem 1rem;
  color: #F8F9FA;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggestion-item:hover {
  background: rgba(13, 110, 253, 0.1);
}
</style> 