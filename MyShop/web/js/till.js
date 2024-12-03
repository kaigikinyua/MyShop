var items=[]
var total=0

//user action buttons
function addItem(){
    itemName=document.getElementById('itemCode').value
    quantity=document.getElementById('quantity').value
    if(itemName.length>0 && quantity.length>0){
        price=100
        total=price*quantity
        items.push({'name':itemName,'price':100,'quantity':quantity,'total':total})
        Render.renderItems(items)
        Transaction.computeTotal()
    }
    else{
        notificationBubble("Please fill in the item code and quantity",3)
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

async function payment(){
    //var x=await eel.makeSale()
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
}

class Product{
    static getProduct(){}
}
class Shift{
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


