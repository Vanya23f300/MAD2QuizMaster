<template>
  <div class="mb-3">
    <FormLabel :for-id="id" :required="required">{{ label }}</FormLabel>
    <input
      :id="id"
      :type="type"
      class="form-control bg-dark text-light border-secondary glass"
      :class="{ 'is-invalid': error }"
      :placeholder="placeholder"
      :required="required"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      v-bind="$attrs"
    />
    <FormError :error="error" />
  </div>
</template>

<script>
import FormLabel from './FormLabel.vue'
import FormError from './FormError.vue'

export default {
  name: 'BaseInput',
  components: { FormLabel, FormError },
  props: {
    id: String,
    label: String,
    type: {
      type: String,
      default: 'text'
    },
    modelValue: String,
    error: String,
    required: Boolean,
    placeholder: String
  }
}
</script> 