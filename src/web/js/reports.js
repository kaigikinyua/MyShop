var reports=['xReport','zReport','cReport','sReport']

function displayReports(){
    reports.forEach((r)=>{
        var reportBody=localStorage.getItem(r)
        var heading=document.createElement('h3')
        heading.innerHTML=r
        var body=document.createElement('div')
        body.classList.add('paddedContainer')
        body.innerHTML='<pre>'+reportBody+'</pre>'
        var reportPanel=document.getElementById(r)
        reportPanel.appendChild(heading)
        reportPanel.appendChild(body)
    })
}

setTimeout(()=>{
    displayReports()
    deleteBrowserTokens()
},500)