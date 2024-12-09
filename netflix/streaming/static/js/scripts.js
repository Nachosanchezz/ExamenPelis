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
        if (nextButton) {
            nextButton.addEventListener("click", () => {
                const maxScroll = carousel.scrollWidth - carousel.clientWidth; // Máximo desplazamiento permitido

                scrollPosition += itemWidth * 5; // Avanzar 5 ítems por clic
                if (scrollPosition > maxScroll) {
                    scrollPosition = maxScroll; // Limitar al máximo desplazamiento
                }

                carousel.style.transform = `translateX(-${scrollPosition}px)`;
            });
        }

        // Evento para retroceder
        if (prevButton) {
            prevButton.addEventListener("click", () => {
                scrollPosition -= itemWidth * 5; // Retroceder 5 ítems por clic
                if (scrollPosition < 0) {
                    scrollPosition = 0; // No permitir retroceder más allá del inicio
                }

                carousel.style.transform = `translateX(-${scrollPosition}px)`;
            });
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".add-to-playlist-btn");

    buttons.forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();

            const movieId = button.dataset.movieId;
            const title = button.dataset.title;

            // Simular un cambio de estado visual del corazón
            const heartIcon = button.querySelector("i");
            heartIcon.classList.toggle("active");

            // Enviar una solicitud POST al servidor
            fetch(`/streaming/add-to-playlist/${movieId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
                body: JSON.stringify({ title }),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Error al agregar la película a la playlist.");
                    }
                    return response.json();
                })
                .then((data) => {
                    console.log(data.message);
                })
                .catch((error) => {
                    console.error("Error:", error);
                    // Revertir el cambio visual si falla
                    heartIcon.classList.toggle("active");
                });
        });
    });
});

