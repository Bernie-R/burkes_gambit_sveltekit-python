<script>
    // Import necessary SvelteKit and Tailwind CSS libraries
    import { onMount } from "svelte";
    import "tailwindcss/tailwind.css";
  
    // Set up initial variables for room and player names
    let roomName = "";
    let playerName = "";
  
    // Function to handle form submission
    const handleSubmit = (event) => {
      event.preventDefault();
      // Handle form submission logic here
    };
  
    // Use onMount lifecycle hook to focus on room name input when the page loads
    onMount(() => {
      document.getElementById("room-name-input").focus();
    });
  </script>
  
  <main class="min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-lg">
      <h1 class="text-3xl font-bold mb-4">Burkes Gambit</h1>
      <form on:submit={handleSubmit}>
        <div class="mb-4">
          <label for="room-name-input" class="block text-gray-700 font-bold mb-2">
            Room Name
          </label>
          <input
            id="room-name-input"
            type="text"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            bind:value={roomName}
          />
        </div>
        <div class="mb-4">
          <label for="player-name-input" class="block text-gray-700 font-bold mb-2">
            Player Name
          </label>
          <input
            id="player-name-input"
            type="text"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            bind:value={playerName}
          />
        </div>
        <button
          type="submit"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Create a New Room
        </button>
      </form>
    </div>
  </main>
  