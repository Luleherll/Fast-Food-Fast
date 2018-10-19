var item = sessionStorage.getItem('data');
var data=JSON.parse(item);
var divs = document.getElementsByClassName('slides')

for (i = -0; i < data.orders.length; i++) {
    var div = document.createElement('div')
    var inputs=document.createElement('div')
    var images=document.createElement('span')
    var qName=document.createElement('span')
    var place=document.createElement('span')
    var price=document.createElement('span')
    var accept=document.createElement('input')
    var decline=document.createElement('input')

    div.setAttribute('class', 'item')
    images.setAttribute('class','images')
    accept.setAttribute('class', 'accept')
    decline.setAttribute('class', 'decline')
    qName.innerText=data.orders[i].quantity+' '+data.orders[i].name
    qName.innerHTML+='<br>'
    place.innerText="From: " + data.orders[i].location+' '
    price.innerText="Price: " + data.orders[i].amount
    accept.setAttribute('id', 'a'+i)
    decline.setAttribute('id', 'd'+i)
    accept.setAttribute('value', 'Accept')
    decline.setAttribute('value', 'Declined')

    inputs.appendChild(images)
    inputs.appendChild(qName)
    inputs.appendChild(place)
    inputs.appendChild(price)
    inputs.appendChild(accept)
    inputs.appendChild(decline)
    div.appendChild(inputs)
    divs[3].appendChild(div)

    accept.addEventListener('click', function () {
        fetch('https://lule-persistent.herokuapp.com/api/v2/orders/'+ data.orders[i].order_id, {
            method: 'put',
            mode: 'cors',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: JSON.stringify({
                "status": "Queued"
            })
        })
    })
}

