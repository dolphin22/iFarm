$(document).ready(function(){
	var socket = io('http://' + document.domain + ':' + location.port);
	socket.emit('server', 'request sent');
	socket.on('client', function(data){
		$('#targettemperature').val(data['targettemperature']);
		$('#starttime').val(data['starttime']);
		$('#endtime').val(data['endtime']);
	});

	$('#settemperature').click(function(event){
		socket.emit('settemperature', $('#targettemperature').val());
		return false;
	});
	$('#setstarttime').click(function(event){
		socket.emit('setstarttime', $('#starttime').val());
		return false;
	});
	$('#setendtime').click(function(event){
		socket.emit('setendtime', $('#endtime').val());
		return false;
	});

});
