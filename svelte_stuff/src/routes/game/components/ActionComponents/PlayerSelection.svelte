<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let isCurrentPlayer;
    export let showDamageHealSelection;
    export let showLRScanSelection;
    export let showScanAnySelection;
    export let showTargetSelection;
    export let players;
    export let leftPlayer;
    export let rightPlayer;
    export let damageHealValue;
    export let playersWithMaxHealth;
    export let hoverPlayer;

    function handleDamageHeal(value) {
        // Emit an event to let the parent know what value was chosen
        dispatch("setDamageHealValue", value);
    }

    function handleLRScanSelection(player) {
        // Emit event to parent with selected player's name
        dispatch("setLRTarget", player);
    }

    function handleScanAnySelection(player) {
        dispatch("setTarget", player);
    }

    function handleTargetSelection(player) {
        dispatch("setTarget", player);
    }

    function mouseOverPlayer(player) {
        dispatch("hoverPlayer", player.name);
    }

    function mouseLeavePlayer() {
        dispatch("leaveHover");
    }
</script>

{#if showDamageHealSelection && isCurrentPlayer}
    <div class="player-selection">
        <p>Heal or Shoot a player:</p>
        <button on:click={() => handleDamageHeal(-1)}>Shoot</button>
        <button on:click={() => handleDamageHeal(1)}>Heal</button>
    </div>
{/if}

{#if showLRScanSelection && isCurrentPlayer}
    <div class="player-selection">
        <p>Select a Player to scan:</p>
        {#if leftPlayer}
            <button
                on:click={() => handleLRScanSelection(leftPlayer)}
                disabled={leftPlayer?.is_quarantined}
                class:quarantined={leftPlayer?.is_quarantined}
                on:mouseover={() => mouseOverPlayer(leftPlayer)}
                on:mouseleave={mouseLeavePlayer}
            >
                Scan left ({leftPlayer?.name})
                {#if hoverPlayer === leftPlayer?.name && leftPlayer?.is_quarantined}
                    <span class="tooltip"
                        >This player is under quarantine and cannot be selected</span
                    >
                {/if}
            </button>
        {/if}
        {#if rightPlayer}
            <button
                on:click={() => handleLRScanSelection(rightPlayer)}
                disabled={rightPlayer?.is_quarantined}
                class:quarantined={rightPlayer?.is_quarantined}
                on:mouseover={() => mouseOverPlayer(rightPlayer)}
                on:mouseleave={mouseLeavePlayer}
            >
                Scan right ({rightPlayer?.name})
                {#if hoverPlayer === rightPlayer?.name && rightPlayer?.is_quarantined}
                    <span class="tooltip"
                        >This player is under quarantine and cannot be selected</span
                    >
                {/if}
            </button>
        {/if}
    </div>
{/if}

{#if showScanAnySelection && isCurrentPlayer}
    <div class="player-selection">
        <p>Select a Player to scan:</p>
        {#each players as player}
            <button
                on:click={() => handleScanAnySelection(player.name)}
                disabled={player.is_quarantined}
                class:quarantined={player.is_quarantined}
                on:mouseover={() => mouseOverPlayer(player)}
                on:mouseleave={mouseLeavePlayer}
            >
                {player.name}
                {#if hoverPlayer === player.name && player.is_quarantined}
                    <span class="tooltip"
                        >This player is under quarantine and cannot be selected</span
                    >
                {/if}
            </button>
        {/each}
    </div>
{/if}

{#if showTargetSelection && isCurrentPlayer}
    <div class="player-selection">
        <p>Select a Player:</p>
        {#each players as player}
            <button
                on:click={() => handleTargetSelection(player.name)}
                on:mouseover={() => mouseOverPlayer(player)}
                on:mouseleave={mouseLeavePlayer}
                disabled={(playersWithMaxHealth.some(
                    (p) => p.name == player.name,
                ) &&
                    damageHealValue == 1) ||
                    (player.is_quarantined && damageHealValue == -1) ||
                    (player.is_quarantined && damageHealValue !== 1)}
                class:max-health={playersWithMaxHealth.some(
                    (p) => p.name == player.name,
                ) && damageHealValue == 1}
                class:quarantined={(player.is_quarantined &&
                    damageHealValue == -1) ||
                    (player.is_quarantined && damageHealValue !== 1)}
            >
                {player.name}
                {#if hoverPlayer === player.name && ((player.is_quarantined && damageHealValue == -1) || (player.is_quarantined && damageHealValue !== 1))}
                    <span class="tooltip"
                        >This player is under quarantine and cannot be selected</span
                    >
                {:else if hoverPlayer === player.name && playersWithMaxHealth.some((p) => p.name == player.name) && damageHealValue == 1}
                    <span class="tooltip"
                        >This player already has max health</span
                    >
                {/if}
            </button>
        {/each}
    </div>
{/if}

<style>
    .player-selection {
        background-color: rgba(0, 0, 0, 0.8);
        border: 1px solid #777;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        color: #eee;
    }
    .player-selection p {
        margin-bottom: 0.5rem;
    }

    .player-selection button {
        padding: 0.5rem;
        background-color: #333;
        color: #eee;
        position: relative;
        transition:
            background-color 0.3s,
            color 0.3s;
    }

    .player-selection button:hover {
        background-color: #555;
        color: #fff;
    }

    .tooltip {
        visibility: hidden;
        background-color: rgba(255, 255, 255, 0.9);
        color: #333;
        text-align: center;
        padding: 5px;
        border-radius: 4px;
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        z-index: 100;
    }

    .player-selection button:hover .tooltip {
        visibility: visible;
    }

    .action-buttons button:disabled {
        background-color: #444;
        color: #888;
        cursor: not-allowed;
    }

    .player-selection button.max-health {
        background-color: #444;
        color: #888;
        cursor: not-allowed;
    }

    .player-selection button.quarantined {
        background-color: #444;
        color: #888;
        cursor: not-allowed;
    }
</style>
