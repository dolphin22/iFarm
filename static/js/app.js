$(document).ready(function(){
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.on('client', function(data){
		$('#targettemperature').val(data['targettemperature']);
		$('#starttime').val(data['starttime']);
		$('#endtime').val(data['endtime']);
		$('#starttime2').val(data['starttime2']);
		$('#endtime2').val(data['endtime2']);
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
	
	$('#setstarttime2').click(function(event){
		socket.emit('setstarttime2', $('#starttime2').val());
		return false;
	});
	$('#setendtime2').click(function(event){
		socket.emit('setendtime2', $('#endtime2').val());
		return false;
	});
	
	$("[name='switch1'],[name='switch2'],[name='switch3'],[name='switch4']").bootstrapSwitch();	
	setInterval(function(){
		socket.emit('getswitches');
		socket.on('receiveswitches', function(switches){
			console.log(switches)
			if(switches.switches[0] == '1') {
				$("[name='switch1']").bootstrapSwitch('state', true, true);
			} else {
				$("[name='switch1']").bootstrapSwitch('state', false, true);
			}
			if(switches.switches[1] == '1') {
				$("[name='switch2']").bootstrapSwitch('state', true, true);
			} else {
				$("[name='switch2']").bootstrapSwitch('state', false, true);
			}
			if(switches.switches[2] == '1') {
				$("[name='switch3']").bootstrapSwitch('state', true, true);
			} else {
				$("[name='switch3']").bootstrapSwitch('state', false, true);
			}
			if(switches.switches[3] == '1') {
				$("[name='switch4']").bootstrapSwitch('state', true, true);
			} else {
				$("[name='switch4']").bootstrapSwitch('state', false, true);
			}
		});
	},10000)
});
