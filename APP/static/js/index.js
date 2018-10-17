

var btnClose = document.getElementById("close");

btnClose.addEventListener("click", function () {
      document.getElementById("banner").style.display="none";
});


document.getElementById("login").addEventListener("click", function() {
	fetch('https://lule-persistent.herokuapp.com/api/v2/auth/login', {
    method: 'post',
    mode: 'cors',
	headers: new Headers({
		'Content-Type': 'application/json'
	}),
	body: JSON.stringify({
		"username": document.getElementById('username').value,
		"password": document.getElementById('password').value
	})
}).then(function(response) { 
	return response.json();
}).then(function(j) {
	if(j.msg!==undefined){
       document.getElementById('msg').innerText=j.msg;
       var alert=document.getElementById('banner')
	   alert.style.display='block';
	   alert.style.background='rgba(172, 255, 47, 0.356)';
	}else if(j.error!==undefined){
		document.getElementById('msg').innerText=j.error;
		var alert=document.getElementById('banner')
		alert.style.background='rgb(224, 22, 22)'
		alert.style.display='block';
	}else{
		fetch('https://lule-persistent.herokuapp.com/api/v2/orders/', {
    method: 'get',
    mode: 'cors',
	headers: new Headers({
		'Content-Type': 'application/json',
		'Authorization': 'Bearer '+j
	})
	
   }).then(function(response) {return response.json();}).then(function(res) {
	   if(res.msg!==undefined){
		fetch('https://lule-persistent.herokuapp.com/api/v2/menu', {
			method: 'get',
			mode: 'cors',
			headers: new Headers({
				'Content-Type': 'application/json',
				'Authorization': 'Bearer '+j
			})
			
		   }).then(function(response) {return response.json();}).then(function(menu) {
			   sessionStorage.setItem('data', JSON.stringify({menu:menu}));
	           window.location.replace('http://localhost:5000/home')
		   })
		   
	   }else{

		sessionStorage.setItem('data', JSON.stringify({orders:res}));
		window.location.replace('http://localhost:5000/admin')
	   }
	   
	   
	   
   })
     
	}
})
});
document.getElementById("signup").addEventListener("click", function() {
	fetch('https://lule-persistent.herokuapp.com/api/v2/auth/signup', {
    method: 'post',
    mode: 'cors',
	headers: new Headers({
		'Content-Type': 'application/json'
	}),
	body: JSON.stringify({
		"username": document.getElementById('newUser').value,
		"password": document.getElementById('newPassword').value,
		"tel": document.getElementById('newTel').value,
		"email": document.getElementById('newEmail').value,
		"location": document.getElementById('location').value,
		"key point": document.getElementById('keyPoint').value
	})
}).then(function(response) {
	sessionStorage.setItem('status', response.status)
	console.log(response.status)
	return response.json();
}).then(function(j) {
	var status=sessionStorage.getItem('status')
	sessionStorage.removeItem('status')
	if(status===401){
       document.getElementById('msg').innerText=j.error;
       var alert=document.getElementById('banner')
	   alert.style.display='block';
	   alert.style.background='rgba(172, 255, 47, 0.356)';
	}else if(status==406){
		document.getElementById('msg').innerText=j.msg;
		var alert=document.getElementById('banner')
		alert.style.background='rgb(224, 22, 22)'
		alert.style.display='block';
	}else{
		current(3)
		document.getElementById('info').innerText=j
		document.getElementById('myModal').style.display='block';
	}
})});