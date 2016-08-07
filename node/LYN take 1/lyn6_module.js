var fs = require('fs');
var path = require('path');


module.exports = function(pwd, ext, callback) {
	fs.readdir(pwd, function (err, data) {
		if(err) return callback(err);
		var filelist=[];
		data.forEach(function(item) {
			if (path.extname(item) == "." + ext) {
				filelist.push(item);
			}
		});
		callback(null, filelist);
	});

}

