<script>
  import { onMount } from "svelte";
  import { goto } from '$app/navigation';
  import "tailwindcss/tailwind.css";
  import Cookies from 'js-cookie'
  import webSocket from "$lib/websocket";


  let playerName = "";
  let wsClient;
  let wsResponse = "";
  let roomName = "";

  const handleSubmit = (event) => {
    event.preventDefault();
  };

  onMount(() => {
    wsClient = webSocket();

    wsClient.on("message", (event) => {
      wsResponse = String(event.data);
    });

    wsClient.on("error", (error) => {
      console.log("websocket error", error);
    });

    wsClient.on("open", () => {
      console.log("websocket connection established");
    });

    wsClient.on("close", () => {
      console.log("websocket connection closed");
    });
  });

  function waitForMessage(wsClient, type) {
  return new Promise((resolve) => {
    const handleMessage = (event) => {
      const data = event.data;
      resolve(data);
    };
    wsClient.on("message", handleMessage);
  });
}

const createServer = async () => {
  wsClient.send(JSON.stringify({ type: "createServer", content: playerName }));

  // Wait for the roomName message from the server
  const roomName = await waitForMessage(wsClient, "roomName");

  Cookies.set("playerName", playerName);
  Cookies.set("roomName", roomName);
  goto("/lobby");
};

  const joinRoom = async () => {
    const data = { playerName: playerName, roomName: roomName };
    wsClient.send(JSON.stringify({ type: "joinRoom", content: data}));
    // Wait for the roomName message from the server
    const check = await waitForMessage(wsClient, "joinRoom");
    if (check == "True") {
      Cookies.set("playerName", playerName);
      Cookies.set("roomName", roomName);
      goto("/lobby");
    }
  };

</script>

<main class="min-h-screen flex items-center justify-center">
  <div class="bg-white p-8 rounded-lg shadow-lg">
    <h1 class="text-3xl font-bold mb-4">Burkes Gambit</h1>
    <form on:submit={handleSubmit}>
      <div class="mb-4">
        <label for="room-name-input" class="block text-gray-700 font-bold mb-2">
          Room Name
        </label>
        <input
          id="room-name-input"
          type="text"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          bind:value={roomName}
        />
      </div>
      <div class="mb-4">
        <label
          for="player-name-input"
          class="block text-gray-700 font-bold mb-2"
        >
          Player Name
        </label>
        <input
          id="player-name-input"
          type="text"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          bind:value={playerName}
          required
        />
      </div>
      <button
      class="bg-blue-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded-r-none focus:outline-none focus:shadow-outline"
      on:click={joinRoom}
      disabled={!roomName || !playerName}
      title={!roomName || !playerName ? "Fill in both room name and player name to join a room": ""}
        style={!roomName || !playerName ? 'opacity: 50%; cursor: not-allowed;' : ''}    
         >
      Join Room
    </button>
    <button
      class="bg-green-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      on:click={createServer}
      disabled={!playerName}
      title={!playerName ? "Fill in player name to create a new room" : ""}
      style={!playerName ? 'opacity: 50%; cursor: not-allowed;' : ''}
          >
      Create a New Room
    </button>
    </form>
  </div>
</main>
