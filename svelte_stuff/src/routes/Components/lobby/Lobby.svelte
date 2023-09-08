<script>
  import Cookies from 'js-cookie';
  import { onMount } from "svelte";
  import { createEventDispatcher } from 'svelte';
  import "tailwindcss/tailwind.css";


  const playerName = Cookies.get("playerName");
  let roomName = Cookies.get("roomName");
  let user_id = Cookies.get("user_id");
  let player_list = [];
  export let receivedData;
  export let server_state = 1;
  let admin;

  $: if (receivedData) {
    if (receivedData.type != "gameStart"){
      player_list = receivedData.player_list
      if (Cookies.get("playerName") == receivedData.admin) {
          admin = true
        }
      }
    if (receivedData.type == "gameStart"){
      server_state = 2
    }
  }


  const dispatch = createEventDispatcher();

  function startGame() {
    dispatch('send', { type: "gameStart", content: roomName });
  }

  function quick_add() {
    dispatch('send', { type: "debug", content: roomName });
  }

</script>

<p>{player_list}</p>

  <title>Lobby: {roomName}</title>
  
  
  <div class="min-h-screen flex flex-col justify-center items-center bg-gray-100">
    <div class="w-11/12 sm:w-4/5 md:w-3/4 lg:w-2/3 xl:w-1/2 bg-white rounded-lg shadow-lg">
      <div class="px-6 py-8">
        <h2 class="text-3xl font-semibold text-gray-800 mb-4">Lobby - {roomName}</h2>
        {#if admin}
          {#if player_list.length >= 4}
            <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4" on:click={startGame}>Start Game</button>
          {:else}
            <p class="text-gray-600 mb-8">Waiting for 4 players to connect</p>
          {/if}
        {:else}
          <p class="text-gray-600 mb-8">Please wait for the host to start the game</p>
        {/if}

        <h3 class="text-lg font-medium text-gray-800 mb-2">Players: </h3>
  
        <ul class="grid grid-cols-1 gap-2">
          {#each player_list as player}
           
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
  <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4" on:click={quick_add}>quick add</button>

</div>