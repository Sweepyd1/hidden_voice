const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    
    port: 5000,
    proxy: {
      '^/api': {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    }
  }
})