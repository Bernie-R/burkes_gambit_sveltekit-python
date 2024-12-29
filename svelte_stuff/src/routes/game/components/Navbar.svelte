<script>
    export let roomName;
    export let playerName;
    export let character;
    export let players = [];
    export let team;

    let isMobileMenuOpen = false;
    let isPlayersDropdownOpen = false;
    let isTeamCardOpen = false;
    let selectedPlayer = null;
    let teamTimeoutId = null;

    function toggleMobileMenu() {
        isMobileMenuOpen = !isMobileMenuOpen;
    }

    function togglePlayersDropdown() {
        isPlayersDropdownOpen = !isPlayersDropdownOpen;
    }

    function showPlayerDetails(player) {
        selectedPlayer = player;
    }

    function closePlayerDetails() {
        selectedPlayer = null;
    }

    function toggleTeamCard() {
        if (isTeamCardOpen) {
            clearTimeout(teamTimeoutId); // Clear any existing timeout if button is clicked while team is displayed
            isTeamCardOpen = false;
        } else {
            isTeamCardOpen = true;
            clearTimeout(teamTimeoutId);
            teamTimeoutId = setTimeout(() => {
                isTeamCardOpen = false;
            }, 5000);
        }
    }

    console.log(character);
</script>

<svelte:head>
    <title>Lobby: {roomName}</title>
</svelte:head>

<header
    class="bg-gray-900 bg-opacity-80 py-4 md:py-6 relative z-10 border-b border-gray-700"
>
    <div
        class="container mx-auto flex justify-between items-center px-4 md:px-6"
    >
        <h1 class="text-lg md:text-xl font-bold text-gray-200">
            Room {roomName}
        </h1>
        <nav class="hidden md:block relative">
            <ul class="flex space-x-4">
                <li class="relative">
                    <button
                        class="text-gray-300 hover:text-white focus:outline-none"
                        on:click={togglePlayersDropdown}
                    >
                        Player Information
                    </button>
                    {#if isPlayersDropdownOpen}
                        <ul
                            class="absolute top-full left-0 bg-gray-900 bg-opacity-80 mt-2 py-2 px-4 rounded shadow-lg z-10 space-y-2 border border-gray-700"
                        >
                            {#each players as p}
                                <li
                                    class="text-gray-300 hover:text-white cursor-pointer"
                                >
                                    <button
                                        class="focus:outline-none"
                                        on:click={() => showPlayerDetails(p)}
                                    >
                                        {p.name}
                                    </button>
                                </li>
                            {/each}
                        </ul>
                    {/if}
                </li>
            </ul>
        </nav>
        <button
            class="md:hidden text-gray-300 hover:text-white"
            on:click={toggleMobileMenu}
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d={isMobileMenuOpen
                        ? "M6 18L18 6M6 6l12 12"
                        : "M4 6h16M4 12h16M4 18h16"}
                />
            </svg>
        </button>
    </div>

    <div
        class="container mx-auto flex justify-between items-center px-4 md:px-6 mt-4 relative"
    >
        <div class="relative">
            <div
                class="bg-gray-800 bg-opacity-80 rounded-md p-3 border border-gray-700"
            >
                <h2 class="text-gray-200 mb-2">Name: {playerName}</h2>
                {#if !isTeamCardOpen}
                    <button
                        class="focus:outline-none"
                        on:click={toggleTeamCard}
                    >
                        <div
                            class="bg-gray-700 hover:bg-gray-600 text-gray-300 rounded-md p-2 w-16 h-8 items-center justify-center cursor-pointer border border-gray-600"
                        >
                            Team
                        </div>
                    </button>
                {/if}
                {#if isTeamCardOpen}
                    {#if team && team[0] === "EVIL"}
                        <div
                            class="bg-red-700 hover:bg-red-600 text-white rounded-md p-2 w-16 h-8 cursor-pointer items-center justify-center border border-red-600"
                            on:click={toggleTeamCard}
                        >
                            EVIL
                        </div>
                    {:else if team && team[0] === "GOOD"}
                        <div
                            class="bg-green-700 hover:bg-green-600 text-white rounded-md p-2 w-16 h-8 cursor-pointer items-center justify-center border border-green-600"
                            on:click={toggleTeamCard}
                        >
                            GOOD
                        </div>
                    {:else}
                        <div
                            class="bg-gray-700 hover:bg-gray-600 text-white rounded-md p-2 w-16 h-8 cursor-pointer items-center justify-center border border-gray-600"
                            on:click={toggleTeamCard}
                        >
                            No team
                        </div>
                    {/if}
                {/if}
            </div>
        </div>
        <div
            class="bg-gray-800 bg-opacity-80 rounded-md p-3 border border-gray-700"
        >
            <h2 class="text-gray-200">Character: {character}</h2>
        </div>
    </div>

    {#if isMobileMenuOpen}
        <nav
            class="md:hidden bg-gray-900 bg-opacity-80 border-t border-gray-700"
        >
            <ul class="flex flex-col space-y-2 p-4">
                <li>
                    <button
                        class="text-gray-300 hover:text-white focus:outline-none"
                        on:click={togglePlayersDropdown}
                    >
                        Players
                    </button>
                    {#if isPlayersDropdownOpen}
                        <ul
                            class="bg-gray-900 bg-opacity-80 mt-2 py-2 px-4 rounded shadow-lg space-y-2 border border-gray-700"
                        >
                            {#each players as p}
                                <li
                                    class="text-gray-300 hover:text-white cursor-pointer"
                                >
                                    <button
                                        class="focus:outline-none"
                                        on:click={() => showPlayerDetails(p)}
                                    >
                                        {p.name}
                                    </button>
                                </li>
                            {/each}
                        </ul>
                    {/if}
                </li>
            </ul>
        </nav>
    {/if}

    {#if selectedPlayer}
        <div
            class="fixed inset-0 flex items-center justify-center z-200 backdrop-blur-sm"
        >
            <div
                class="bg-gray-800 bg-opacity-90 p-6 rounded-lg shadow-lg max-w-sm w-full border border-gray-700 relative"
            >
                <button
                    class="absolute top-2 right-2 text-gray-400 hover:text-gray-200"
                    on:click={closePlayerDetails}
                >
                    <svg
                        class="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M6 18L18 6M6 6l12 12"
                        />
                    </svg>
                </button>
                <h3 class="text-lg font-bold mb-2 text-gray-200">
                    {selectedPlayer.name}
                </h3>
                <p class="text-gray-300">
                    <strong>Role:</strong>
                    {selectedPlayer.role}
                </p>
                <p class="text-gray-300">
                    <strong>Health:</strong>
                    {selectedPlayer.health}
                </p>

                {#if selectedPlayer.role_description}
                    <p class="mt-2 text-gray-300">
                        <strong>Description:</strong>
                        {selectedPlayer.role_description}
                    </p>
                {/if}
            </div>
        </div>
    {/if}
</header>
