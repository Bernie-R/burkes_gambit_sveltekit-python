<script>
  import { createEventDispatcher } from 'svelte';
  import Cookies from 'js-cookie';
  import "tailwindcss/tailwind.css";

  const dispatch = createEventDispatcher();

  let playerName = "";
  export let roomName;
  export let server_state = 0;
  export let receivedData;

  $: if (receivedData) {
    if (receivedData.type == "createServer"){
    
    Cookies.set("playerName", receivedData.current_player); // move to store or find a better storing solution
    Cookies.set("roomName", receivedData.id);
    Cookies.set("user_id", receivedData.user_id);

    const send_data = { playerName: receivedData.current_player, roomName: receivedData.id, user_id: receivedData.user_id };
    dispatch('send', { type: "lobbyUpdate", content: send_data });
  }
  else {
    server_state = 1
  }
}

  const createServer = () => {
    dispatch('send', { type: "createServer", content: playerName });
  };

  const joinRoom = () => {
    dispatch('send', { type: "joinRoom", content: { roomName, playerName } });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
  };
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
        <label
          for="player-name-input"
          class="block text-gray-700 font-bold mb-2"
        >
          Player Name
        </label>
        <input
          id="player-name-input"
          type="text"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          bind:value={playerName}
          required
        />
      </div>
      <button
      class="bg-blue-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded-r-none focus:outline-none focus:shadow-outline"
      on:click={joinRoom}
      disabled={!roomName || !playerName}
      title={!roomName || !playerName ? "Fill in both room name and player name to join a room": ""}
        style={!roomName || !playerName ? 'opacity: 50%; cursor: not-allowed;' : ''}    
         >
      Join Room
    </button>
    <button
      class="bg-green-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      on:click={createServer}
      disabled={!playerName}
      title={!playerName ? "Fill in player name to create a new room" : ""}
      style={!playerName ? 'opacity: 50%; cursor: not-allowed;' : ''}
          >
      Create a New Room
    </button>
    </form>
  </div>
</main>
