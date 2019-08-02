const log = require('simple-node-logger').createSimpleLogger()
const service = require('../services/s3v1')
const merge = require('deepmerge')

module.exports = {

  listBuckets: (request, response) => {
    service.listBuckets().then(data => {
      results = JSON.stringify(data.Buckets)
      response.status(200).send(`{"status": "success", "data": "${results}"}`)
    }).catch(err => {
      log.error(err)
      response.status(err.statusCode).send(`{"status": "failed", "data": "${err.message}"`)
    })
  },

  createBucket: (request, response) => {
    service.createBucket(request.params).then(data => {
      response.status(200).send(`{"status": "success", "data": "${request.params.Bucket}"}`)
    }).catch(err => {
      log.error(err)
      response.status(err.statusCode).send(`{"status": "failed", "data": "${err.message}"`)
    })
  },

  deleteBucket: (request, response) => {
    service.deleteBucket(request.params).then(data => {
      response.status(200).send(`{"status": "success", "data": "${request.params.Bucket}"}`)
    }).catch(err => {
      log.error(err)
      response.status(err.statusCode).send(`{"status": "failed", "data": "${err.message}"`)
    })
  },

  putObject: (request, response) => {
    service.putObject(merge(request.params, {
      Body: request.body.data
    })).then(data => {
      response.status(200).send(`{"status": "success", "data": "s3://${request.params.Bucket}/${request.params.Key}"}`)
    }).catch(err => {
      log.error(err)
      response.status(err.statusCode).send(`{"status": "failed", "data": "${err.message}"`)
    })
  },

  getObject: (request, response) => {
    service.getObject(request.params).then(data => {
      response.status(200).send(`{"status": "success", "data": "${data.Body.toString('utf-8')}"}`)
    }).catch(err => {
      log.error(err)
      response.status(err.statusCode).send(`{"status": "failed", "data": "${err.message}"`)
    })
  },

  deleteObject: (request, response) => {
    service.deleteObject(request.params).then(data => {
      response.status(200).send(`{"status": "success", "data": "s3://${request.params.Bucket}/${request.params.Key}"}`)
    }).catch(err => {
      log.error(err)
      response.status(err.statusCode).send(`{"status": "failed", "data": "${err.message}"`)
    })
  }
}
