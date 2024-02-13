$(document).ready(function() {
 
    $("#owl-demo").owlCarousel({
        margin:12,
        navigation: true, // Show next and prev buttons
        slideSpeed: 100,
        paginationSpeed: 100,
        items: 1, 
        autoplay: true, // Enable autoplay
        autoplayTimeout: 2000, // Set autoplay interval (in milliseconds)
        autoplayHoverPause: true, // Pause autoplay on hover
        loop: true,
        itemsDesktop: false,
        itemsDesktopSmall: false,
        itemsTablet: false,
        itemsMobile: false
    });
    
   
   });