const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

const path = require('path');

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
  outputDir: path.resolve(__dirname, '../static'),
  assetsDir: '',
  indexPath: path.resolve(__dirname, '../templates/index.html')
}