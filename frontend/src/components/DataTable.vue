<template>
  <div class="data-table-container">
    <!-- Table Header with Search and Actions -->
    <div class="table-header glass mb-3">
      <div class="row align-items-center">
        <div class="col-md-6">
          <div class="search-container">
            <div class="input-group">
              <span class="input-group-text search-icon-container">
                <i class="bi bi-search"></i>
              </span>
              <input
                type="text"
                class="form-control"
                placeholder="Search..."
                v-model="localSearchQuery"
                @input="handleSearch"
              />
            </div>
          </div>
        </div>
        <div class="col-md-6 text-end">
          <slot name="actions"></slot>
        </div>
      </div>
    </div>

    <!-- Data Table -->
    <div class="table-responsive">
      <table class="table table-hover glass">
        <thead class="table-dark">
          <tr>
            <th
              v-for="column in columns"
              :key="column.key"
              :class="column.sortable ? 'sortable' : ''"
              @click="column.sortable ? handleSort(column.key) : null"
              :style="{ cursor: column.sortable ? 'pointer' : 'default' }"
            >
              <div class="d-flex align-items-center justify-content-between">
                <span>{{ column.label }}</span>
                <i
                  v-if="column.sortable"
                  :class="getSortIcon(column.key)"
                  class="sort-icon"
                ></i>
              </div>
            </th>
            <th class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in paginatedData"
            :key="item.id || index"
            class="table-row glass"
          >
            <td
              v-for="column in columns"
              :key="column.key"
              :class="column.class || ''"
            >
              <slot
                :name="`cell-${column.key}`"
                :item="item"
                :value="item[column.key]"
              >
                <span v-if="column.type === 'date'">
                  {{ formatDate(item[column.key]) }}
                </span>
                <span v-else-if="column.type === 'status'">
                  <span
                    :class="getStatusClass(item[column.key])"
                    class="badge"
                  >
                    {{ item[column.key] }}
                  </span>
                </span>
                <span v-else-if="column.type === 'boolean'">
                  <i
                    :class="item[column.key] ? 'bi bi-check-circle-fill text-success' : 'bi bi-x-circle-fill text-danger'"
                  ></i>
                </span>
                <span v-else>
                  {{ item[column.key] }}
                </span>
              </slot>
            </td>
            <td class="text-end">
              <div class="btn-group" role="group">
                <button
                  class="btn btn-sm btn-outline-primary glass"
                  @click="$emit('edit', item)"
                  title="Edit"
                >
                  <i class="bi bi-pencil"></i>
                </button>
                <button
                  class="btn btn-sm btn-outline-danger glass"
                  @click="$emit('delete', item)"
                  title="Delete"
                >
                  <i class="bi bi-trash"></i>
                </button>
                <slot name="actions" :item="item"></slot>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div
      v-if="filteredData.length === 0"
      class="empty-state glass text-center py-5"
    >
      <i class="bi bi-inbox display-1 text-muted"></i>
      <h5 class="mt-3 text-muted">No data found</h5>
      <p class="text-muted">
        {{ searchQuery ? 'Try adjusting your search criteria.' : 'No items available.' }}
      </p>
    </div>

    <!-- Pagination -->
    <div
      v-if="showPagination && totalPages > 1"
      class="pagination-container glass mt-3"
    >
      <nav aria-label="Table pagination">
        <ul class="pagination justify-content-center mb-0">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button
              class="page-link glass"
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
            >
              <i class="bi bi-chevron-left"></i>
            </button>
          </li>
          
          <li
            v-for="page in visiblePages"
            :key="page"
            class="page-item"
            :class="{ active: page === currentPage }"
          >
            <button
              class="page-link glass"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
          </li>
          
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button
              class="page-link glass"
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
            >
              <i class="bi bi-chevron-right"></i>
            </button>
          </li>
        </ul>
      </nav>
      
      <div class="pagination-info text-center mt-2">
        <small class="text-muted">
          Showing {{ startIndex + 1 }}-{{ endIndex }} of {{ filteredData.length }} items
        </small>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    data: {
      type: Array,
      required: true,
      default: () => []
    },
    columns: {
      type: Array,
      required: true
    },
    searchQuery: {
      type: String,
      default: ''
    },
    sortBy: {
      type: String,
      default: ''
    },
    sortOrder: {
      type: String,
      default: 'asc',
      validator: value => ['asc', 'desc'].includes(value)
    },
    currentPage: {
      type: Number,
      default: 1
    },
    itemsPerPage: {
      type: Number,
      default: 10
    },
    showPagination: {
      type: Boolean,
      default: true
    },
    showAddButton: {
      type: Boolean,
      default: true
    }
  },
  emits: ['search', 'sort', 'page-change', 'add', 'edit', 'delete'],
  data() {
    return {
      localSearchQuery: this.searchQuery,
      localSortBy: this.sortBy,
      localSortOrder: this.sortOrder,
      localCurrentPage: this.currentPage
    }
  },
  computed: {
    filteredData() {
      let filtered = [...this.data]
      
      // Apply search filter
      if (this.localSearchQuery) {
        const query = this.localSearchQuery.toLowerCase()
        filtered = filtered.filter(item => {
          return this.columns.some(column => {
            const value = item[column.key]
            if (value != null) {
              return value.toString().toLowerCase().includes(query)
            }
            return false
          })
        })
      }
      
      // Apply sorting
      if (this.localSortBy) {
        filtered.sort((a, b) => {
          const aVal = a[this.localSortBy]
          const bVal = b[this.localSortBy]
          
          if (aVal == null && bVal == null) return 0
          if (aVal == null) return 1
          if (bVal == null) return -1
          
          let comparison = 0
          if (typeof aVal === 'string' && typeof bVal === 'string') {
            comparison = aVal.localeCompare(bVal)
          } else {
            comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0
          }
          
          return this.localSortOrder === 'desc' ? -comparison : comparison
        })
      }
      
      return filtered
    },
    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage)
    },
    paginatedData() {
      const start = (this.localCurrentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredData.slice(start, end)
    },
    startIndex() {
      return (this.localCurrentPage - 1) * this.itemsPerPage
    },
    endIndex() {
      return Math.min(this.startIndex + this.itemsPerPage, this.filteredData.length)
    },
    visiblePages() {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, this.localCurrentPage - Math.floor(maxVisible / 2))
      let end = Math.min(this.totalPages, start + maxVisible - 1)
      
      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1)
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    }
  },
  watch: {
    searchQuery(newVal) {
      this.localSearchQuery = newVal
    },
    sortBy(newVal) {
      this.localSortBy = newVal
    },
    sortOrder(newVal) {
      this.localSortOrder = newVal
    },
    currentPage(newVal) {
      this.localCurrentPage = newVal
    }
  },
  methods: {
    handleSearch() {
      this.$emit('search', this.localSearchQuery)
      this.localCurrentPage = 1
    },
    handleSort(key) {
      if (this.localSortBy === key) {
        this.localSortOrder = this.localSortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        this.localSortBy = key
        this.localSortOrder = 'asc'
      }
      this.$emit('sort', { key: this.localSortBy, order: this.localSortOrder })
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.localCurrentPage = page
        this.$emit('page-change', page)
      }
    },
    getSortIcon(key) {
      if (this.localSortBy !== key) {
        return 'bi bi-arrow-down-up text-muted'
      }
      return this.localSortOrder === 'asc' 
        ? 'bi bi-arrow-up text-primary' 
        : 'bi bi-arrow-down text-primary'
    },
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString()
    },
    getStatusClass(status) {
      const statusClasses = {
        active: 'bg-success',
        inactive: 'bg-secondary',
        pending: 'bg-warning',
        completed: 'bg-info',
        failed: 'bg-danger'
      }
      return statusClasses[status?.toLowerCase()] || 'bg-secondary'
    }
  }
}
</script>

<style scoped>
.data-table-container {
  width: 100%;
}

.table-header {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.search-container .input-group {
  max-width: 300px;
}

.search-icon-container {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-right: none !important;
  border-radius: 12px 0 0 12px !important;
  backdrop-filter: blur(10px);
  color: rgba(255, 255, 255, 0.7) !important;
}

.search-container .form-control {
  border-left: none !important;
  border-radius: 0 12px 12px 0 !important;
}

.table {
  margin-bottom: 0;
  border-radius: 0.5rem;
  overflow: hidden;
}

.table thead th {
  border: none;
  background: rgba(52, 58, 64, 0.8);
  color: #f8f9fa;
  font-weight: 600;
  padding: 1rem 0.75rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.table tbody tr {
  transition: all 0.2s ease;
  border: none;
}

.table tbody tr:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-1px);
}

.table tbody td {
  border: none;
  padding: 1rem 0.75rem;
  vertical-align: middle;
}

.sortable:hover {
  background: rgba(255, 255, 255, 0.1);
}

.sort-icon {
  font-size: 0.875rem;
  margin-left: 0.5rem;
}

.btn-group .btn {
  margin-left: 0.25rem;
  border-radius: 0.375rem;
}

.empty-state {
  border-radius: 0.5rem;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.pagination-container {
  padding: 1rem;
  border-radius: 0.5rem;
}

.pagination .page-link {
  border: none;
  color: #f8f9fa;
  background: transparent;
  padding: 0.5rem 0.75rem;
  margin: 0 0.125rem;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
}

.pagination .page-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #f8f9fa;
}

.pagination .page-item.active .page-link {
  background: #0d6efd;
  color: #f8f9fa;
}

.pagination .page-item.disabled .page-link {
  color: #6c757d;
  background: transparent;
  cursor: not-allowed;
}

.pagination-info {
  color: #adb5bd;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .table-header .row {
    flex-direction: column;
    gap: 1rem;
  }
  
  .table-header .col-md-6 {
    width: 100%;
  }
  
  .search-container .input-group {
    max-width: 100%;
  }
  
  .btn-group {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .btn-group .btn {
    margin-left: 0;
  }
}
</style> 