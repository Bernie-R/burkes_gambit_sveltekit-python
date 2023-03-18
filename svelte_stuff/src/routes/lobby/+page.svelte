<script>
import Cookies from 'js-cookie';
import webSocket from "$lib/websocket";
import { onMount } from "svelte";
import { goto } from '$app/navigation';


const playerName = Cookies.get("playerName");
const roomName = Cookies.get("roomName");
let wsClient;
let lobbystatus = 1;
let players = [];
let wsResponse;
let intervalId; // declare variable to hold intervalId

async function waitForMessage(wsClient, type) {
  return new Promise((resolve) => {
    const handleMessage = (event) => {
      const data = JSON.parse(event.data);
      resolve(data);
    };
    wsClient.on("message", handleMessage);
  });
}

async function joinRoom() {
  const data = { playerName: playerName, roomName: roomName };
  wsClient.send(JSON.stringify({ type: "lobbyUpdate", content: data }));
  const newPlayers = await waitForMessage(wsClient, "players");
  players = newPlayers;
  lobbystatus = players.running
  return players;
}

function startGame() {
  wsClient.send(JSON.stringify({ type: "gameStatusUpdate", content: roomName }));
}

onMount(() => {
  wsClient = webSocket();

  wsClient.on("message", (event) => {
    wsResponse = String(event.data);
  });

  wsClient.on("error", (error) => {
    console.log("websocket error", error);
  });

  wsClient.on("open", async () => {
    console.log("websocket connection established");

    // Call joinRoom immediately to get the initial list of players
    await joinRoom();

    // Clear any existing intervals and start a new one
    clearInterval(intervalId);

    intervalId = setInterval(async () => {
      if (lobbystatus === 1) {
        await joinRoom();
      }
      else {
        goto("/game");
      }
    }, 3000);

    wsClient.on("close", () => {
      clearInterval(intervalId); // clear the interval when the connection closes
      console.log("websocket connection closed");
    });
  });
});


</script>
<title>Lobby: {roomName}</title>

    <div class="min-h-screen flex flex-col justify-center items-center bg-gray-100">
      <div class="w-11/12 sm:w-4/5 md:w-3/4 lg:w-2/3 xl:w-1/2 bg-white rounded-lg shadow-lg">
        <div class="px-6 py-8">
          <h2 class="text-3xl font-semibold text-gray-800 mb-4">Lobby - {roomName}</h2>
          {#if players.admin === 1}
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4" on:click={startGame}>Start Game</button>
          <p class="text-gray-600 mb-8">Waiting for players to connect</p>

          {:else}
          <p class="text-gray-600 mb-8">Please wait for the host to start the game</p>
          {/if}
          <h3 class="text-lg font-medium text-gray-800 mb-2">Players: </h3>

          <ul class="grid grid-cols-1 gap-2">
            {#each [players.player_list] as player}
              <li class="flex items-center space-x-2">
                <div class="bg-gray-300 rounded-full h-6 w-6"></div>
                <span class="text-gray-800">{player}</span>
              </li>
            {/each}
          </ul>
          <div class="flex justify-center items-center space-x-4 mt-8">
            <div class="animate-pulse bg-gray-300 rounded-full h-16 w-16"></div>
            <div class="animate-pulse bg-gray-300 rounded-full h-16 w-16"></div>
            <div class="animate-pulse bg-gray-300 rounded-full h-16 w-16"></div>
          </div>
        </div>
      </div>
      </div>
