<script>
  import { onMount, onDestroy } from "svelte";
  import { goto } from "$app/navigation";
  import { playerNameStore, roomNameStore } from "./store";
  import "tailwindcss/tailwind.css";
  import webSocket, { waitForMessage } from "$lib/websocket";
  import { socketData } from "$lib/websocket";
  import Spaceship from "$lib/images/SpaceShip.png";

  let playerName = "";
  let roomName = "";
  let wsClient;
  let response;
  let unsubSocketData = () => {};
  let playerData;
  let errorMessage = ""; // For displaying error popup
  let showPopup = false;
  let animating = false; // Flag to indicate animation is in progress

  // Function to handle name restriction length
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
    if (animating) return;
    animating = true;

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

      // Add animation classes
      const formCard = document.querySelector(".form-card");
      const spaceship = document.querySelector(".spaceship");
      if (formCard && spaceship) {
        formCard.classList.add("fade-out");
        spaceship.classList.add("fly-out");
      }

      // Navigate to the lobby page after animation delay
      setTimeout(() => {
        goto("/lobby");
        animating = false;
      }, 500); // Adjust the timeout to match the animation duration
    } else {
      animating = false;
    }
  };

  const joinRoom = async () => {
    if (animating) return;
    animating = true;

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

      // Add animation classes
      const formCard = document.querySelector(".form-card");
      const spaceship = document.querySelector(".spaceship");
      if (formCard && spaceship) {
        formCard.classList.add("fade-out");
        spaceship.classList.add("fly-out");
      }

      setTimeout(() => {
        goto("/lobby");
        animating = false;
      }, 500); // Adjust the timeout to match the animation duration
    } else {
      errorMessage = "Server not found. Please try with another Room Name";
      showPopup = true;
      animating = false;
    }
  };

  function closePopup() {
    showPopup = false;
    errorMessage = "";
  }
</script>

<main class="space-background">
  <div class="form-card flex flex-col">
    <h1 class="text-3xl font-bold mb-4 text-white">Burkes Gambit</h1>
    <form on:submit={handleSubmit}>
      <div class="mb-4">
        <label for="room-name-input" class="block text-white font-bold mb-2">
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
        <label for="player-name-input" class="block text-white font-bold mb-2">
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
        disabled={!roomName || !playerName || animating}
        title={!roomName || !playerName
          ? "Fill in both room name and player name to join a room"
          : ""}
        style={!roomName || !playerName || animating
          ? "opacity: 50%; cursor: not-allowed;"
          : ""}
      >
        Join Room
      </button>
      <button
        class="bg-green-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        on:click={createServer}
        disabled={!playerName || animating}
        title={!playerName ? "Fill in player name to create a new room" : ""}
        style={!playerName || animating
          ? "opacity: 50%; cursor: not-allowed;"
          : ""}
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
  <img class="spaceship" src={Spaceship} alt="Spaceship" />
</main>

<style>
  html,
  body {
    height: 100%; /* Ensure html and body take up full height */
    margin: 0; /* Remove default margin */
  }

  .space-background {
    min-height: 100vh; /* Use viewport height for consistent sizing */
    width: 100vw; /* Use viewport width for consistent sizing */
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .form-card {
    background-color: rgba(0, 0, 0, 0.7); /* Dark and transparent */
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow:
      0 4px 6px -1px rgba(0, 0, 0, 0.1),
      0 2px 4px -1px rgba(0, 0, 0, 0.06);
    position: relative; /* To position the spaceship */
    z-index: 10; /* Ensure card is above the background */
    transition: opacity 0.5s ease-in-out; /* Fade out transition */
  }

  .form-card.fade-out {
    opacity: 0;
  }

  .spaceship {
    animation: flying 10s ease-in-out alternate infinite;
    position: absolute;
    bottom: -5%; /* Adjust position as needed */
    left: 34%;
    transform: translateX(-50%) scaleX(-1) rotate(180deg); /* Center and rotate */
    z-index: 1; /* Ensure spaceship is below the card */
    transition: transform 0.5s ease-in-out; /* Fly out transition */
  }

  .spaceship.fly-out {
    transform: translateX(100vw) scaleX(-1) rotate(180deg); /* Move to the right */
  }

  @keyframes spaceScroller {
    from {
      background-position: 0 0;
    }
    to {
      background-position: -1000px 0;
    }
  }

  @keyframes flying {
    from {
      transform: translate(20px, -20px) scaleX(-1) rotate(-184deg);
    }
    to {
      transform: translate(-10px, 20px) scaleX(-1) rotate(184deg);
    }
  }
</style>
