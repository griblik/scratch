var http = require('http');
var url = require('url');

var server = http.createServer(function(req, res) {
	var reqUrl = url.parse(req.url, true);
	var reqDate;
	var resDate = {};

	if(reqUrl.query['iso']) {
		reqDate = new Date("" + reqUrl.query['iso']);
		console.log("Date: " + reqDate);
	}

	if(reqUrl.path.indexOf("/api/parsetime") == 0) {
		resDate.hour = reqDate.getHours();
		resDate.minute = reqDate.getMinutes();
		resDate.second = reqDate.getSeconds();
	}
	
	if(reqUrl.path.indexOf("/api/unixtime") == 0) {
		resDate.unixtime = reqDate.getTime();
	}

	res.setHeader('Content-Type', 'application/json');
	res.write(JSON.stringify(resDate));
	res.end();
});

server.listen(process.argv[2]);