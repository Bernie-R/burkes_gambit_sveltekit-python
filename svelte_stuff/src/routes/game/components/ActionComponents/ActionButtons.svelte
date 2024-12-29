<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let isEndGame;
    export let players;
    export let isCurrentPlayer;
    export let rolling;
    export let face_value;
    export let canReroll;
    export let latest_dice;
    export let canUseReservedDie;
    export let gameLoopData;
    export let usingReservedDie;
    export let disableAll = false;

    let consoleMessage = [];
    let isReservedDieFour = false;
    let isRolledDieFour = false;

    $: {
        if (gameLoopData?.self?.dice?.face_value === 4) {
            isReservedDieFour = true;
        } else {
            isReservedDieFour = false;
        }
        if (latest_dice) {
            if (latest_dice.face_value === 4) {
                isRolledDieFour = true;
            } else {
                isRolledDieFour = false;
            }
        }
    }

    // Instead of dispatchEvent, use dispatch('eventName', detail)
    function pickAndRoll() {
        usingReservedDie = false;
        console.log(usingReservedDie);

        dispatch("rollAllDice");
    }

    function handleReroll() {
        usingReservedDie = false;
        console.log(usingReservedDie);

        dispatch("rerollDice");
    }

    function doAction() {
        usingReservedDie = false;
        dispatch("handleAction", face_value);
    }

    function useReservedDice() {
        usingReservedDie = true;
        console.log(usingReservedDie);
        dispatchMessage = [gameLoopData?.self?.dice?.face_value, true];
        dispatch("handleAction", dispatchMessage);
    }

    function reserveDice() {
        usingReservedDie = false;
        console.log(usingReservedDie);
        dispatch("reserveDieAction");
    }

    function discardDice() {
        usingReservedDie = false;
        console.log(usingReservedDie);
        dispatch("discardDice");
    }

    function doSubmitVote(playerName) {
        usingReservedDie = false;
        console.log(usingReservedDie);

        dispatch("submitVote", playerName);
    }

    function doResolveEndGame() {
        usingReservedDie = false;
        console.log(usingReservedDie);

        dispatch("resolveEndGame");
    }

    function openScanHistory() {
        usingReservedDie = false;
        console.log(usingReservedDie);

        dispatch("toggleScanHistoryModal");
    }

    function openGameHistory() {
        usingReservedDie = false;
        console.log(usingReservedDie);

        dispatch("toggleGameHistoryModal");
    }
</script>

<footer class="action-buttons">
    {#if isEndGame}
        <div class="end-game-options">
            {#each players as player}
                <button on:click={() => doSubmitVote(player.name)}>
                    Vote for {player.name}
                </button>
            {/each}
            <button on:click={doResolveEndGame}>Resolve End Game</button>
        </div>
    {:else if isCurrentPlayer}
        {#if canUseReservedDie && gameLoopData?.self?.dice}
            <button
                on:click={useReservedDice}
                disabled={isReservedDieFour || disableAll}
                >Use Reserved Dice</button
            >
            <button disabled={rolling || disableAll} on:click={pickAndRoll}>
                Pick & Roll Dice
            </button>
        {:else if !latest_dice}
            <button disabled={rolling || disableAll} on:click={pickAndRoll}>
                Pick & Roll Dice
            </button>
        {:else if latest_dice}
            <button disabled={!canReroll || disableAll} on:click={handleReroll}>
                Re-roll Dice
            </button>
            <button disabled={isRolledDieFour || disableAll} on:click={doAction}
                >Resolve Dice</button
            >
            <button on:click={reserveDice}>Reserve Dice</button>
            <button on:click={discardDice}>Discard Dice</button>
        {/if}
    {/if}
    <button on:click={openScanHistory}>Show Scan History</button>
    <button on:click={openGameHistory}>Show Game History</button>
</footer>

<style>
    .action-buttons {
        display: flex;
        justify-content: space-around;
        padding: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        background-color: rgba(0, 0, 0, 0.7);
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .action-buttons button {
        padding: 0.75rem 1rem;
        border: 1px solid #777;
        background-color: #333;
        color: #eee;
        cursor: pointer;
        border-radius: 0.3rem;
        font-size: 1rem;
        flex: 1 1 auto;
        min-width: 0;
        transition:
            background-color 0.3s,
            color 0.3s;
    }

    .action-buttons button:hover {
        background-color: #555;
        color: #fff;
    }

    .end-game-options {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .action-buttons button:disabled {
        background-color: #444;
        color: #888;
        cursor: not-allowed;
    }

    @media (min-width: 768px) {
        .action-buttons {
            padding: 1.5rem;
        }
        .action-buttons button {
            font-size: 1.1rem;
            padding: 1rem 1.5rem;
        }
    }

    @media (min-width: 1024px) {
        .action-buttons {
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
    }
</style>
