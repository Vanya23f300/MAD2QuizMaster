<template>
  <div class="admin-users-view">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-lg-3 col-md-4">
        <BaseSidebar user-role="admin" />
      </div>
      
      <!-- Main Content -->
      <div class="col-lg-9 col-md-8">
        <div class="container-fluid p-4">
          <!-- Page Header -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div class="d-flex align-items-center gap-3">
              <button 
                class="btn btn-outline-light d-flex align-items-center gap-2"
                @click="goBack"
              >
                <i class="bi bi-arrow-left"></i>
                Back
              </button>
              <h2 class="text-light mb-0">User Management</h2>
            </div>
            <div class="d-flex gap-2">
              <button 
                class="btn btn-success d-flex align-items-center gap-2"
                @click="exportUsers"
              >
                <i class="bi bi-download"></i>
                Export
              </button>
            </div>
          </div>

          <!-- Stats Cards -->
          <div class="row mb-4">
            <div class="col-md-3">
              <div class="card glass p-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="text-light mb-1">Total Users</h6>
                    <h3 class="text-primary mb-0">{{ stats.totalUsers }}</h3>
                  </div>
                  <i class="bi bi-people fs-1 text-primary opacity-50"></i>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="card glass p-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="text-light mb-1">Active Users</h6>
                    <h3 class="text-success mb-0">{{ stats.activeUsers }}</h3>
                  </div>
                  <i class="bi bi-person-check fs-1 text-success opacity-50"></i>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="card glass p-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="text-light mb-1">New This Month</h6>
                    <h3 class="text-info mb-0">{{ stats.newThisMonth }}</h3>
                  </div>
                  <i class="bi bi-person-plus fs-1 text-info opacity-50"></i>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="card glass p-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="text-light mb-1">Avg Quiz Score</h6>
                    <h3 class="text-warning mb-0">{{ stats.avgQuizScore }}%</h3>
                  </div>
                  <i class="bi bi-graph-up fs-1 text-warning opacity-50"></i>
                </div>
              </div>
            </div>
          </div>

          <!-- Search and Filter -->
          <div class="card glass p-3 mb-4">
            <div class="row g-3">
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text bg-transparent border-secondary text-light">
                    <i class="bi bi-search"></i>
                  </span>
                  <input
                    type="text"
                    class="form-control bg-transparent border-secondary text-light"
                    placeholder="Search by name, email, or qualification..."
                    v-model="searchQuery"
                    @input="filterUsers"
                  />
                </div>
              </div>
              <div class="col-md-3">
                <select 
                  class="form-select bg-transparent border-secondary text-light"
                  v-model="filterQualification"
                  @change="filterUsers"
                >
                  <option value="">All Qualifications</option>
                  <option value="High School">High School</option>
                  <option value="Bachelor's">Bachelor's</option>
                  <option value="Master's">Master's</option>
                  <option value="PhD">PhD</option>
                </select>
              </div>
              <div class="col-md-3">
                <select 
                  class="form-select bg-transparent border-secondary text-light"
                  v-model="filterStatus"
                  @change="filterUsers"
                >
                  <option value="">All Status</option>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Users Table -->
          <div class="card glass p-3">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="text-light mb-0">Registered Users</h5>
              <span class="text-light-50">{{ filteredUsers.length }} users found</span>
            </div>
            
            <div class="table-responsive">
              <table class="table table-dark table-hover">
                <thead>
                  <tr>
                    <th>User</th>
                    <th>Contact</th>
                    <th>Qualification</th>
                    <th>Joined</th>
                    <th>Quiz Attempts</th>
                    <th>Avg Score</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in paginatedUsers" :key="user.id">
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="user-avatar me-2">
                          {{ getUserInitials(user.full_name) }}
                        </div>
                        <div>
                          <div class="fw-medium">{{ user.full_name }}</div>
                          <small class="text-muted">ID: {{ user.id }}</small>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div>{{ user.username }}</div>
                      <small class="text-muted">{{ formatDate(user.dob) }}</small>
                    </td>
                    <td>
                      <span class="badge bg-info">{{ user.qualification }}</span>
                    </td>
                    <td>{{ formatDate(user.created_at) }}</td>
                    <td>
                      <span class="badge bg-primary">{{ user.quiz_attempts || 0 }}</span>
                    </td>
                    <td>
                      <span class="badge" :class="getScoreBadgeClass(user.avg_score)">
                        {{ user.avg_score || 0 }}%
                      </span>
                    </td>
                    <td>
                      <span 
                        class="badge" 
                        :class="user.is_active ? 'bg-success' : 'bg-secondary'"
                      >
                        {{ user.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          class="btn btn-outline-primary"
                          @click="viewUserDetails(user)"
                          title="View Details"
                        >
                          <i class="bi bi-eye"></i>
                        </button>
                        <button 
                          class="btn btn-outline-warning"
                          @click="toggleUserStatus(user)"
                          :title="user.is_active ? 'Deactivate' : 'Activate'"
                        >
                          <i class="bi" :class="user.is_active ? 'bi-person-dash' : 'bi-person-check'"></i>
                        </button>
                        <button 
                          class="btn btn-outline-danger"
                          @click="confirmDeleteUser(user)"
                          title="Delete User"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination -->
            <div class="d-flex justify-content-between align-items-center mt-3">
              <span class="text-light-50">
                Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to 
                {{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }} 
                of {{ filteredUsers.length }} users
              </span>
              <nav>
                <ul class="pagination pagination-sm mb-0">
                  <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <button class="page-link bg-transparent border-secondary text-light" @click="currentPage--">
                      Previous
                    </button>
                  </li>
                  <li 
                    class="page-item" 
                    v-for="page in totalPages" 
                    :key="page"
                    :class="{ active: page === currentPage }"
                  >
                    <button 
                      class="page-link bg-transparent border-secondary text-light"
                      @click="currentPage = page"
                    >
                      {{ page }}
                    </button>
                  </li>
                  <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                    <button class="page-link bg-transparent border-secondary text-light" @click="currentPage++">
                      Next
                    </button>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Details Modal -->
    <div class="modal fade" id="userDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content bg-dark">
          <div class="modal-header border-secondary">
            <h5 class="modal-title text-light">User Details</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedUser">
            <div class="row">
              <div class="col-md-6">
                <h6 class="text-primary">Personal Information</h6>
                <table class="table table-dark table-sm">
                  <tbody>
                    <tr>
                      <td><strong>Full Name:</strong></td>
                      <td>{{ selectedUser.full_name }}</td>
                    </tr>
                    <tr>
                      <td><strong>Email:</strong></td>
                      <td>{{ selectedUser.username }}</td>
                    </tr>
                    <tr>
                      <td><strong>Date of Birth:</strong></td>
                      <td>{{ formatDate(selectedUser.dob) }}</td>
                    </tr>
                    <tr>
                      <td><strong>Qualification:</strong></td>
                      <td>{{ selectedUser.qualification }}</td>
                    </tr>
                    <tr>
                      <td><strong>Joined:</strong></td>
                      <td>{{ formatDate(selectedUser.created_at) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="col-md-6">
                <h6 class="text-success">Quiz Statistics</h6>
                <table class="table table-dark table-sm">
                  <tbody>
                    <tr>
                      <td><strong>Total Attempts:</strong></td>
                      <td>{{ selectedUser.quiz_attempts || 0 }}</td>
                    </tr>
                    <tr>
                      <td><strong>Average Score:</strong></td>
                      <td>{{ selectedUser.avg_score || 0 }}%</td>
                    </tr>
                    <tr>
                      <td><strong>Best Score:</strong></td>
                      <td>{{ selectedUser.best_score || 0 }}%</td>
                    </tr>
                    <tr>
                      <td><strong>Last Activity:</strong></td>
                      <td>{{ formatDate(selectedUser.last_activity) }}</td>
                    </tr>
                    <tr>
                      <td><strong>Status:</strong></td>
                      <td>
                        <span class="badge" :class="selectedUser.is_active ? 'bg-success' : 'bg-secondary'">
                          {{ selectedUser.is_active ? 'Active' : 'Inactive' }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <DeleteConfirm 
      :show="showDeleteModal"
      :item-name="userToDelete?.full_name"
      item-type="user"
      @confirm="deleteUser"
      @cancel="showDeleteModal = false"
    />
  </div>
</template>

<script>
import BaseSidebar from '../../components/BaseSidebar.vue'
import DeleteConfirm from '../../components/DeleteConfirm.vue'
import { Modal } from 'bootstrap'

export default {
  name: 'AdminUsersView',
  components: {
    BaseSidebar,
    DeleteConfirm
  },
  data() {
    return {
      users: [],
      filteredUsers: [],
      searchQuery: '',
      filterQualification: '',
      filterStatus: '',
      currentPage: 1,
      itemsPerPage: 10,
      selectedUser: null,
      showDeleteModal: false,
      userToDelete: null,
      stats: {
        totalUsers: 0,
        activeUsers: 0,
        newThisMonth: 0,
        avgQuizScore: 0
      },
      loading: true
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredUsers.length / this.itemsPerPage)
    },
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredUsers.slice(start, end)
    }
  },
  async mounted() {
    await this.loadUsers()
    this.calculateStats()
  },
  methods: {
    async loadUsers() {
      try {
        // Mock data for now - replace with actual API call
        this.users = [
          {
            id: 1,
            username: 'john.doe@email.com',
            full_name: 'John Doe',
            qualification: "Bachelor's",
            dob: '1995-06-15',
            created_at: '2024-01-15',
            is_active: true,
            quiz_attempts: 12,
            avg_score: 85,
            best_score: 95,
            last_activity: '2024-01-20'
          },
          {
            id: 2,
            username: 'jane.smith@email.com',
            full_name: 'Jane Smith',
            qualification: "Master's",
            dob: '1992-08-22',
            created_at: '2024-01-10',
            is_active: true,
            quiz_attempts: 8,
            avg_score: 92,
            best_score: 98,
            last_activity: '2024-01-19'
          },
          {
            id: 3,
            username: 'bob.wilson@email.com',
            full_name: 'Bob Wilson',
            qualification: 'High School',
            dob: '1998-03-10',
            created_at: '2024-01-05',
            is_active: false,
            quiz_attempts: 5,
            avg_score: 72,
            best_score: 85,
            last_activity: '2024-01-15'
          }
        ]
        this.filteredUsers = [...this.users]
        this.loading = false
      } catch (error) {
        console.error('Error loading users:', error)
        this.loading = false
      }
    },
    calculateStats() {
      this.stats.totalUsers = this.users.length
      this.stats.activeUsers = this.users.filter(user => user.is_active).length
      
      // Calculate new users this month
      const thisMonth = new Date().getMonth()
      const thisYear = new Date().getFullYear()
      this.stats.newThisMonth = this.users.filter(user => {
        const createdDate = new Date(user.created_at)
        return createdDate.getMonth() === thisMonth && createdDate.getFullYear() === thisYear
      }).length
      
      // Calculate average quiz score
      const totalScore = this.users.reduce((sum, user) => sum + (user.avg_score || 0), 0)
      this.stats.avgQuizScore = Math.round(totalScore / this.users.length)
    },
    filterUsers() {
      let filtered = [...this.users]
      
      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(user => 
          user.full_name.toLowerCase().includes(query) ||
          user.username.toLowerCase().includes(query) ||
          user.qualification.toLowerCase().includes(query)
        )
      }
      
      // Qualification filter
      if (this.filterQualification) {
        filtered = filtered.filter(user => user.qualification === this.filterQualification)
      }
      
      // Status filter
      if (this.filterStatus) {
        const isActive = this.filterStatus === 'active'
        filtered = filtered.filter(user => user.is_active === isActive)
      }
      
      this.filteredUsers = filtered
      this.currentPage = 1
    },
    getUserInitials(name) {
      return name.split(' ').map(n => n[0]).join('').toUpperCase()
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    },
    getScoreBadgeClass(score) {
      if (score >= 90) return 'bg-success'
      if (score >= 75) return 'bg-primary'
      if (score >= 60) return 'bg-warning'
      return 'bg-danger'
    },
    viewUserDetails(user) {
      this.selectedUser = user
      const modal = new Modal(document.getElementById('userDetailsModal'))
      modal.show()
    },
    toggleUserStatus(user) {
      // Toggle user active status
      user.is_active = !user.is_active
      // Here you would make an API call to update the user status
      console.log(`User ${user.full_name} status changed to: ${user.is_active ? 'Active' : 'Inactive'}`)
      this.calculateStats()
    },
    confirmDeleteUser(user) {
      this.userToDelete = user
      this.showDeleteModal = true
    },
    deleteUser() {
      if (this.userToDelete) {
        const index = this.users.findIndex(u => u.id === this.userToDelete.id)
        if (index > -1) {
          this.users.splice(index, 1)
          this.filterUsers()
          this.calculateStats()
        }
      }
      this.showDeleteModal = false
      this.userToDelete = null
    },
    exportUsers() {
      // Export functionality
      const csvContent = this.generateCSV()
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `users_export_${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
    },
    generateCSV() {
      const headers = ['ID', 'Name', 'Email', 'Qualification', 'DOB', 'Joined', 'Quiz Attempts', 'Avg Score', 'Status']
      const rows = this.users.map(user => [
        user.id,
        user.full_name,
        user.username,
        user.qualification,
        user.dob,
        user.created_at,
        user.quiz_attempts || 0,
        user.avg_score || 0,
        user.is_active ? 'Active' : 'Inactive'
      ])
      
      return [headers, ...rows].map(row => row.join(',')).join('\n')
    },
    goBack() {
      this.$router.push('/admin')
    }
  }
}
</script>

<style scoped>
.admin-users-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #181A1B 0%, #23272B 100%);
  padding-top: 2rem;
}

.card.glass {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0d6efd, #6f42c1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  color: white;
}

.table-dark {
  background: transparent;
}

.table-dark td, .table-dark th {
  border-color: rgba(255, 255, 255, 0.1);
  vertical-align: middle;
}

.table-hover tbody tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.form-control:focus, .form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  background-color: rgba(35, 39, 43, 0.6);
  color: white;
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-select option {
  background-color: #23272B;
  color: white;
}

.pagination .page-link:hover {
  background-color: rgba(13, 110, 253, 0.1);
}

.pagination .active .page-link {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.text-light-50 {
  color: rgba(255, 255, 255, 0.5);
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
}
</style>