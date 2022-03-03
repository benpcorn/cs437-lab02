document.onkeydown = updateKey;
document.onkeyup = resetKey;

var flask_addr = "http://192.168.4.160:5000"

function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        postMoveRequest("forward");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        postMoveRequest("backward");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        postMoveRequest("left");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        postMoveRequest("right");
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

function postMoveRequest(direction){
    axios.post(flask_addr + '/api/v1/move', {
        direction: direction,
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
}

function getVehicleVitals(){
    axios.get(flask_addr + '/api/v1/vitals')
    .then(function (response) {
        console.log(response);
        document.getElementById("servo1").innerText = response["data"]["servo1_angle"];
        document.getElementById("temperature").innerText = response["data"]["temp"];
        document.getElementById("us_dist").innerText = response["data"]["us_dist"];
        document.getElementById("servo0").innerText = response["data"]["servo0_angle"];
    })
    .catch(function (error) {
        console.log(error);
    })
}

var intervalId = window.setInterval(function(){
    console.log('GET: Vehicle Vitals')
    getVehicleVitals()
  }, 5000);