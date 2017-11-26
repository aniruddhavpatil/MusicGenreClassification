var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var index = require('./routes/index');
var video = require('./routes/video');
var videolist = require('./routes/videolist');
var PythonShell = require('python-shell');
// var passport = require('passport');
// var LocalStrategy = require('passport-local').Strategy;
//
// passport.use(new LocalStrategy(
//   function(username, password, done) {
//     var options = {
//       mode: 'text',
//       args: ['find-user', username, password]
//     };
//
//
//     PythonShell.run('scriptMongo.py', options, function (err, results) {
//         if (err) throw err;
//         // results is an array consisting of messages collected during execution
//         if(results == 'wrong-username'){
//           return done(null, false, { message: 'Incorrect username.' });
//         }
//         if(results == 'wrong-pass'){
//           return done(null, false, { message: 'Incorrect password.' });
//         }
//         if(results == 'correct'){
//           return done(null,true);
//         }
//     });
//   }
// ));
//
// passport.serializeUser(function(user, done) {
//   done(null, user.id);
// });
//
// passport.deserializeUser(function(id, done) {
//   User.findById(id, function(err, user) {
//     done(err, user);
//   });
// });

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
// app.use(passport.initialize());
// app.use(passport.session());

app.use('/', index);
app.use('/video', video);
// app.use('/videolist', videolist);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
