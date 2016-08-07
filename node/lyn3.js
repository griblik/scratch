var fs = require('fs');

var splitfile, infile = process.argv[2];
if(infile) {
	text = fs.readFileSync(infile).toString();
	splitfile = text.split('\n');
}

console.log(splitfile.length - 1);
