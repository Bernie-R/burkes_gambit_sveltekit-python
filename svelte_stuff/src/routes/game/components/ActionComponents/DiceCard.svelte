<script>
    import Dice from "$lib/components/DiceDisplay.svelte";
    export let isCurrentPlayer;
    export let face_value;
    export let last_dice_roller;
    export let numberToImage;
</script>

{#if isCurrentPlayer && face_value}
    <div class="dice-card current-player-dice">
        <p>You Rolled:</p>
        <Dice face={numberToImage[face_value]} />
    </div>
{:else if face_value}
    <div class="dice-card other-player-dice">
        <p>{last_dice_roller} Rolled:</p>
        <Dice face={numberToImage[face_value]} />
    </div>
{/if}

<style>
    .dice-card {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .current-player-dice {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        margin-bottom: 0;
    }
    .other-player-dice {
        position: absolute;
        bottom: 80px;
        left: 1rem;
        margin-bottom: 0;
    }
</style>
