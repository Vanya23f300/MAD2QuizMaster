<template>
  <label :for="forId" class="form-label text-light fw-semibold">
    <slot />
    <span v-if="required" class="text-danger ms-1">*</span>
  </label>
</template>

<script>
export default {
  name: 'FormLabel',
  props: {
    forId: String,
    required: Boolean
  }
}
</script> 