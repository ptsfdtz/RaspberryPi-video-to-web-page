const socket = new WebSocket("ws://192.168.10.103:12345");

const leftStick = document.getElementById("LeftStick");
const rightStick = document.getElementById("RightStick");
const l2 = document.getElementById("L2");
const r2 = document.getElementById("R2");
const radius = parseInt(leftStick.getAttribute("r"));

function updateView({ left, right, L2, R2 }) {
  const scale = radius * 0.4;
  leftStick.setAttribute("cx", left.x * scale);
  leftStick.setAttribute("cy", left.y * scale);

  rightStick.setAttribute("cx", right.x * scale);
  rightStick.setAttribute("cy", right.y * scale);

  const leftOpacity = Math.min(Math.pow(left.x, 2) + Math.pow(left.y, 2), 1);
  const rightOpacity = Math.min(Math.pow(right.x, 2) + Math.pow(right.y, 2), 1);

  leftStick.style.fill = `rgba(0,0,0,${leftOpacity})`;
  rightStick.style.fill = `rgba(0,0,0,${rightOpacity})`;

  const L2Opacity = L2;
  const R2Opacity = R2;

  l2.style.fill = `rgba(0,0,0,${L2Opacity})`;
  r2.style.fill = `rgba(0,0,0,${R2Opacity})`;
}

socket.onopen = function () {
  console.log("Connected to server");
  requestJoystickData();
};

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  const left = { x: data.left_stick[0], y: data.left_stick[1] };
  const right = { x: data.right_stick[0], y: data.right_stick[1] };
  const L2 = data.triggers[1];
  const R2 = data.triggers[0];

  updateView({ left, right, L2, R2 });

  setTimeout(requestJoystickData, 50);
};

socket.onerror = function (error) {
  console.log("WebSocket Error: " + error);
};

socket.onclose = function () {
  console.log("WebSocket connection closed");
};

function requestJoystickData() {
  socket.send("get_joystick_data");
}
