<script>
    export let isEndGame;
    export let players;
    // submitVote(playerName), resolveEndGame()

    function handleVote(playerName) {
        const event = new CustomEvent("submitVote", { detail: playerName });
        dispatchEvent(event);
    }

    function handleResolveEndGame() {
        const event = new Event("resolveEndGame");
        dispatchEvent(event);
    }
</script>

{#if isEndGame}
    <div class="end-game-options">
        {#each players as player}
            <button on:click={() => handleVote(player.name)}>
                Vote for {player.name}
            </button>
        {/each}
        <button on:click={handleResolveEndGame}>Resolve End Game</button>
    </div>
{/if}

<style>
    .end-game-options {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
</style>
