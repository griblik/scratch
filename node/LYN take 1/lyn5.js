var fs = require('fs');
var path = require('path');

var pwd = process.argv[2];
var extension = "." + process.argv[3];

fs.readdir(pwd, function callback(err, list) {
	if (extension == undefined) {
		console.log(list);
		return;
	} else {
		for (var i=0; i<list.length; i++) {
			var item = list[i];
			if(path.extname(item) == extension) {
				console.log(item);
			}
		}
	}
});