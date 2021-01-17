
var  updateBtns  = document.getElementsByClassName('update-cart')
for (i=0; i < updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productID:',productID, 'action:', action)


        // user is gotten from main.html in head section
        
        console.log('User:' , user)    

        if(user =='AnonymousUser'){
            addCookieItem(productID,action)

        }else{
            updateUserOrder(productID,action)
        }
    })
}

function addCookieItem(productID,action){
    console.log('Not logged in..')
    if(action == 'add'){
        if(cart[productID] == undefined){
            cart[productID]  ={'quantity':1}
        }else{
            cart[productID]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productID]['quantity'] -=1
        
        if(cart[productID]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[productID]
        }
    }
    console.log('item is added')
    console.log('Cart : ',cart)
    document.cookie = 'cart=' +JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}

// in the Above Code, this refer to the button that call the addEventListner method


function updateUserOrder(productID,action){
    console.log('User is loggin in, sending data..')
    var url ='/update_item/'
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type' :'application/json',
            'X-CSRFToken' :csrftoken,
        },
        body:JSON.stringify({'productID':productID,'action':action})

    })

    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('data:' ,data)
        location.reload()
    })
}



