const socket = io("/test");
const room = "test";


socket.on('connect', function () {
	console.log("test")
	socket.emit('test', {data: 'I\'m connected!'});
});

socket.on('test', function (data) {
	let testElement = document.getElementById("test");
	console.log("test2");
	console.log(testElement);
	testElement.innerHTML = data.data;
});