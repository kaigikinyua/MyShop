const windows=['reportsWindow','stockWindow','usersWindow']
function viewWindow(windowId){
    windows.forEach(w=>{
        console.log(w)
        document.getElementById(w).style.display='none'
    })
    document.getElementById(windowId).style.display=''
}