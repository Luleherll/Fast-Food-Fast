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
    console.log(menu)
	menu.forEach((food) => {
    const pDiv = document.createElement('div');
    const pInputs = document.createElement('div');
    const pName = document.createElement('span');
    const pStatus = document.createElement('span');
    const pPrice = document.createElement('span');
    const orderNow = document.createElement('input');
    
    pDiv.setAttribute('class', 'item')
    pDiv.setAttribute('id', food.food_id)
    orderNow.setAttribute('class', 'decline')
    orderNow.setAttribute('type', 'button')
    orderNow.setAttribute('value', 'Order Now')

    orderNow.addEventListener('click', function() {
        document.getElementById('foodName').innerText=food.name
        document.getElementById('foodPrice').innerText='Ush '+food.price+' each';
        current(3)
    })

    pName.innerText=food.name
    pName.innerHTML+='<br>'
    pStatus.innerText=food.status;
    pPrice.innerText=' Price: Ush'+food.price
    pInputs.appendChild(pName);
    pInputs.appendChild(pStatus);
    pInputs.appendChild(pPrice);
    pInputs.appendChild(orderNow);
    pDiv.appendChild(pInputs);
    home.appendChild(pDiv);
  }); 
})

fetch('https://lule-persistent.herokuapp.com/api/v2/users/orders', {
			method: 'get',
			mode: 'cors',
			headers: new Headers({
				'Content-Type': 'application/json',
				'Authorization': 'Bearer '+sessionStorage.getItem('token')
			})
			
}).then(function(response) {return response.json();}).then(function(orders) {
    console.log(orders)
	orders.forEach((order) => {
    const pDiv = document.createElement('div');
    const pInputs = document.createElement('div');
    const pName = document.createElement('span');
    const pPlace = document.createElement('span');
    const pPrice = document.createElement('span');
    const pending = document.createElement('span');
    
    pDiv.setAttribute('class', 'item')
    pDiv.setAttribute('id', order.order_id)
    pending.setAttribute('class', 'accept')

    pName.innerText=order.quantity+' '+order.name
    pName.innerHTML+='<br>'
    pPlace.innerText='From: '+order.location;
    pPrice.innerText=' Price: Ush'+order.amount
    pending.innerText='Pending..'
    pInputs.appendChild(pName);
    pInputs.appendChild(pPlace);
    pInputs.appendChild(pPrice);
    pInputs.appendChild(pending);
    pDiv.appendChild(pInputs);
    pendingOrders.appendChild(pDiv);
  }); 
})

fetch('https://lule-persistent.herokuapp.com/api/v2/users/history', {
			method: 'get',
			mode: 'cors',
			headers: new Headers({
				'Content-Type': 'application/json',
				'Authorization': 'Bearer '+sessionStorage.getItem('token')
			})
			
}).then(function(response) {return response.json();}).then(function(orders) {
    console.log(orders)
	orders.forEach((order) => {
    const pDiv = document.createElement('div');
    const pInputs = document.createElement('div');
    const pName = document.createElement('span');
    const pTime = document.createElement('span');
    const pPrice = document.createElement('span');
    const state = document.createElement('span');
    
    pDiv.setAttribute('class', 'item')
    pDiv.setAttribute('id', order.order_id)
    state.setAttribute('class', 'decline')


    pName.innerText=order.quantity+' '+order.name
    
    pTime.innerText='Delivered At: '+order.ended_at;
    pPrice.innerText=' Price: Ush'+order.amount
    pPrice.innerHTML+='<br>'
    state.innerText=order.status
    state.innerHTML+='<br>'
    pInputs.appendChild(pName);
    pInputs.appendChild(state);
    pInputs.appendChild(pPrice);
    pInputs.appendChild(pTime);
    
    pDiv.appendChild(pInputs);
    myHistory.appendChild(pDiv);
  }); 
})

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
		"quantity": select.options[select.selectedIndex].text,
		"comment": document.getElementById('foodComment').value

	})
}).then(function(response) {
	sessionStorage.setItem('status', response.status)
	return response.json();
}).then(function(j) {
	var status=sessionStorage.getItem('status')
    sessionStorage.removeItem('status')
      console.log(j)  
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