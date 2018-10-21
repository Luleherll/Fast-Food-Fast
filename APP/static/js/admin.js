var divs = document.getElementsByClassName('slides')[3];
fetch('https://lule-persistent.herokuapp.com/api/v2/orders/', {
			method: 'get',
			mode: 'cors',
			headers: new Headers({
				'Content-Type': 'application/json',
				'Authorization': 'Bearer '+sessionStorage.getItem('token')
			})
			
}).then(function(response) {return response.json();}).then(function(orders) {
    console.log(orders)
	orders.forEach((order) => {
    const div = document.createElement('div');
    const inputs = document.createElement('div');
    const qName = document.createElement('span');
    const place = document.createElement('span');
    const price = document.createElement('span');
    const accept = document.createElement('input');
    const decline = document.createElement('input');
    
    div.setAttribute('class', 'item')
    div.setAttribute('id', order.order_id)
    accept.setAttribute('class', 'accept')
    decline.setAttribute('class', 'decline')
    accept.setAttribute('type', 'button')
    decline.setAttribute('type', 'button')
    accept.setAttribute('value', 'Accept')
    decline.setAttribute('value', 'Decline')

    accept.addEventListener('click', function() {

        fetch('https://lule-persistent.herokuapp.com/api/v2/orders/'+order.order_id, {
    method: 'put',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': "Bearer "+sessionStorage.getItem('token')
	}),
	body: JSON.stringify({
		"status": "Pending"
	})
}).then(function(response) {
    if(response.status==205){
      window.location.reload();
    }else{

    }
})
    })
    decline.addEventListener('click', function() {
        fetch('https://lule-persistent.herokuapp.com/api/v2/orders/'+order.order_id, {
    method: 'put',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+sessionStorage.getItem('token')
	}),
	body: JSON.stringify({
		"status": "Declined"
	})
}).then(function(response) { 
    if(response.status==205){
        window.location.reload();
      }else{
  
      }
})
    })

    qName.innerText=order.quantity+' '+order.name
    qName.innerHTML+='<br>'
    place.innerText=order.location+order.order_id;
    price.innerText=order.amount
    inputs.appendChild(qName);
    inputs.appendChild(place);
    inputs.appendChild(price);
    inputs.appendChild(accept);
    inputs.appendChild(decline);
    div.appendChild(inputs);
    divs.appendChild(div);
  }); 
})


document.getElementById('aFood').addEventListener('click', function() {
    document.getElementById('yes').style.display='none';
    fetch('https://lule-persistent.herokuapp.com/api/v2/menu', {
    method: 'post',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+sessionStorage.getItem('token')
	}),
	body: JSON.stringify({
        "name": document.getElementById('newName').value,
        "price": document.getElementById('newPrice').value,
        "status": document.getElementById('newStatus').value,
        "tags": document.getElementById('newTags').value
	})
}).then(function(response) {
    console.log(response.status)
    sessionStorage.setItem('status', response.status)
    return response.json();
}).then(function(res) {
    console.log(res)
    var status=sessionStorage.getItem('status')
    console.log(res.msg)
    
	if(status==201){
		document.getElementById('info').innerText=res.msg
	    document.getElementById('myModal').style.display='block';
	}
})})
 
