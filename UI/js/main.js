function on() {
     document.getElementById("overlay").style.display = "block";
 }

function current(n) {
    show(slideIndex = n);
  }
  
  function show(n) {
    var i;
    var slides = document.getElementsByClassName("slides");
    var pages = document.getElementsByClassName("page");
    if (n > slides.length) {slideIndex = 1} 
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
         
    }
    for (i = 0; i < pages.length; i++) {
        pages[i].className = pages[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block"; 
    pages[slideIndex-1].className += " active";
  }