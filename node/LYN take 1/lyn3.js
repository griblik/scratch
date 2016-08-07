var fs = require('fs');
var inputFile = fs.readFileSync(process.argv[2]);
console.log(inputFile.toString().split('\n').length-1);