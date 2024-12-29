<script>
    export let cancelPerson;
    export let dicePlayer;
</script>

<div class="modal-overlay">
    <div class="modal">
        <h2 style="text-align: center;">
            {cancelPerson} is deciding what to do about {dicePlayer}'s dice
            action
        </h2>
    </div>
</div>

<style>
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }
    .modal {
        background-color: #222;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
        width: 80%;
        max-width: 600px;
        display: flex;
        flex-direction: column;
        position: relative;
        color: #eee;
    }
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
</style>
