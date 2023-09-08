<script>
  import { onMount } from "svelte";
  import JoinGame from "./Components/join/JoinGame.svelte";
  import Lobby from "./Components/lobby/Lobby.svelte";
  import Game from "./Components/game/Game.svelte";
  import webSocket from "$lib/websocket";
  import Cookies from 'js-cookie';


  let wsClient;
  let server_state = 0;
  let roomName;
  let receivedData;
  let user_id;
  let reconnect_data

  onMount(() => {
    wsClient = webSocket();

    wsClient.on("message", handleWebSocketMessage);

    wsClient.on("error", (error) => {
      console.log("websocket error", error);
    });

    wsClient.on("open", () => { //When websocket connection dies, this updates websocket connection in server
      user_id = Cookies.get("user_id");
      reconnect_data = { type: "reconnect", content: {user_id : user_id, roomName : roomName } }
      wsClient.send(JSON.stringify(reconnect_data));
    });

    wsClient.on("close", () => {
      console.log("websocket connection closed");
    });
  });


  function handleWebSocketMessage(event) {
    if (event.data !== "False"){
      const data = JSON.parse(event.data);
      receivedData = data;
    }}

  function handleSendEvent(event) {
    const messageToSend = JSON.stringify(event.detail);
    wsClient.send(messageToSend);
    console.log(messageToSend)
  }

</script>

{#if server_state == 0}
  <JoinGame on:send={handleSendEvent} bind:server_state bind:roomName bind:receivedData/>
{:else if server_state == 1}
  <Lobby on:send={handleSendEvent} bind:server_state bind:receivedData/>
{:else if server_state == 2}
  <Game/>
{/if}