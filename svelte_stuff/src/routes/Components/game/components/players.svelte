<script>
  import { writable } from 'svelte/store';
  
  export let players;
  export let player_data;

  const playersArray = players.replace(/,+$/, '').split(',');

  const activePlayerIndex = writable(null);

  function toggleInfoBox(event) {
    const playerIndex = playersArray.indexOf(event.currentTarget.querySelector('span').textContent);
    activePlayerIndex.set(playerIndex);
  }

  function handleKeyDown(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      const playerIndex = playersArray.indexOf(event.currentTarget.querySelector('span').textContent);
      activePlayerIndex.set(playerIndex);
    }
  }

  function closeInfoBox() {
    activePlayerIndex.set(null);
  }
</script>

{#if players}
  <div class="fixed top-0 left-0 h-full w-36 bg-gray-800 text-white pt-16 border-r border-gray-900 transition-all duration-500 ease-in-out overflow-auto">
    <ul>
      {#each playersArray as player, i}
        <li>
          <div
            role="button"
            class="flex justify-between items-center px-4 py-2 border-b border-gray-900 cursor-pointer hover:bg-gray-900"
            tabindex="0"
            on:click={toggleInfoBox}
            on:keydown={handleKeyDown}
          >
            <span>{player}</span>
            <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
              <path d="M7.293 9.293a1 1 0 0 1 1.414 0L10 10.586l1.293-1.293a1 1 0 0 1 1.414 1.414l-2 2a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 0-1.414z"/>
            </svg>
          </div>
        </li>
      {/each}
    </ul>
  </div>

  {#if $activePlayerIndex !== null}
    <div class="fixed inset-0 bg-black bg-opacity-50 z-20 flex justify-center items-center" on:click={closeInfoBox}>
      <div class="bg-white p-4 rounded shadow w-3/5 h-auto transform scale-125 transition-all duration-300" on:click|stopPropagation>
        <h1 class="text-lg font-bold mb-2">Role: {player_data.players[playersArray[$activePlayerIndex]].character}</h1>
        <p class="text-gray-700">{player_data.players[playersArray[$activePlayerIndex]].description}</p>
      </div>
    </div>
  {/if}
{/if}

<style>
  .fixed {
  z-index: 10;
}
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
