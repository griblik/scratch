var total = 0;
// console.log(process.argv);
for (i=2;i<process.argv.length;i++) {
//	console.log(process.argv[i]);
	total += Number(process.argv[i]);
}
console.log(total);
