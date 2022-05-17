
var express = require('express');
var app = express();
var server = require('http').createServer(app);
var url_server = '192.168.0.10'
const io = require('socket.io')(server, {
    cors: {
      origin: '*',
    }
  });

server.listen(3000, url_server);


app.get('/', function(request, response){
    response.sendFile(__dirname  + '/index.html');
});

users = []
connections = [];


io.sockets.on('connection', function(socket){
  console.log("Connected");
    socket.on('joinroom', function(room) {
      socket.join(room)
      console.log(room);
      io.in(room).emit("setroom", {rom: room})
    });
    socket.on("sendmessage", (room,account,message, csrftoken)=>{
      json = {"id": room, "account_a": account,"message": message}
      fetch("http://"+url_server+":8000/control/send/message/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(json)
    }).then(resp => resp.json()).then(data => {
        io.in(room).emit("addmessage", data)
    })
    });
    socket.on('disconnect', function(data){
        connections.splice(connections.indexOf(socket), 1);
    });

});