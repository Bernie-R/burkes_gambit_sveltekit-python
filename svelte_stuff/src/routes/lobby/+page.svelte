<!-- svelte_stuff\src\routes\lobby\+page.svelte -->
<script>
  import webSocket, { closeConnection } from "$lib/websocket";
  import { onMount, onDestroy } from "svelte";
  import { goto } from "$app/navigation";
  import { playerNameStore, roomNameStore } from "../store";
  import { socketData } from "$lib/websocket";
  import Spaceship from "$lib/images/SpaceShip.png";

  let playerName = "";
  let roomName = "";
  let wsClient;
  let lobbystatus = 1;
  let players = { player_list: [] };
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

<main class="space-background">
  <div class="form-card flex flex-col">
    <h2 class="text-3xl font-bold mb-4 text-white">
      Lobby - {roomName}
    </h2>
    {#if players.admin === playerName}
      {#if players.player_list && players.player_list.length === 4}
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4"
          on:click={startGame}>Start Game</button
        >
      {:else}
        <p class="block text-white font-bold mb-2">
          Waiting for 4 players to connect
        </p>
      {/if}
    {:else}
      <p class="block text-white font-bold mb-2">
        Please wait for the host to start the game
      </p>
    {/if}
    <h3 class="block text-white font-bold mb-2">Players:</h3>

    <ul class="grid grid-cols-1 gap-2">
      {#each players.player_list || [] as player}
        <li class="flex items-center space-x-2">
          <span class="block text-white mb-2">{player}</span>
        </li>
      {/each}
    </ul>
  </div>

  <img class="spaceship" src={Spaceship} alt="Spaceship" />
</main>

<style>
  html,
  body {
    height: 100%; /* Ensure html and body take up full height */
    margin: 0; /* Remove default margin */
  }

  .space-background {
    min-height: 100vh; /* Use viewport height for consistent sizing */
    width: 100vw; /* Use viewport width for consistent sizing */
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .form-card {
    background-color: rgba(0, 0, 0, 0.7); /* Dark and transparent */
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow:
      0 4px 6px -1px rgba(0, 0, 0, 0.1),
      0 2px 4px -1px rgba(0, 0, 0, 0.06);
    position: relative; /* To position the spaceship */
    z-index: 10; /* Ensure card is above the background */
  }

  .spaceship {
    animation: flying 10s ease-in-out alternate infinite;
    position: absolute;
    bottom: -5%; /* Adjust position as needed */
    left: 34%;
    transform: translateX(-50%) scaleX(-1); /* Center and rotate */
    z-index: 1; /* Ensure spaceship is below the card */
  }

  @keyframes spaceScroller {
    from {
      background-position: 0 0;
    }
    to {
      background-position: -1000px 0;
    }
  }

  @keyframes flying {
    from {
      transform: translate(20px, -20px) scaleX(-1) rotate(-184deg);
    }
    to {
      transform: translate(-10px, 20px) scaleX(-1) rotate(-176deg);
    }
  }
</style>
