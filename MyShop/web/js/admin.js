const windows=['reportsWindow','usersWindow','productsWindow']
function viewWindow(windowId){
    windows.forEach(w=>{
        //console.log(w)
        document.getElementById(w).style.display='none'
    })
    document.getElementById(windowId).style.display=''
}

class ButtonActions{
    static async clickXReport(){
        var report=await ReportsActions.getXReport()
        RenderClass.renderReport(report,'X Report')
    }
    static async clickZReport(){
        var report=await ReportsActions.getZreport()
        RenderClass.renderReport(report,'Z Report')
    }
    static async clickCreditReport(){
        var report=await ReportsActions.genCreditreport()
        RenderClass.renderReport(report,'Credit Report') 
    }
    static async clickStockReport(){}
    static async clickStockTake(){}
    static async clickReceiveStock(){}
}

class ReportsActions{
    static async getXReport(){
        var shiftId=Auth.getShiftId()
        var userId=Auth.getUserId()
        var response=await eel.generateXReport(userId,shiftId)()
        if(response['state']==true){
            return response
        }else{
            notificationBubble(response['message'],0,5)
            return response
        }
    }
    static async getZreport(){
        var shiftId=Auth.getShiftId()
        var userId=Auth.getUserId()
        var response=await eel.generateZReport(userId,shiftId)()
        if(response['state']==true){
            return response
        }else{
            notificationBubble(response['message'],0,5)
            return response
        }
    }

    static async genCreditReport(){
        var shiftId=Auth.getShiftId()
        var userId=Auth.getUserId()
        var response=await eel.generateCreditReport(userId)()
        if(response['state']==true){
            return response
        }else{
            notificationBubble(response['message'],0,5)
            return response
        }
    }
}

class ProductActions{
    static addProduct(){

    }
    static async deleteProduct(productId){
        var userId=AdminActions.getUserId()
        var result=await eel.deleteProduct(userId,productId)();
        if(result){

        }
    }
    
}

class AdminFetchDataItems{
    static async getProducts(){
        var products=await eel.getAllProducts()()
        return products
    }
}
class RenderClass{
    //reportsWindow [xReport,zReport,creditReport,stockReport,stockTake,receiveStock]
    static headerId="reportType"
    static parentId="reportContent"
    
    static renderReport(reportContent,reportName){
        var header=document.getElementById(this.headerId)
        var parent=document.getElementById(this.parentId)
        parent.innerHTML='<pre>'+reportContent+'</pre>'
        header.innerHTML=reportName
    }

    static renderStockTake(){}
    static renderReceiveStock(){}

    //products
    static renderProduct(product){
        var parent=document.getElementById('productList')
        var pElement=document.createElement('div')
        var pName=document.createElement('p')
        pName.innerHTML=product['name']
        var deleteProduct=document.createElement('button')
        deleteProduct.classList='danger'
        deleteProduct.innerHTML='Delete'
        deleteProduct.onclick=(()=>{
            AdminActions.deleteProduct(product['id'])
        });
    }
    //users
}


//redundant Auth class and methods in till.js and admin.js
class Auth{
    static renderShiftId(){
        var shiftId=Auth.getShiftId()
        var x=document.getElementById("shiftId")
        x.innerHTML="Shift "+shiftId+" | "
    }
    static getUserId(){
        var token=localStorage.getItem('token')
        var splitToken=token.split(':')
        return splitToken[splitToken.length-1]
    }
    static getShiftId(){
        var shiftId=localStorage.getItem('shiftId')
        if(shiftId!=null && shiftId!=undefined){
            return shiftId
        }else{return 'UnknownShiftId'}
    }
}

function setUpAdmin(){
    Auth.renderShiftId()
}
setTimeout(async ()=>{
    setUpAdmin()
},1000)