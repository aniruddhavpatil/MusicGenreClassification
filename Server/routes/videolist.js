var express = require('express');
var router = express.Router();
var fs = require('fs'),
    http = require("http"),
    url = require("url"),
    path = require("path");

var PythonShell = require('python-shell');
router.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

router.post('/', function(req, res, next) {

  var options = {
    mode: 'text',
    args: ['get-all',req.body.user]
  };

  PythonShell.run('scriptMongo.py', options, function (err, results) {
      if (err) throw err;
      res.json(results)
  });
});

module.exports = router;
