<!-- svelte_stuff\src\routes\game\components\GameStatus.svelte -->
<script>
    import thunder from "$lib/images/thunder.png";
    import heart from "$lib/images/heart.png";

    export let numberOfPowerups;
    export let health;
    export let current_player;

    $: console.log(health);
</script>

<div
    class="container mx-auto flex flex-col md:flex-row justify-between items-center px-4 md:px-6 py-2"
>
    <div
        class="flex flex-wrap justify-center md:justify-start items-center space-x-2 mb-4 md:mb-0"
    >
        {#each Array(numberOfPowerups) as _, index}
            <img
                src={thunder}
                alt={`thunder-${index + 1}`}
                class="w-8 h-8 md:w-10 md:h-10"
            />
        {/each}
    </div>
    <div class="flex justify-center md:justify-end items-center space-x-2">
        {#each Array(health) as _, index}
            <img src={heart} alt="heart" class="w-6 h-6 md:w-8 md:h-8" />
        {/each}
    </div>
    <div class="flex justify-center md:justify-end items-center space-x-2">
        <h3>Current Player: {current_player}</h3>
    </div>
</div>
