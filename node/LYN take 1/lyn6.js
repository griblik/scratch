var myModule = require('./lyn6_module.js');

myModule(process.argv[2], process.argv[3], function(err, data) {
	if(err) {
		console.log(err);
	} else {
		for(i=0;i<data.length;i++) {
			console.log(data[i]);
		}
	}

});