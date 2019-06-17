const express = require('express'),
      app = express(),
      Prometheus = require('prom-client'),
      log = require('simple-node-logger').createSimpleLogger(),
      port = 8080,
      collectDefaultMetrics = Prometheus.collectDefaultMetrics,
      ENV = {
        iterations: process.env.ITERATIONS || 15
      };

collectDefaultMetrics({ timeout: 5000 });
const counter = new Prometheus.Counter({
  name: 'metric_name',
  help: 'metric_help'
});

app.get('/', (request, response) => {
  response.send(`
      <h2> Hello demo app ------- ! </h2>
      <ul>
        <li> /metrics  --> will return prometheus nodejs metrics </li>
        <li> /api/v1/health --> will retrun healthy status </li>
        <li> /api/v1/largeresp --> will return largeresp </li>
        <li> /api/v1/500 --> will return 500 error </li>
        <li> /api/v1/504 --> will return 504 error </li>
        <li> /api/v1/499 --> will return 499 error </li>
      </ul>
    `)
  log.info('index page accepted at ', new Date().toJSON());
})

app.get('/metrics', (request, response) => {
  response.set('Content-Type', 'text/plain');
  response.send(Prometheus.register.metrics())
  counter.inc();
  log.info('app metrics');
})

app.get('/api/v1/health', (request, response) => {
  response.send('OK!');
  log.info('app healthy at ', new Date().toJSON());
})

app.get('/api/v1/499', (request, response) => {
  try {
    throw new Error('499 Error');
  } catch (ex) {
    response.status(499).send('499 Error!')
    log.info('app 499 failure at ', new Date().toJSON());
  }
})

app.get('/api/v1/500', (request, response) => {
  try {
    throw new Error('500 Error');
  } catch (ex) {
    response.status(500).send('500 Error!')
    log.info('app 500 failure at ', new Date().toJSON());
  }
})

app.get('/api/v1/504', (request, response) => {
  try {
    throw new Error('504 Error');
  } catch (ex) {
    response.status(504).send('504 Error!')
    log.info('app 504 failure at ', new Date().toJSON());
  }
})

app.get('/api/v1/largeresp', (request, response) => {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var iterations = parseInt(ENV.iterations);

  for (let i=0, len=possible.length; i<len; i++ ){
    text += possible + Math.random()
  }

  for (var i = 0; i < iterations; i++) {
    text += text;
  }

  response.send(text)
  log.info('largeresp at ', new Date().toJSON());
})

app.listen(port, (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }
  console.log(`server is listening on ${port}`)
})
