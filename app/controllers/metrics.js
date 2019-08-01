const Prometheus = require('prom-client')
const ResponseTime = require('response-time')

const Register = Prometheus.register
const Counter = Prometheus.Counter
const Histogram = Prometheus.Histogram
const Summary = Prometheus.Summary

const requests = new Counter({
  name: 'app_requests',
  help: 'Number of app requests',
  labelNames: ['method', 'path']
});

const responses = new Summary({
  name: 'app_responses',
  help: 'App response time in millis',
  labelNames: ['method', 'path', 'status']
})

const responseCounters = ResponseTime((req, res, time) => {
  if (req.url != '/metrics') {
    responses.labels(req.method, req.originalUrl, res.statusCode).observe(time)
  }
})

const requestCounters = (req, res, next) => {
  if (req.path != '/metrics') {
    requests.inc({
      method: req.method,
      path: req.originalUrl
    })
  }
  next();
}

module.exports = {

  collect: () => {
    Register.setDefaultLabels({
      app: "node-app"
    });
    Prometheus.collectDefaultMetrics({
      timeout: 5000
    });
  },

  inject: app => {
    app.use(requestCounters)
    app.use(responseCounters)
    app.get('/metrics', (req, res) => {
      res.setHeader('Content-Type', Register.contentType);
      res.end(Register.metrics());
    });
  }

};
