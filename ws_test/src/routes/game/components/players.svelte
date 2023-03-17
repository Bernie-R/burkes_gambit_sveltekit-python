<script>
  export let players;

  function toggleInfoBox(event) {
    const infoBox = event.currentTarget.querySelector(".info-box");
    infoBox.classList.toggle("hidden");
  }

  function handleKeyDown(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      toggleInfoBox(event);
    }
  }
</script>

<!-- Add a div to display the player list and info box -->
<div class="fixed top-0 left-0 h-full w-36 bg-gray-800 text-white pt-16 border-r border-gray-900 transition-all duration-500 ease-in-out overflow-auto">
  <ul>
    <!-- Use the each block to iterate over the players array and display each player -->
    {#each players as player}
      <li>
        <!-- Add a role attribute for accessibility -->
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
          <div class="info-box hidden absolute top-full left-1/2 transform -translate-x-1/2 p-4 bg-white rounded-lg shadow-lg border border-gray-300 z-10">
            <p>test box</p>
          </div>
        </div>
      </li>
    {/each}
  </ul>
</div>
