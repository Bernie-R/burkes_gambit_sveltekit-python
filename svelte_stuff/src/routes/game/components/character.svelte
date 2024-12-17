<!-- svelte_stuff\src\routes\game\components\character.svelte -->
<script>
  import { writable } from "svelte/store";

  export let character_text;
  export let character;
  export let team_text;
  export let team_name;

  const isOpen = writable(true);

  function closeInfoBox() {
    isOpen.set(false);
  }
</script>

{#if $isOpen}
  <div
    class="fixed inset-0 bg-black bg-opacity-50 z-20 flex justify-center items-center px-4"
  >
    <div
      class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md transform scale-100 transition-transform duration-300"
      on:click|stopPropagation
    >
      <h1 class="text-xl font-bold mb-3">Role: {character}</h1>
      <p class="text-gray-700 mb-4">{character_text}</p>
      <h2 class="text-xl font-bold mb-2">Team</h2>
      <p class="text-gray-700">{team_text}</p>
    </div>
  </div>
{/if}
