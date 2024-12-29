<script>
    import Dice from "$lib/components/DiceDisplay.svelte";
    export let diceFaceValue;
    export let numberToImage;
</script>

<div class="reserved-dice-container">
    <p>Your Reserved Die</p>
    <Dice face={numberToImage[diceFaceValue]} />
</div>

<style>
    .reserved-dice-container {
        position: absolute;
        bottom: 1rem;
        right: 1rem;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        color: #eee;
    }
</style>
