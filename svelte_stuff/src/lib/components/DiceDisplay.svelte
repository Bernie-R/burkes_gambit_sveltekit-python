<script>
    export let face;
</script>

<div class="dice-container">
    <img src={face} alt="dice face" class="dice-image" />
</div>

<style>
    .dice-container {
        width: 60px;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 2px solid #616161;
        border-radius: 12%;
        background-color: #fffffe;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        cursor: pointer;
    }
    .dice-image {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    @media (min-width: 768px) {
        .dice-container {
            width: 80px;
            height: 80px;
        }
    }
</style>
