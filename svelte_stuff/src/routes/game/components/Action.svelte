<!-- svelte_stuff\src\routes\game\components\Action.svelte -->
<script>
    import { onDestroy } from "svelte";
    import Dice from "./Dice.svelte";
    import diceData from "$lib/jsons/diceData.json";
    import webSocket, { closeConnection } from "$lib/websocket";

    import Dice1HP from "$lib/images/Dice1HP.png";
    import DiceScanRL from "$lib/images/DiceScanRL.png";
    import DicePower from "$lib/images/DicePower.png";
    import DiceCancelPower from "$lib/images/DiceCancelPower.png";
    import DiceShuffle from "$lib/images/DiceShuffle.png";
    import DiceScanID from "$lib/images/DiceScanID.png";
    import DiceInstaKill from "$lib/images/DiceInstaKill.png";
    import DiceQuarantine from "$lib/images/DiceQuarantine.png";
    import DiceCancel from "$lib/images/DiceCancel.png";
    import DiceScanAny from "$lib/images/DiceScanAny.png";

    export let gameLoopData;
    export let playerName;
    export let roomName;
    let face_value;
    let all_face_values;
    let latest_dice;
    let reservedDie = null;
    let canReroll = false;
    let rolling = false;
    let targetPlayer = null;
    let showTargetSelection = false;
    let players = [];
    let showLRScanSelection = false;
    let leftPlayer = null;
    let rightPlayer = null;
    let scanResult = null;
    let idCheckResult = null;
    let last_dice_roller = null;
    let game_history = [];
    let lastScan = null;
    let scanResults = null;
    let showScanHistoryModal = false;
    let playerScanHistory = [];
    let currentScanMessage = null;
    let currentIdCheckMessage = null;
    let showGameHistoryModal = false;
    let showScanAnySelection = false;

    $: console.log(game_history);

    $: if (gameLoopData && gameLoopData.current_dice) {
        face_value = gameLoopData.current_dice.face_value;
        all_face_values = gameLoopData.current_dice.all_faces_value;
        latest_dice = gameLoopData.current_dice;
        last_dice_roller = gameLoopData.current_dice.rolled_by;
        // Clear current messages when a new dice is rolled
        currentScanMessage = null;
        currentIdCheckMessage = null;
    } else {
        latest_dice = null;
        face_value = null;
        all_face_values = null;
        last_dice_roller = null;
    }

    $: if (gameLoopData) {
        players = gameLoopData.players.filter((p) => !p.is_dead);
        game_history = gameLoopData.history;
    }

    $: if (gameLoopData && gameLoopData.players) {
        const currentPlayerIndex = gameLoopData.players.findIndex(
            (p) => p.name === playerName,
        );
        if (currentPlayerIndex !== -1) {
            leftPlayer =
                gameLoopData.players[
                    (currentPlayerIndex - 1 + gameLoopData.players.length) %
                        gameLoopData.players.length
                ].name;
            rightPlayer =
                gameLoopData.players[
                    (currentPlayerIndex + 1) % gameLoopData.players.length
                ].name;
        }
    }

    $: isCurrentPlayer = gameLoopData?.current_player === playerName;
    $: isEndGame = gameLoopData?.is_end_game;
    $: if (gameLoopData && gameLoopData.last_scan) {
        lastScan = gameLoopData.last_scan;
        scanResults = gameLoopData.scan_result;
        if (lastScan[0] === playerName) {
            currentScanMessage = getScanText(lastScan, scanResults);
        }
    } else {
        lastScan = null;
    }
    $: lastIdCheck = gameLoopData?.last_id_check;
    $: if (gameLoopData && gameLoopData.last_id_check) {
        if (gameLoopData.last_id_check[0] === playerName) {
            currentIdCheckMessage = getIdCheckText(gameLoopData.last_id_check);
        }
    }

    $: if (gameLoopData) {
        scanResult = gameLoopData.self.scan_result;
        idCheckResult = gameLoopData.self.id_check_result;
        // Update playerScanHistory whenever scanResult changes
        if (
            gameLoopData.last_scan &&
            gameLoopData.last_scan[0] === playerName
        ) {
            playerScanHistory = [
                ...playerScanHistory,
                getScanText(gameLoopData.last_scan, scanResult),
            ];
        }
    }

    const numberToImage = {
        1: Dice1HP,
        2: DiceScanRL,
        3: DicePower,
        4: DiceCancelPower,
        5: DiceShuffle,
        6: DiceScanID,
        7: DiceInstaKill,
        8: DiceQuarantine,
        9: DiceCancel,
        10: DiceScanAny,
    };

    const ws = webSocket();

    async function rollAllDice() {
        if (!isCurrentPlayer || rolling || reservedDie) return;
        rolling = true;
        try {
            const content = {
                roomName: roomName,
                player: playerName,
            };
            ws.send(JSON.stringify({ type: "rollDice", content: content }));
            canReroll = true;
        } catch (error) {
            console.error("WebSocket error:", error);
        } finally {
            setTimeout(() => (rolling = false), 1000);
        }
    }

    async function rerollDice() {
        if (!isCurrentPlayer || !canReroll || rolling) return;
        rolling = true;
        try {
            const content = {
                roomName: roomName,
                player: playerName,
                reroll: true,
            };
            ws.send(JSON.stringify({ type: "rollDice", content: content }));
            canReroll = false;
        } catch (error) {
            console.error("WebSocket error:", error);
        } finally {
            setTimeout(() => (rolling = false), 1000);
        }
    }

    async function resolveDice(resolve = true) {
        if (!isCurrentPlayer || rolling || !face_value) return;
        try {
            const content = {
                roomName: roomName,
                player: playerName,
                resolve,
                targetPlayer: targetPlayer,
            };
            ws.send(JSON.stringify({ type: "resolveDice", content: content }));
            targetPlayer = null;
            showTargetSelection = false;
            showLRScanSelection = false;
            showScanAnySelection = false;
            canReroll = false;
        } catch (error) {
            console.error("WebSocket error:", error);
        }
    }

    async function submitVote(vote) {
        if (!isCurrentPlayer || rolling || !isEndGame) return;
        try {
            const content = {
                roomName: roomName,
                player: playerName,
                vote: vote,
            };
            ws.send(JSON.stringify({ type: "submitVote", content: content }));
        } catch (error) {
            console.error("WebSocket error:", error);
        }
    }
    async function resolveEndGame() {
        if (!isCurrentPlayer || rolling || !isEndGame) return;
        try {
            const content = {
                roomName: roomName,
            };
            ws.send(
                JSON.stringify({ type: "resolveEndGame", content: content }),
            );
        } catch (error) {
            console.error("WebSocket error:", error);
        }
    }

    async function reserveDieAction() {
        if (!isCurrentPlayer || rolling || !face_value) return;
        try {
            const content = {
                roomName: roomName,
                player: playerName,
                reserve: true,
                die: latest_dice,
            };
            ws.send(JSON.stringify({ type: "reserveDice", content: content }));
            canReroll = false;
        } catch (error) {
            console.error("WebSocket error:", error);
        }
    }

    function handleAction(dieFace) {
        if (!isCurrentPlayer || rolling || !face_value) return;

        switch (dieFace) {
            case 1:
            case 6:
            case 7:
            case 8:
                showTargetSelection = true;
                break;
            case 2:
                showLRScanSelection = true;
                break;
            case 10:
                showScanAnySelection = true;
                break;
            default:
                resolveDice(true);
                break;
        }
    }

    function selectLRTarget(player) {
        targetPlayer = player;
        resolveDice(true);
    }

    function selectTarget(player) {
        targetPlayer = player;
        resolveDice(true);
    }

    function getScanText(scanData, scanResult) {
        if (!scanData) return "";
        return `${scanData[0]} scanned ${scanData[1]} and showed ${scanResult}`;
    }

    function getIdCheckText(idCheckData) {
        if (!idCheckData) return "";
        return `${idCheckData[0]} did an ID check on ${idCheckData[1]}`;
    }

    function toggleScanHistoryModal() {
        showScanHistoryModal = !showScanHistoryModal;
    }

    function toggleGameHistoryModal() {
        showGameHistoryModal = !showGameHistoryModal;
    }

    function formatGameHistoryText(event) {
        return `${event.player}
        ${event.action === "PICK_AND_ROLL" ? "picked and rolled a dice" : ""}
                    ${event.action === "REROLL" ? "rerolled a dice" : ""}
                    ${event.action === "RESERVE_DICE" ? "reserved a dice" : ""}
                    ${
                        event.action === "USE_DICE_ACTION"
                            ? `used dice action ${event.dice_face}`
                            : ""
                    }
                    ${event.dice_face ? `and got ${event.dice_face}` : ""}`;
    }
</script>

<div class="game-container">
    <div class="game-content">
        {#if isCurrentPlayer}
            {#if !face_value}{:else}
                <Dice face={numberToImage[face_value]} />
            {/if}
        {:else}
            {#if face_value}
                <Dice face={numberToImage[face_value]} />
            {/if}
            <p>It is not your turn.</p>
        {/if}
        {#if isCurrentPlayer && scanResult}
            <p>Scan Result: {scanResult}</p>
        {/if}
        {#if isCurrentPlayer && idCheckResult}
            <p>ID Check Result: {idCheckResult}</p>
        {/if}
        {#if currentScanMessage}
            <p>{currentScanMessage}</p>
        {/if}
        {#if currentIdCheckMessage}
            <p>{currentIdCheckMessage}</p>
        {/if}
        {#if reservedDie}
            <p>Reserved Die</p>
            <Dice face={numberToImage[reservedDie.face_value]} />
        {/if}
        {#if isEndGame}
            <p>END GAME</p>
        {/if}
        {#if showLRScanSelection && isCurrentPlayer}
            <div class="player-selection">
                <p>Select a Player to scan:</p>
                {#if leftPlayer}
                    <button on:click={() => selectLRTarget(leftPlayer)}
                        >Scan left ({leftPlayer})</button
                    >
                {/if}
                {#if rightPlayer}
                    <button on:click={() => selectLRTarget(rightPlayer)}
                        >Scan right ({rightPlayer})</button
                    >
                {/if}
            </div>
        {/if}
        {#if showScanAnySelection && isCurrentPlayer}
            <div class="player-selection">
                <p>Select a Player to scan:</p>
                {#each players as player}
                    <button on:click={() => selectTarget(player.name)}
                        >{player.name}</button
                    >
                {/each}
            </div>
        {/if}
        {#if showTargetSelection && isCurrentPlayer}
            <div class="player-selection">
                <p>Select a Player:</p>
                {#each players as player}
                    <button on:click={() => selectTarget(player.name)}
                        >{player.name}</button
                    >
                {/each}
            </div>
        {/if}
        {#if targetPlayer && isCurrentPlayer}
            <p>Targeted player: {targetPlayer}</p>
        {/if}
    </div>
    <footer class="action-buttons">
        {#if isEndGame && isCurrentPlayer}
            <div class="end-game-options">
                {#each players as player}
                    <button on:click={() => submitVote(player.name)}
                        >Vote for {player.name}</button
                    >
                {/each}
                <button on:click={resolveEndGame}>Resolve End Game</button>
            </div>
        {:else if isCurrentPlayer}
            <!-- If it's the current player's turn and they don't have a dice from previous turn (reservedDie) and no latest dice, only show Pick & Roll -->
            {#if !latest_dice && !reservedDie}
                <button disabled={rolling} on:click={rollAllDice}
                    >Pick & Roll Dice</button
                >
            {:else}
                <!-- If player has a newly rolled dice (latest_dice), they can re-roll and resolve -->
                {#if latest_dice}
                    <button disabled={!canReroll} on:click={rerollDice}
                        >Re-roll Dice</button
                    >
                    <button on:click={() => handleAction(face_value)}
                        >Resolve Dice</button
                    >
                    <button on:click={reserveDieAction}>Reserve Dice</button>
                {:else}
                    <!-- If player does not have a newly rolled dice, but has a reservedDie, they still need to pick and roll a new one -->
                    <button disabled={rolling} on:click={rollAllDice}
                        >Pick & Roll Dice</button
                    >
                {/if}
            {/if}
        {/if}
        <button on:click={toggleScanHistoryModal}>Show Scan History</button>
        <button on:click={toggleGameHistoryModal}>Show Game History</button>
    </footer>
</div>

{#if showScanHistoryModal}
    <div class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h2>{playerName}'s Scan History</h2>
                <button class="close-button" on:click={toggleScanHistoryModal}
                    >×</button
                >
            </div>

            <div class="modal-content">
                {#if playerScanHistory.length > 0}
                    <ul>
                        {#each playerScanHistory as scan, i}
                            <li>{scan}</li>
                        {/each}
                    </ul>
                {:else}
                    <p>No scans yet</p>
                {/if}
            </div>
        </div>
    </div>
{/if}

{#if showGameHistoryModal}
    <div class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h2>Game History</h2>
                <button class="close-button" on:click={toggleGameHistoryModal}
                    >×</button
                >
            </div>
            <div class="modal-content">
                {#if game_history.length > 0}
                    <ul>
                        {#each game_history as event, i}
                            <li>{formatGameHistoryText(event)}</li>
                        {/each}
                    </ul>
                {:else}
                    <p>No history yet</p>
                {/if}
            </div>
        </div>
    </div>
{/if}

<style>
    .game-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }

    .game-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        text-align: center;
    }
    .action-buttons {
        display: flex;
        justify-content: space-around;
        padding: 1rem;
        border-top: 1px solid #ddd;
        background-color: #f9f9f9;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .action-buttons button {
        padding: 0.75rem 1rem;
        border: 1px solid #ccc;
        background-color: #eee;
        cursor: pointer;
        border-radius: 0.3rem;
        font-size: 1rem;
        flex: 1 1 auto;
        min-width: 0;
    }
    .player-selection {
        background-color: #f0f0f0;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .player-selection p {
        margin-bottom: 0.5rem;
    }

    .player-selection button {
        padding: 0.5rem;
    }

    .action-buttons button:disabled {
        background-color: #ddd;
        cursor: not-allowed;
    }

    .end-game-options {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    @media (min-width: 768px) {
        .action-buttons {
            padding: 1.5rem;
        }
        .action-buttons button {
            font-size: 1.1rem;
            padding: 1rem 1.5rem;
        }
        .game-content {
            padding: 30px;
        }
    }

    @media (min-width: 1024px) {
        .action-buttons {
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        .game-content {
            padding: 50px;
        }
    }

    .history-log {
        margin-top: 20px;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        background-color: #f9f9f9;
    }

    .history-log h3 {
        margin-top: 0;
    }

    .history-log p {
        margin: 5px 0;
        font-size: 0.9rem;
    }
    /* Modal Styles */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .modal {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        width: 80%; /* Adjust as needed */
        max-width: 600px;
        display: flex;
        flex-direction: column;
        position: relative;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .modal-content {
        flex: 1; /* Allow the content to scroll */
        overflow-y: auto; /* Add scroll if the content is longer than the modal */
        padding-right: 1rem;
    }

    .close-button {
        background-color: transparent;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
    }
</style>
