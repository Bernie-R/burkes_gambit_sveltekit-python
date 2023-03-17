// websocket.js
import WSReqonet from 'ws-reqonet';

const SERVER_URL = 'ws://localhost:8765/';

export default function websocket() {
 return new WSReqonet(SERVER_URL, [], { debug: true });
}