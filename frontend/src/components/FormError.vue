<template>
  <div v-if="error" class="invalid-feedback d-block text-danger">
    {{ error }}
  </div>
</template>

<script>
export default {
  name: 'FormError',
  props: {
    error: String
  }
}
</script> 