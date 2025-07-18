<template>
  <nav class="navbar navbar-expand-lg glass-navbar py-3">
    <div class="container-fluid">
      <div class="d-flex align-items-center">
        <div class="navbar-brand-container">
          <span class="navbar-brand fw-bold text-light d-flex align-items-center">
            <div class="brand-icon me-2">
              <i class="bi bi-clipboard-check-fill"></i>
            </div>
            Quiz Master
          </span>
        </div>
      </div>
      <slot />
    </div>
  </nav>
</template>

<script>
export default {
  name: 'BaseNavbar'
}
</script>

<style scoped>
.navbar {
  border-radius: 0 0 20px 20px;
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3);
}

.navbar-brand-container {
  position: relative;
}

.navbar-brand {
  font-size: 1.5rem;
  letter-spacing: 0.5px;
  color: #ffffff !important;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.brand-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #4a5568, #2d3748);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.1rem;
  box-shadow: 0 3px 12px rgba(74, 85, 104, 0.3);
  transition: all 0.3s ease;
}

.navbar-brand:hover {
  transform: scale(1.02);
  color: #ffffff !important;
}

.navbar-brand:hover .brand-icon {
  box-shadow: 0 4px 15px rgba(74, 85, 104, 0.4);
  transform: translateY(-1px);
}
</style> 