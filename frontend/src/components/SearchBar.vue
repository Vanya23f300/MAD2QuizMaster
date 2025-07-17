<template>
  <div class="search-container position-relative">
    <div class="input-group">
      <span class="input-group-text bg-transparent border-0">
        <i class="bi bi-search text-secondary"></i>
      </span>
      <input
        type="text"
        class="form-control bg-dark text-light border-0"
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

.form-control {
  background: rgba(35, 39, 43, 0.8) !important;
  color: #F8F9FA !important;
  border: 1.5px solid #343A40 !important;
  border-radius: 0.75rem !important;
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