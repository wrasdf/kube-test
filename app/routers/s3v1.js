const express = require('express')
const router = express.Router()
const controller = require('../controllers/s3v1')

router.get('/list', controller.listBuckets)
router.post('/:Bucket', controller.createBucket)
router.delete('/:Bucket', controller.deleteBucket)
router.get('/:Bucket/:Key', controller.getObject)
router.put('/:Bucket/:Key', controller.putObject)
router.delete('/:Bucket/:Key', controller.deleteObject)

module.exports = router;
