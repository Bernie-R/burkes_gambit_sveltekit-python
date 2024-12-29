<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    export let gameLoopData;

    import DiceCard from "./DiceCard.svelte";

    function cancelAction() {
        dispatch("cancelAction");
    }

    function doNothingCancel() {
        dispatch("doNothingCancel");
    }
</script>

<div class="stall-engine-popup-backdrop">
    <div class="stall-engine-popup">
        <p>
            You have the option to cancel {gameLoopData.current_player} action
        </p>
        <button on:click={doNothingCancel}
            >Let {gameLoopData.current_player} proceed with their action</button
        >
        <button on:click={cancelAction}
            >Deny {gameLoopData.current_player} their action</button
        >
    </div>
</div>

<style>
    .stall-engine-popup-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .stall-engine-popup {
        background: #222;
        padding: 2rem;
        border-radius: 0.5rem;
        text-align: center;
        color: #eee;
    }

    .stall-engine-popup button {
        margin: 0.5rem;
        background: #333;
        color: #eee;
        border: 1px solid #777;
        padding: 0.75rem 1rem;
        border-radius: 0.3rem;
        cursor: pointer;
    }

    .stall-engine-popup button:hover {
        background: #555;
    }
</style>
