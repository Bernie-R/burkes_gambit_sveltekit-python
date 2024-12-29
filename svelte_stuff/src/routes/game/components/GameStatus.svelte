<script>
    import thunderoff from "$lib/images/thunder.png";
    import thunderon from "$lib/images/thunderon.png";
    import heart from "$lib/images/heart.png";

    export let numberOfPowerups;
    export let health;
    export let current_player;
    export let endGamePowerUps;

    $: console.log(endGamePowerUps);
    $: console.log(health);

    $: powerUpImages = Array(endGamePowerUps)
        .fill(0)
        .map((_, index) => {
            if (index < numberOfPowerups) {
                return thunderon;
            } else {
                return thunderoff;
            }
        });
</script>

<div
    class="container mx-auto flex flex-col md:flex-row justify-between items-center px-4 md:px-6 py-2"
>
    <!-- Life Box -->
    <div
        class="relative flex flex-col items-center mr-4 min-w-[100px] min-h-[50px] max-w-[200px] max-h-[150px] py-2"
    >
        <div
            class="absolute inset-0 bg-gray-800 bg-opacity-50 rounded-md"
        ></div>
        <h3 class="text-white z-10">Life</h3>
        <div class="flex justify-center space-x-2 z-10 mt-1">
            {#each Array(health) as _, index}
                <img src={heart} alt="heart" class="w-6 h-6 md:w-8 md:h-8" />
            {/each}
        </div>
    </div>

    <!-- Center elements-->
    <div class="flex justify-center items-center space-x-2 mb-4 md:mb-0">
        <div class="flex justify-center items-center space-x-2">
            <h3>Current Player: {current_player}</h3>
        </div>
    </div>

    <!-- Engine Power Box -->
    <div
        class="relative flex flex-col items-center ml-4 min-w-[100px] min-h-[50px] max-w-[200px] max-h-[150px] py-2"
    >
        <div
            class="absolute inset-0 bg-gray-800 bg-opacity-50 rounded-md"
        ></div>
        <h3 class="text-white z-10">Engine Power</h3>
        <div class="flex flex-wrap justify-center space-x-2 z-10 mt-1">
            {#each powerUpImages as image, index}
                <img
                    src={image}
                    alt={`thunder-${index + 1}`}
                    class="w-8 h-8 md:w-10 md:h-10"
                />
            {/each}
        </div>
    </div>
</div>
