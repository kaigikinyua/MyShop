function login(){
    console.log("Login")
    eel.login()
}
function logOut(){
    
}


function notificationBubble(message,mode){
    //crimsonRed,mint green,amber
    const colors=['#DC143C','#98FB98','#FFBF00']
    var elm=document.getElementById('notification')
    elm.innerHTML=message
    elm.style.backgroundColor=colors[mode]
    elm.classList.add('active')
    setTimeout(()=>{
        var elm=document.getElementById('notification')
        elm.classList.remove('active')
    },10000)
    console.log(message)
}