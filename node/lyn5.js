var fs = require('fs');
var path = require('path');

var dirlist = fs.readdir(process.argv[2],doSomething);
var ext = "." + process.argv[3];

function doSomething(err,data) {
	if(data) {
		for (i=0; i<data.length;i++) {
			if(path.extname(data[i]) == ext) {
				console.log(data[i]);
			}
		}
	}
}
