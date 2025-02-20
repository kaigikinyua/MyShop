//var items=[]
var productsList=[]
var branches=[]

var customerBusket=[]
var busketTotalPrice=0
var payments=[]
//user action buttons
//adds item to the list when user clicks 'Add Product' btn
function addItem(){
    itemName=document.getElementById('itemCode').value
    quantity=document.getElementById('quantity').value
    if(itemName.length>0 && quantity.length>0){
        var itemFound=false
        productsList.forEach((p)=>{
            if(p['barCode']==itemName){
                price=p['sPrice']
                total=price*quantity
                customerBusket.push({'name':p['name'],'barCode':p['barCode'],'price':p['sPrice'],'quantity':quantity,'total':total,'discount':0,})
                Render.renderItems(customerBusket)
                Transaction.computeTotal(customerBusket)
                itemFound=true
                Render.clearItemCode()
            }
        });
        if(itemFound==false){
            console.log("There is no product with id "+itemName)
            notificationBubble("There is no product with id "+itemName,2,4)
        }
    }
    else{
        notificationBubble("Please fill in the item code and quantity",2,4)
    }

}

//removes item from the productsList when user clicks 'remove' btn on item list in the UI
function removeItem(itemId){
    var id=itemId.split(',')
    if(customerBusket.length>0){
        customerBusket.splice(id,1)
    }
    Transaction.computeTotal(customerBusket)
    Render.renderItems(customerBusket)
}
//when user clicks 'Pay' button on UI it displays a Pay Pop Up
function displayPaymentBox(){
    showPopUp("")
    var popUpPanel=document.getElementById('popUpPanel')
    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Payment"
    //var x=await eel.makeSale()

    var paymentMethods=document.createElement('div')
    var paymentOptions=document.createElement('div')

    paymentOptions.innerHTML="<button id='mpesaOpt' class='cool' onclick=changePaymentTo('mpesa')>Mpesa</button>" 
    paymentOptions.innerHTML+="<button id='cashOpt' class='innactive' onclick=changePaymentTo('cash')>Cash</button>"
    paymentOptions.innerHTML+="<button id='bankOpt' class='innactive' onclick=changePaymentTo('bank')>Bank</button>"
    paymentOptions.innerHTML+="<button id='creditOpt' class='innactive' onclick=changePaymentTo('credit')>Credit</button>"

    var mpesaOption=document.createElement('div')
    var cashOption=document.createElement('div')
    var bankOption=document.createElement('div')
    var creditOption=document.createElement('div')

    mpesaOption.innerHTML='<input type="text" placeholder="Transaction Id" id="mpesaId"/>'
    mpesaOption.innerHTML+='<input type="number" placeholder="Phone Number" id="mpesaPhoneNum"/>'
    mpesaOption.innerHTML+='<input type="number" id="mpesaAmount" placeholder="Mpesa Amount"/>'
    mpesaOption.innerHTML+='<button onclick=addPayment("mpesa")>Add Payment</button>'

    cashOption.innerHTML='<input type="number" placeholder="Cash Amount" id="cashAmount"/>'
    cashOption.innerHTML+='<button onclick=addPayment("cash")>Add Payment</button>'

    bankOption.innerHTML='<input type="number" placeholder="Bank Account Number" id="bankAccNumber">'
    bankOption.innerHTML+='<input type="number" id="bankAmount" placeholder="Bank Amount"/>'
    bankOption.innerHTML+='<input type="text" placeholder="Bank Name eg Equity or KCB" id="bankName"/>'
    bankOption.innerHTML+='<button onclick=addPayment("bank")>Add Payment</button>'

    creditOption.innerHTML='<input type="number" placeholder="Credit Amount" id="creditAmount"/>'
    creditOption.innerHTML+='<input type="date" id="creditDeadline"/>'
    creditOption.innerHTML+='<input type="text" id="creditCustomerId" placeholder="Customer System Id Name"/>'
    creditOption.innerHTML+='<input type="text" id="creditCustomerPhone" placeholder="Customer Phone Number"/>'
    creditOption.innerHTML+='<button onclick=addPayment("credit")>Add Payment</button>'

    mpesaOption.id="mpesa";cashOption.id="cash";bankOption.id="bank";creditOption.id="credit"
    mpesaOption.style.display="";cashOption.style.display="none";bankOption.style.display="none";creditOption.style.display="none"
    paymentMethods.appendChild(mpesaOption);paymentMethods.appendChild(cashOption);paymentMethods.appendChild(bankOption);paymentMethods.appendChild(creditOption)
    
    var customerIdTile=document.createElement("div")
    customerIdTile.innerHTML="<input type='text' id='customerId' placeholder='Customer Registration Number'/>"

    var paymentTile=document.createElement('div')
    paymentTile.id='paymentTile'

    var balanceTile=document.createElement('h3')
    balanceTile.innerHTML="Balance "+busketTotalPrice
    balanceTile.id="transactionBalance"

    var completeTransaction=document.createElement("button")
    completeTransaction.innerHTML="Complete Transaction"
    completeTransaction.classList.add("minLenBtn")
    completeTransaction.classList.add("innactive")
    completeTransaction.disabled=true
    completeTransaction.id="completeTransaction"
    completeTransaction.onclick=(()=>sendTransactionToBackend())

    var cancel=document.createElement("button")
    cancel.innerHTML="Cancel"
    cancel.classList.add("minLenBtn")
    cancel.classList.add("cool")
    cancel.onclick=closePopUp

    popUpPanel.appendChild(header)
    popUpPanel.appendChild(paymentOptions)
    popUpPanel.appendChild(paymentMethods)
    popUpPanel.appendChild(paymentTile)
    popUpPanel.appendChild(customerIdTile)
    popUpPanel.appendChild(balanceTile)
    popUpPanel.appendChild(cancel)
    popUpPanel.appendChild(completeTransaction)
}

//changes the view on the payment pop up to the selected payment by the user
function changePaymentTo(paymentType){
    console.log("Changing Pyament to "+paymentType)
    var paymentTypes=['mpesa','cash','bank','credit']
    var elmToDisplay=document.getElementById(paymentType)
    var paymentBtnClicked=document.getElementById(paymentType+'Opt')
    //hidding all the divs containg the payment option fields/inputs
    paymentTypes.forEach(elm=>{
        document.getElementById(elm).style.display='none'
        var btn=document.getElementById(elm+'Opt')
        btn.classList.remove('cool')
        btn.classList.add('innactive')
    });
    //getting the divs containing the payment option and display it
    elmToDisplay.style.display=''
    paymentBtnClicked.classList.remove('innactive')
    paymentBtnClicked.classList.add('cool')

}
//Adds the payment to payments global variable and renders the payment details in paymetTile on the payment Pop Up
function addPayment(paymentMethod){
    var amount=0
    var tDetails=null
    switch(paymentMethod){
        case 'mpesa':
            amount=document.getElementById("mpesaAmount").value
            var phoneNum=document.getElementById("mpesaPhoneNum").value
            var mpesaTId=document.getElementById("mpesaId").value
            tDetails={"paymentType":"mpesa","amount":amount,"phoneNum":phoneNum,"mpesaTid":mpesaTId}
           break;
        case 'cash':
            amount=document.getElementById("cashAmount").value
            tDetails={"paymentType":"cash","amount":amount}
            break;
        case 'bank':
            amount=document.getElementById("bankAmount").value
            var bankAccNum=document.getElementById("bankAccNumber").value
            var bankName=document.getElementById("bankName").value
            tDetails={"paymentType":"bank","amount":amount,"bankAccNumber":bankAccNum,"bankName":bankName}
            break;
        case 'credit':
            amount=document.getElementById("creditAmount").value
            var custId=document.getElementById("creditCustomerId").value
            var custPhone=document.getElementById("creditCustomerPhone").value
            tDetails={"paymentType":"credit","amount":amount,"custId":custId,"custPhone":custPhone}
            break; 
    }
    var balance=busketTotalPrice
    var addNewPaymentTransaction=true
    if(tDetails!=null && amount!=0){
        payments.forEach(p=>{
            balance=balance-p["amount"]
        });
        if((balance-amount)<0){
            //ensures that you don't add another transaction that makes the balance go to negative
            addNewPaymentTransaction=false
            notificationBubble("You Will overcharge the customer",0,3)
        }else if((balance-amount)>=0){
            payments.push(tDetails)
            balance=balance-amount
            notificationBubble("Balance Updated successfully",1,3)
        }
    }
    
    if(addNewPaymentTransaction){
        //rendering the details to the Payment Tile on The Payment Pop Up
        var paymentTile=document.getElementById("paymentTile")
        paymentTile.innerHTML="<h3>Payments</h3>"
        var pList=document.createElement('div')
        pList.classList.add('listView')
        payments.forEach(p=>{
            var xPayment=document.createElement("div")
            var paymentType=p["paymentType"]
            var paymentAmount=p["amount"]
            xPayment.innerHTML+="<div>Paid "+paymentType+" Ksh "+paymentAmount+"</div>"
            pList.appendChild(xPayment)
        });
        var balanceTile=document.getElementById("transactionBalance")
        balanceTile.innerHTML="Balance "+balance
        paymentTile.appendChild(pList)
        if(balance==0){
            var btn=document.getElementById("completeTransaction")
            btn.disabled=false
            btn.classList.remove("innactive")
            btn.classList.add("danger")
        }
    }
}

function sendTransactionToBackend(){
    var counterId=document.getElementById("counterID").value
    var customerId=document.getElementById("customerId").value
    if(customerId.length==0){
        customerId='null'
    }
    Transaction.sendTransactionToBackend(customerBusket,payments,counterId,customerId)
}


//shift action buttons
function displayStartingAmount(){
    showPopUp("")
    var popUpPanel=document.getElementById('popUpPanel')
    
    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Declare Starting Amount"
    var sAmount=document.createElement("input")
    sAmount.placeholder='Starting Amount'
    sAmount.id="sAmountDeclaration"
    var submit=document.createElement("button")
    submit.innerHTML="Submit"
    //submit.classList.add("submit")
    submit.classList.add("minLenBtn")
    submit.classList.add("danger")
    submit.onclick=(()=>{
        var sAmount=document.getElementById("sAmountDeclaration").value
        if(sAmount!=undefined && sAmount!=null && sAmount!=""){
            Shift.declareStartingAmount(sAmount)
            closePopUp()
            notificationBubble("Declared starting amount",1,3)
        }else{
            notificationBubble("Please fill in the starting amount",2,3)
        }
    })
    var cancel=document.createElement("button")
    cancel.innerHTML="Cancel"
    cancel.classList.add("minLenBtn")
    cancel.classList.add("cool")
    cancel.onclick=closePopUp

    popUpPanel.appendChild(header)
    popUpPanel.appendChild(sAmount)
    popUpPanel.appendChild(submit)
    popUpPanel.appendChild(cancel)
}
function displayClosingAmount(){
    showPopUp("")
    var popUpPanel=document.getElementById('popUpPanel')
    
    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Declare Closing Amount"
    var cAmount=document.createElement("input")
    cAmount.placeholder='Closing Amount'
    cAmount.id="cAmountDeclaration"
    var submit=document.createElement("button")
    submit.innerHTML="Submit"
    //submit.classList.add("submit")
    submit.classList.add("minLenBtn")
    submit.classList.add("danger")
    submit.onclick=(()=>{
        var cAmount=document.getElementById("cAmountDeclaration").value
        if(cAmount!=undefined && cAmount!=null && cAmount!=""){
            Shift.declareClosingAmount(sAmount)
            closePopUp()
            notificationBubble("Declared closing amount",1,3)
        }else{
            notificationBubble("Please fill in the closing amount",2,3)
        }
    })
    var cancel=document.createElement("button")
    cancel.innerHTML="Cancel"
    cancel.classList.add("minLenBtn")
    cancel.classList.add("cool")
    cancel.onclick=closePopUp

    popUpPanel.appendChild(header)
    popUpPanel.appendChild(cAmount)
    popUpPanel.appendChild(submit)
    popUpPanel.appendChild(cancel)
}


class Render{
    static renderItems(items){
        var list=document.getElementById('itemList')
        while(list.hasChildNodes()){
            list.removeChild(list.firstChild)
        }
        var i=0
        items.forEach(item=>{
            i+=1
            var itemParent=document.getElementById('itemList')
            var itemDiv=document.createElement('div')
            itemDiv.classList.add('item')
            itemDiv.id='item,'+i
            itemDiv.innerHTML=item['name']+' @ '+item['price']+' * '+item['quantity']+' ='+item['total']
            var deleteItem=document.createElement('button')
            deleteItem.addEventListener('click',()=>{removeItem(itemDiv.id)})
            deleteItem.innerHTML="remove"
            deleteItem.classList.add('danger')
            itemDiv.appendChild(deleteItem)
            itemParent.appendChild(itemDiv)
        });
    }
    static clearAllItems(){
        var list=document.getElementById('itemList')
        while(list.hasChildNodes()){
            list.removeChild(list.firstChild)
        }
    }
    static clearItemCode(){
        document.getElementById('itemCode').value=""
        document.getElementById('quantity').value=1
    }
    static renderSearchBoxProducts(products){
        let parent=document.getElementById('searchItemCode')
        products.forEach(p=>{
            var container=document.createElement('ul')
            container.innerHTML="<li>"+p['name']+" "+p['barCode']+"</li>"
            container.classList.add('listView')
            parent.appendChild(container)
        })
    }
    static renderBranchesToSelectBox(branches){
        var selectBox=document.getElementById('counterID')
        var defaultid=0
        branches.forEach(b=>{
            var opt=document.createElement('option')
            opt.value=b['id']
            opt.innerHTML=b['name']
            selectBox.appendChild(opt)
            defaultid=defaultid+1
        });
    }
}

class FetchData{
    static async getProductsAndBranches(){
        var response=await eel.getProductsAndBranches()()
        return response
    }

    static async customerCreditWorthy(custIdName,custPhoneNumber,amount){
        var response=await eel.isCustomerCreditWorth(custIdName,custPhoneNumber,amount)
        return response
    }
}
class Shift{
    static declareStartingAmount(amount){
        console.log("Starting amount is "+amount)
    }
    static declareClosingAmount(amount){
        console.log("Closing amount is "+amount)
    }
    openShift(){}
    closeShift(){}
}

class Transaction{
    static getTransaction(transactionId){}
    static loadTransaction(transaction){}
    static getTransactions(){}
    static getAllTransactions(){}
    static async sendTransactionToBackend(busket,payments,counterId,custId){
        console.log("Sending transaction to the backend")
        var cashierId=Auth.getUserId()
        var response=await eel.makeSale(busket,payments,counterId,cashierId,custId)()
        console.log(response['state'])
        if(response['state']==true){
            Transaction.clearTransactionFromUi()
            notificationBubble("Transaction Completed Successfully",1,5)
        }else{
            notificationBubble("Transaction Failed",0,5)
        }
    }
    static clearTransactionFromUi(){
        Render.clearAllItems()
        customerBusket=[]
        busketTotalPrice=0
        payments=[]
        closePopUp()
    }

    static computeTotal(items){
        var tot=0
        items.forEach(i=>{
            tot+=i["total"]
        });
        busketTotalPrice=tot
        document.getElementById("basketTotal").innerHTML=busketTotalPrice
    }
}

class Reports{
    static generateXReport(){}
    static generateZReport(){}
}

class Auth{
    static renderShiftId(){
        var shiftId=localStorage.getItem('shiftId')
        var x=document.getElementById("shiftId")
        x.innerHTML="Shift "+shiftId+" | "
    }
    static getUserId(){
        var token=localStorage.getItem('token')
        var splitToken=token.split(':')
        return splitToken[splitToken.length-1]
    }
}

function setUpUser(){
    Auth.renderShiftId()
}

setTimeout(async ()=>{
    setUpUser()
    response=await FetchData.getProductsAndBranches()
    productsList=response['products']
    branches=response['branches']
    Render.renderSearchBoxProducts(productsList)
    Render.renderBranchesToSelectBox(branches)
},1000)
