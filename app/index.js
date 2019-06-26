const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const helmet = require('helmet')
const prometheus = require('/app/controllers/metrics')
const root = require('/app/routers/root')
const apiv1 = require('/app/routers/apiv1')
const s3 = require('/app/routers/s3')

app.set('port', process.env.PORT || 8080)
app.use(helmet())

app.use((req, res, next) => {
  res.setHeader("Content-Type", "text/plain");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE");
  next();
});
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

prometheus.inject(app)
app.use('/', root)
app.use('/api/v1', apiv1);
app.use('/s3', s3);
prometheus.collect()
app.listen(app.get('port'), (err) => {
  if (err) {
    return console.log('Something bad happened', err)
  }
  console.log('Server is listening on ' + app.get('port'))
})
