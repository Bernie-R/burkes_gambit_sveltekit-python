<script>
    import { onMount } from "svelte";
    import { createEventDispatcher } from 'svelte';
    import Cookies from "js-cookie";
    import webSocket from "$lib/websocket";
    import { triggerRoll } from './components/store.js';


    import Players from "./components/players.svelte";
    import Character from "./components/character.svelte";
    import Dice from "./components/DiceRoller.svelte";

    import "tailwindcss/tailwind.css";
    
    import thunder from '$lib/images/thunder.png';
    import heart from '$lib/images/heart.png';
    import dice from '$lib/images/dice.png';

    
    let playerName = "";
    let roomName = "";
    let players = [];
    let wsClient;
    let wsResponse;
    let start_data;
    let character = "";
    let character_text = "";


    async function waitForMessage(wsClient, type) {
      return new Promise((resolve) => {
        const handleMessage = (event) => {
          const data = JSON.parse(event.data);
          resolve(data);
        };
        wsClient.on("message", handleMessage);
      });
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

    playerName = Cookies.get("playerName");
    roomName = Cookies.get("roomName");

    wsClient.send(JSON.stringify({ type: "gameStart", content: roomName }));
    start_data = await waitForMessage(wsClient, "players");

    players = Object.keys(start_data.players);

    const player = start_data.players[playerName]; // retrieve the player object based on the name
    character = player.character; // retrieve the character property of the player
    character_text = player.description;



    wsClient.on("close", () => {
      console.log("websocket connection closed");
    });
  });
});




    const dispatch = createEventDispatcher();

    let isCharacterShown = false;
    let isPlayersShown = false;

    function toggleCharacter() {
    isCharacterShown = !isCharacterShown;
    if (isCharacterShown) {
      dispatch('showCharacter');
      isPlayersShown = false;
      dispatch('hidePlayers');
    } else {
      dispatch('hideCharacter');
    }
  }

  function togglePlayers() {
    isPlayersShown = !isPlayersShown;
    if (isPlayersShown) {
      dispatch('showPlayers');
      isCharacterShown = false;
      dispatch('hideCharacter');
    } else {
      dispatch('hidePlayers');
    }
  }
  
function rollDice() {
    // Set the triggerRoll store value to true
    triggerRoll.set(true);

    // Reset the triggerRoll store value to false after a short delay
    setTimeout(() => {
      triggerRoll.set(false);
    }, 100);
  }

</script>
<!-- Header -->
<title>Lobby: {roomName}</title>

<header class="bg-gray-800 py-6 relative z-30">
  <div class="container mx-auto flex justify-between items-center px-6">
    <h1 class="text-xl font-bold text-white">Room {roomName}</h1>
    <nav>
      <ul class="flex space-x-4">
        <li><a href="#" class="text-gray-300 hover:text-white" on:click={toggleCharacter}>Character</a></li>
        <li><a href="#" class="text-gray-300 hover:text-white" on:click={togglePlayers}>Players</a></li>
      </ul>
    </nav>
  </div>
</header>

<!-- Body -->
<body>
  <div class="container mx-auto flex justify-between items-center px-6">
    <div class="flex items-center">
      <img src={thunder} alt="image 1">
      <img src={thunder} alt="image 2">
      <img src={thunder} alt="image 3">
      <img src={thunder} alt="image 4">
      <img src={thunder} alt="image 5">
    </div>
    <div class="flex items-center">
      <img src={heart} alt="heart" class="w-6 h-6">
      <img src={heart} alt="heart" class="w-6 h-6">
    </div>
  </div>

  <Dice/>

  {#if isCharacterShown}
    <Character character_text = {character_text} character = {character}/>
  {/if}

{#if isPlayersShown}
  <Players players = {players}, player_data = {start_data}/>
{/if}

  <div class="fixed bottom-40 left-1/2 transform -translate-x-1/2">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={rollDice}>Roll the Dice</button>
  </div>
</body>

<!-- Style -->
<style>
  img {
    width: 35px;
    height: 35px;
  }

  .fixed {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
  }

  body {
    overflow: hidden;
  }

</style>
