//var items=[]
var productsList=[]
var branches=[]
var allCustomers=[]

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
                customerBusket.push({'name':p['name'],'barCode':p['barCode'],'price':p['sPrice'],'quantity':parseInt(quantity),'total':total,'discount':0,})
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
    mpesaOption.innerHTML+='<input type="number" id="mpesaAmount" placeholder="Mpesa Amount" min=0 oninput="this.value = Math.abs(this.value)"/>'
    mpesaOption.innerHTML+='<button onclick=addPayment("mpesa")>Add Payment</button>'

    cashOption.innerHTML='<input type="number" placeholder="Cash Amount" id="cashAmount" min="0" oninput="this.value = Math.abs(this.value)"/>'
    cashOption.innerHTML+='<button onclick=addPayment("cash")>Add Payment</button>'

    bankOption.innerHTML='<input type="number" placeholder="Bank Account Number" id="bankAccNumber">'
    bankOption.innerHTML+='<input type="number" id="bankAmount" placeholder="Bank Amount" min="0" oninput="this.value = Math.abs(this.value)"/>'
    bankOption.innerHTML+='<input type="text" placeholder="Bank Name eg Equity or KCB" id="bankName"/>'
    bankOption.innerHTML+='<button onclick=addPayment("bank")>Add Payment</button>'

    creditOption.innerHTML='<input type="number" placeholder="Credit Amount" id="creditAmount" min="0" oninput="this.value = Math.abs(this.value)"/>'
    creditOption.innerHTML+='<input type="date" id="creditDeadline"/>'
    creditOption.innerHTML+='<input type="text" id="creditCustomerId" placeholder="Customer System Id Name"/>'
    creditOption.innerHTML+='<input type="text" id="creditCustomerPhone" placeholder="Customer Phone Number"/>'
    creditOption.innerHTML+='<button onclick=addPayment("credit")>Add Payment</button>'

    mpesaOption.id="mpesa";cashOption.id="cash";bankOption.id="bank";creditOption.id="credit"
    mpesaOption.style.display="";cashOption.style.display="none";bankOption.style.display="none";creditOption.style.display="none"
    paymentMethods.appendChild(mpesaOption);paymentMethods.appendChild(cashOption);paymentMethods.appendChild(bankOption);paymentMethods.appendChild(creditOption)
    
    var customerIdTile=document.createElement("div")
    customerIdTile.innerHTML="<input type='number' id='customerId' placeholder='Customer Registration Number' default='0'/>"

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
    completeTransaction.onclick=(async ()=>{
        var counterId=document.getElementById("counterID").value
        var customerId=document.getElementById("customerId").value
        if(customerId ==null || customerId==undefined || parseInt(customerId)==0){
            customerId=0
        }
        var response=await Transaction.sendTransactionToBackend(customerBusket,payments,counterId,customerId)
        if(response['state']==true){
            var receipt=Transaction.showReceipt(response)
        }
    })

    var cancel=document.createElement("button")
    cancel.innerHTML="Cancel"
    cancel.classList.add("minLenBtn")
    cancel.classList.add("cool")
    cancel.addEventListener('click',()=>{
        Transaction.clearTransactionFromUi()
    })

    popUpPanel.appendChild(header)
    popUpPanel.appendChild(paymentOptions)
    popUpPanel.appendChild(paymentMethods)
    popUpPanel.appendChild(paymentTile)
    popUpPanel.appendChild(customerIdTile)
    popUpPanel.appendChild(balanceTile)
    popUpPanel.appendChild(cancel)
    popUpPanel.appendChild(completeTransaction)
}

function displayPayCreditBox(){
    showPopUp("")
    var popUpPanel=document.getElementById('popUpPanel')
    popUpPanel.style.minHeight='600px';
    popUpPanel.style.minWidth='600px'
    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Payment"
    //var x=await eel.makeSale()

    var paymentMethods=document.createElement('div')
    var paymentOptions=document.createElement('div')

    paymentOptions.innerHTML="<button id='mpesaOpt' class='cool' onclick=changePaymentTo('mpesa')>Mpesa</button>" 
    paymentOptions.innerHTML+="<button id='cashOpt' class='innactive' onclick=changePaymentTo('cash')>Cash</button>"
    paymentOptions.innerHTML+="<button id='bankOpt' class='innactive' onclick=changePaymentTo('bank')>Bank</button>"

    var mpesaOption=document.createElement('div')
    var cashOption=document.createElement('div')
    var bankOption=document.createElement('div')

    mpesaOption.innerHTML='<input type="text" placeholder="Mpesa Transaction Id" id="mpesaId"/>'
    mpesaOption.innerHTML+='<input type="number" placeholder="Phone Number" id="mpesaPhoneNum"/>'
    mpesaOption.innerHTML+='<input type="number" id="mpesaAmount" placeholder="Mpesa Amount" min="0" oninput="this.value = Math.abs(this.value)"/>'
    mpesaOption.innerHTML+='<button onclick=addPayment("mpesa")>Add Payment</button>'

    cashOption.innerHTML='<input type="number" placeholder="Cash Amount" id="cashAmount" min="0" oninput="this.value = Math.abs(this.value)"/>'
    cashOption.innerHTML+='<button onclick=addPayment("cash")>Add Payment</button>'

    bankOption.innerHTML='<input type="number" placeholder="Bank Account Number" id="bankAccNumber">'
    bankOption.innerHTML+='<input type="number" id="bankAmount" placeholder="Bank Amount" min="0" oninput="this.value = Math.abs(this.value)"/>'
    bankOption.innerHTML+='<input type="text" placeholder="Bank Name eg Equity or KCB" id="bankName"/>'
    bankOption.innerHTML+='<button onclick=addPayment("bank")>Add Payment</button>'

    mpesaOption.id="mpesa";cashOption.id="cash";bankOption.id="bank"
    mpesaOption.style.display="";cashOption.style.display="none";bankOption.style.display="none"
    paymentMethods.appendChild(mpesaOption);paymentMethods.appendChild(cashOption);paymentMethods.appendChild(bankOption)
    
    var customerIdTile=document.createElement("input")
    customerIdTile.id='customerId'
    customerIdTile.placeholder='Customer System Id'
    customerIdTile.onkeyup=(()=>{
        var sCustomer=document.getElementById('searchedCustomers')
        sCustomer.innerHTML=''
        var value=document.getElementById('customerId').value
        allCustomers.forEach((cust)=>{
            var id=String(cust['id'])
            var name=String(cust['name'].toLowerCase())
            if(id.includes(value) || name.includes(value)){
                var h3Cust=document.createElement('h3')
                h3Cust.innerHTML+="ID "+cust['id']+"<small>Name "+cust["name"]+" Phone "+cust['phoneNum']+"</small>"
                h3Cust.addEventListener('click',()=>{
                    var x=document.getElementById('customerId')
                    x.value=cust['id']
                    x.disabled=true
                    
                    var cTransactions=document.getElementById('customerCreditTransactions')
                    cTransactions.innerHTML=''
                    cTransactions.removeChil
                    cust['creditTrasactions'].forEach(t=>{
                        var transaction=document.createElement('h4')
                        transaction.innerHTML=t['time']+'Total= '+t['saleAmount']+' Paid='+t['paidAmount']+' Transaction Id= '+t['tId']+'</h4>'
                        transaction.addEventListener('click',()=>{
                            busketTotalPrice=t['saleAmount']-t['paidAmount']
                            document.getElementById('transactionBalance').innerHTML=busketTotalPrice
                            var completeBtn=document.getElementById('completeTransaction')
                            completeBtn.disabled=false
                            completeBtn.classList.remove('innactive')
                            completeBtn.classList.add('danger')
                            var y=document.getElementById('transactionId')
                            y.value=t['tId']
                            y.disabled=true
                        });
                        cTransactions.appendChild(transaction)
                    });
                });
                sCustomer.appendChild(h3Cust)
            }
        });
    })

    var searchedCustomers=document.createElement('div')
    searchedCustomers.id='searchedCustomers'

    var creditIdInput=document.createElement('input')
    creditIdInput.id='transactionId'
    creditIdInput.placeholder='Transaction Id'

    var customerCreditTransactions=document.createElement('div')
    customerCreditTransactions.id='customerCreditTransactions'


    
    var paymentTile=document.createElement('div')
    paymentTile.id='paymentTile'

    var balanceTile=document.createElement('h3')
    balanceTile.innerHTML="Balance "+busketTotalPrice
    balanceTile.id="transactionBalance"

    var customerDetails=document.createElement('div')
    customerDetails.id='customerDetails'

    var completeTransaction=document.createElement("button")
    completeTransaction.innerHTML="Complete Transaction"
    completeTransaction.classList.add("minLenBtn")
    completeTransaction.classList.add("innactive")
    completeTransaction.disabled=true
    completeTransaction.id="completeTransaction"
    completeTransaction.addEventListener('click',async ()=>{
        var custId=document.getElementById('customerId').value
        var creditId=document.getElementById('transactionId').value
        if(custId!=undefined && custId!=null){
            if(creditId!=undefined && creditId!=null){
                var state=await Transaction.payCredit(creditId,custId,payments)
                if(state==true){
                    notificationBubble('Paid customer credit Successfully',1,5)
                    closePopUp()
                    payments=[]
                    Transaction.clearTransactionFromUi()
                }else{
                
                }
            }else{notificationBubble('Please fill in the transaction id'),3,5}
        }else{
            notificationBubble('Please fill in the customer id',3,5)
        }
    })

    var cancel=document.createElement("button")
    cancel.innerHTML="Cancel"
    cancel.classList.add("minLenBtn")
    cancel.classList.add("cool")
    cancel.addEventListener('click',()=>{
        closePopUp()
        payments=[]
        Transaction.clearTransactionFromUi()
    })

    popUpPanel.appendChild(header)
    popUpPanel.appendChild(customerIdTile)
    popUpPanel.appendChild(searchedCustomers)
    popUpPanel.appendChild(creditIdInput)
    popUpPanel.appendChild(customerCreditTransactions)
    popUpPanel.appendChild(paymentOptions)
    popUpPanel.appendChild(paymentMethods)
    popUpPanel.appendChild(paymentTile)
    popUpPanel.appendChild(balanceTile)
    popUpPanel.appendChild(cancel)
    popUpPanel.appendChild(completeTransaction)
}

function displayReceiveStock(){
    showPopUp("")
    var popUpPanel=document.getElementById('popUpPanel')
    popUpPanel.style.minHeight='600px';
    popUpPanel.style.minWidth='600px'
    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Receive Stock"

    var invoiceNumber=document.createElement('input')
    invoiceNumber.id='invoiceNumber'
    invoiceNumber.defaultValue=''
    invoiceNumber.placeholder='Invoice Number'


    var stockList=document.createElement('div')
    stockList.classList.add('paddedContainer')
    stockList.classList.add('listView')
    stockList.innerHTML=""
    productsList.forEach(p=>{
        var product=document.createElement('div')
        product.innerHTML+="<h4 class='grid listItem'>"+p['name']+" "+p['barCode']+"<div><input class='minLen' id='receiveStock|"+p['id']+"' placeholder='Quantity Received' default='0' type='number' min='0' oninput='this.value = Math.abs(this.value)'/><button class='iconBtn danger'>Remove</button></div></h4>"
        stockList.appendChild(product)
    })


    var receiveStockBtn=document.createElement("button")
    receiveStockBtn.innerHTML="Receive Stock"
    receiveStockBtn.classList.add("minLenBtn")
    receiveStockBtn.classList.add("danger")
    receiveStockBtn.id="receiveStock"
    receiveStockBtn.addEventListener('click',async ()=>{
        var iNumber=document.getElementById('invoiceNumber').value
        if(iNumber!=null && iNumber!=undefined && iNumber!=''){
            var receivedItems=[]
            productsList.forEach(p=>{
                var receivedQuantity=document.getElementById('receiveStock|'+p['id']).value
                if(receivedQuantity>0){
                    receivedItems.push({'id':p['id'],'barCode':p['barCode'],'quantity':parseInt(receivedQuantity)})
                }
            })
            if(receivedItems.length>0){
                console.log(receivedItems)
                var response=await Stock.receiveStock(iNumber,receivedItems)
                if(response['state']==true){
                    closePopUp()
                }
            }else{
                notificationBubble("Please fill in the stock items received",3,5)
            }
        }else{notificationBubble("Please fill in the invoice number",3,5)}
       
    })

    var cancel=document.createElement("button")
    cancel.innerHTML="Cancel"
    cancel.classList.add("minLenBtn")
    cancel.classList.add("cool")
    cancel.addEventListener('click',()=>{
        closePopUp()
    })

    popUpPanel.appendChild(header)
    popUpPanel.appendChild(invoiceNumber)
    popUpPanel.appendChild(stockList)
    popUpPanel.appendChild(receiveStockBtn)
    popUpPanel.appendChild(cancel)

}


//changes the view on the payment pop up to the selected payment by the user
function changePaymentTo(paymentType){
    console.log("Changing Pyament to "+paymentType)
    var paymentTypes=['mpesa','cash','bank','credit']
    var elmToDisplay=document.getElementById(paymentType)
    var paymentBtnClicked=document.getElementById(paymentType+'Opt')
    //hidding all the divs containg the payment option fields/inputs
    paymentTypes.forEach(elm=>{
        try{
            document.getElementById(elm).style.display='none'
            var btn=document.getElementById(elm+'Opt')
            btn.classList.remove('cool')
            btn.classList.add('innactive')
        }catch(err){

        }
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
            var deadLine=document.getElementById('creditDeadline').value
            tDetails={"paymentType":"credit","amount":amount,"custId":custId,"custPhone":custPhone,'deadline':new Date(deadLine).getTime()/1000}
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

//shift action buttons
function displayStartingAmount(){
    showPopUp("")
    var popUpPanel=document.getElementById('popUpPanel')
    popUpPanel.style.minHeight='300px'
    popUpPanel.style.minWidth='300px'

    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Declare Starting Amount"
    var sAmount=document.createElement("input")
    sAmount.placeholder='Starting Amount'
    sAmount.id="sAmountDeclaration"
    sAmount.type='number'
    var submit=document.createElement("button")
    submit.innerHTML="Submit"
    //submit.classList.add("submit")
    submit.classList.add("minLenBtn")
    submit.classList.add("danger")
    submit.onclick=(()=>{
        var sAmount=document.getElementById("sAmountDeclaration").value
        if(sAmount!=undefined && sAmount!=null && sAmount!="" && sAmount>=0){
            sAmount=parseInt(sAmount)
            var result=Shift.declareStartingAmount(sAmount)
            if(result){
                closePopUp()
                notificationBubble("Declared starting amount",1,3)
            }else{
                notificationBubble("Error in declaring starting amount",2,4)
            }
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
    popUpPanel.style.minHeight='300px'
    popUpPanel.style.minWidth='300px'

    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Declare Closing Amount"
    var cAmount=document.createElement("input")
    cAmount.placeholder='Closing Amount'
    cAmount.id="cAmountDeclaration"
    cAmount.type='number'
    var submit=document.createElement("button")
    submit.innerHTML="Submit"
    //submit.classList.add("submit")
    submit.classList.add("minLenBtn")
    submit.classList.add("danger")
    submit.onclick=(()=>{
        var cAmount=document.getElementById("cAmountDeclaration").value
        if(cAmount!=undefined && cAmount!=null && cAmount!="" && cAmount>=0){
            var state=Shift.declareClosingAmount(cAmount)
            if(state==true){
                closePopUp()
            }
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

function registerCustomerPanel(){
    showPopUp("")
    var popUpPanel=document.getElementById('popUpPanel')
    
    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Register Customer"
    
    var inputs=document.createElement('div')
    var custNameInput=document.createElement("input")
    custNameInput.placeholder='Customer Name'
    custNameInput.id="custNameInput"
    
    var custPhoneInput=document.createElement("input")
    custPhoneInput.placeholder='Customer Phone Number'
    custPhoneInput.type='number'
    custPhoneInput.id='custPhoneInput'
    inputs.appendChild(custNameInput)
    inputs.appendChild(custPhoneInput)

    var submit=document.createElement("button")
    submit.innerHTML="Submit"
    //submit.classList.add("submit")
    submit.classList.add("minLenBtn")
    submit.classList.add("danger")
    submit.onclick=(()=>{
        var cName=document.getElementById('custNameInput').value
        var cPhone=document.getElementById('custPhoneInput').value
        if(cName!=undefined && cName!=null && cPhone!=undefined && cPhone!=null){
            var state=Customer.registerCustomer(cName,cPhone)
            if(state==true){
                closePopUp()
            }
        }else{
            notificationBubble('Please fill in the customer name and phone number',2,4)
        }
    })

    var cancel=document.createElement("button")
    cancel.innerHTML="Cancel"
    cancel.classList.add("minLenBtn")
    cancel.classList.add("cool")
    cancel.onclick=closePopUp

    popUpPanel.appendChild(header)
    popUpPanel.appendChild(inputs)
    popUpPanel.appendChild(submit)
    popUpPanel.appendChild(cancel)
}

async function checkCustomerCredit(){
    showPopUp("")
    var popUpPanel=document.getElementById('popUpPanel')
    popUpPanel.style.minHeight='600px'
    popUpPanel.style.minWidth='600px'


    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Check Customer Credit"
    
    var custSearchBox=document.createElement('input')
    custSearchBox.placeholder='Customer Name or Customer id'

    var custDebtBox=document.createElement('div')
    custDebtBox.id='custDebtBox'


    var customersBox=document.createElement('div')
    customersBox.classList.add('listView')
    var customers=await Customer.fetchAllCustomers()
    customers.forEach(cust=>{
        var custTile=document.createElement('div')
        custTile.innerHTML='<h3>'+cust['name']+'</h3><small>Phone '+cust['phoneNum']+'</small><small> Credit Taken = '+cust['creditOwed']+'</small>'
        custTile.classList.add('item')
        custTile.addEventListener('click',async ()=>{
            var debt=await Customer.fetchCustomerTotalCredit(cust['id'])
            var dbtBox=document.getElementById('custDebtBox')
            dbtBox.innerHTML="<h3>"+cust['name']+"</h3>"
            dbtBox.innerHTML+="<h4>Taken Credit = "+debt['creditTaken']+"</h4>"
            dbtBox.innerHTML+="<h4>Credit Available = "+debt['creditAvailable']+"</h4>"
        
        })
        customersBox.appendChild(custTile)
    })

    var cancel=document.createElement("button")
    cancel.innerHTML="Cancel"
    cancel.classList.add("minLenBtn")
    cancel.classList.add("cool")
    cancel.onclick=closePopUp

    popUpPanel.appendChild(header)
    popUpPanel.appendChild(custDebtBox)
    popUpPanel.appendChild(custSearchBox)
    popUpPanel.appendChild(customersBox)
    popUpPanel.appendChild(cancel)
}

function displayReports(){
    showPopUp("")
    var popUpPanel=document.getElementById('popUpPanel')
    popUpPanel.style.minHeight='300px'
    popUpPanel.style.minWidth='300px'
    var header=document.createElement("h3")
    header.classList.add("header")
    header.innerHTML="Reports"
    
    var buttonsContainer=document.createElement("div")
    var xReportBtn=document.createElement('button')
    var creditReportBtn=document.createElement('button')
    var emptiesAndStockReportBtn=document.createElement('button')

    xReportBtn.classList.add('cool')
    creditReportBtn.classList.add('success')
    emptiesAndStockReportBtn.classList.add('cool')

    xReportBtn.innerHTML='X Report'
    creditReportBtn.innerHTML='Credit Report'
    emptiesAndStockReportBtn.innerHTML='Empties Report'

    var buttonsList=[xReportBtn,creditReportBtn,emptiesAndStockReportBtn]
    buttonsList.forEach(btn=>{
        btn.classList.add('minLenBtn')
        buttonsContainer.appendChild(btn)
    })

    xReportBtn.addEventListener('click',async ()=>{
        var response=await Reports.getXReport()
        if(response['state']==true){
            var r=document.getElementById('reportsContent')
            r.innerHTML=response['report']
        }
    })

    creditReportBtn.addEventListener('click',async ()=>{
        var response=await Reports.genCreditReport()
        if(response['state']==true){
            var r=document.getElementById('reportsContent')
            r.innerHTML=response['report']
        }
    })

    emptiesAndStockReportBtn.addEventListener('click',()=>{

    })

    var reportsContent=document.createElement('pre')
    reportsContent.id='reportsContent'
    reportsContent.style='padding:5px;max-height:300px;overflow-y:scroll;'

    var cancel=document.createElement("button")
    cancel.innerHTML="Cancel"
    cancel.classList.add("minLenBtn")
    cancel.classList.add("cool")
    cancel.addEventListener('click',()=>{
        closePopUp()   
    })

    popUpPanel.appendChild(header)
    popUpPanel.appendChild(buttonsContainer)
    popUpPanel.appendChild(reportsContent)
    popUpPanel.appendChild(cancel)
}
async function closeShift(){
    var response=await Shift.closeShift()
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
            itemDiv.innerHTML=item['name']+' @ '+item['price']+' * '+item['quantity']+' ='+item['total'].toLocaleString()
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
        let parent=document.getElementById('allProductsBox')
        products.forEach(p=>{
            var container=document.createElement('li')
            container.innerHTML+="<button class='iconBtn'>+</button>"+p['name']+" @ Ksh"+p['sPrice']+" code="+p['barCode']
            container.addEventListener('click',()=>{
                var itemCodeInput=document.getElementById('itemCode')
                itemCodeInput.value=p['barCode']
            })
            container.classList.add('item')
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
    static renderTransactionSearchBox(transactions){
        var selectBox=document.getElementById('miniTransactionBox')
        transactions.forEach(p=>{
            var container=document.createElement('li')
            container.innerHTML+="<div>SellDate: "+p['sellDate']+" SaleAmount: "+p['saleAmount']+"<div>"
            container.classList.add('item')
            container.addEventListener('click',(event)=>{
                Transaction.displayTransaction(p)
            })
            selectBox.appendChild(container)
        })
    }
}

class FetchData{
    static async getProductsAndBranches(){
        var response=await eel.getProductsAndBranches()()
        return response
    }

    static async customerCreditWorthy(custIdName,custPhoneNumber,amount){
        var response=await eel.isCustomerCreditWorth(custIdName,custPhoneNumber,amount)()
        return response
    }

    static async getAllTransactions(){
        var response=await eel.getAllTransactions()()
        return response
    }

    static async declareStartingAmount(userId,shiftId,amount){
        var response=await eel.declareStartingAmount(userId,shiftId,amount)()
        return response  
    }
    static async declareClosingAmount(userId,shiftId,amount){
        var response=await eel.declareClosingAmount(userId,shiftId,amount)()
        return response
    }
    static async getAllCustomers(){
        var response=await eel.getAllCustomers()()
        return response['customers']
    }

}

class Shift{
    static async declareStartingAmount(amount){
        var shiftId=Auth.getShiftId()
        if(amount!=null && amount!=undefined){
            var userId=getUserId()
            var response=await FetchData.declareStartingAmount(userId,shiftId,amount)
            if(response['state']==true){
                notificationBubble(response['message'],1,2)
                return true
            }else{
                console.log(response['message'])
                notificationBubble(response['message'],2,4)    
                return false
            }
        }else{
            notificationBubble("ShiftId or Starting amout is empty",2,4)
        }
    }
    static declareClosingAmount(amount){
        var shiftId=Auth.getShiftId()
        if(amount!=null && amount!=undefined){
            var userId=getUserId()
            var response=FetchData.declareClosingAmount(userId,shiftId,amount)
            if(response['state']==true){
                notificationBubble(response['message'],1,2)
                return true
            }else{
                notificationBubble(response['message'],2,4)
                return false
            }
        }else{
            notificationBubble("ShiftId or Closing amout is empty",2,4)
        }
    }
    static async closeShift(){
        var userId=Auth.getUserId()
        var shiftId=Auth.getShiftId()
        var response=await eel.closeShift(userId,shiftId)()
        if(response['state']==true){
            var r=response['reports']
            localStorage.setItem('xReport',r['x'])
            localStorage.setItem('zReport',r['z'])
            localStorage.setItem('cReport',r['c'])
            localStorage.setItem('sReport',r['s'])
            redirectToPage('reports')
            return response
        }else{
            notificationBubble(response['message'],0,10)
            return response
        }
    }
}

class Customer{
    static async registerCustomer(custName,custPhone){
        var response=await eel.registerCustomer(custName,custPhone)()
        if(response['state']==true){
            notificationBubble(response['message'],1,2)
            closePopUp()
            return true
        }else{
            notificationBubble(response['message'],2,4)
            return false
        }
    }
    static async fetchAllCustomers(){
        var response=await eel.getAllCustomers()()
        var state=response['state']
        if(state==true){
            var customers=response['customers']
            return customers
        }else{return []}    
    }
    static async fetchCustomerTotalCredit(custId){
        var response=await eel.fetchCustomerTotalCredit(custId)()
        console.log(response)
        var state=response['state']
        if(state==true){
            allCustomers=await FetchData.getAllCustomers()
            return response
        }else{
            notificationBubble("Error while fetching customer credit",2,5)
            return {'creditTaken':'XYZ','creditAvailable':'ZYX','creditTransactions':[]}
        }
    }
}

class Transaction{
    static getTransaction(transactionId){}
    static loadTransaction(transaction){}
    static displayTransaction(transaction){
        showPopUp("")
        var popUpPanel=document.getElementById('popUpPanel')
        var header=document.createElement("h3")
        header.classList.add("header")
        header.innerHTML="Transaction"

        var transactionContainer=document.createElement('div')
        var transactionInnerHtml=document.createElement('div')
        transactionInnerHtml.innerHTML='<h3>Transaction ID: '+transaction['id']+'</h3>'
        transactionInnerHtml.innerHTML='<h3>Sell Date: '+transaction['sellDate']+'</h3>'
        transactionInnerHtml.innerHTML+='<p>Sale Amount: '+transaction['saleAmount']+'</p>'
        transactionInnerHtml.innerHTML+='<p>Paid Amount: '+transaction['paidAmount']+'</p>'
        var soldItems=document.createElement('table')
        soldItems.innerHTML='<th><td>Item Name </td><td>Quantity</td> <td>Total</td></th>'
        transaction['soldItems'].forEach(item=>{
            soldItems.innerHTML+='<tr><td>'+item['name']+'</td><td>'+item['quantity']+'</td><td>'+item['quantity']*item['soldPrice']+'</td></tr>'
        });
        transactionInnerHtml.appendChild(soldItems)
        transactionContainer.appendChild(transactionInnerHtml)
        var cancel=document.createElement("button")
        cancel.innerHTML="Cancel"
        cancel.classList.add("minLenBtn")
        cancel.classList.add("cool")
        cancel.onclick=closePopUp
        popUpPanel.appendChild(header)
        popUpPanel.appendChild(transactionContainer)
        popUpPanel.appendChild(cancel)
    }
    
    static showReceipt(receiptData){
        showPopUp("")
        var popUpPanel=document.getElementById('popUpPanel')
        var header=document.createElement("h3")
        header.classList.add("header")
        header.innerHTML="<h3>STEMAR DISTRIBUTORS RECEIPT</h3>"
        header.innerHTML+="<div>Date: "+new Date().toUTCString()+"</div>"
        header.innerHTML+="<div>Receipt Number"+receiptData['tId']+"</div>"

        var itemsDiv=document.createElement('table')
        var paymentsDiv=document.createElement('table')

        itemsDiv.innerHTML='<tr><th>Items</th></tr>'
        receiptData['busketList'].forEach(item=>{
            var i=document.createElement('tr')
            i.innerHTML='<td>'+item['barCode']+'</td><td> '+item['name']+'</td><td>'+item['quantity']+'</td><td>* '+item['price']+'</td>'+parseInt(item['quantity'])*parseInt(item['price'])+'</td>'
            itemsDiv.appendChild(i)
        })

        var totalRow=document.createElement('tr')
        totalRow.innerHTML='<th>Total Cost</th><th>'+Transaction.computeTotal(receiptData['busketList'])+'</th>'
        itemsDiv.appendChild(totalRow)

        paymentsDiv.innerHTML='<tr><th>Customer Payments</th><th></th></tr>'
        receiptData['payments'].forEach(p=>{
            var i=document.createElement('tr')
            i.innerHTML='<td>'+p['paymentType']+'</td><td>'+p['amount']+'</td>'
            paymentsDiv.appendChild(i)
        })
        
        var custPayment=Transaction.computeTotalPaid(receiptData['payments'])
        var totalRow=document.createElement('tr')
        totalRow.innerHTML='<th>Total Paid</th><th>'+custPayment['paid'].toLocaleString()+'</th>'
        itemsDiv.appendChild(totalRow)
        if(custPayment['credit']>0){
            var totalRow=document.createElement('tr')
            totalRow.innerHTML='<th>Customer Credit</th><th> - '+custPayment['credit']+'</th>'
            itemsDiv.appendChild(totalRow)
        }

        var printReceiptBtn=document.createElement('button')
        printReceiptBtn.classList.add('cool')
        printReceiptBtn.innerHTML='Print Receipt'
        printReceiptBtn.addEventListener('click',()=>{
            printReceiptBtn.style.display='none';
            window.print()
            closePopUp()
            setTimeout(()=>{
                Transaction.clearTransactionFromUi()
            },1000)
        })

        popUpPanel.appendChild(header)
        popUpPanel.appendChild(itemsDiv)
        popUpPanel.appendChild(paymentsDiv)
        popUpPanel.appendChild(printReceiptBtn)
    }

    static getAllTransactions(){}

    static async sendTransactionToBackend(busket,payments,counterId,custId){
        console.log("Sending transaction to the backend")
        var cashierId=Auth.getUserId()
        var response=await eel.makeSale(busket,payments,counterId,cashierId,parseInt(custId))()
        console.log(response['state'])
        if(response['state']==true){
            notificationBubble("Transaction Completed Successfully",1,5)
            return response
        }else{
            notificationBubble("Transaction Failed\n"+response['message'],0,5)
            return response
        }
    }

    static clearTransactionFromUi(){
        Render.clearAllItems()
        customerBusket=[]
        busketTotalPrice=0
        payments=[]
        closePopUp()
        Transaction.computeTotal(customerBusket)
    }

    static computeTotal(items){
        var tot=0
        items.forEach(i=>{
            tot+=i["total"]
        });
        busketTotalPrice=tot
        document.getElementById("basketTotal").innerHTML=busketTotalPrice.toLocaleString()
        return tot
    }
    static computeTotalPaid(payments){
        var tot=0
        var credit=0
        payments.forEach(i=>{
            if(i['paymentType']!='credit'){
                tot+=parseFloat(i['amount'])
            }else{
                credit+=parseFloat(i['amount'])
            }
        })
        return {'paid':tot,'credit':credit}
    }

    static addCommaToNumber(figure){
        return figure.toLocaleString()
    }

    static async payCredit(tId,custId,paymentList){
        var userId=Auth.getUserId()
        if(userId!=null && userId!=undefined){
            var response=await eel.payCustomerCredit(userId,tId,custId,paymentList)()
            allCustomers=await FetchData.getAllCustomers()
            if(response['state']==true){
                return true
            }else{
                notificationBubble(response['message'],0,5)
            }
        }
        return false
    }
}

class Stock{
    static async receiveStock(invoiceNumber,items){
        var userId=Auth.getUserId()
        var response=await eel.receiveStock(userId,invoiceNumber,items)()
        if(response['state']==true){
            return response
        }else{
            notificationBubble(response['message'],0,5)
        }
    }
    static async receiveEmpties(transactionId,empties){

    }
    static async dispatchEmpties(empties){}
}

class Reports{
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
    
    static async closeShift(){
        
    }
    static async emptiesReport(){

    }
}

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

function setUpUser(){
    Auth.renderShiftId()
}

setTimeout(async ()=>{
    setUpUser()
    response=await FetchData.getProductsAndBranches()
    tResponse=await FetchData.getAllTransactions()
    productsList=response['products']
    branches=response['branches']
    allCustomers=await FetchData.getAllCustomers()
    Render.renderSearchBoxProducts(productsList)
    Render.renderBranchesToSelectBox(branches)
    Render.renderTransactionSearchBox(tResponse['transactions'])

},1000)
