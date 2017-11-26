var express = require('express');
var router = express.Router();
var PythonShell = require('python-shell');
/* GET home page. */
var fs = require('fs'),
    http = require("http"),
    url = require("url"),
    path = require("path");

router.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

var multer = require('multer')
const storage = multer.diskStorage({
  destination: './uploads',
  filename(req, file, cb) {
    cb(null, file.originalname);
  },
});
const upload = multer({ storage });


router.post('/upload', upload.single('file'), (req, res) => {
  const file = req.file; // file passed from client
  const meta = req.body; // all other values passed from the client, like name, etc..

  id = meta.id

});

router.post('/upload/done', (req, res) => {
  console.log('Hello')
  console.log(req)

  var options = {
    mode: 'text',
    args: ['get-genre', req.body.filename]
  };


  PythonShell.run('scriptMongo.py', options, function (err, results) {
      if (err) throw err;
      // results is an array consisting of messages collected during execution
      res.json(results)
  });
});

router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});


module.exports = router;
