document.getElementById("toggle").addEventListener("click", function() {
    var text = document.getElementById("text");
    if (text.style.display === "none") {
        text.style.display = "block";
        document.getElementById("toggle").innerText = "Read Less";
    } else {
        text.style.display = "none";
        document.getElementById("toggle").innerText = "Read More";
    }
});