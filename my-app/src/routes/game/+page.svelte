<script>
    import { createEventDispatcher } from 'svelte';
    import "tailwindcss/tailwind.css";
    import thunder from '$lib/images/thunder.png';
    import heart from '$lib/images/heart.png';
    import dice from '$lib/images/dice.png';

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
</script>


<!-- Header -->
<header class="bg-gray-800 py-6 relative z-30">
  <div class="container mx-auto flex justify-between items-center px-6">
    <h1 class="text-xl font-bold text-white">Room 1234</h1>
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

  <div class="flex items-center justify-center h-screen">
    <img src={dice} alt="middle image" class="h-48">
  </div>

  {#if isCharacterShown}
  <div class="fixed inset-0 bg-black bg-opacity-50 z-20">
    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50">
      <div class="bg-white p-4 rounded shadow w-4/5">
        <p>Some text goes here...</p>
      </div>
    </div>
  </div>
{/if}

{#if isPlayersShown}
<div class="fixed inset-0 bg-black bg-opacity-50 z-20">
    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50">
      <div class="bg-white p-4 rounded shadow w-4/5">
        <p>Some text goes here...</p>
      </div>
    </div>
  </div>
{/if}

  <div class="fixed bottom-40 left-1/2 transform -translate-x-1/2">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Roll the Dice</button>
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
