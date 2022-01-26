const webSocketsServerPort = 8000;
const webSocketServer = require('websocket').server;
const http = require('http');
// Spinning the http server and the websocket server.
const server = http.createServer();
server.listen(webSocketsServerPort);
const wsServer = new webSocketServer({ httpServer: server });


const WebSocket = require('ws');
const apollo = new WebSocket(`ws://localhost:8888/websocket`);
apollo.binaryType = "arraybuffer";

// Listen for messages
apollo.addEventListener("message", function (event) {
    if(event.data instanceof ArrayBuffer) {
        // binary frame
        const view = new DataView(event.data);
        console.log(view.getInt32(0));
    } else {
        // text frame
        console.log(event.data);
    }
});

apollo.onopen = () => {
    console.log("Apollo Connection open ...");
    var command = { type: 'HMIAction', action: "START_MODULE", value: "Planning" };
    apollo.send(JSON.stringify(command));
    var command = { type: 'HMIAction', action: "START_MODULE", value: "Prediction" };
    apollo.send(JSON.stringify(command));
}
apollo.onmessage = function(evt) {
  console.log( "Received Message: " + evt.data);
  // apollo.close();
}
apollo.onclose = () => {
    console.log("Apollo Connection closed.");
}





wsServer.on('request', function(request) {
    const connection = request.accept(null, request.origin);
    connection.on('message', function(message) {
      console.log('Received Message:', message.utf8Data);
      if(message.utf8Data.indexOf('CMD') != -1){
        console.log('A command received')
        
      }
      
      connection.sendUTF('Hi this is WebSocket server!');
    });
    connection.on('close', function(reasonCode, description) {
        console.log('Client has disconnected.');
    });
});


