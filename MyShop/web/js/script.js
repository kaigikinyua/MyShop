function login(){
    console.log("Login")
    eel.login()
}


function notificationBubble(message,mode){
    //crimsonRed,mint green,amber
    const colors=['#DC143C','#98FB98','#FFBF00']
    var elm=document.getElementById('notification')
    elm.innerHTML=message
    elm.style.backgroundColor=colors[mode]
}