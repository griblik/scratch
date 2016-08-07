
var fs = require('fs');
var inputFile = fs.readFile(process.argv[2], 'utf8', callback);

function callback(err, data) {
	if(err) {
		console.log('Error occurred: ' + err);
		return;
	} else {
		console.log(data.split('\n').length -1);
	}
}