const socket = new WebSocket('ws://localhost:8000/ws/chat/');

socket.onopen = function () {
  console.log("Connection established!");
};

socket.onclose = function () {
  console.log("Connection closed!");
};

socket.onerror = function (error) {
  console.error(`WebSocket error: ${error.message}`);
};

export default socket;
