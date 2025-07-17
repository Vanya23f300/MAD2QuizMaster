<template>
  <nav class="navbar navbar-expand-lg glass-navbar py-3">
    <div class="container-fluid">
      <a class="navbar-brand fw-bold text-light" href="#">Quiz Master</a>
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
  border-radius: 0 0 1.25rem 1.25rem;
  box-shadow: 0 2px 16px 0 rgba(0,0,0,0.12);
}
.navbar-brand {
  font-size: 1.5rem;
  letter-spacing: 1px;
  color: #F8F9FA !important;
}
</style> 