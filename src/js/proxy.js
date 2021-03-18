const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');


const httpProxy = createProxyMiddleware(['/run', '/interactive'], {
  target: 'http://doesnt.matter:5000',
  router: (req) => 'http://localhost:5000', // find node's IP based on request
  changeOrigin: true,
});

const wsProxy = createProxyMiddleware('/ws', {
  target: 'ws://doesnt.matter:5000',
  router: (req) => 'ws://localhost:5000',
  changeOrigin: true,
  ws: true,
});

const app = express();
app.use(httpProxy);
app.use(wsProxy);

const server = app.listen(8080);
server.on('upgrade', wsProxy.upgrade);
