<template>
  <div class="sidebar glass" :class="{ 'sidebar-collapsed': collapsed }">
    <div class="sidebar-header d-flex align-items-center justify-content-between mb-4">
      <h5 class="sidebar-title text-light mb-0">Navigation</h5>
      <button class="btn btn-link text-light p-0" @click="toggleCollapse">
        <i :class="collapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left'"></i>
      </button>
    </div>
    <nav class="sidebar-nav">
      <ul class="nav flex-column">
        <li v-for="item in navigationItems" :key="item.path" class="nav-item">
          <router-link
            :to="item.path"
            class="nav-link d-flex align-items-center"
            :class="{ 'active': $route.path === item.path }"
          >
            <i :class="item.icon" class="nav-icon me-3"></i>
            <span v-if="!collapsed" class="nav-text">{{ item.label }}</span>
          </router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'BaseSidebar',
  props: {
    userRole: {
      type: String,
      default: 'user'
    }
  },
  data() {
    return {
      collapsed: false
    }
  },
  computed: {
    navigationItems() {
      if (this.userRole === 'admin') {
        return [
          { path: '/admin', label: 'Dashboard', icon: 'bi bi-house' },
          { path: '/admin/subjects', label: 'Subjects', icon: 'bi bi-book' },
          { path: '/admin/chapters', label: 'Chapters', icon: 'bi bi-collection' },
          { path: '/admin/quizzes', label: 'Quizzes', icon: 'bi bi-file-text' },
          { path: '/admin/questions', label: 'Questions', icon: 'bi bi-question-circle' },
          { path: '/login', label: 'Logout', icon: 'bi bi-box-arrow-right' }
        ]
      } else {
        return [
          { path: '/user', label: 'Dashboard', icon: 'bi bi-house' },
          { path: '/user/scores', label: 'My Scores', icon: 'bi bi-trophy' },
          { path: '/user/summary', label: 'Summary Charts', icon: 'bi bi-graph-up' },
          { path: '/login', label: 'Logout', icon: 'bi bi-box-arrow-right' }
        ]
      }
    }
  },
  methods: {
    toggleCollapse() {
      this.collapsed = !this.collapsed
    }
  }
}
</script>

<style scoped>
.sidebar {
  min-height: 100vh;
  padding: 1.5rem;
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  transition: width 0.3s ease;
  width: 250px;
}

.sidebar-collapsed {
  width: 80px;
}

.sidebar-header {
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-title {
  font-size: 1.1rem;
  font-weight: 600;
}

.nav-link {
  color: #adb5bd;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
  text-decoration: none;
  margin-bottom: 0.5rem;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #f8f9fa;
  transform: translateX(5px);
}

.nav-link.active {
  background: rgba(13, 110, 253, 0.2);
  color: #0d6efd;
  border-left: 3px solid #0d6efd;
}

.nav-icon {
  width: 20px;
  text-align: center;
}

.nav-text {
  font-weight: 500;
}

.sidebar-collapsed .nav-text {
  display: none;
}

.sidebar-collapsed .sidebar-title {
  display: none;
}
</style> 