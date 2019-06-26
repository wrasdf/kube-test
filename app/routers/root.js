const express = require('express')
const router = express.Router()
const log = require('simple-node-logger').createSimpleLogger()

router.get('/', (request, response) => {
  response.send(`
      <h2> Hello demo app ------- ! </h2>
      <ul>
        <li> /metrics  --> will return prometheus nodejs metrics </li>
        <li> /health --> will retrun healthy status </li>
        <li> /api/v1/500 --> will return 500 error </li>
        <li> /api/v1/504 --> will return 504 error </li>
        <li> /api/v1/499 --> will return 499 error </li>
        <li> /api/v1/largeresp --> will return largeresp </li>
        <li> /s3/list --> list all the s3 bucket </li>
      </ul>
    `)
  log.info('index page accepted at ', new Date().toJSON());
})

router.get('/health', (request, response) => {
  response.send('OK!');
  log.info('app healthy at ', new Date().toJSON());
})

module.exports = router;
