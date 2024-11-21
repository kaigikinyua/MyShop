var timeOutId
function getAuthToken(){

}
function storeAuthToken(){
    
}


function notificationBubble(message,mode,delay){
    if(timeOutId!=null){
        clearTimeout(timeOutId)
    }
    //crimsonRed,mint green,amber
    const colors=['#DC143C','#98FB98','#EEAE00']
    var elm=document.getElementById('notification')
    elm.classList.remove('active')

    elm.innerHTML=message
    elm.style.backgroundColor=colors[mode]
    elm.classList.add('active')
    timeOutId=setTimeout(()=>{
        var elm=document.getElementById('notification')
        elm.classList.remove('active')
        timeOutId=null
    },1000*delay)
}