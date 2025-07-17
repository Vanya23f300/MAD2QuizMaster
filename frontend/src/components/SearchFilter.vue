<template>
  <div class="search-filter-container glass">
    <div class="filter-header">
      <h6 class="filter-title mb-0">
        <i class="bi bi-funnel me-2"></i>
        Filters
      </h6>
      <button
        v-if="hasActiveFilters"
        type="button"
        class="btn btn-sm btn-outline-secondary glass"
        @click="clearAllFilters"
      >
        <i class="bi bi-x-circle me-1"></i>
        Clear All
      </button>
    </div>

    <div class="filter-content">
      <!-- Search Input -->
      <div class="filter-group">
        <label class="form-label small text-muted">Search</label>
        <div class="input-group">
          <span class="input-group-text glass">
            <i class="bi bi-search"></i>
          </span>
          <input
            type="text"
            class="form-control glass"
            placeholder="Search..."
            v-model="localSearchQuery"
            @input="handleSearchChange"
          />
        </div>
      </div>

      <!-- Filter Controls -->
      <div class="filter-controls">
        <div
          v-for="filter in filters"
          :key="filter.key"
          class="filter-group"
        >
          <label class="form-label small text-muted">
            {{ filter.label }}
          </label>

          <!-- Select Filter -->
          <select
            v-if="filter.type === 'select'"
            class="form-select glass"
            v-model="localFilterValues[filter.key]"
            @change="handleFilterChange"
          >
            <option value="">All {{ filter.label }}</option>
            <option
              v-for="option in filter.options"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>

          <!-- Multi-Select Filter -->
          <div
            v-else-if="filter.type === 'multi-select'"
            class="multi-select-container"
          >
            <div class="selected-items" v-if="getSelectedItems(filter.key).length > 0">
              <span
                v-for="item in getSelectedItems(filter.key)"
                :key="item.value"
                class="selected-item glass"
              >
                {{ item.label }}
                <button
                  type="button"
                  class="btn-remove"
                  @click="removeSelectedItem(filter.key, item.value)"
                >
                  <i class="bi bi-x"></i>
                </button>
              </span>
            </div>
            <select
              class="form-select glass"
              @change="handleMultiSelectChange($event, filter.key)"
            >
              <option value="">Add {{ filter.label }}</option>
              <option
                v-for="option in getAvailableOptions(filter.key)"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>

          <!-- Date Range Filter -->
          <div
            v-else-if="filter.type === 'date-range'"
            class="date-range-container"
          >
            <div class="row">
              <div class="col-6">
                <input
                  type="date"
                  class="form-control glass"
                  v-model="localFilterValues[filter.key].start"
                  @change="handleFilterChange"
                />
              </div>
              <div class="col-6">
                <input
                  type="date"
                  class="form-control glass"
                  v-model="localFilterValues[filter.key].end"
                  @change="handleFilterChange"
                />
              </div>
            </div>
          </div>

          <!-- Boolean Filter -->
          <div
            v-else-if="filter.type === 'boolean'"
            class="boolean-filter"
          >
            <div class="form-check">
              <input
                type="checkbox"
                class="form-check-input"
                :id="`filter-${filter.key}`"
                v-model="localFilterValues[filter.key]"
                @change="handleFilterChange"
              />
              <label class="form-check-label" :for="`filter-${filter.key}`">
                {{ filter.label }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Filters Display -->
      <div v-if="hasActiveFilters" class="active-filters">
        <div class="active-filters-header">
          <small class="text-muted">Active Filters:</small>
        </div>
        <div class="active-filters-list">
          <span
            v-for="filter in activeFiltersList"
            :key="filter.key"
            class="active-filter glass"
          >
            {{ filter.label }}: {{ filter.displayValue }}
            <button
              type="button"
              class="btn-remove"
              @click="clearFilter(filter.key)"
            >
              <i class="bi bi-x"></i>
            </button>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchFilter',
  props: {
    searchQuery: {
      type: String,
      default: ''
    },
    filterValues: {
      type: Object,
      default: () => ({})
    },
    filters: {
      type: Array,
      required: true
    }
  },
  emits: ['search-change', 'filter-change', 'clear-all'],
  data() {
    return {
      localSearchQuery: this.searchQuery,
      localFilterValues: { ...this.filterValues }
    }
  },
  computed: {
    hasActiveFilters() {
      return this.localSearchQuery || 
             Object.values(this.localFilterValues).some(value => {
               if (Array.isArray(value)) return value.length > 0
               if (typeof value === 'object') {
                 return value.start || value.end
               }
               return value !== '' && value !== null && value !== undefined
             })
    },
    activeFiltersList() {
      const activeFilters = []
      
      // Add search query if present
      if (this.localSearchQuery) {
        activeFilters.push({
          key: 'search',
          label: 'Search',
          displayValue: this.localSearchQuery
        })
      }
      
      // Add other active filters
      this.filters.forEach(filter => {
        const value = this.localFilterValues[filter.key]
        if (this.isFilterActive(filter, value)) {
          activeFilters.push({
            key: filter.key,
            label: filter.label,
            displayValue: this.getFilterDisplayValue(filter, value)
          })
        }
      })
      
      return activeFilters
    }
  },
  watch: {
    searchQuery(newVal) {
      this.localSearchQuery = newVal
    },
    filterValues: {
      handler(newVal) {
        this.localFilterValues = { ...newVal }
      },
      deep: true
    }
  },
  methods: {
    handleSearchChange() {
      this.$emit('search-change', this.localSearchQuery)
    },
    handleFilterChange() {
      this.$emit('filter-change', { ...this.localFilterValues })
    },
    handleMultiSelectChange(event, filterKey) {
      const value = event.target.value
      if (value) {
        if (!this.localFilterValues[filterKey]) {
          this.localFilterValues[filterKey] = []
        }
        this.localFilterValues[filterKey].push(value)
        this.handleFilterChange()
        event.target.value = ''
      }
    },
    getSelectedItems(filterKey) {
      const filter = this.filters.find(f => f.key === filterKey)
      const selectedValues = this.localFilterValues[filterKey] || []
      return filter.options.filter(option => selectedValues.includes(option.value))
    },
    getAvailableOptions(filterKey) {
      const filter = this.filters.find(f => f.key === filterKey)
      const selectedValues = this.localFilterValues[filterKey] || []
      return filter.options.filter(option => !selectedValues.includes(option.value))
    },
    removeSelectedItem(filterKey, value) {
      const index = this.localFilterValues[filterKey].indexOf(value)
      if (index > -1) {
        this.localFilterValues[filterKey].splice(index, 1)
        this.handleFilterChange()
      }
    },
    clearFilter(filterKey) {
      if (filterKey === 'search') {
        this.localSearchQuery = ''
        this.handleSearchChange()
      } else {
        this.$set(this.localFilterValues, filterKey, this.getDefaultValue(filterKey))
        this.handleFilterChange()
      }
    },
    clearAllFilters() {
      this.localSearchQuery = ''
      this.localFilterValues = {}
      this.$emit('clear-all')
    },
    isFilterActive(filter, value) {
      if (Array.isArray(value)) return value.length > 0
      if (typeof value === 'object') return value.start || value.end
      return value !== '' && value !== null && value !== undefined
    },
    getFilterDisplayValue(filter, value) {
      if (filter.type === 'multi-select' && Array.isArray(value)) {
        const selectedOptions = filter.options.filter(option => value.includes(option.value))
        return selectedOptions.map(option => option.label).join(', ')
      }
      if (filter.type === 'date-range' && typeof value === 'object') {
        const parts = []
        if (value.start) parts.push(`From: ${value.start}`)
        if (value.end) parts.push(`To: ${value.end}`)
        return parts.join(' ')
      }
      if (filter.type === 'select') {
        const option = filter.options.find(opt => opt.value === value)
        return option ? option.label : value
      }
      return value
    },
    getDefaultValue(filterKey) {
      const filter = this.filters.find(f => f.key === filterKey)
      if (filter.type === 'multi-select') return []
      if (filter.type === 'date-range') return { start: '', end: '' }
      if (filter.type === 'boolean') return false
      return ''
    }
  }
}
</script>

<style scoped>
.search-filter-container {
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filter-title {
  color: #f8f9fa;
  font-weight: 600;
}

.filter-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.multi-select-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.selected-items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.selected-item {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

.btn-remove {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 0;
  font-size: 0.75rem;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.btn-remove:hover {
  opacity: 1;
}

.date-range-container {
  display: flex;
  gap: 0.5rem;
}

.boolean-filter {
  display: flex;
  align-items: center;
}

.active-filters {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.active-filters-header {
  margin-bottom: 0.5rem;
}

.active-filters-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.active-filter {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .filter-controls {
    grid-template-columns: 1fr;
  }
  
  .date-range-container {
    flex-direction: column;
  }
  
  .active-filters-list {
    flex-direction: column;
  }
  
  .active-filter {
    width: 100%;
    justify-content: space-between;
  }
}
</style> 