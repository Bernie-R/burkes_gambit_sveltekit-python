<script>
  import { onMount, onDestroy } from "svelte";
  import { goto } from "$app/navigation";
  import { playerNameStore, roomNameStore } from "./store";
  import "tailwindcss/tailwind.css";
  import webSocket, { waitForMessage } from "$lib/websocket";
  import { socketData } from "$lib/websocket";
  import { Alert } from "flowbite-svelte";

  let playerName = "";
  let roomName = "";
  let wsClient;
  let response;
  let unsubSocketData = () => {};
  let playerData;
  let errorMessage = ""; // For displaying error popup
  let showPopup = false;

  //Function to handle name restriction length
  const handleRoomNameChange = (event) => {
    const value = event.target.value;
    if (value.length <= 4) {
      roomName = value;
    } else {
      roomName = value.slice(0, 4);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
  };

  onMount(() => {
    wsClient = webSocket();
    unsubSocketData = socketData.subscribe((data) => {
      if (data) {
        try {
          playerData = JSON.parse(data);
        } catch (error) {
          console.error("Error parsing JSON:", error);
        }
      }
    });
  });

  onDestroy(() => {
    unsubSocketData();
  });

  const createServer = async () => {
    wsClient.send(
      JSON.stringify({ type: "createServer", content: playerName }),
    );

    const data = await waitForMessage("createServer");
    wsClient.off("message", (event) => {}); // Clean up message listener.

    if (data) {
      const response = data.content;
      const roomName = response.roomId;
      // Update the stores
      playerNameStore.set(playerName);
      roomNameStore.set(roomName);

      // Navigate to the lobby page
      goto("/lobby");
    }
  };

  const joinRoom = async () => {
    const data = { playerName: playerName, roomName: roomName };
    wsClient.send(JSON.stringify({ type: "joinRoom", content: data }));

    const playerData = await waitForMessage("joinRoom");
    wsClient.off("message", (event) => {}); // Clean up message listener.

    if (
      playerData &&
      playerData.content &&
      typeof playerData.content === "object" &&
      playerData.content.player_list !== false
    ) {
      // Update the stores
      playerNameStore.set(playerName);
      roomNameStore.set(roomName);

      goto("/lobby");
    } else {
      errorMessage = "Server not found. Please try with another Room Name";
      showPopup = true;
    }
  };

  function closePopup() {
    showPopup = false;
    errorMessage = "";
  }
</script>

<main class="min-h-screen flex items-center justify-center">
  <div class="bg-white p-8 rounded-lg shadow-lg relative">
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
          value={roomName}
          on:input={handleRoomNameChange}
          maxlength="4"
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
        title={!roomName || !playerName
          ? "Fill in both room name and player name to join a room"
          : ""}
        style={!roomName || !playerName
          ? "opacity: 50%; cursor: not-allowed;"
          : ""}
      >
        Join Room
      </button>
      <button
        class="bg-green-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        on:click={createServer}
        disabled={!playerName}
        title={!playerName ? "Fill in player name to create a new room" : ""}
        style={!playerName ? "opacity: 50%; cursor: not-allowed;" : ""}
      >
        Create a New Room
      </button>
    </form>
    {#if showPopup}
      <div
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
      >
        <div class="bg-white p-6 rounded shadow-lg">
          <p class="mb-4 text-lg">{errorMessage}</p>
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            on:click={closePopup}>Close</button
          >
        </div>
      </div>
    {/if}
  </div>
</main>
