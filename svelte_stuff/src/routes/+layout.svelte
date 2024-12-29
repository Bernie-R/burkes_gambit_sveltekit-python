<script>
    let stars = [];
    const numStars = 30; // Adjust the number of stars as needed

    function createStar() {
        const size = Math.random() * 2 + 1; // Random size between 1 and 3
        let x = Math.random() * 100; // Random horizontal position
        const y = Math.random() * 100; // Random vertical position
        const animationDelay = Math.random() * 3; // Random delay for fade-in
        const speed = Math.random() * 1 + 15; // Random speed for movement

        return {
            id: Math.random(), // Unique id for key
            size,
            x,
            y,
            animationDelay,
            speed,
        };
    }

    function generateStars() {
        for (let i = 0; i < numStars; i++) {
            stars = [...stars, createStar()];
        }
    }

    generateStars();
</script>

<div class="relative min-h-screen bg-black overflow-hidden">
    <div class="absolute inset-0 overflow-hidden z-0">
        {#each stars as star (star.id)}
            <div
                class="star"
                style="
                    width: {star.size}px;
                    height: {star.size}px;
                    top: {star.y}%;
                    left: {star.x}%;
                    animation-delay: {star.animationDelay}s;
                    animation-duration: {star.speed}s;
                  "
            ></div>
        {/each}
    </div>
    <div class="relative z-10">
        <slot />
    </div>
</div>

<style>
    .star {
        position: absolute;
        border-radius: 50%;
        background-color: white;
        opacity: 0;
        animation:
            fadeIn 2s ease-out forwards,
            twinkle 5s infinite ease-in-out,
            move linear infinite;
        filter: blur(1px);
        box-shadow: 0 0 2px 1px rgba(255, 255, 255, 0.1);
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 0.8;
        }
    }

    @keyframes twinkle {
        0% {
            opacity: 0.8;
        }
        50% {
            opacity: 0.2;
        }
        100% {
            opacity: 0.8;
        }
    }

    @keyframes move {
        from {
            transform: translateX(0);
        }
        to {
            transform: translateX(-50vw);
        }
    }
</style>
