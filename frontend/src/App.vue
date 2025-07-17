<template>
  <div class="app-bg min-vh-100">
    <BaseNavbar class="glass-navbar sticky-top" />
    <div class="main-content d-flex flex-column align-items-center justify-content-center min-vh-100">
      <router-view />
    </div>
  </div>
</template>

<script>
import BaseNavbar from './components/BaseNavbar.vue'

export default {
  name: 'App',
  components: {
    BaseNavbar
  }
}
</script>

<style>
.app-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #181A1B 0%, #23272B 100%);
}

.glass {
  background: rgba(35, 39, 43, 0.6);
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 32px 0 rgba(0,0,0,0.25);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}

.glass-navbar {
  background: rgba(35, 39, 43, 0.7) !important;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 2px 16px 0 rgba(0,0,0,0.12);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 1050;
}

body {
  background: #181A1B;
  color: #F8F9FA;
}

.main-content {
  flex: 1 1 auto;
  width: 100%;
  padding-top: 32px;
  padding-bottom: 32px;
}
</style>
