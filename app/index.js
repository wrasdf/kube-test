const express = require('express')
const app = express()
const helmet = require('helmet')
const root = require('/app/routers/root')
const apiv1 = require('/app/routers/apiv1')
const s3 = require('/app/routers/s3')

app.use(helmet())
app.use('/', root);
app.use('/api/v1', apiv1);
app.use('/s3', s3);

app.listen('8080', (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }
  console.log(`server is listening on 8080`)
})
