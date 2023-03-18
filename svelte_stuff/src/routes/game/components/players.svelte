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
          {#if activePlayerIndex === i}
            <div class="fixed inset-0 bg-black bg-opacity-50 z-20 flex justify-center items-center">
              <div class="bg-white p-4 rounded shadow w-3/5 h-auto transform scale-125 transition-all duration-300">
                <h1 class="text-lg font-bold mb-2">Role: {player_data.players[player].character}</h1>
                <p class="text-gray-700">{player_data.players[player].description}</p>
                <br>
                <h1 class="text-lg font-bold mb-2">Team</h1>
                <p class="text-gray-700">{player_data.players[player].team_text}</p>
              </div>
            </div>
          {/if}
        </li>
      {/each}
    </ul>
  </div>
{/if}
  <style>
    .info-box {
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%);
      padding: 1rem;
      background-color: white;
      border: 1px solid black;
      border-radius: 0.5rem;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
      display: none;
      z-index: 9999;
    }

    .info-box[style*="display: block"] {
      display: block;
    }
  </style>

