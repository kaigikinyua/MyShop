var items=[]
var productsList=[]
var total=0

//user action buttons
function addItem(){
    itemName=document.getElementById('itemCode').value
    quantity=document.getElementById('quantity').value
    if(itemName.length>0 && quantity.length>0){
        var itemFound=false
        productsList.forEach((p)=>{
            if(p['barCode']==itemName){
                price=p['sPrice']
                total=price*quantity
                items.push({'name':p['name'],'price':p['sPrice'],'quantity':quantity,'total':total})
                Render.renderItems(items)
                Transaction.computeTotal()
                itemFound=true
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

function removeItem(itemId){
    var id=itemId.split(',')
    if(items.length>0){
        items.splice(id,1)
    }
    Transaction.computeTotal()
    Render.renderItems(items)
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

async function payment(){
    //var x=await eel.makeSale()
}

function setUpUser(){
    Auth.renderShiftId()
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
    static renderProducts(products){
        let parent=document.getElementById('searchItemCode')
        products.forEach(p=>{
            var container=document.createElement('div')
            container.innerHTML=p['name']
        })
    }
}

class Product{
    static getProduct(){}
}

class FetchData{
    static async getAllProducts(){
        var products=await eel.getAllProducts()()
        return products
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
    static makeTransaction(){}

    static computeTotal(){
        var tot=0
        items.forEach(i=>{
            tot+=i["total"]
        });
        total=tot
        document.getElementById("basketTotal").innerHTML=total
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
}
setTimeout(async ()=>{
    setUpUser()
    productsList=await FetchData.getAllProducts()
    Render.renderProducts(productsList)
},1000)
