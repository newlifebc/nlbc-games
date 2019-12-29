const fs = require('fs');
const path = require("path");
const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const fileupload = require("express-fileupload");

const forever = require('forever');
const assert = require('assert');


// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ++++ Base Express Webserver setup
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

process.env.NODE_ENV = "development"; //production
var port = process.env.PORT || 80;
console.log('beginning nlbc-games server now, running in '+process.env.NODE_ENV+' mode on port '+port+'.');
server.listen(port);



app.use(express.static(path.join(__dirname, '/public')));
app.use('/js', express.static(__dirname + '/node_modules/jquery/dist')); // redirect jQuery JS
app.use('/', express.static(__dirname + '/node_modules/bootstrap/dist')); // redirect bootstrap JS, CSS, and fonts
app.use('/css', express.static(__dirname + '/node_modules/normalize.css')); // redirect normalize.css
app.use('/js', express.static(__dirname + '/node_modules/babylon/bin')); // redirect babylon JS
app.use('/js', express.static(__dirname + '/node_modules/phaser/dist')); // redirect phaser JS
app.use('/js', express.static(__dirname + '/node_modules/kinect2/lib')); // redirect kinect2 JS
app.use('/js', express.static(__dirname + '/node_modules/tracking/build')); // redirect tracking JS
app.use('/tracking', express.static(__dirname + '/node_modules/tracking')); // redirect kinect2 JS



var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());
// app.use(bodyParser.text());


app.post('/upload', function(req, res) {
    // //if (Object.keys(req.files).length == 0) {
    // //    return res.status(400).send('No files were uploaded.');
    // //}
    
    // // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
    // //let sampleFile = req.files.sampleFile;
    // //let sampleFile = req.files.sampleFile;
    // //let img = Object.keys(req.body)[0]; //assumes input is json format as key
    // let img = req.body;
    // console.dir(img);

    // // var img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0"
    // // + "NAAAAKElEQVQ4jWNgYGD4Twzu6FhFFGYYNXDUwGFpIAk2E4dHDRw1cDgaCAASFOffhEIO"
    // // + "3gAAAABJRU5ErkJggg==";
    // // strip off the data: url prefix to get just the base64-encoded bytes
    // var data = img.replace(/^data:image\/\w+;base64,/, "");
    // var buf = new Buffer(data, 'base64');
    // fs.writeFile('image.png', buf);

    // // Grab the extension to resolve any image error
    // var ext = img['data'].split(';')[0].match(/jpeg|png|gif/)[0];
    // // strip off the data: url prefix to get just the base64-encoded bytes
    // var data = img['base64'].replace(/^data:image\/\w+;base64,/, "");
    // var buf = new Buffer(img, 'base64');
    // fs.writeFile('image.' + ext, buf);
    
    // // Use the mv() method to place the file somewhere on your server
    // // sampleFile.mv('/tools/filename.jpg', function(err) {
    // //     if (err)
    // //         return res.status(500).send(err);
    // //     res.send('File uploaded!');
    // // });
    res.send('File uploaded!');
});


io.on('connection',function(socket){

    socket.on('subscribe',function(roomName){
        socket.join(roomName);
        console.log("client "+socket['id']+" joined room "+roomName);
    });

    socket.on('unsubscribe',function(roomName){
        socket.leave(roomName);
        console.log("client "+socket['id']+" left room "+roomName);
    });
    

    socket.on('disconnect', function(){
        console.log("client "+socket['id']+" disconnected");
    });


    socket.on('saveImage',function(data){
        //should have 'filename' and 'b64'
        fs.writeFile(data['filename'], data['b64'], {encoding: 'base64'}, function(err){
            if (err) throw err
            console.log('File saved.')
        });
    });
});