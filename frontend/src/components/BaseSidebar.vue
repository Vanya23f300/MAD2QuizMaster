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
          { path: '/admin/questions', label: 'Questions', icon: 'bi bi-question-circle' },
          { path: '/admin/quizzes', label: 'Quizzes', icon: 'bi bi-file-text' },
          { path: '/admin/summary', label: 'Summary', icon: 'bi bi-graph-up' },
          { path: '/logout', label: 'Logout', icon: 'bi bi-box-arrow-right' }
        ]
      } else {
        return [
          { path: '/user', label: 'Dashboard', icon: 'bi bi-house' },
          { path: '/user/quizzes', label: 'Quizzes', icon: 'bi bi-file-text' },
          { path: '/user/scores', label: 'Scores', icon: 'bi bi-trophy' },
          { path: '/user/summary', label: 'Summary', icon: 'bi bi-graph-up' },
          { path: '/logout', label: 'Logout', icon: 'bi bi-box-arrow-right' }
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
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.5rem;
  width: 280px;
  transition: width 0.3s ease;
  height: calc(100vh - 2rem);
  position: sticky;
  top: 1rem;
}

.sidebar-collapsed {
  width: 80px;
}

.sidebar-title {
  font-weight: 600;
  font-size: 1.1rem;
}

.nav-link {
  color: #ADB5BD;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.2s;
  text-decoration: none;
}

.nav-link:hover {
  color: #F8F9FA;
  background: rgba(13, 110, 253, 0.1);
}

.nav-link.active {
  color: #0D6EFD;
  background: rgba(13, 110, 253, 0.15);
  font-weight: 600;
}

.nav-icon {
  font-size: 1.1rem;
  width: 20px;
  text-align: center;
}

.nav-text {
  font-weight: 500;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
    margin-bottom: 1rem;
  }
  
  .sidebar-collapsed {
    width: 100%;
  }
}
</style> 