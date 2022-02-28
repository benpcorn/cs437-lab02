document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.3.49";   // the IP address of your Raspberry PI

var net = require('net');

console.log('Creating connection');
var client = net.createConnection({ port: server_port, host: server_addr }, () => {
    console.log('Connected to' + server_addr);
    sync();
});

function send_data(data) {
    if (data == null) {
        return
    }
    console.log('Writing data: ' + data)
    client.write(`${data}\r\n`);
}

function retrieve_data() {
    client.on('data', (data) => {
        console.log(data.toString());
    });
}

function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("68");
    }
}

function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}

function sync(){
    console.log('Setting up data sync every 50ms')
    setInterval(function(){
        retrieveData();
    }, 50);
}
