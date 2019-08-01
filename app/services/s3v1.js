const AWS = require('aws-sdk');
const s3 = new AWS.S3({apiVersion: '2006-03-01', region: 'ap-southeast-2'})

module.exports = {

  listBuckets: params => {
    return s3.listBuckets(params).promise()
  },

  createBucket: params => {
    return s3.createBucket(params).promise()
  },

  deleteBucket: params => {
    return s3.deleteBucket(params).promise()
  },

  putObject: params => {
    return s3.putObject(params).promise()
  },

  getObject: params => {
    return s3.getObject(params).promise()
  },

  deleteObject: params => {
    return s3.deleteObject(params).promise()
  }

}
