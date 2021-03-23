const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');


const httpProxy = createProxyMiddleware(['/run', '/interactive'], {
  target: 'http://doesnt.matter:5000',
  router: function(req) {
    console.log(req.body);
    const port = req.body.port;
    return `http://localhost:${port}`; // find node based on request
  },
  changeOrigin: true,
});

const wsProxy = createProxyMiddleware('/ws', {
  target: 'ws://doesnt.matter:5000',
  router: function(req) {
    const port = req.body.port;
    return `ws://localhost:${port}`;
  },
  changeOrigin: true,
  ws: true,
});

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(httpProxy);
app.use(wsProxy);


const server = app.listen(8080);
server.on('upgrade', wsProxy.upgrade);
