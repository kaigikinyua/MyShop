async function login(){
    var username=document.getElementById("username").value
    var password=document.getElementById("password").value
    //console.log(username+''+password)
    if(username.length>0 && password.length>0){
        var response=await eel.login(username,password)()
        if(response['auth']==true){
            localStorage.setItem('token',response['token'])
            localStorage.setItem('shiftId',response['shiftId'])
            redirectToPage(response['userLevel'])
        }else{
            notificationBubble(response['message'])
        }
    }else{
        notificationBubble("Please fill in your Username and Password",2,5)
    }
}
async function logOut(){
    var token=localStorage.getItem('token')
    var arr_token=token.split(':')
    console.log(arr_token[arr_token.length-1])
    var response=await eel.logOut(arr_token[arr_token.length-1])()
    if(response['state']==true){
        localStorage.removeItem('token')
        redirectToPage('login')
    }
}
function redirectToPage(page){
    const pages={'admin':'admin.html','cashier':'till.html','login':'login.html'}
    location.href=pages[page]
}
