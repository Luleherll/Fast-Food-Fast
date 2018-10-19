var item = sessionStorage.getItem('data');
var data=JSON.parse(item);
var token = sessionStorage.getItem('token');
var pass=JSON.parse(token);
var divs = document.getElementsByClassName('slides')[3];

data.orders.forEach((order) => {
    const div = document.createElement('div');
    const inputs = document.createElement('div');
    const qName = document.createElement('span');
    const place = document.createElement('span');
    const price = document.createElement('span');
    const accept = document.createElement('input');
    const decline = document.createElement('input');
    
    div.setAttribute('class', 'item')
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
        'Authorization': 'Bearer '+pass.access
	}),
	body: JSON.stringify({
		"status": "Pending"
	})
}).then(function(response) { 
	return response.json();
}).then(function(j) { 
	console.log(j)
})
    })
    decline.addEventListener('click', function() {
        fetch('https://lule-persistent.herokuapp.com/api/v2/orders/'+order.order_id, {
    method: 'put',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+pass.access
	}),
	body: JSON.stringify({
		"status": "Declined"
	})
}).then(function(response) { 
	return response.json();
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
