
var sum = 0;
// console.log(process.argv);
for (i=2;i<process.argv.length;i++) {
	var arg=parseInt(process.argv[i]);
	if (arg != "NaN") sum += arg;
}

console.log(sum);