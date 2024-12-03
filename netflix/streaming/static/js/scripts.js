document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".carousel");
    const prevButton = document.querySelector(".carousel-control.prev");
    const nextButton = document.querySelector(".carousel-control.next");

    let scrollAmount = 0;

    nextButton.addEventListener("click", () => {
        scrollAmount += 220; // Tamaño de una película + margen
        if (scrollAmount >= carousel.scrollWidth - carousel.clientWidth) {
            scrollAmount = 0; // Volver al inicio
        }
        carousel.style.transform = `translateX(-${scrollAmount}px)`;
    });

    prevButton.addEventListener("click", () => {
        scrollAmount -= 220;
        if (scrollAmount < 0) {
            scrollAmount = carousel.scrollWidth - carousel.clientWidth;
        }
        carousel.style.transform = `translateX(-${scrollAmount}px)`;
    });
});
