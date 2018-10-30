var home = document.getElementsByClassName('slides')[3];
var pendingOrders = document.getElementsByClassName('slides')[1];
var myHistory = document.getElementsByClassName('slides')[0];
var select = document.getElementsByTagName('select')[0];

fetch('https://lule-persistent.herokuapp.com/api/v2/menu', {
			method: 'get',
			mode: 'cors',
			headers: new Headers({
				'Content-Type': 'application/json',
				'Authorization': 'Bearer '+sessionStorage.getItem('token')
			})
			
}).then(function(response) {return response.json();}).then(function(menu) {
	menu.forEach((food) => {
    const pDiv = document.createElement('div');
    const pInputs = document.createElement('div');
    const pName = document.createElement('span');
    const pStatus = document.createElement('span');
    const pPrice = document.createElement('span');
    const orderNow = document.createElement('input');
    const images = document.createElement('span');
    const img1 = document.createElement('img');
    const img2 = document.createElement('img');
    const img3 = document.createElement('img');
    
    pDiv.setAttribute('class', 'item')
    pDiv.setAttribute('id', food.food_id)
    orderNow.setAttribute('class', 'decline')
    orderNow.setAttribute('type', 'button')
    orderNow.setAttribute('value', 'Order Now')
    images.setAttribute('class', 'images')

    orderNow.addEventListener('click', function() {
        if(food.status=='Unavailable'){
            document.getElementById('info').innerText=food.name+' is unavailable at the moment.'
	        document.getElementById('myModal').style.display='block';
        }else{
            document.getElementById('orderImage').setAttribute('src', food.img1)
            document.getElementById('foodName').innerText=food.name
            document.getElementById('foodPrice').innerText='Ush '+food.price+' each';
            current(3)
        }
    })

    pName.innerText=food.name
    pName.innerHTML+='<br>'
    pStatus.innerText=food.status;
    pPrice.innerText=' Price: Ush'+food.price
    img1.setAttribute('src', food.img1)
    img2.setAttribute('src', food.img2)
    img3.setAttribute('src', food.img3)
    images.appendChild(img1)
    images.appendChild(img2)
    images.appendChild(img3)
    pInputs.appendChild(pName);
    pInputs.appendChild(pStatus);
    pInputs.appendChild(pPrice);
    pInputs.appendChild(orderNow);
    pDiv.appendChild(images)
    pDiv.appendChild(pInputs);
    home.appendChild(pDiv);
  }); 
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';
    }else if("TypeError: menu.forEach is not a function"){
        window.location.replace('http://lule-foods.herokuapp.com/')
    }
    
});

fetch('https://lule-persistent.herokuapp.com/api/v2/users/orders', {
			method: 'get',
			mode: 'cors',
			headers: new Headers({
				'Content-Type': 'application/json',
				'Authorization': 'Bearer '+sessionStorage.getItem('token')
			})
			
}).then(function(response) {return response.json();}).then(function(orders) {
	orders.forEach((order) => {
    const pDiv = document.createElement('div');
    const pInputs = document.createElement('div');
    const pName = document.createElement('span');
    const pPlace = document.createElement('span');
    const pPrice = document.createElement('span');
    const time = document.createElement('span');
    const pending = document.createElement('input');
    const images = document.createElement('span');
    const img1 = document.createElement('img');
    
    pDiv.setAttribute('class', 'item')
    pDiv.setAttribute('id', order.order_id)
    pending.setAttribute('class', 'accept')
    time.setAttribute('class', 'accept')
    pending.setAttribute('type', 'button')
    pending.setAttribute('value', 'Pending..')
    images.setAttribute('class', 'images')
    img1.setAttribute('src', order.img1)

    pName.innerText=order.quantity+' '+order.name+' || Started At:'
    time.innerText=order.ended_at
    time.innerHTML+='<br>'
    pPlace.innerText='From: '+order.location;
    pPrice.innerText=' Price: Ush'+order.amount
    pInputs.appendChild(pName);
    pInputs.appendChild(time);
    pInputs.appendChild(pPlace);
    pInputs.appendChild(pPrice);
    pInputs.appendChild(pending);
    images.appendChild(img1);
    pDiv.appendChild(images);
    pDiv.appendChild(pInputs);
    pendingOrders.appendChild(pDiv);
  }); 
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';
    }else if("TypeError: orders.forEach is not a function"){
        window.location.replace('http://lule-foods.herokuapp.com/')
    }
    
});

fetch('https://lule-persistent.herokuapp.com/api/v2/users/history', {
			method: 'get',
			mode: 'cors',
			headers: new Headers({
				'Content-Type': 'application/json',
				'Authorization': 'Bearer '+sessionStorage.getItem('token')
			})
			
}).then(function(response) {return response.json();}).then(function(orders) {
	orders.forEach((order) => {
    const pDiv = document.createElement('div');
    const pInputs = document.createElement('div');
    const pName = document.createElement('span');
    const pstate = document.createElement('span');
    const pPrice = document.createElement('span');
    const time = document.createElement('span');
    const images = document.createElement('span');
    const img1 = document.createElement('img');
    
    pDiv.setAttribute('class', 'item')
    pDiv.setAttribute('id', order.order_id)
    pstate.setAttribute('class', 'accept')
    time.setAttribute('class', 'accept')
    images.setAttribute('class', 'images')
    img1.setAttribute('src', order.img1)

    pName.innerText=order.quantity+' '+order.name+' || '
    time.innerText='Delivered At: '+order.ended_at
    pstate.innerText=order.status
    pstate.innerHTML+='<br>'
    pPrice.innerText=' Price: Ush'+order.amount
    pPrice.innerHTML+='<br>'
    pInputs.appendChild(pName);
    pInputs.appendChild(pstate);
    pInputs.appendChild(pPrice);
    pInputs.appendChild(time);
    
    images.appendChild(img1);
    pDiv.appendChild(images);
    pDiv.appendChild(pInputs);
    myHistory.appendChild(pDiv);
  }); 
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';
    }else if("TypeError: orders.forEach is not a function"){
        window.location.replace('http://lule-foods.herokuapp.com/')
    }
    
});

document.getElementById('remove').addEventListener("click", function(){
	document.getElementById('myModal').style.display='none'
});

document.getElementById("orderNow").addEventListener("click", function() {
    var select = document.getElementById('foodQ')
	fetch('https://lule-persistent.herokuapp.com/api/v2/users/orders', {
    method: 'post',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+sessionStorage.getItem('token')
	}),
	body: JSON.stringify({
		"name": document.getElementById('foodName').innerText,
		"quantity": parseInt(select.options[select.selectedIndex].text, 10) ,
		"comment": document.getElementById('foodComment').value

	})
}).then(function(response) {
	sessionStorage.setItem('status', response.status)
	return response.json();
}).then(function(j) {
	var status=sessionStorage.getItem('status')
    sessionStorage.removeItem('status') 
	if(status==201){
		document.getElementById('info').innerText=j.msg
	    document.getElementById('myModal').style.display='block';
	    
	}else if(status==406){
		document.getElementById('msg').innerText=j.msg;
		var alert=document.getElementById('banner')
		alert.style.background='rgb(224, 22, 22)'
		alert.style.display='block';
	}else{
		if(j.msg!==undefined){
			document.getElementById('msg').innerText=j.msg;
            var alert=document.getElementById('banner')
	        alert.style.display='block';
	        alert.style.background='rgb(233, 139, 16)';
		}else if(j.error!==undefined){
			document.getElementById('msg').innerText=j.error;
            var alert=document.getElementById('banner')
	        alert.style.display='block';
	        alert.style.background='rgb(233, 139, 16)';
		}else{
			document.getElementById('msg').innerText=j;
            var alert=document.getElementById('banner')
	        alert.style.display='block';
	        alert.style.background='rgb(233, 139, 16)';
		}
		
	}
})});
document.getElementById('logout').addEventListener("click", function(){
    sessionStorage.removeItem('token')
    window.location.replace('http://lule-foods.herokuapp.com/')
});