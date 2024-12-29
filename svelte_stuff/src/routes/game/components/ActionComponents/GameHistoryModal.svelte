<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let game_history;
    export let formatGameHistoryText;

    function closeModal() {
        dispatch("close");
    }
</script>

<div class="modal-overlay">
    <div class="modal">
        <div class="modal-header">
            <h2>Game History</h2>
            <button class="close-button" on:click={closeModal}>×</button>
        </div>
        <div class="modal-content">
            {#if game_history.length > 0}
                <ul>
                    {#each game_history as event}
                        <li>{formatGameHistoryText(event)}</li>
                    {/each}
                </ul>
            {:else}
                <p>No history yet</p>
            {/if}
        </div>
        <div class="modal-footer">
            <button class="close-modal-button" on:click={closeModal}
                >Close</button
            >
        </div>
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
    .modal-content {
        flex: 1;
        overflow-y: auto;
        padding-right: 1rem;
        margin-bottom: 1rem;
    }
    .close-button {
        background-color: transparent;
        border: none;
        font-size: 1.5rem;
        color: #eee;
        cursor: pointer;
    }
    .modal-footer {
        display: flex;
        justify-content: flex-end;
    }
    .close-modal-button {
        padding: 0.5rem 1rem;
        background-color: #444;
        color: #eee;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .close-modal-button:hover {
        background-color: #555;
    }
</style>
