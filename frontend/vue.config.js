const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080
  },
  configureWebpack: {
    plugins: [
      require('unplugin-vue-components/webpack')({
        /* options */
      }),
    ],
  },
  // Fix for VUE_PROD_HYDRATION_MISMATCH_DETAILS warning
  chainWebpack: config => {
    config.plugins.delete('feature-flags')
  }
})
