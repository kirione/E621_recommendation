// Wait for DOM to be ready
function initSnowfall() {
  const snowContainer = document.getElementById("snow-container");
  
  if (!snowContainer) {
    console.error("Snow container not found");
    return;
  }

  // Create 80 snowflakes
  for (let i = 0; i < 80; i++) {
    const flake = document.createElement("div");
    flake.classList.add("snowflake");
    flake.innerHTML = "❄";

    const startX = Math.random() * window.innerWidth;
    const size = Math.random() * 15 + 10;

    flake.style.left = `${startX}px`;
    flake.style.fontSize = `${size}px`;
    flake.style.opacity = Math.random() * 0.6 + 0.4;

    snowContainer.appendChild(flake);

    gsap.to(flake, {
      y: window.innerHeight + 40,
      x: `+=${Math.random() * 100 - 50}`,
      rotation: Math.random() * 360,
      duration: Math.random() * 5 + 6,
      delay: Math.random() * 5,
      repeat: -1,
      ease: "none",
      onRepeat: () => {
        gsap.set(flake, {
          y: -20,
          x: Math.random() * window.innerWidth,
          rotation: 0
        });
      }
    });
  }
}

// Initialize when GSAP is loaded
if (typeof gsap !== 'undefined') {
  initSnowfall();
} else {
  window.addEventListener('load', initSnowfall);
}