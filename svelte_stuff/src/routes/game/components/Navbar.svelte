<script>
    export let roomName;
    export let playerName;
    export let character;
    export let players = [];
    export let team; // Expecting an array like ["EVIL"] or ["GOOD"]

    let isMobileMenuOpen = false;
    let isPlayersDropdownOpen = false;
    let isTeamCardOpen = false;
    let selectedPlayer = null;

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
        isTeamCardOpen = !isTeamCardOpen;
    }

    console.log(character);
</script>

<title>Lobby: {roomName}</title>

<header class="bg-gray-800 py-4 md:py-6 relative z-30">
    <div
        class="container mx-auto flex justify-between items-center px-4 md:px-6"
    >
        <h1 class="text-lg md:text-xl font-bold text-white">Room {roomName}</h1>
        <nav class="hidden md:block relative">
            <ul class="flex space-x-4">
                <li class="relative">
                    <button
                        class="text-gray-300 hover:text-white focus:outline-none"
                        on:click={togglePlayersDropdown}
                    >
                        Players
                    </button>
                    {#if isPlayersDropdownOpen}
                        <ul
                            class="absolute top-full left-0 bg-gray-700 mt-2 py-2 px-4 rounded shadow-lg z-10 space-y-2"
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
        class="container mx-auto flex justify-between items-center px-4 md:px-6 relative"
    >
        <div class="relative">
            <h2 class="text-white">Name: {playerName}</h2>
            {#if !isTeamCardOpen}
                <button class="focus:outline-none" on:click={toggleTeamCard}>
                    <div
                        class="bg-gray-600 text-gray-200 rounded-md p-2 w-16 h-8 items-center justify-center cursor-pointer"
                    >
                        Team
                    </div>
                </button>
            {/if}
            {#if isTeamCardOpen}
                {#if team && team[0] === "EVIL"}
                    <div
                        class="bg-red-600 text-white rounded-md p-2 w-16 h-8 cursor-pointer items-center justify-center"
                        on:click={toggleTeamCard}
                    >
                        EVIL
                    </div>
                {:else if team && team[0] === "GOOD"}
                    <div
                        class="bg-green-600 text-white rounded-md p-2 w-16 h-8 cursor-pointer items-center justify-center"
                        on:click={toggleTeamCard}
                    >
                        GOOD
                    </div>
                {:else}
                    <div
                        class="bg-gray-700 text-white rounded-md p-2 w-16 h-8 cursor-pointer items-center justify-center"
                        on:click={toggleTeamCard}
                    >
                        No team
                    </div>
                {/if}
            {/if}
        </div>
        <h2 class="text-white">Character: {character}</h2>
    </div>

    {#if isMobileMenuOpen}
        <nav class="md:hidden bg-gray-700">
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
                            class="bg-gray-700 mt-2 py-2 px-4 rounded shadow-lg space-y-2"
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
        <!-- Player details overlay or panel -->
        <div
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        >
            <div class="bg-white p-4 rounded shadow max-w-sm w-full">
                <h3 class="text-lg font-bold mb-2">{selectedPlayer.name}</h3>
                <p><strong>Role:</strong> {selectedPlayer.role}</p>
                <p><strong>Health:</strong> {selectedPlayer.health}</p>

                {#if selectedPlayer.role_description}
                    <p class="mt-2">
                        <strong>Description:</strong>
                        {selectedPlayer.role_description}
                    </p>
                {/if}
                <button
                    class="mt-4 bg-gray-800 text-white px-4 py-2 rounded focus:outline-none hover:bg-gray-700"
                    on:click={closePlayerDetails}
                >
                    Close
                </button>
            </div>
        </div>
    {/if}
</header>
