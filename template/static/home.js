document.addEventListener("DOMContentLoaded", function () {
    const contactLink = document.getElementById("contact-link");
    const modal = document.getElementById("contact-modal");
    const closeModal = document.querySelector(".close-btn");

    // Open Modal on Click
    contactLink.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default link behavior
        modal.style.display = "flex";
    });

    // Close Modal on Clicking Close Button
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Close Modal on Clicking Outside of Modal Content
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});