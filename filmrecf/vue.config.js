module.exports = {
    publicPath: "./",
    devServer: {
      open: true,
      host: "localhost",
      port: 8080,
      https: false,
      hotOnly: false,
      proxy: {
        "/": {
          target: "http://127.0.0.1:8848/",
          pathRewrite: {
            '/': '/'
          },
          changOrigin: true
        }
      }
    },
  }
  