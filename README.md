Chunked Transfer Encoding
```
curl -N http://localhost:8000/chunked
```

WebSocket
```
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (event) => console.log("Received:", event.data);
```