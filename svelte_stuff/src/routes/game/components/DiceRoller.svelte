<!-- DiceRoller.svelte -->
<script>

  import { triggerRoll } from './store.js';

  const probabilities = [0.3305785124, 0.3305785124, 0.1652892562, 0.02479338843, 0.02479338843, 0.02479338843, 0.02479338843, 0.02479338843, 0.02479338843, 0.02479338843];

  function roll() {
    // Generate a random number between 0 and 1
    const rand = Math.random();

    // Use the probabilities to determine the result
    let cumulativeProb = 0;
    let result = 0;

    probabilities.some((prob, i) => {
      cumulativeProb += prob;
      if (rand <= cumulativeProb) {
        result = i + 1;
        return true;
      }
      return false;
    });

    return result;
  }

  let result = 0;

  $: if ($triggerRoll) {
    result = roll();
  }
</script>
<div class="flex items-center justify-center h-24 w-24 mx-auto my-12 border border-gray-300 rounded-lg">
  <span class="text-6xl">{result}</span>
</div>
<style>
  * {
    font-family: Helvetica, Arial, sans-serif;
    text-align: center;
  }
  button {
    background-color: rgb(82, 186, 179);
    border-radius: 6px;
    border: none;
    color: rgb(255, 255, 255);
    padding: 10px;
    text-transform: uppercase;
    width: 200px;
    cursor: pointer;
  }
  .placeholder {
    height: 100px;
    width: 100px;
    margin: 50px auto;
    border: 1px solid gray;
    border-radius: 10px;
    font-size: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

</style>