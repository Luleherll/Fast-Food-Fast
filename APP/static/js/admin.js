var newOrders = document.getElementsByClassName('slides')[3];
var pendingOrders = document.getElementsByClassName('slides')[2];
var archive = document.getElementsByClassName('slides')[0];
var updateSelect = document.getElementsByTagName('select')[0];
var deleteSelect = document.getElementsByTagName('select')[1];

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
    const time = document.createElement('span');
    const accept = document.createElement('input');
    const decline = document.createElement('input');
    const images = document.createElement('span');
    const img1 = document.createElement('img');
    
    div.setAttribute('class', 'item')
    div.setAttribute('id', order.order_id)
    accept.setAttribute('class', 'accept')
    decline.setAttribute('class', 'decline')
    accept.setAttribute('type', 'button')
    decline.setAttribute('type', 'button')
    accept.setAttribute('value', 'Accept')
    decline.setAttribute('value', 'Decline')
    time.setAttribute('class', 'accept')
    images.setAttribute('class', 'images')
    img1.setAttribute('src', order.img1)
    console.log(order.img1)

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
    if(response.status==200){
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
    if(response.status==200){
        window.location.reload();
      }else{
  
      }
})
    })

    qName.innerText=order.quantity+' '+order.name+' || Ordered At:'
    time.innerText=order.created_at
    time.innerHTML+='<br>'
    place.innerText='From: '+order.location;
    price.innerText=' Price: Ush'+order.amount
    inputs.appendChild(qName);
    inputs.appendChild(time);
    inputs.appendChild(place);
    inputs.appendChild(price);
    inputs.appendChild(accept);
    inputs.appendChild(decline);
    images.appendChild(img1);
    div.appendChild(images);
    div.appendChild(inputs);
    newOrders.appendChild(div);
  }); 
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';
    }else if("TypeError: orders.forEach is not a function"){
        window.location.replace('http://localhost:5000/')
    }
    
});

fetch('https://lule-persistent.herokuapp.com/api/v2/orders/pending', {
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
    const time = document.createElement('span');
    const complete = document.createElement('input');
    const images = document.createElement('span');
    const img1 = document.createElement('img');
    
    pDiv.setAttribute('class', 'item')
    pDiv.setAttribute('id', order.order_id)
    time.setAttribute('class', 'accept')
    complete.setAttribute('class', 'accept')
    complete.setAttribute('type', 'button')
    complete.setAttribute('value', 'Complete')
    images.setAttribute('class', 'images')
    img1.setAttribute('src', order.img1)

    complete.addEventListener('click', function() {

        fetch('https://lule-persistent.herokuapp.com/api/v2/orders/'+order.order_id, {
    method: 'put',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': "Bearer "+sessionStorage.getItem('token')
	}),
	body: JSON.stringify({
		"status": "Completed"
	})
}).then(function(response) {
    if(response.status==200){
      window.location.reload();
    }else{

    }
})
    })

    pName.innerText=order.quantity+' '+order.name+' || Started At:'
    time.innerText=order.ended_at
    time.innerHTML+='<br>'
    pPlace.innerText='From: '+order.location;
    pPrice.innerText=' Price: Ush'+order.amount
    pInputs.appendChild(pName);
    pInputs.appendChild(time);
    pInputs.appendChild(pPlace);
    pInputs.appendChild(pPrice);
    pInputs.appendChild(complete);
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
        window.location.replace('http://localhost:5000/')
    }
    
});

fetch('https://lule-persistent.herokuapp.com/api/v2/orders/archive', {
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
    const time = document.createElement('span');
    const state = document.createElement('span');
    const del = document.createElement('input');
    const images = document.createElement('span');
    const img1 = document.createElement('img');
    
    pDiv.setAttribute('class', 'item')
    pDiv.setAttribute('id', order.order_id)
    state.setAttribute('class', 'decline')
    del.setAttribute('class', 'decline')
    time.setAttribute('class', 'accept')
    del.setAttribute('type', 'button')
    del.setAttribute('value', 'Delete')
    images.setAttribute('class', 'images')
    img1.setAttribute('src', order.img1)

    del.addEventListener('click', function() {

        fetch('https://lule-persistent.herokuapp.com/api/v2/orders/'+order.order_id, {
    method: 'delete',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': "Bearer "+sessionStorage.getItem('token')
	})
}).then(function(response) {
    window.location.reload()
})
    })

    pName.innerText=order.quantity+' '+order.name+' || Delivered At:'
    time.innerText=order.ended_at
    time.innerHTML+='<br>'
    pPlace.innerText='From: '+order.location;
    pPrice.innerText=' Price: Ush'+order.amount+'  '
    state.innerText=order.status
    pInputs.appendChild(pName);
    pInputs.appendChild(time);
    pInputs.appendChild(pPlace);
    pInputs.appendChild(pPrice);
    pInputs.appendChild(state);
    pInputs.appendChild(del);
    images.appendChild(img1);
    pDiv.appendChild(images);
    pDiv.appendChild(pInputs);
    archive.appendChild(pDiv);
  }); 
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';
    }else if("TypeError: orders.forEach is not a function"){
        window.location.replace('http://localhost:5000/')
    }})
fetch('https://lule-persistent.herokuapp.com/api/v2/menu', {
			method: 'get',
			mode: 'cors',
			headers: new Headers({
				'Content-Type': 'application/json',
				'Authorization': 'Bearer '+sessionStorage.getItem('token')
			})
			
}).then(function(response) {return response.json();}).then(function (menu) {
    menu.forEach((food) => {
       const name1 = document.createElement('option');
       const name2 = document.createElement('option');
       name1.innerText=food.name
       name2.innerText=food.name
       updateSelect.appendChild(name1)
       deleteSelect.appendChild(name2)
       
       updateSelect.addEventListener('change', function(){
         if(updateSelect.options[updateSelect.selectedIndex].text==food.name){
           document.getElementsByClassName('uImages')[0].setAttribute('src', food.img1)
           document.getElementsByClassName('uImages')[1].setAttribute('src', food.img2)
           document.getElementsByClassName('uImages')[2].setAttribute('src', food.img3)
           document.getElementById('uPrice').value = food.price
           document.getElementById('uStatus').value = food.status
           document.getElementById('uTags').value = food.tags
       }
      });
       deleteSelect.addEventListener('change', function(){
    if(deleteSelect.options[deleteSelect.selectedIndex].text==food.name){
        document.getElementsByClassName('dImages')[0].setAttribute('src', food.img1)
        document.getElementsByClassName('dImages')[1].setAttribute('src', food.img2)
        document.getElementsByClassName('dImages')[2].setAttribute('src', food.img3)
        document.getElementById('dPrice').value = food.price
        document.getElementById('dStatus').value = food.status
        document.getElementById('dTags').value = food.tags
  }
});
    })
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';
    }else if("TypeError: menu.forEach is not a function"){
        window.location.replace('http://localhost:5000/')
    }
    
});

document.getElementById('close').addEventListener("click", function(){
	close('banner')
});

document.getElementById('aFood').addEventListener('click', function() {

    fetch('https://lule-persistent.herokuapp.com/api/v2/menu', {
    method: 'post',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+sessionStorage.getItem('token')
	}),
	body: JSON.stringify({
        "img1": sessionStorage.getItem('img1'),
        "img2": sessionStorage.getItem('img2'),
        "img3": sessionStorage.getItem('img3'),
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
    sessionStorage.removeItem('img1')
    sessionStorage.removeItem('img2')
    sessionStorage.removeItem('img3')
    console.log(res)
    var status=sessionStorage.getItem('status')
    console.log(res.msg)
    
	if(status==201){
		document.getElementById('info').innerText=res.msg
	    document.getElementById('myModal').style.display='block';
	}else if(status==406){
        document.getElementById('msg').innerText=res.msg
        document.getElementById('banner').style.background='rgb(175, 9, 9)';
        document.getElementById('banner').style.display='block';
    }else{
        if(res.msg!==undefined){
            document.getElementById('msg').innerText=res.msg
            document.getElementById('banner').style.background='rgba(90, 41, 21, 0.781)';
            document.getElementById('banner').style.display='block';
        }else{
            document.getElementById('msg').innerText=res.error
            document.getElementById('banner').style.display='block';
        }
    }
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';}
    
});})

document.getElementById('show1').addEventListener("click", function(){
	document.getElementsByClassName('confirms')[0].style.display='block'
});
document.getElementById('show2').addEventListener("click", function(){
	document.getElementsByClassName('confirms')[1].style.display='block'
});
document.getElementById('logout').addEventListener("click", function(){
    sessionStorage.removeItem('token')
    window.location.replace('http://localhost:5000/')
});
document.getElementById('switch').addEventListener("click", function(){
    window.location.replace('http://localhost:5000/home')
});
document.getElementById('remove').addEventListener("click", function(){
	document.getElementById('myModal').style.display='none'
});
document.getElementsByClassName('exit')[0].addEventListener("click", function(){
	document.getElementsByClassName('confirms')[0].style.display='none'
});
document.getElementsByClassName('exit')[1].addEventListener("click", function(){
	document.getElementsByClassName('confirms')[1].style.display='none'
});
document.getElementById('newImg1').addEventListener("change", function upload(){
    fetch("https://api.cloudinary.com/v1_1/lule/image/upload", {
        method: 'post',
        redirect: 'follow',
        body: new FormData(document.getElementById('xform'))
      }).then(function(response) {
        
        return response.json();
      }).then(function(j) {
        document.getElementsByClassName('newImages')[0].setAttribute('src', j["secure_url"])
        sessionStorage.setItem('img1', j["secure_url"])
        console.log(j)
      })
});
document.getElementById('newImg2').addEventListener("change", function upload(){
    fetch("https://api.cloudinary.com/v1_1/lule/image/upload", {
        method: 'post',
        redirect: 'follow',
        body: new FormData(document.getElementById('yform'))
      }).then(function(response) {
        return response.json();
      }).then(function(j) {
        document.getElementsByClassName('newImages')[1].setAttribute('src', j["secure_url"])
        sessionStorage.setItem('img2', j["secure_url"])
        console.log(j)
      })
});
document.getElementById('newImg3').addEventListener("change", function upload(){
    fetch("https://api.cloudinary.com/v1_1/lule/image/upload", {
        method: 'post',
        redirect: 'follow',
        body: new FormData(document.getElementById('zform'))
      }).then(function(response) {
        return response.json();
      }).then(function(j) {
        document.getElementsByClassName('newImages')[2].setAttribute('src', j["secure_url"])
        sessionStorage.setItem('img3', j["secure_url"])
        console.log(j)
      })
});

document.getElementById('uFood').addEventListener('click', function() {
    document.getElementsByClassName('confirms')[0].style.display='none';
    fetch('https://lule-persistent.herokuapp.com/api/v2/menu', {
    method: 'put',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+sessionStorage.getItem('token')
	}),
	body: JSON.stringify({
        "img1": document.getElementsByClassName('uImages')[0].src,
        "img2": document.getElementsByClassName('uImages')[1].src,
        "img3": document.getElementsByClassName('uImages')[2].src,
        "name": updateSelect.options[updateSelect.selectedIndex].text,
        "price": document.getElementById('uPrice').value,
        "status": document.getElementById('uStatus').value,
        "tags": document.getElementById('uTags').value
	})
}).then(function(response) {
    console.log(response.status)
    sessionStorage.setItem('status', response.status)
    return response.json();
}).then(function(res) {
    
    var status=sessionStorage.getItem('status')
    sessionStorage.removeItem('status')
    console.log(res.msg)
    
	if(status==200){
		document.getElementById('info').innerText=res.msg
	    document.getElementById('myModal').style.display='block';
	}else if(status==406){
        document.getElementById('msg').innerText=res.msg
        document.getElementById('banner').style.background='rgb(175, 9, 9)';
        document.getElementById('banner').style.display='block';
    }else{
        if(res.msg!==undefined){
            document.getElementById('msg').innerText=res.msg
            document.getElementById('banner').style.background='rgba(90, 41, 21, 0.781)';
            document.getElementById('banner').style.display='block';
        }else{
            document.getElementById('msg').innerText=res.error
            document.getElementById('banner').style.display='block';
        }
    }
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';}
    
});})
document.getElementById('dFood').addEventListener('click', function() {
    document.getElementsByClassName('confirms')[1].style.display='none';
    fetch('https://lule-persistent.herokuapp.com/api/v2/menu', {
    method: 'delete',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+sessionStorage.getItem('token')
	}),
	body: JSON.stringify({
        "name": updateSelect.options[updateSelect.selectedIndex].text,
	})
}).then(function(response) {
    console.log(response.status)
    sessionStorage.setItem('status', response.status)
    return response.json();
}).then(function(res) {
    
    var status=sessionStorage.getItem('status')
    sessionStorage.removeItem('status')
    console.log(res.msg)
    
	if(status==200){
		document.getElementById('info').innerText=res.msg
	    document.getElementById('myModal').style.display='block';
	}else if(status==406){
        document.getElementById('msg').innerText=res.msg
        document.getElementById('banner').style.background='rgb(175, 9, 9)';
        document.getElementById('banner').style.display='block';
    }else{
        if(res.msg!==undefined){
            document.getElementById('msg').innerText=res.msg
            document.getElementById('banner').style.background='rgba(90, 41, 21, 0.781)';
            document.getElementById('banner').style.display='block';
        }else{
            document.getElementById('msg').innerText=res.error
            document.getElementById('banner').style.display='block';
        }
    }
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';}
    
});})
document.getElementById('makeAdmin').addEventListener('click', function() {
    document.getElementsByClassName('confirms')[1].style.display='none';
    fetch('https://lule-persistent.herokuapp.com/api/v2/auth/admin', {
    method: 'put',
    mode: 'cors',
	headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+sessionStorage.getItem('token')
	}),
	body: JSON.stringify({
        "username": document.getElementById('userToPromote').value,
	})
}).then(function(response) {
    console.log(response.status)
    sessionStorage.setItem('status', response.status)
    return response.json();
}).then(function(res) {
    
    var status=sessionStorage.getItem('status')
    sessionStorage.removeItem('status')
    console.log(res.msg)
    
	if(status==200){
		document.getElementById('info').innerText=res.msg
	    document.getElementById('myModal').style.display='block';
	}else if(status==406){
        document.getElementById('msg').innerText=res.msg
        document.getElementById('banner').style.background='rgb(175, 9, 9)';
        document.getElementById('banner').style.display='block';
    }else{
        if(res.msg!==undefined){
            document.getElementById('msg').innerText=res.msg
            document.getElementById('banner').style.background='rgba(90, 41, 21, 0.781)';
            document.getElementById('banner').style.display='block';
        }else{
            document.getElementById('msg').innerText=res.error
            document.getElementById('banner').style.display='block';
        }
    }
}).catch(function(error) {
    if(error=="TypeError: NetworkError when attempting to fetch resource."){
        document.getElementById('info').innerText='Please check your internet connection.'
	    document.getElementById('myModal').style.display='block';};
    
});})