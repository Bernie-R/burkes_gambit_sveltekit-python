<script>
  import { writable } from 'svelte/store';

  export let character_text;
  export let character;
  export let team_text;
  export let team_name;

  const isOpen = writable(true);

  function closeInfoBox() {
    isOpen.set(false);
  }
</script>

{#if $isOpen}
  <div class="fixed inset-0 bg-black bg-opacity-50 z-20 flex justify-center items-center" on:click={closeInfoBox}>
    <div class="bg-white p-4 rounded shadow w-3/5 h-auto transform scale-125 transition-all duration-300" on:click|stopPropagation>
      <h1 class="text-lg font-bold mb-2">Role: {character}</h1>
      <p class="text-gray-700">{character_text}</p>
      <br>
      <h1 class="text-lg font-bold mb-2">Team</h1>
      <p class="text-gray-700">{team_text}</p>
    </div>
  </div>
{/if}

<style>
  .bg-black {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 9999;
  }

  .bg-white {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 1rem;
    background-color: white;
    border: 1px solid black;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    z-index: 10000;
  }
</style>
