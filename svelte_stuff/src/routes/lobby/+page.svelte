<!-- svelte_stuff\src\routes\lobby\+page.svelte -->
<script>
  import webSocket, { closeConnection } from "$lib/websocket";
  import { onMount, onDestroy } from "svelte";
  import { goto } from "$app/navigation";
  import { playerNameStore, roomNameStore } from "../store";
  import { socketData } from "$lib/websocket";

  let playerName = "";
  let roomName = "";
  let wsClient;
  let lobbystatus = 1;
  let players = [];
  let response;
  let unsubSocketData = () => {};

  playerNameStore.subscribe((value) => {
    playerName = value;
  });

  roomNameStore.subscribe((value) => {
    roomName = value;
  });

  async function startGame() {
    if (players.admin === playerName && players.player_list.length === 4) {
      wsClient.send(JSON.stringify({ type: "gameStart", content: roomName }));
    } else {
      console.warn("Cannot start game: conditions not met.");
    }
  }

  onMount(async () => {
    wsClient = webSocket();

    unsubSocketData = socketData.subscribe(async (data) => {
      if (data) {
        try {
          const response = JSON.parse(data);
          if (response.type === "players") {
            players = response.content;
            lobbystatus = players.running;
          } else if (response.type === "gameState") {
            goto("/game");
          }
        } catch (error) {
          console.log(error);
        }
      }
    });

    // Initial join to get the initial lobby state
    const data = { playerName: playerName, roomName: roomName };
    wsClient.send(JSON.stringify({ type: "lobbyUpdate", content: data }));
  });

  onDestroy(() => {
    // Cleanup listeners and interval on component destroy
    unsubSocketData();
  });
</script>

<title>Lobby: {roomName}</title>

<div class="min-h-screen flex flex-col justify-center items-center bg-gray-100">
  <div
    class="w-11/12 sm:w-4/5 md:w-3/4 lg:w-2/3 xl:w-1/2 bg-white rounded-lg shadow-lg"
  >
    <div class="px-6 py-8">
      <h2 class="text-3xl font-semibold text-gray-800 mb-4">
        Lobby - {roomName}
      </h2>
      {#if players.admin === playerName}
        {#if players.player_list.length === 4}
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4"
            on:click={startGame}>Start Game</button
          >
        {:else}
          <p class="text-gray-600 mb-8">Waiting for 4 players to connect</p>
        {/if}
      {:else}
        <p class="text-gray-600 mb-8">
          Please wait for the host to start the game
        </p>
      {/if}
      <h3 class="text-lg font-medium text-gray-800 mb-2">Players:</h3>

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
