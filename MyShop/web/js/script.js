var timeOutId=null
var highlightFieldId=null
function notificationBubble(message,mode,delay){
    if(timeOutId!=null){
        clearTimeout(timeOutId)
        var elm=document.getElementById('notification')
        elm.innerHTML=""
        elm.classList.remove('active')
        elm.classList.add('passive')
        timeOutId=null
    }
    //crimsonRed,mint green,amber
    //0->error 1->success 2->warning
    const colors=['#DC143C','#98FB98','#EEAE00']
    var elm=document.getElementById('notification')
    elm.classList.remove('active')
    
    elm.innerHTML=message
    elm.style.backgroundColor=colors[mode]
    elm.classList.remove('passive')
    elm.classList.add('active')
    elm.style.animationDuration=delay*1.5+'s'

    timeOutId=setTimeout(()=>{
        var elm=document.getElementById('notification')
        elm.classList.remove('active')
        elm.classList.add('passive')
        timeOutId=null
    },1000*delay)
}
function highlightField(field){
    
}


function closePopUp(){
    var popUp=document.getElementById('popUp')
    var popUpPanel=document.getElementById('popUpPanel')
    popUp.classList.add('passive')
    popUpPanel.classList.add('passive')
    popUpPanel.innerHTML=""
}
function showPopUp(innerHTML){
    var popUp=document.getElementById('popUp')
    var popUpPanel=document.getElementById('popUpPanel')
    popUp.classList.remove('passive')
    popUpPanel.classList.remove('passive')
    popUpPanel.innerHTML=innerHTML
}