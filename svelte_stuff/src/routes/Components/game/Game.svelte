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

    
    let playerName = "";
    let roomName = "";
    let players = [];
    let start_data;
    let character = "";
    let character_text = "";



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
