<script>
  import { onDestroy } from "svelte";
  import webSocket from "$lib/websocket";
  import { socketData } from "$lib/websocket";
  import { playerNameStore, roomNameStore } from "../store";

  import Navbar from "./components/Navbar.svelte";
  import GameStatus from "./components/GameStatus.svelte";
  import Character from "./components/Character.svelte";
  import Action from "./components/Action.svelte";

  import "tailwindcss/tailwind.css";

  let playerName = "";
  let roomName = "";
  let players = [];
  let gameLoopData;
  let character = "";
  let character_text = "";
  let numberOfPowerups;
  let health;
  let latestAction; // add this line
  let current_player;
  let wsOpen = false;
  let wsClient; // Declare wsClient outside onMount
  let team;

  playerNameStore.subscribe((value) => {
    playerName = value;
  });

  roomNameStore.subscribe((value) => {
    roomName = value;
  });

  // Function to process socket messages
  const handleSocketMessage = async (data) => {
    if (data) {
      try {
        const response = JSON.parse(data);
        if (response.type === "gameState") {
          gameLoopData = response.content;
          character = gameLoopData.self.role;
          players = gameLoopData.players;
          numberOfPowerups = gameLoopData.n_power_ups;
          health = gameLoopData.self.health;
          current_player = gameLoopData.current_player;
          latestAction = gameLoopData.latest_action; // Add this line
          team = gameLoopData.self.team;
        }
      } catch (error) {
        console.log(error);
      }
    }
  };

  // Initialize websocket connection and listener
  const setupWebSocket = () => {
    wsClient = webSocket(); // Assign wsClient here

    const unsubSocketData = socketData.subscribe(handleSocketMessage); // Subscribe to socketData
    wsClient.on("error", (error) => {
      console.log("websocket error", error);
    });

    wsClient.on("open", async () => {
      wsOpen = true;
      console.log("websocket connection established");

      let content = { roomName: roomName, player: playerName };
      console.log(content);

      wsClient.send(
        JSON.stringify({
          type: "gameState",
          content: content,
        }),
      );
    });

    return unsubSocketData; // Return the unsubscribe function
  };

  const unsubSocketData = setupWebSocket(); // Call setupWebSocket to initialize

  onDestroy(() => {
    if (wsOpen) {
      wsClient.close();
    }
    unsubSocketData(); // Call the unsubscribe function to clean up
  });

  let isCharacterShown = false;
</script>

{#if gameLoopData}
  <Navbar {roomName} {playerName} {character} {players} {team} />
  <GameStatus {numberOfPowerups} {health} {current_player} />

  <Action {gameLoopData} {playerName} {roomName} />
{/if}
{#if isCharacterShown}
  <Character {character_text} {character} />
{/if}

<!-- Style -->
<style>
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
