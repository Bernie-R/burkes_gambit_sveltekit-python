// websocket.js
import WSReqonet from 'ws-reqonet';
import { writable } from 'svelte/store';

const SERVER_URL = 'ws://localhost:8765/';

let socketInstance = null;
export const socketData = writable(null);

export default function websocket() {
    if (!socketInstance) {
        socketInstance = new WSReqonet(SERVER_URL, [], { debug: true });

        socketInstance.on('open', () => {
            console.log("websocket connection established");
        });

        socketInstance.on('error', (error) => {
            console.error("websocket error:", error);
            socketData.set(error); // Set to the store to update any component.
        });

        socketInstance.on('close', () => {
            console.log("websocket connection closed");
        });

        socketInstance.on('message', (event) => {
            console.log('WebSocket message received:', event.data);
            socketData.set(event.data); // Set to the store to update any component.
        });
    }
    return socketInstance;
}

export function closeConnection() {
    if (socketInstance) {
        socketInstance.close();
        socketInstance = null; // Reset to allow future connections.
        console.log("Websocket connection closed from service.");
    }
}


export function waitForMessage(type) {
    return new Promise((resolve) => {
        const handleMessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === type) {
                resolve(data);
            }
            else {
                console.log("Failed to recieve!")
            }
        };
        socketInstance.on('message', handleMessage);

    });
}