var updateBtns = document.getElementsByClassName('update-cart')

for (i=0;i< updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var nhanvienId = this.dataset.nhanvien
        var action =this.dataset.action
        console.log('nhanvienId',nhanvienId,'action',action)
        console.log('user: ',user)
        if (user === "AnonymousUser"){
            console.log('user not logged')
        } else{updateUserOrder (nhanvienId,action)
            
        }
    })
}

function updateUserOrder (nhanvienId,action){
    console.log('user logged in, success add')
    var url = '/update_item/'
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'nhanvienId':nhanvienId,'action':action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data',data)
        location.reload()
    })
}