const express = require('express')
const router = express.Router()
const log = require('simple-node-logger').createSimpleLogger()

router.get('/list', (request, response) => {
    response.send("hello s3 list")
})

module.exports = router;
