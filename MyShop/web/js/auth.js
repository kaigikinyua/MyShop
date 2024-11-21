async function login(){
    var username=document.getElementById("username").value
    var password=document.getElementById("password").value
    console.log(username+''+password)
    if(username.length>0 && password.length>0){
        var response=await eel.login(username,password)()
        if(response['auth']==true){
            localStorage.setItem('token',response['token'])
            redirectToPage(response['userLevel'])
        }else{
            notificationBubble(response['message'])
        }
    }else{
        notificationBubble("Please fill in your Username and Password",2)
    }
}
async function logOut(){
    console.log("logging out")
    var token=localStorage.getItem('token')
    var arr_token=token.split(':')
    console.log(arr_token[arr_token.length-1])
    var response=await eel.logOut(arr_token[arr_token.length-1])()
    console.log(response)
    if(response['state']==true){
        localStorage.removeItem('token')
        console.log("Logged out")
        redirectToPage('login')
    }
}
function redirectToPage(page){
    const pages={'admin':'admin.html','cashier':'till.html','login':'login.html'}
    location.href=pages[page]
}
