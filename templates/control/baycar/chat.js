const { randomUUID } = require('crypto');
var express = require('express');
var app = express();
var server = require('http').createServer(app);
const io = require('socket.io')(server, {
    cors: {
      origin: '*',
    }
  });
server.listen(3000, '192.168.0.10');


app.get('/', function(request, response){
    response.sendFile(__dirname  + '/index.html');
});

users = []
connections = [];


io.sockets.on('connection', function(socket){
  console.log("Connected");
    socket.on('create', function(room) {
      socket.join(room)
      io.in(room).emit("setroom", {rom: room})
    });
    socket.on("send mess", (room,message)=>{
      io.in(room).emit("add mess", {msg: message})
    });
    socket.on('disconnect', function(data){
        connections.splice(connections.indexOf(socket), 1);
    });

});