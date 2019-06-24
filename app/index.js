const express = require('express')
const app = express()
const helmet = require('helmet')
const root = require('/app/routers/root')
const apiv1 = require('/app/routers/apiv1')
const s3 = require('/app/routers/s3')

app.set('port', process.env.PORT || 8080)
app.use(helmet())
app.use('/', root);
app.use('/api/v1', apiv1);
app.use('/s3', s3);

app.listen(app.get('port'), (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }
  console.log('server is listening on ' + app.get('port'))
})
