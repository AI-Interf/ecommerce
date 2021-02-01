var updateBtn = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtn.length; i++){
	updateBtn[i].addEventListener('click', function(){
		var itemID = this.dataset.product
		var action = this.dataset.action
		console.log('itemID:', itemID, 'Action:', action)

		console.log('USER', user)// check for user info

		//condition to check if the user is logged in or not
		if(user === 'AnonymousUser'){
			addCookie(itemID, action)
		}else{
			updateOrder(itemID, action)
		}
	})
}

//function to add cookie in the browser
function addCookie(itemID, action){
	console.log('User not authenticated')

	if(action == 'add'){
		//check if the cart has item in it and if there is item in it than add to it
		if(cart[itemID] == undefined){
			cart[itemID] = {'quantity':1}
		}else{
			cart[itemID]['quantity'] += 1
		}
	}

	if(action == 'remove'){
		cart[itemID]['quantity'] -= 1

		//if the quantity is less than zero than delete it 
		if(cart[itemID]['quantity'] <= 0){
			console.log('remove item')
			delete cart[itemID]
		}
	}

	console.log('Cart:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path/"
	location.reload()
}



function updateOrder(itemID, action){
	console.log("user is logged in...")

	var url = '/updateItem/'//this is where we want to send the data to

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'itemID': itemID, 'action': action})
	})

	.then((response) =>{
		return response.json()
	})

	.then((data) =>{
		console.log('data:', data)
		location.reload()
	})
}

