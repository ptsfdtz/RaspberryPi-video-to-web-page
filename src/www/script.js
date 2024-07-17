const video = document.getElementById("video");
const leftStick = document.getElementById("LeftStick");
const rightStick = document.getElementById("RightStick");
const l2 = document.getElementById("L2");
const r2 = document.getElementById("R2");
const l1 = document.getElementById("L1");
const r1 = document.getElementById("R1");

const radius = parseInt(leftStick.getAttribute("r"));

const wsVideo = new WebSocket("ws://192.168.10.103:8000");
const wsJoystick = new WebSocket("ws://192.168.10.103:8001");

wsVideo.binaryType = "arraybuffer";

wsVideo.onmessage = function (event) {
  const arrayBuffer = event.data;
  const blob = new Blob([arrayBuffer], { type: "image/jpeg" });
  const url = URL.createObjectURL(blob);
  video.src = url;
};

wsVideo.onopen = function () {
  console.log("WebSocket connection for video stream established");
};

wsVideo.onclose = function () {
  console.log("WebSocket connection for video stream closed");
};

wsVideo.onerror = function (error) {
  console.log("WebSocket Error (video stream): " + error);
};

wsJoystick.onopen = function () {
  console.log("Connected to joystick server");
  requestJoystickData();
};

wsJoystick.onmessage = function (event) {
  const data = JSON.parse(event.data);
  const left = { x: data.left_stick[0], y: data.left_stick[1] };
  const right = { x: data.right_stick[0], y: data.right_stick[1] };
  const L2 = data.triggers[1];
  const R2 = data.triggers[0];
  const L1 = data.RB;
  const R1 = data.LB;

  updateView({ left, right, L2, R2, L1, R1 });

  setTimeout(requestJoystickData, 50);
};

wsJoystick.onerror = function (error) {
  console.log("WebSocket Error (joystick): " + error);
};

wsJoystick.onclose = function () {
  console.log("WebSocket connection for joystick data closed");
};

function requestJoystickData() {
  wsJoystick.send("get_joystick_data");
}

function updateView({ left, right, L2, R2, L1, R1 }) {
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

  const L1Opacity = L1;
  const R1Opacity = R1;
  l1.style.fill = `rgba(0,0,0,${L1Opacity})`;
  r1.style.fill = `rgba(0,0,0,${R1Opacity})`;
}
