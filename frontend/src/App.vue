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
/* Global Reset & Base Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, 
    #1a1a2e 0%, 
    #16213e 25%, 
    #0f3460 50%, 
    #1a1a2e 75%, 
    #16213e 100%
  );
  background-size: 400% 400%;
  animation: gradientShift 20s ease infinite;
  position: relative;
  overflow-x: hidden;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Enhanced Glassmorphism */
.glass {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 8px 32px 0 rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  transition: all 0.3s ease;
}

.glass:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 40px 0 rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.15);
}

.glass-navbar {
  background: rgba(0, 0, 0, 0.2) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  z-index: 1050;
  border-radius: 0 0 20px 20px;
}

/* Professional Button Styles */
.btn-primary {
  background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  font-weight: 600;
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(74, 85, 104, 0.3);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(74, 85, 104, 0.4);
  background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
  color: #ffffff;
}

.btn-outline-light {
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.03);
  color: #ffffff;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
  color: #ffffff;
  transform: translateY(-1px);
}

/* Form Controls */
.form-control {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 12px !important;
  color: #ffffff !important;
  padding: 12px 16px !important;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.form-control:focus {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: rgba(74, 85, 104, 0.6) !important;
  box-shadow: 0 0 0 0.25rem rgba(74, 85, 104, 0.25) !important;
  color: #ffffff !important;
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.5) !important;
}

.form-select {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 12px !important;
  color: #ffffff !important;
  backdrop-filter: blur(10px);
}

.form-select option {
  background: #1a1a2e !important;
  color: #ffffff !important;
}

/* Card Styles */
.card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(15px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 45px rgba(0, 0, 0, 0.4);
}

/* Table Enhancements */
.table-dark {
  background: rgba(255, 255, 255, 0.03) !important;
  border-radius: 12px;
  overflow: hidden;
}

.table-dark td, .table-dark th {
  border-color: rgba(255, 255, 255, 0.08) !important;
  color: #ffffff !important;
  padding: 16px !important;
}

.table-dark thead th {
  background: rgba(255, 255, 255, 0.08);
  border: none;
  color: #ffffff !important;
  font-weight: 600;
}

/* Professional Badge Styles */
.badge {
  border-radius: 8px;
  padding: 6px 12px;
  font-weight: 500;
  font-size: 0.75rem;
}

.bg-success {
  background: linear-gradient(135deg, #38a169, #2f855a) !important;
  color: #ffffff !important;
}

.bg-primary {
  background: linear-gradient(135deg, #4a5568, #2d3748) !important;
  color: #ffffff !important;
}

.bg-warning {
  background: linear-gradient(135deg, #ed8936, #dd6b20) !important;
  color: #ffffff !important;
}

.bg-danger {
  background: linear-gradient(135deg, #e53e3e, #c53030) !important;
  color: #ffffff !important;
}

/* Text Styles - Ensure Visibility */
body {
  background: transparent;
  color: #ffffff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-weight: 400;
  line-height: 1.6;
}

.text-light {
  color: #ffffff !important;
  font-weight: 500;
}

.text-muted, .text-secondary {
  color: rgba(255, 255, 255, 0.6) !important;
}

h1, h2, h3, h4, h5, h6 {
  color: #ffffff !important;
  font-weight: 600;
}

/* Minimal Animations */
.fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Main Content */
.main-content {
  flex: 1 1 auto;
  width: 100%;
  padding-top: 1rem;
  padding-bottom: 1rem;
  position: relative;
}

/* Responsive Design */
@media (max-width: 768px) {
  .glass {
    border-radius: 12px;
    margin: 0 10px;
  }
  
  .btn-primary, .btn-outline-light {
    border-radius: 10px;
    padding: 10px 18px;
  }
  
  .form-control, .form-select {
    border-radius: 10px !important;
  }
}

/* Remove unnecessary animations */
.app-bg {
  animation: gradientShift 25s ease infinite;
}

/* Focus on quiz application feel */
.quiz-focused {
  border-left: 3px solid #4a5568;
}

.professional-shadow {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}
</style>

