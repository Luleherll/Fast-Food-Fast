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
  function check(data,action) {
    var status=sessionStorage.getItem('status')
    sessionStorage.removeItem('status')
    var alert=document.createElement('div')
    var message=document.createElement('span')
    var close=document.createElement('span')

    if(action=='add'){
        var div=document.getElementsByClassName('editors')[0]
    }else if(action=='update'){
        var div=document.getElementsByClassName('editors')[1]
    }else{var div=document.getElementsByClassName('editors')[2]}

    alert.setAttribute('id', 'alert')
    
    close.setAttribute('id', 'close')
    close.addEventListener('click', function () {
        alert.style.display='none';
    })
        
	if(status==201){
		document.getElementById('info').innerText=data.msg
	    document.getElementById('myModal').style.display='block';
	}else if(status==400){
		message.innerText=data.error;
		alert.style.background='rgb(224, 22, 22)'
        alert.appendChild(message)
        alert.appendChild(close)
        div.insertBefore(alert,document.getElementsByTagName('div'))
	}else{
		if(data.msg!==undefined){
			document.getElementById('msg').innerText=data.msg;
            var alert=document.getElementById('confirm1')
	        alert.style.display='block';
	        alert.style.background='rgb(233, 139, 16)';
		}else if(j.error!==undefined){
			document.getElementById('msg').innerText=data.error;
            var alert=document.getElementById('confirm1')
	        alert.style.display='block';
	        alert.style.background='rgb(233, 139, 16)';
		}else{
			document.getElementById('msg').innerText=data;
            var alert=document.getElementById('confirm1')
	        alert.style.display='block';
	        alert.style.background='rgb(233, 139, 16)';
		}
  }}