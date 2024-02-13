document.addEventListener("DOMContentLoaded", function() {
    const quickViewBtns = document.querySelectorAll(".quick-view-btn");
    const popupCardOverlay = document.querySelectorAll(".popup-card-overlay");
    const popupCards = document.querySelectorAll(".popup-card");
    const closePopupBtns = document.querySelectorAll(".close-popup-btn");

    quickViewBtns.forEach((button, index) => {
        button.addEventListener("click", function(e) {
            e.preventDefault(); // Prevent default behavior of the link
            popupCardOverlay[index].style.display = "block";
            popupCards[index].style.display = "block";
        });
    });

    closePopupBtns.forEach((button, index) => {
        button.addEventListener("click", function() {
            popupCardOverlay[index].style.display = "none";
            popupCards[index].style.display = "none";
        });
    });
});
