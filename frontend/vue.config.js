// const { defineConfig } = require('@vue/cli-service')

// const path = require("path");
// function resolve(dir) {
//   return path.join(__dirname, dir)
// }

// module.exports = defineConfig({
//   transpileDependencies: true,
//   assetsDir: 'static',
//   publicPath: "./"

// })

module.exports = {
  transpileDependencies: true,
  assetsDir: 'static',
  publicPath: "./",
  devServer: {
      proxy: {
        '/api': {
          target: 'http://bakatat.pythonanywhere.com/', //测试环境
          secure: false, //允许访问https
          ws:false,
          changeOrigin: true,   //允许跨域
          pathRewrite: {
              '^/api': ''
          }
        },
        '/': {
          target: 'http://bakatat.pythonanywhere.com/', //测试环境
          secure: false, //允许访问https
          ws:false,
          changeOrigin: true,   //允许跨域
          pathRewrite: {
              '^/': ''
          }
        },
      }
  }
}
