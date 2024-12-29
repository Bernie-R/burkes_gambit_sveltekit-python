<script>
    export let showTypewrittenMessage;
    export let showNotYourTurnMessage;
    export let currentSpaceMessage;
    export let currentMessage;
</script>

{#if showTypewrittenMessage}
    <div class="not-your-turn-box fade-in-out">
        <span class="typewriter-text">{currentMessage}</span>
    </div>
{:else if showNotYourTurnMessage}
    <div class="not-your-turn-box fade-in-out">
        {currentSpaceMessage}
    </div>
{/if}

<style>
    .not-your-turn-box {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
        color: #eee;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 500;
        white-space: pre-wrap;
    }
    .fade-in-out {
        animation: fadeInOut 7s ease-out forwards;
    }
    @keyframes fadeInOut {
        0% {
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            opacity: 0;
        }
    }
    .typewriter-text {
        display: inline-block;
    }
</style>
