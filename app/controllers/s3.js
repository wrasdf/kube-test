const log = require('simple-node-logger').createSimpleLogger()
const service = require('../services/s3')
module.exports = {

  listBuckets: (request, response) => {
    service.listBuckets().then(data => {
      log.info(data)
      response.status(200).send(`${data.Buckets}`)
    }).catch(err => {
      log.error(err)
      response.status(500).send(`${err}`)
    })
  },

  createBucket: (request, response) => {
    service.createBucket(request.params).then(data => {
      response.status(200).send(`create ${request.params.Bucket} bucket success`)
    }).catch(err => {
      log.error(err)
      response.status(500).send(`${err}`)
    })
  },

  deleteBucket: (request, response) => {
    service.deleteBucket(request.params).then(data => {
      response.status(200).send(`delete ${request.params.Bucket} bucket success`)
    }).catch(err => {
      log.error(err)
      response.status(500).send(`${err}`)
    })
  },

  createObject: (request, response) => {
    response.send(`create ${request.params.bucket} ${request.params.key} ${request.params.data}`)
  },
  getObject: (request, response) => {
    response.send(`get ${request.params.bucket} ${request.params.key}`)
  },
  putObject: (request, response) => {
    response.send(`put ${request.params.bucket} ${request.params.key} ${request.params.data}`)
  },
  deleteObject: (request, response) => {
    response.send(`delete ${request.params.bucket} ${request.params.key}`)
  }
}
