var express = require('express');
var router = express.Router();
const spawn = require('child_process').spawn;
var fs = require('fs'),
    http = require("http"),
    url = require("url"),
    path = require("path");

var PythonShell = require('python-shell');
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
  // var dir = './data/'.concat(file.originalname.split('.')[0]).concat('split')
  // console.log(dir)
  // fs.mkdirSync(dir);
  // var child = spawn("python", ["script.py","upload-start",file.originalname]);
  // const sp = spawn('python', ['script.py','upload-start',file.originalname], (error, stdout, stderr) => {
  //   if (error) {
  //       console.error('stderr', stderr);
  //       throw error;
  //   }
  //   console.log('stdout', stdout);
  // });
  // cmd = 'python script.py upload-start ' + file.originalname
  // spawn(cmd, (e, stdout, stderr)=> {
  //   if (e instanceof Error) {
  //       console.error(e);
  //       throw e;
  //   }
  //   console.log('stdout ', stdout);
  // });
  // child.stdout.on('data', function(data){
  //   console.log(data)
  // });

  // child.unref();
  //
  var options = {
    mode: 'text',
    args: ['upload-start', file.originalname]
  };


  PythonShell.run('scriptMongo.py', options, function (err, results) {
      if (err) throw err;
      // results is an array consisting of messages collected during execution
      console.log(results)
  });
});

router.post('/upload/done', (req, res) => {

  var options = {
    mode: 'text',
    args: ['get-genre', req.body.filename]
  };


  PythonShell.run('scriptMongo.py', options, function (err, results) {
      if (err) throw err;
      // results is an array consisting of messages collected during execution
      console.log(results)
      res.json({
        genre: results[0]
      })
  });
});

router.post('/reco', (req, res) => {

  console.log(req.body)
  var options = {
    mode: 'text',
    args: ['get-reco', req.body.filename,req.body.genre]
  };


  PythonShell.run('scriptMongo.py', options, function (err, results) {
      if (err) throw err;
      // results is an array consisting of messages collected during execution
      console.log(results)
      // results = ['Hello','asfasf','asfsaf','afsasf','asfasf']
      res.json({
        reco: results
      })
  });
});

router.get('/:fileName', function(req, res, next) {
  filename = req.params.fileName.replace(/-d-/g, '/')
  console.log(filename)
  var file = path.resolve(__dirname, '../' + filename);
  const stat = fs.statSync(file)
  const fileSize = stat.size
  const range = req.headers.range
  console.log(range)
  if (range) {
    const parts = range.replace(/bytes=/, "").split("-")
    const start = parseInt(parts[0], 10)
    const end = parts[1]
      ? parseInt(parts[1], 10)
      : fileSize-1
    const chunksize = (end-start)+1
    const filePart = fs.createReadStream(file, {start, end})
    const head = {
      'Content-Range': `bytes ${start}-${end}/${fileSize}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': 'video/mkv',
    }
    res.writeHead(206, head);
    filePart.pipe(res);
  } else {
    const head = {
      'Content-Length': fileSize,
      'Content-Type': 'video/avi',
    }
    res.writeHead(200, head)
    fs.createReadStream(file).pipe(filePart)
  }
});

module.exports = router;
