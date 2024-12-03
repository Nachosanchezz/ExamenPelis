document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".carousel");
    const prevButton = document.querySelector(".carousel-control.prev");
    const nextButton = document.querySelector(".carousel-control.next");

    let scrollPosition = 0; // Posición inicial del carrusel

    // Ancho de cada ítem (película) incluyendo el margen
    const itemWidth = document.querySelector(".carousel-item").offsetWidth + 15;

    nextButton.addEventListener("click", () => {
        const maxScroll = carousel.scrollWidth - carousel.clientWidth; // Máximo desplazamiento permitido

        scrollPosition += itemWidth * 5; // Avanzar 5 ítems por clic
        if (scrollPosition > maxScroll) {
            scrollPosition = 0; // Volver al inicio si se supera el límite
        }

        carousel.style.transform = `translateX(-${scrollPosition}px)`;
    });

    prevButton.addEventListener("click", () => {
        const maxScroll = carousel.scrollWidth - carousel.clientWidth; // Máximo desplazamiento permitido

        scrollPosition -= itemWidth * 5; // Retroceder 5 ítems por clic
        if (scrollPosition < 0) {
            scrollPosition = maxScroll; // Ir al final si se pasa del inicio
        }

        carousel.style.transform = `translateX(-${scrollPosition}px)`;
    });
});
