var http = require('http');
var BufferList = require('bl');

var chunks = [];
var urls = [process.argv[2],process.argv[3],process.argv[4]];

var count = 0;
//  console.log(urls);

urls.forEach(function(url, index) {
	var bl = new BufferList(function(err, bl) {
		chunks[index] = bl.toString();
		count++;
		if(count >= 3) dump();
	});

	http.get(url, function(response) {
		response.pipe(bl);
	});
});


function dump() {
	chunks.forEach(function(item) {console.log(item)});
}
