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
  function opt(n) {
    slide(slideIndex = n);
  }
  
  function slide(n) {
    var i;
    var edits = document.getElementsByClassName("editors");
    var opts = document.getElementsByClassName("opts");
    if (n > edits.length) {slideIndex = 1} 
    if (n < 1) {slideIndex = edits.length}
    for (i = 0; i < edits.length; i++) {
        edits[i].style.display = "none";
         
    }
    for (i = 0; i < opts.length; i++) {
        opts[i].className = opts[i].className.replace(" active", "");
    }
    edits[slideIndex-1].style.display = "block"; 
    opts[slideIndex-1].className += " active";
  }