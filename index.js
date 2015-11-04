var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var readline = require('readline');

app.get('/', function(req, res){
  res.sendFile(__dirname + '/newgametest.html');
});

function getusermove(){
	var rl = readline.createInterface({
		input: process.stdin,
		output: process.stdout
	});
	rl.question("Input User Move (rowcol format) ", function(answer) {
		io.emit('usermove', answer);
		console.log("User Move1:", answer);
		rl.close();
	});
}

io.on('connection', function(socket){
	//io.emit('this', 'stuff happened');
	console.log('a user connected');
	socket.on('aimove', function(msg){
		io.emit('aimove', msg);
		console.log('AI Move: ',msg);
	});
	
	socket.on('new_user_move_found', function(answer){
		io.emit('usermove', answer);
		console.log("User Move from Img Processor:", answer);
	});
	
	socket.on('get_board_state', function(msg){
		io.emit('get_board_state');
		console.log("get_board_state request from app");
	});
	
	// this will be replaced by img processor
	socket.on('aimoveend', function(){
		//io.emit('aimove', msg);
		console.log('AI Move over. Need new user move.');
		//getusermove();
		io.emit('get_user_move');
	});
	
	// this will be replaced by img processor
	socket.on('getnewusermove', function(){
		//getusermove();
		io.emit('get_user_move');
	});
	
	socket.on('game_reset', function(msg){
		console.log('Game Reset Occurred');
	});
	
	socket.on('game_over', function(msg){
		console.log('Game End Occurred');
	});
	
	socket.on('disconnect', function () {
		io.emit('disconnect');
		console.log('a user disconnected');
	});
	
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
