document.addEventListener("DOMContentLoaded", function () {
    const carousels = document.querySelectorAll(".carousel-container");

    carousels.forEach((carouselContainer) => {
        const carousel = carouselContainer.querySelector(".carousel");
        const prevButton = carouselContainer.querySelector(".carousel-control.prev");
        const nextButton = carouselContainer.querySelector(".carousel-control.next");

        let scrollPosition = 0; // Posición inicial del carrusel

        // Ancho de cada ítem (película) incluyendo el margen
        const itemWidth = carousel.querySelector(".carousel-item").offsetWidth + 15;

        // Evento para avanzar
        nextButton.addEventListener("click", () => {
            const maxScroll = carousel.scrollWidth - carousel.clientWidth; // Máximo desplazamiento permitido

            scrollPosition += itemWidth * 5; // Avanzar 5 ítems por clic
            if (scrollPosition > maxScroll) {
                scrollPosition = maxScroll; // Limitar al máximo desplazamiento
            }

            carousel.style.transform = `translateX(-${scrollPosition}px)`;
        });

        // Evento para retroceder
        prevButton.addEventListener("click", () => {
            scrollPosition -= itemWidth * 5; // Retroceder 5 ítems por clic
            if (scrollPosition < 0) {
                scrollPosition = 0; // No permitir retroceder más allá del inicio
            }

            carousel.style.transform = `translateX(-${scrollPosition}px)`;
        });
    });
});


