var fs = require('fs');

var infile = fs.readFile(process.argv[2],'utf-8',doSomething);

function doSomething(err,data) {
	console.log(data.split('\n').length - 1);
}
