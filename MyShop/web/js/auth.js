async function login(){
    var username=document.getElementById("username").value
    var password=document.getElementById("password").value
    console.log(username+''+password)
    if(username.length>0 && password.length>0){
        var response=await eel.login(username,password)()
        if(response['auth']==true){
            redirectToPage(response['userLevel'])
        }else{
            notificationBubble(response['message'])
        }
    }else{
        notificationBubble("Please fill in your Username and Password",2)
    }
}
function redirectToPage(page){
    const pages={'admin':'admin.html','cashier':'till.html'}
    location.href=pages[page]
}
