<script>
  export let character_text;
  export let character;
  export let team_text;
  export let team_name;
  let isOpen = true;
</script>

<div class="fixed inset-0 bg-black bg-opacity-50 z-20 flex justify-center items-center">
  {#if isOpen}
    <div class="bg-white p-4 rounded shadow w-3/5 h-auto transform scale-125 transition-all duration-300">
      <h1 class="text-lg font-bold mb-2">Role: {character}</h1>
      <p class="text-gray-700">{character_text}</p>
      <br>
      <h1 class="text-lg font-bold mb-2">Team</h1>
      <p class="text-gray-700">team_text</p>
    </div>
  {/if}
</div>