function login(){
    var username=document.getElementById("username")
    var password=document.getElementById("password")
    if(username.length>0 && password.length>0){
        
    }else{
        notificationBubble("Please fill in your Username and Password",2)
    }
}
