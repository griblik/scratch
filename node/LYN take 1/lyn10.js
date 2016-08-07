
var net = require('net');
var port = process.argv[2];

var server = net.createServer(function (socket) {
	var date = new Date();
	var current = date.getFullYear() + "-" + (date.getMonth()+1) + "-" + date.getDate() + " " + date.getHours() + ":" + date.getMinutes();
	socket.write(current + "\n");
	socket.end();
});

// console.log("starting server")

server.listen(port);