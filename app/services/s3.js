const AWS = require('aws-sdk');
const s3 = new AWS.S3({apiVersion: '2006-03-01', region: 'ap-southeast-2'})
const merge = require('deepmerge')

module.exports = {

  listBuckets: params => {
    const config = merge({}, params || {})
    return s3.listBuckets(config).promise()
  },

  createBucket: params => {
    const config = merge({}, params)
    return s3.createBucket(params).promise()
  },

  deleteBucket: params => {
    const config = merge({}, params)
    return s3.deleteBucket(params).promise()
  }

}
