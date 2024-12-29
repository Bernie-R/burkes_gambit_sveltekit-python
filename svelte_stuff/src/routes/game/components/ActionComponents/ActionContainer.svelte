<script>
    import { onDestroy } from "svelte";
    import DiceCard from "./DiceCard.svelte";
    import ReservedDice from "./ReservedDice.svelte";
    import TypewriterMessage from "./TypewriterMessage.svelte";
    import PlayerSelection from "./PlayerSelection.svelte";
    import ScanHistoryModal from "./ScanHistoryModal.svelte";
    import GameHistoryModal from "./GameHistoryModal.svelte";
    import ActionButtons from "./ActionButtons.svelte";
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
    import spaceMessages from "$lib/spacemessages/spaceMessages";
    import OtherPlayerDecisionModalStallEngine from "./OtherPlayerDecisionModalStallEngine.svelte";
    import OtherPlayerDecisionModalCancel from "./OtherPlayerDecisionModalCancel.svelte";
    import StallEngineDecision from "./StallEngineDecision.svelte";
    import CancelDecision from "./CancelDecision.svelte";

    export let gameLoopData;
    export let playerName;
    export let roomName;

    $: console.log(gameLoopData);

    let face_value;
    let all_face_values;
    let latest_dice;
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
    let showGameHistoryModal = false;
    let showScanAnySelection = false;
    let showDamageHealSelection = false;
    let damageHealValue = 0;
    let hoverPlayer = null;
    let canUseReservedDie = false;
    let usingReservedDie = false;
    let showStallEnginePopup = false;
    let disableAll = false;
    let showOtherPlayerDecisionStallEngine = false;
    let showOtherPlayerDecisionCancel = false;
    let cancel_pending_decision_player = false;

    // Space message and typewriter logic
    let showNotYourTurnMessage = false;
    let currentSpaceMessage = "";
    let messageInterval = null;
    let currentMessage = "";
    let currentMessageIndex = 0;
    let isTypewriting = false;
    let messageQueue = [];
    let currentMessageType = null;
    let currentMessageTimeout = null;
    let currentText = "";
    let isProcessingQueue = false;
    let showTypewrittenMessage = false;
    let cycleRunning = false;

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
        if (!isCurrentPlayer || rolling) return;
        rolling = true;
        try {
            const content = { roomName: roomName, player: playerName };
            ws.send(JSON.stringify({ type: "rollDice", content: content }));
            canReroll = true;
            canUseReservedDie = false;
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

    async function resolveDice(resolve = true, isReserved = false) {
        let dieFaceToResolve = face_value;

        if (usingReservedDie && gameLoopData?.self?.dice) {
            dieFaceToResolve = gameLoopData.self.dice.face_value;
        }

        if (!isCurrentPlayer || rolling || (!dieFaceToResolve && !face_value))
            return;

        // Normal resolve logic for when we've got all the info (including target if needed)
        try {
            const content = {
                roomName: roomName,
                player: playerName,
                resolve,
                targetPlayer: targetPlayer,
                damageHealValue: damageHealValue,
                usingReservedDie: usingReservedDie,
            };
            ws.send(JSON.stringify({ type: "resolveDice", content: content }));

            // Reset states after final resolve
            targetPlayer = null;
            showTargetSelection = false;
            showLRScanSelection = false;
            showScanAnySelection = false;
            showDamageHealSelection = false;
            canReroll = false;
            damageHealValue = 0;
            hoverPlayer = null;
        } catch (error) {
            console.error("WebSocket error:", error);
        } finally {
            usingReservedDie = false; // Reset this once the action is completed
        }
    }

    async function discardDice() {
        if (!isCurrentPlayer || rolling || !face_value) return;
        try {
            const content = {
                roomName: roomName,
                player: playerName,
            };
            ws.send(JSON.stringify({ type: "discardDice", content: content }));
            canReroll = false;
        } catch (error) {
            console.error("WebSocket error:", error);
        }
    }

    async function submitVote(vote) {
        if (rolling || !isEndGame) return;
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
            const content = { roomName: roomName };
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

    function handleAction(dieFace, isReserved = false) {
        if (typeof dieFace === "object") {
            [dieFace, isReserved] = dieFace;
        }

        if (!isCurrentPlayer || rolling || (!dieFace && !face_value)) return;

        let face = dieFace ? dieFace : face_value;

        switch (face) {
            case 1:
                showDamageHealSelection = true;
                break;
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

    function selectDamageHealValue(value) {
        damageHealValue = value;
        showTargetSelection = true;
    }

    function getScanText(scanData, scanResult) {
        if (!scanData) return "";
        return `${scanData[0]} scanned ${scanData[1]} and showed ${scanResult}`;
    }

    function getIdCheckText(idCheckData, idResult) {
        if (!idCheckData) return "";
        return `You did an ID check on ${idCheckData[1]} and showed ${idResult}`;
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
        ${event.action === "USE_DICE_ACTION" ? `used dice action ${event.dice_face}` : ""}
        ${event.dice_face ? `and got ${event.dice_face}` : ""}`;
    }

    $: {
        // If it's the player's turn and they have the cancel flag,
        // show the canel popup.
        if (gameLoopData.cancel_pending_decision_player) {
            if (
                gameLoopData.cancel_pending_decision_player ===
                gameLoopData.self.name
            ) {
                cancel_pending_decision_player = true;
            } else {
                cancel_pending_decision_player = false;
                showOtherPlayerDecisionCancel = true;
                disableAll = true;
            }
        } else {
            showOtherPlayerDecisionCancel = false;
            cancel_pending_decision_player = false;
        }
    }

    $: console.log("show other", showOtherPlayerDecisionCancel);
    $: console.log("cancel pending", cancel_pending_decision_player);
    $: console.log("gmae", gameLoopData.cancel_pending_decision_player);

    $: {
        // If it's the player's turn and they have the stall_engine_decision flag,
        // show the stall engine popup.
        if (gameLoopData.stall_engine_pending_decision_player) {
            if (
                gameLoopData.stall_engine_pending_decision_player ===
                gameLoopData.self.name
            ) {
                showStallEnginePopup = true;
            } else {
                showStallEnginePopup = false;
                showOtherPlayerDecisionStallEngine = true;
                disableAll = true;
            }
        } else {
            showOtherPlayerDecisionStallEngine = false;
        }
    }

    function cancelAction() {
        const content = {
            roomName: roomName,
            player: playerName,
        };
        ws.send(JSON.stringify({ type: "cancelAction", content }));
        // Once done, close the popup
        showStallEnginePopup = false;
    }

    function doNothingCancel() {
        const content = {
            roomName: roomName,
            player: playerName,
        };
        ws.send(JSON.stringify({ type: "noCancelAction", content }));
        // Once done, close the popup
        showStallEnginePopup = false;
    }

    function stallEngines() {
        const content = {
            roomName: roomName,
            player: playerName,
        };
        ws.send(JSON.stringify({ type: "stallEngine", content }));
        // Once done, close the popup
        showStallEnginePopup = false;
    }

    function doNothing() {
        const content = {
            roomName: roomName,
            player: playerName,
        };
        ws.send(JSON.stringify({ type: "dontStallEngine", content }));
        // Once done, close the popup
        showStallEnginePopup = false;
    }

    function handleMouseOver(player) {
        if (
            damageHealValue == 1 &&
            playersWithMaxHealth.some((p) => p.name === player.name)
        ) {
            hoverPlayer = player.name;
        }
    }
    function handleMouseLeave() {
        hoverPlayer = null;
    }

    // Reactive assignments
    $: if (gameLoopData && gameLoopData.current_dice) {
        face_value = gameLoopData.current_dice.face_value;
        all_face_values = gameLoopData.current_dice.all_faces_value;
        latest_dice = gameLoopData.current_dice;
        last_dice_roller = gameLoopData.current_dice.rolled_by;
        canUseReservedDie = false;
    } else {
        latest_dice = null;
        face_value = null;
        all_face_values = null;
        last_dice_roller = null;
        canUseReservedDie = !!gameLoopData?.self?.dice;
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
            addMessageToQueue({
                text: getScanText(lastScan, scanResults),
                type: "scan",
            });
        }
    } else {
        lastScan = null;
    }

    $: lastIdCheck = gameLoopData?.last_id_check;

    $: if (gameLoopData && gameLoopData.last_id_check) {
        if (gameLoopData.last_id_check[0] === playerName) {
            addMessageToQueue({
                text: getIdCheckText(
                    gameLoopData.last_id_check,
                    gameLoopData.id_check_result,
                ),
                type: "idCheck",
            });
        }
    }

    $: if (gameLoopData) {
        scanResult = gameLoopData.self.scan_result;
        idCheckResult = gameLoopData.self.id_check_result;
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

    $: playersWithMaxHealth = players.filter((player) => player.health >= 2);

    // Cycle logic
    function startMessageCycle() {
        if (isProcessingQueue) return;
        if (cycleRunning) return;
        cycleRunning = true;
        showNextMessage();
    }

    function stopMessageCycle() {
        cycleRunning = false;
        showNotYourTurnMessage = false;
        currentSpaceMessage = "";
        if (messageInterval) {
            clearTimeout(messageInterval);
            messageInterval = null;
        }
    }

    function showNextMessage() {
        if (!cycleRunning) return;
        currentSpaceMessage =
            spaceMessages[Math.floor(Math.random() * spaceMessages.length)];
        addMessageToQueue({ text: currentSpaceMessage, type: "space" });
    }

    // Typewriter logic
    function typewrite(messageText, messageType) {
        if (isTypewriting) return;
        isTypewriting = true;
        currentText = messageText;
        currentMessageType = messageType;
        showTypewrittenMessage = true;
        currentMessage = "";
        currentMessageIndex = 0;

        function writeNext() {
            if (currentMessageIndex < currentText.length) {
                currentMessage += currentText[currentMessageIndex];
                currentMessageIndex++;
                currentMessageTimeout = setTimeout(writeNext, 30);
            } else {
                clearTimeout(currentMessageTimeout);
                currentMessageTimeout = null;
                isTypewriting = false;
                setTimeout(() => {
                    currentText = "";
                    currentMessage = "";
                    currentMessageIndex = 0;
                    showTypewrittenMessage = false;
                    processMessageQueue();
                }, 1000);
            }
        }
        writeNext();
    }

    function processMessageQueue() {
        if (isProcessingQueue) return;

        if (messageQueue.length > 0) {
            isProcessingQueue = true;
            const nextMessage = messageQueue.shift();
            typewrite(nextMessage.text, nextMessage.type);
            setTimeout(() => {
                isProcessingQueue = false;
            }, 1000);
        } else {
            startMessageCycle();
        }
    }

    function addMessageToQueue(message) {
        messageQueue.push(message);
        stopMessageCycle();
        processMessageQueue();
    }

    $: {
        if (!isCurrentPlayer && gameLoopData && !isEndGame) {
            startMessageCycle();
        } else {
            stopMessageCycle();
            if (isTypewriting) isTypewriting = false;
            showTypewrittenMessage = false;
        }
    }

    onDestroy(() => {
        stopMessageCycle();
        clearTimeout(currentMessageTimeout);
        currentMessageTimeout = null;
    });
</script>

<div class="game-container">
    <div class="game-content">
        <!-- DiceCard -->
        {#if !isEndGame}
            <DiceCard
                {isCurrentPlayer}
                {face_value}
                {last_dice_roller}
                {numberToImage}
            />

            <!-- Reserved Dice -->
            {#if gameLoopData?.self?.dice}
                <ReservedDice
                    diceFaceValue={gameLoopData.self.dice.face_value}
                    {numberToImage}
                />
            {/if}

            <!-- Typewriter Messages -->
            <TypewriterMessage
                {showTypewrittenMessage}
                {showNotYourTurnMessage}
                {currentSpaceMessage}
                {currentMessage}
            />
        {/if}

        {#if isEndGame}
            <p>We are approaching our target planet</p>
            <p>Make sure to vote for the person you believe is infected</p>
        {/if}

        <!-- Player Selection Panels -->
        <PlayerSelection
            {isCurrentPlayer}
            {showDamageHealSelection}
            {showLRScanSelection}
            {showScanAnySelection}
            {showTargetSelection}
            {players}
            {leftPlayer}
            {rightPlayer}
            {damageHealValue}
            {playersWithMaxHealth}
            {hoverPlayer}
            on:setDamageHealValue={(e) => selectDamageHealValue(e.detail)}
            on:setLRTarget={(e) => selectLRTarget(e.detail)}
            on:setTarget={(e) => selectTarget(e.detail)}
            on:hoverPlayer={(e) => handleMouseOver(e.detail)}
            on:leaveHover={handleMouseLeave}
        />

        {#if targetPlayer && isCurrentPlayer}
            <p>Targeted player: {targetPlayer}</p>
        {/if}
    </div>

    <!-- Action Buttons -->
    <ActionButtons
        {isEndGame}
        {players}
        {isCurrentPlayer}
        {rolling}
        {face_value}
        {canReroll}
        {latest_dice}
        {canUseReservedDie}
        {gameLoopData}
        disableAll={showStallEnginePopup}
        bind:usingReservedDie
        on:rollAllDice={rollAllDice}
        on:rerollDice={rerollDice}
        on:handleAction={(e, detail) =>
            handleAction(e.detail, detail?.isReserved)}
        on:resolveDice={resolveDice}
        on:reserveDieAction={reserveDieAction}
        on:submitVote={(e) => submitVote(e.detail)}
        on:resolveEndGame={resolveEndGame}
        on:toggleScanHistoryModal={toggleScanHistoryModal}
        on:toggleGameHistoryModal={toggleGameHistoryModal}
        on:discardDice={discardDice}
    />
</div>
{#if !isEndGame}
    {#if cancel_pending_decision_player}
        <CancelDecision
            {gameLoopData}
            {face_value}
            on:cancelAction={cancelAction}
            on:doNothingCancel={doNothingCancel}
        />
    {/if}

    {#if showStallEnginePopup}
        <StallEngineDecision
            on:stallEngines={stallEngines}
            on:doNothing={doNothing}
        />
    {/if}

    <!-- Modals -->
    {#if showOtherPlayerDecisionCancel}
        <OtherPlayerDecisionModalCancel
            cancelPerson={gameLoopData.cancel_pending_decision_player}
            dicePlayer={gameLoopData.current_player}
        />
    {/if}

    <!-- Modals -->
    {#if showOtherPlayerDecisionStallEngine}
        <OtherPlayerDecisionModal
            stallEnginePlayer={gameLoopData.stall_engine_pending_decision_player}
        />
    {/if}
{/if}

{#if showScanHistoryModal}
    <ScanHistoryModal
        {playerName}
        {playerScanHistory}
        on:close={toggleScanHistoryModal}
    />
{/if}

{#if showGameHistoryModal}
    <GameHistoryModal
        {game_history}
        {formatGameHistoryText}
        on:close={toggleGameHistoryModal}
    />
{/if}

<style>
    .game-container {
        display: flex;
        flex-direction: column;
        height: 50vh;
    }

    .game-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        text-align: center;
        color: #eee;
        position: relative;
    }
</style>
